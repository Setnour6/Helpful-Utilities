import requests
from bs4 import BeautifulSoup
import validators
from datetime import datetime
import os
from websites import whitelisted_websites, blacklisted_websites
from urllib.parse import urlparse

# ANSI escape sequences for text color
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Function to check if a website is blacklisted
def is_blacklisted(url):
    return any(site in url for site in blacklisted_websites)
    
# Function to check if a website is whitelisted
def is_whitelisted(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in [urlparse(site).netloc for site in whitelisted_websites]

def check_website_credibility(url):
    # Step 1: Validate the URL
    if not validators.url(url):
        return "Invalid URL."

    # Step 2: Fetch website content
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException:
        return "Failed to fetch website content."

    # Step 3: Perform credibility checks
    credibility_score = 0
    max_credibility_score = 8  # Updated maximum credibility score

    # Domain analysis
    if response.url.endswith(".com"):
        credibility_score -= 1
    elif not response.url.endswith(".com"):
        credibility_score += 1

     # Check if website is blacklisted or whitelisted
    if is_blacklisted(response.url):
        credibility_score -= 1
    if is_whitelisted(response.url):
        credibility_score += 1

    # Author and source evaluation
    author_tag = soup.find("meta", attrs={"name": "author"})
    if not author_tag or not author_tag.get("content"):
        credibility_score -= 1

    # Release or update date
    date_tag = soup.find("meta", attrs={"name": "date"})
    if not date_tag or not date_tag.get("content"):
        credibility_score -= 1
    else:
        date_string = date_tag.get("content")
        try:
            publish_date = datetime.strptime(date_string, "%Y-%m-%d")
            if (datetime.now() - publish_date).days > 3650:  # Older than 10 years
                credibility_score -= 1
        except ValueError:
            credibility_score -= 1

    # Clear and unbiased sources cited by the author
    sources_cited = soup.find_all("a", attrs={"rel": "nofollow"})
    if sources_cited:
        credibility_score += 1

    # Typos in the website
    if "typos" in soup.text.lower():
        credibility_score -= 1
    else:
        credibility_score += 1

    # CRAAP test
    # Currency: Check if the website's content is up to date
    # Relevance: Evaluate the relevance of the content to the topic
    # Authority: Consider the authority and expertise of the author/source
    # Accuracy: Assess the accuracy of facts and information presented
    # Purpose: Analyze the purpose and potential biases of the website
    # Sources: Check for clear and unbiased sources cited by the author

    # Step 4: Print credibility information
    print(f"Credibility Score: {credibility_score}/{max_credibility_score}")
    print("Reasons for the Score:")
    print(RED + "- Website is blacklisted" + RESET if is_blacklisted(response.url) else "")
    print(GREEN + "- Website is whitelisted" + RESET if is_whitelisted(response.url) else "")
    print(RED + "- Domain analysis: Suspicious TLD" + RESET if response.url.endswith(".com") else GREEN + "- Domain analysis: Trustful TLD" + RESET)
    print(RED + "- Author and source information missing from metadata" + RESET if not author_tag or not author_tag.get("content") else GREEN + "- Author and source information available in metadata" + RESET)
    print(RED + "- Release or update date missing from metadata" + RESET if not date_tag or not date_tag.get("content") else GREEN + "- Release or update date available in metadata" + RESET)
    print(RED + "- Typos in the website" + RESET if "typos" in soup.text.lower() else GREEN + "- No typos detected in the website" + RESET)
    if date_tag and date_tag.get("content"):
        try:
            publish_date = datetime.strptime(date_tag.get("content"), "%Y-%m-%d")
            if (datetime.now() - publish_date).days > 3650:  # Older than 10 years
                print(RED + "- Website published over 10 years ago" + RESET)
            else:
                print(GREEN + "- Website published less than 10 years ago" + RESET)
        except ValueError:
            pass
    print(GREEN + "- Clear and unbiased sources cited by the author" + RESET if sources_cited else "")

    # Step 5: Return credibility assessment
    if credibility_score >= 2:
        print("The website is credible.")
    elif credibility_score >= 0:
        print("The website appears credible.")
    elif credibility_score >= -1:
        print("The website may not be credible.")
    else:
        print("The website is not credible.")
    
    print()
    print("Remember, search through the website itself and determine if it is credible through your experience")
    return ""

# Function to prompt user for website input
def prompt_user_input():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear the console screen

        option = input("Select an option (enter a number):\n1. Enter a website URL\n2. Check whitelisted websites\n3. Check blacklisted websites\n4. Exit\n")

        if option == "1":
            url = input("Enter the website URL (starting with https:// or other applicable protocol): ")
            result = check_website_credibility(url)
            print(result)
            input("Press Enter to continue...")
        elif option == "2":
            for url in whitelisted_websites:
                print(f"Checking {url}...")
                result = check_website_credibility(url)
                print(result)
                input("Press Enter to continue...")
        elif option == "3":
            for url in blacklisted_websites:
                print(f"Checking {url}...")
                result = check_website_credibility(url)
                print(result)
                input("Press Enter to continue...")
        elif option == "4":
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")


# Example usage
prompt_user_input()
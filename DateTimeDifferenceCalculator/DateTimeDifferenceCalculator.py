from datetime import datetime

def calculate_difference():
    # Calculate the difference between dates, times, or datetimes based on user input.
    datetime_format = "%Y-%m-%d %H:%M:%S"
    date_format = "%Y-%m-%d"
    time_format = "%H:%M:%S"
    
    while True:  # Continue running until the user decides to exit
        try:
            option = input("Choose an option:\n1. Date\n2. Time\n3. Date and Time\nEnter option number (1/2/3), or 'q' to quit: ")
            
            if option == '1':
                print()
                date1 = input("Enter the first date (YYYY-MM-DD): ")
                date2 = input("Enter the second date (YYYY-MM-DD): ")
                
                date_obj1 = datetime.strptime(date1, date_format)
                date_obj2 = datetime.strptime(date2, date_format)
                print()
                date_difference = abs((date_obj2 - date_obj1).days)
                print("Date difference in days:", date_difference)
                print()
                
            elif option == '2':
                print()
                time1 = input("Enter the first time in 24-hour format (HH:MM:SS): ")
                time2 = input("Enter the second time in 24-hour format (HH:MM:SS): ")
                
                time_obj1 = datetime.strptime(time1, time_format)
                time_obj2 = datetime.strptime(time2, time_format)
                print()
                time_difference = abs(time_obj2 - time_obj1)
                print("Time difference:", time_difference)
                print()
                
            elif option == '3':
                print()
                datetime1 = input("Enter the first date and time in 24-hour format (YYYY-MM-DD HH:MM:SS): ")
                datetime2 = input("Enter the second date and time in 24-hour format (YYYY-MM-DD HH:MM:SS): ")
                
                datetime_obj1 = datetime.strptime(datetime1, datetime_format)
                datetime_obj2 = datetime.strptime(datetime2, datetime_format)
                print()
                datetime_difference = abs(datetime_obj2 - datetime_obj1)
                print("Datetime difference:", datetime_difference)
                print()
                
            elif option.lower() == 'q':
                print()
                print("Exiting the program.")
                break  # Exit the loop and end the program
            
            else:
                print("Invalid option. Please choose 1, 2, 3, or 'q'.")
                print()
            
        except ValueError:
            print("Invalid format. Please enter dates in YYYY-MM-DD, times in HH:MM:SS, or datetime in YYYY-MM-DD HH:MM:SS.")
            print()

if __name__ == "__main__":
    calculate_difference()

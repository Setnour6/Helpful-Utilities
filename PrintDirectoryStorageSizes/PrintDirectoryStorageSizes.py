import os
import sys
import time

# Calculate the total size of a directory and its contents
def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

# Load the exclusion list from the exclusion_list text file
def load_exclusion_list():
    exclusion_list = []
    if os.path.exists('exclusion_list.txt'):
        with open('exclusion_list.txt', 'r') as file:
            exclusion_list = [line.strip() for line in file]
    return exclusion_list

# Format size in a human-readable format
def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def main():
    path = input("Enter the directory path for the scan (e.g., C:\\Users\\admin\\Desktop\\): ")
    if not os.path.exists(path):
        input("Invalid path. Press Enter to exit...")
        return

    exclusion_list = load_exclusion_list()

    dir_info = []

    total_size_sum = 0

    print("\nScanning and organizing directories...\n")
    
    # Iterate through items in the specified directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and item_path not in exclusion_list:
            size = get_directory_size(item_path)
            dir_info.append((item_path, size))
            total_size_sum += size
    
    # Sort the list of directories by size in descending order
    sorted_dirs = sorted(dir_info, key=lambda x: x[1], reverse=True)

    total_items = len(sorted_dirs)
    current_item = 0

    for item_path, size in sorted_dirs:
        current_item += 1
        percentage_complete = (current_item / total_items) * 100

        sys.stdout.write("\rProgress: [{:<50}] {:.2f}%".format("=" * int(percentage_complete / 2), percentage_complete))
        sys.stdout.flush()

        time.sleep(0.01)  # Simulating processing time

    print("\n\nTotal Storage from all scanned items:")
    print(f"   Size: {format_size(total_size_sum)}\n")

    print("Sorted list of directories by storage space used:")
    for item_path, size in sorted_dirs:
        print(f"{item_path}")
        print(f"   Size: {format_size(size)}")
        print()
    print("")
    print("Scroll up to see all of the items listed")
    print("")
    input("COMPLETE! Press Enter to exit...")

if __name__ == "__main__":
    main()

import os
import sys
import time
import json
from datetime import datetime
import argparse

# Function for colored text
def colored_text(text, color):
    colors = {
        'green': '\033[92m',
        'blue': '\033[94m',
        'reset': '\033[0m',
        'cyan': '\033[96m'
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"

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
            return colored_text(f"{size:.2f} {unit}", 'green')
        size /= 1024.0

# Load cached directory size information
def load_cache():
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as file:
            return json.load(file)
    return {}

# Save directory size information to cache
def save_cache(cache):
    with open('cache.json', 'w') as file:
        json.dump(cache, file)

# Print message with timestamp
def timestamped_print(message):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {message}")

# Define command line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(
        description=colored_text('Directory Storage Sizes Printer\n\n', 'cyan') +
                    colored_text('Options:\n', 'cyan') +
                    '  ' + colored_text('-d <DIRECTORY>, --directory <DIRECTORY>\n', 'cyan') +
                    '                        Directory path to scan\n' +
                    '                        Example: -d C:\\Users\n' +
                    '  ' + colored_text('-hd, --hidden          Include hidden files\n', 'cyan') +
                    '                        Example: -hd\n' +
                    '  ' + colored_text('-o {alpha,reverse-alpha,smallest,largest}, --order {alpha,reverse-alpha,smallest,largest}\n', 'cyan') +
                    '                        Order of directories: alphabetically, reverse-alphabetically, by smallest size first, or by largest size first (default)\n' +
                    '                        Example: -o alpha\n' +
                    '  ' + colored_text('-t, --tree             Show directory tree for largest folders (limited to specified depth and file limit)\n', 'cyan') +
                    '                        Example: -t 2 5\n' +
                    '  ' + colored_text('-dbg, --debug          Show debug information including permission errors\n', 'cyan') +
                    '                        Example: -dbg'
    )
    parser.add_argument('-d', '--directory', required=True, help='Directory path to scan')
    parser.add_argument('-hd', '--hidden', action='store_true', help='Include hidden files')
    parser.add_argument('-o', '--order', choices=['alpha', 'reverse-alpha', 'smallest', 'largest'], default='largest',
                        help='Order of directories: alphabetically, reverse-alphabetically, by smallest size first, or by largest size first (default)')
    parser.add_argument('-t', '--tree', type=int, nargs=2, metavar=('DEPTH', 'LIMIT'),
                        help='Show directory tree with specified depth and file limit')
    parser.add_argument('-dbg', '--debug', action='store_true', help='Show debug information including permission errors')
    return parser.parse_args()

def print_directory_tree(path, depth, limit, indent=0, debug=False):
    if depth == 0:
        return
    try:
        items = os.listdir(path)[:limit]
        for item in items:
            item_path = os.path.join(path, item)
            size = format_size(get_directory_size(item_path))
            print(f"{'    ' * indent}{colored_text('----', 'blue')} {item_path} | Size: {size}")
            if os.path.isdir(item_path):
                print_directory_tree(item_path, depth - 1, limit, indent + 1, debug)
    except PermissionError as e:
        if debug:
            print(f"PermissionError: {e}")

def main():
    args = parse_arguments()
    
    path = args.directory
    if not os.path.exists(path):
        input("Invalid path. Press Enter to exit...")
        return

    exclusion_list = load_exclusion_list()
    cache = load_cache()

    dir_info = []
    total_size_sum = 0
    timestamped_print("Scanning and organizing directories...")

    total_items = len(os.listdir(path))
    start_time = time.time()

    # Iterate through items in the specified directory
    for index, item in enumerate(os.listdir(path)):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and item_path not in exclusion_list:
            if item_path in cache:
                size = cache[item_path]
            else:
                size = get_directory_size(item_path)
                cache[item_path] = size
            dir_info.append((item_path, size))
            total_size_sum += size

        # Update progress bar
        percentage_complete = ((index + 1) / total_items) * 100
        sys.stdout.write("\r{:%Y-%m-%d %H:%M:%S} - Progress: [{:<50}] {:.2f}%".format(
            datetime.now(), "=" * int(percentage_complete / 2), percentage_complete))
        sys.stdout.flush()

        # Update estimated time remaining below progress bar
        elapsed_time = time.time() - start_time
        estimated_total_time = elapsed_time / ((index + 1) / total_items)
        remaining_time = estimated_total_time - elapsed_time
        sys.stdout.write("\nEstimated Time Remaining: {:.2f} seconds".format(remaining_time))
        sys.stdout.flush()

        # Move cursor up one line
        sys.stdout.write("\033[F")
        sys.stdout.flush()

    save_cache(cache)
    print("\n\nTotal Storage from all scanned items:")
    print(f"   Size: {format_size(total_size_sum)}\n")

    if args.order == 'alpha':
        dir_info.sort(key=lambda x: x[0])
    elif args.order == 'reverse-alpha':
        dir_info.sort(key=lambda x: x[0], reverse=True)
    elif args.order == 'smallest':
        dir_info.sort(key=lambda x: x[1])
    elif args.order == 'largest':
        dir_info.sort(key=lambda x: x[1], reverse=True)

    print("Sorted list of directories by storage space used:")
    for item_path, size in dir_info:
        print(f"{item_path}")
        print(f"   Size: {format_size(size)}")
        print("")

    # Print directory tree if requested
    if args.tree:
        depth, limit = args.tree
        print("\nDirectory tree:")
        for item_path, _ in dir_info:
            print_directory_tree(item_path, depth, limit, indent=0, debug=args.debug)
            print("")

    print("Scroll up to see all of the items listed")
    input("COMPLETE! Press Enter to exit...")

if __name__ == "__main__":
    main()
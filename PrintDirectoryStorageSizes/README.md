This program is called the Directory Storage Sizes Printer.
It scans the files in the directory and most of, if not all, the subdirectories and then prints the sizes of the directories that takes up the storage space on your computer.
NOTICE: The program is case-sensitive.

### Prerequisites

- Python (version 3.10 or higher is preferred)
- the sys and time modules (type `pip install x`, where x is the module, to install said module with pip).

make sure you have a good understanding on how command line interfaces (CLIs) work, how to use Python in a basic manner, and how to open a .py file.

If you notice that file sizes of results did not change, delete the cache.json file if it exists within the same directory.
If you get errors related to an undefined module, install the `argparse` and/or `datetime` modules using pip.
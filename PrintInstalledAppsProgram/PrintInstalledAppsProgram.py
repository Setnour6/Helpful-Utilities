import winreg

def get_installed_programs():
    # Open the registry key containing the list of installed programs
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")

    # Get the number of installed programs
    num_subkeys = winreg.QueryInfoKey(key)[0]

    installed_programs = []

    for i in range(num_subkeys):
        try:
            # Open each subkey
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name)

            # Read the display name value
            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]

            # Append the display name to the list
            installed_programs.append(display_name)

            # Close the subkey
            winreg.CloseKey(subkey)
        except WindowsError:
            pass

    # Close the main key
    winreg.CloseKey(key)

    return installed_programs

# Get the list of installed programs
programs = get_installed_programs()

# Print the list of installed programs
print("PRINT PROGRAM START: ")
for program in programs:
    print(program)

# Wait for user input before exiting
print("")
print("Scroll up to see all of the items listed")
print("")
input("COMPLETE! Press Enter to exit...")

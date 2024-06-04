import os
import subprocess
import sys
import json
from urllib.parse import urlparse

'''
STEP 2: MODIFY JSON FILE
global input = list of the configuration file, source url, destination
1. Check if the source url is in the following configuration file
    a. If mode == "modify" and there is no source url, ask if they want to add
    b. If mode == "delete" and there is no source url or dst url, quit
2. Make a copy of the configuration file
    a. Add the date to the title
    b. Directory is subdirectory (ex. )
    c. Make an another code so the user can recover to the version they want?
3. Edit
'''

def splitURL(url):
    # https:// (protocol) www. (subdomain) kia.com (domain name) /hello/world/ (path/page)
    try:
        domain_path = url.split("://")[1] # domain_path = ['https', 'www.kia.com/hello/world/'][1] = 'www.kia.com/hello/world/'
        domain = domain_path.split("/")[0] # domain = ['www.kia.com', 'hello', 'world', ''][0] = 'www.kia.com'
        pattern = domain_path.replace(domain, "")
        return pattern
    except Exception:
        return False

def inputMode():
    modes = ['modify', 'add', 'delete']
    mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()
    while mode not in modes:
        print(f"\nMode '{mode}' is not a valid request")
        mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()
        if (mode in modes):
            break
    print("\n")
    return mode

def findPattern(config_file, pattern):
    if not os.path.exists(config_file):
        print(f"JSON file '{config_file}' not found.")
    
    with open(config_file, 'r') as file:
        data = json.load(file)
        hosting = data["functions"]["network"]["http"]["frontEnd"]["accessControl"]["matchingList"]
        for host in hosting:
            if host["pattern"] == f"$URL[{pattern}]":
                return host["location"]
        return -1
    
def backup():
    return 0
        
def modify():
    return 0

def add():
    return 0

def delete():
    return 0

def sub_main(src, dst, mode, config_file, location):
    if location == -1:
        print(f"There is NO '{src}' found from '{config_file}'")
        if mode == 'add':
            print(f"PROCEED: Add the redirection rule from {src} to {dst}")
        elif mode == 'modify':
            ask_again = input(f"Do you want to add the redirection rule instead of modify? (y/n):  ")    # ask again
            if ask_again == 'y':
                mode = 'add'
            else:
                print("Cannot proceed. Exit the code.")
        elif mode == 'delete':
            print(f"Cannot delete the requested URL. Exit the code.")   # Can't delete
            # quit()
    else:
        print(f"Current dst URL found from '{config_file}' is '{location}'")
        if mode == 'add':
            ask_again = input(f"Source URL {src} already exits; do you want to modify? (y/n):  ")    # ask again
            if ask_again == 'y':
                mode = 'modify'
            else:
                print("Cannot proceed. Exit the code.")
        elif mode == 'modify':
            if location == dst:
                print(f"Redirection rule from '{src}' to '{dst}' has already applied")
            else:
                print(f"PROCEED: Modify the redirection rule from {src} to {dst}")
        elif mode == 'delete':
            if location != dst:
                print(f"Redirection rule from '{src}' to '{dst}' has already deleted")
                # quit()
            else:
                print(f"PROCEED: Delete the redirection rule from {src} to {dst}")

def main():
    src = 'https://www.kia.com/nl/dealers/sliedrecht/'
    pattern = splitURL(src)
    # src = input("Type in the source URL:  ")
    
    #dst = 'https://www.kia.com/nl/dealers/0/'
    dst = 'https://www.kia.com/nl/dealers/auto-dewaard/'
    # dst = input("Type in the destination URL:  ")
    mode = 'modify'
    # mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()

    # Assume config file = 'www.kia.com-acl.json'
    config_file = "C:\\Users\\Kim\\Desktop\\Assignments\\1_Hyundai_CDN\\www.kia.com-acl.json"
    location = findPattern(config_file, pattern)

    sub_main(src, dst, mode, config_file, location)

    
if __name__ == '__main__':
    main()
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

def is_config(config_file):
    if not os.path.exists(config_file):
        print(f"JSON file '{config_file}' not found.")
    
    with open(config_file, 'r') as file:
        data = json.load(file)
        hosting = data["hosting"]
        
        file.close()

def modify():
    return 0

def add():
    return 0

def delete():
    return 0

def main():
    # https://www.kia.com/nl/dealers/sliedrecht/
    src = input("Type in the source URL:  ")
    # https://www.kia.com/nl/dealers/0/
    dst = input("Type in the destination URL:  ")
    mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()

    # Assume config file = 'www.kia.com-acl.json'
    config_file = "C:\\Users\\Kim\\Desktop\\Assignments\\1_Hyundai_CDN\\www.kia.com-acl.json"
    is_config(config_file)
    print(is_config)

    if mode=='modify':
        modify()
    elif mode=='add':
        add()
    elif mode=='delete':
        delete()

    
if __name__ == '__main__':
    main()
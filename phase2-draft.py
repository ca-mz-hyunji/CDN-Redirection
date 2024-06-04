import os
import subprocess
import sys
import json
from urllib.parse import urlparse

### STEP 2: MODIFY JSON FILE

def modify():
    # json_file = "/usr/local/m2/setting.json"
    json_file = "www.kia.com-acl.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")
    
    with open(json_file, 'r') as file:
        data = json.load(file)
        hosting = data["hosting"]
        
        file.close()
    return 0

def add():
    return 0

def delete():
    return 0

def main():
    src = input("Type in the source URL:  ")
    dst = input("Type in the destination URL:  ")
    mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()

    # Assume config file = 'www.kia.com-acl.json'

    if mode=='modify':
        modify()
    elif mode=='add':
        add()
    elif mode=='delete':
        delete()

    
if __name__ == '__main__':
    main()
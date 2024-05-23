import os
import subprocess
import sys
import json
from urllib.parse import urlparse
import time

# 1.3: After running the "grep" command, read the output log file names
def LogFiles(grep):
    result = subprocess.run(grep, stdout=subprocess.PIPE, text=True, shell=True)
    log_files = result.stdout.splitlines()
    return log_files

# 1.5: Open the log file, find the virtual host name between "id=- -" and "HTTP" (from the bottom)
def HostName(log_file):
    search = []
    host_name = ''
    with open(log_file, 'r') as file:
        lines = file.readlines()    # return lists
        for line in lines:
            id_index = line.find("id=- -")
            http_index = line.find("HTTP")
            if (id_index != -1) and (http_index != -1):
                host_name = line[id_index+7:http_index-1]
                search.append(host_name)
            else:
                None
    file.close()
    return search[-1]

# 1.6: Find the configuration file in "setting.json".
# Configuration file location is next to the basehost under the virtual hostname you found.
def BaseHost(json_file):
    '''
    json_file = "/usr/local/m2/setting.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")
    '''
    with open(json_file, 'r') as file:
        data = json.load(file)
        
    file.close()

def main():
    #src = input("Type in the source URL:  ")
    #dst = input("Type in the destination URL:  ")

    #cmd = GrepCommand(src)
    #print(cmd)

    '''
    cmd = input("Type in the command:  ")
    logLists = LogFiles(cmd)
    for log in logLists:
        print(log)
        hostname = HostName(log)
        HostNames.append(hostname)
    hostname = HostName('example_log')
    print(hostname)
    '''

    BaseHost('www.kia.com-acl.json')

    
if __name__ == '__main__':
    main()
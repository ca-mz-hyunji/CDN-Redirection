import os
import subprocess
import sys
import json
from urllib.parse import urlparse

### STEP 0: RUN REDIRECTIONo LOG

# 0.0: Check if the URL is valid (Extra)
def valid_url(url):
    try:
        check = urlparse(url)
        return all([check.scheme, check.netloc])
    except Exception:
        return False

def host_ip(lists, url):
    # Ex. 'url = https://www.kia.com/hello/'
    try:
        url_parts = url.split("://")[1] # url_parts = ['https', 'www.kia.com/hello/'][1] == 'www.kia.com'
        host = url_parts.split("/")[0] # host = ['www.kia.com', 'hello', ''][0] == 'www.kia.com'
        if host in lists:
            return True
        else:
            return False  
    except Exception:
        return False
    
# 0.1: Return 'curl -I -H "HOST:..." command
def curl(lists, url):
    ip = ''

    # Ex. 'url = https://www.kia.com/hello/'
    url_parts = url.split("://")[1] # url_parts = ['https', 'www.kia.com/hello/'][1] == 'www.kia.com'
    host = url_parts.split("/")[0] # host = ['www.kia.com', 'hello', ''][0] == 'www.kia.com'

    # Assign IPs based on the documentation
    ip = lists[host]
    
    new_url = url.replace(host, ip, 1) # 1 - only the first occurance will be replaced

    shellCommand = 'curl -I -H "HOST:{}"'.format(host) + ' ' + new_url
    return shellCommand # 'curl -I -H "HOST:www.kia.com"' https://34.160.76.133/hello

# 0.2: Check if the redirection rule has already applied
def RedirLogs(curl, dstURL):
    check = subprocess.run(curl, stdout=subprocess.PIPE, text=True, shell=True)
    output = check.stdout
    if output.find(dstURL) != -1:
        return False    # Redirection rule already applied
    else:
        return True     # Redirection rule has not been applied

### STEP 1: FIND THE VM INSTANCE

# 1.1: Inside 'main()' function: sudo su - -> cd / (root directory) -> cd m2log
# 1.2: Return "grep" command
def GrepCommand(url):
    new_url = url.split('.com')[1]
    shellCommand = 'grep -rl ' + new_url + ' .'
    return shellCommand

# 1.3: After running the "grep" command, read the output log file names
## EDGE CASE
def LogFiles(grep):
    result = subprocess.run(grep, stdout=subprocess.PIPE, text=True, shell=True)
    log_files = result.stdout.splitlines()
    return log_files
    
# 1.5: Open the log file, find the virtual host name between "id=- -" and "HTTP" (from the bottom)
## EDGE CASE: Assumed that "id=- -" and "HTTP" appears only once in each line
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
def BaseHost(host_name):
    # json_file = "/usr/local/m2/setting.json"
    json_file = "C:\\Users\\Kim\\Desktop\\Assignments\\1_Hyundai_CDN\\setting.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")
    
    with open(json_file, 'r') as file:
        data = json.load(file)
        
        file.close()

### STEP 2: MODIFY JSON FILE
# 2.1: Open the configuration file

def main():
    ip_list = {'www.kia.com':'34.160.76.133',
               'www.hyundai.com':'34.107.246.212',
               'www.hyundaiusa.com':'34.160.79.194',
               'www.genesis.com':'34.149.135.209',
               'www.casper.hyundai.com':'35.244.253.146',
               'casper.hyundai.com':'34.64.165.126',
               'sweb.hyundaiusa.com':'34.149.243.31',
               'sweb-owners.genesis.com':'34.117.224.125',
               'owners.genesis.com':'34.36.215.56',
               'owners-kia.com':'34.110.185.95',
               'preprod2-eu.kia.com':'34.102.172.183',
               'connectstore.kia.com':'34.49.88.90'}
    
    # User input: source URL
    src = input("Type in the source URL:  ")
    
    src_url = valid_url(src)
    ip = host_ip(ip_list, src)

    while (src_url == False) or (ip == False):
        print(f"Source {src} is not a valid URL or out of a valid IP range")
        src = input("Type in the source URL:  ")
        src_url = valid_url(src)
        ip = host_ip(ip_list, src)
        if (src_url == True) and (ip == True):
            break
    
    # User input: destination URL
    dst = input("Type in the destination URL:  ")
    dst_url = valid_url(dst)
    
    while dst_url == False:
        print(f"Destination {dst} is not a valid URL")
        dst = input("Type in the destination URL:  ")
        dst_url = valid_url(dst)
        if dst_url == True:
            break

    # User input: [Modify, Add, Delete]
    modes = ['modify', 'add', 'delete']
    mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete')  ").lower()
    while mode not in modes:
        print(f"Mode '{mode}' is not a valid request")
        mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete')  ").lower()
        if (mode in modes):
            break

    curlCommend = curl(ip_list, src)

    configList = []

    if RedirLogs(curlCommend, dst):
        print("Switch to the user account"); subprocess.run('sudo su -', shell=True)
        print("Change work directory into root directory"); os.chdir("/")
        print("Change to m2log directory"); os.chdir("m2log")
        grepCommand = GrepCommand(src)
        logLists = LogFiles(grepCommand)    
        logLists = sorted(logLists, key=len)    # The log file with the simpliest name has the priority
        for log in logLists:
            hostname = HostName(log)
            config = BaseHost(hostname)
            configList.append(config)
        
    else:
        print(f"Redirection from '{src}' to '{dst}' has already applied")


if __name__=='__main__':
    main()
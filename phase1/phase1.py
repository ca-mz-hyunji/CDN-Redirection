import os
import subprocess
import json
from urllib.parse import urlparse

### STEP 0: RUN REDIRECTION LOG

# 0.0: Check if the URL is valid
def validURL(url):
    try:
        check = urlparse(url)
        return all([check.scheme, check.netloc])
    except Exception:
        return False

def hostIP(lists, url):
    # Ex. 'url = https://www.kia.com/hello/'
    is_host = False
    try:
        url_parts = url.split("://")[1] # url_parts = ['https', 'www.kia.com/hello/'][1] == 'www.kia.com'
        host = url_parts.split("/")[0]  # host = ['www.kia.com', 'hello', ''][0] == 'www.kia.com'
        if host in lists:
            is_host = True
            return is_host
        return is_host
    except Exception:
        return False
    
# 0.1: Return 'curl -I -H "HOST:..." command
def curl(lists, url):
    ip = ''

    # Ex. 'url = https://www.kia.com/hello/'
    http = url.split("://")[0]  # change if 'https'
    url_parts = url.split("://")[1] # url_parts = ['https', 'www.kia.com/hello/'][1] == 'www.kia.com'
    host = url_parts.split("/")[0]  # host = ['www.kia.com', 'hello', ''][0] == 'www.kia.com'

    # Assign IPs based on the documentation
    ip = lists[host]
    
    new_url = url.replace(http, "http", 1)
    final_url = new_url.replace(host, ip, 1) # 1 - only the first occurance will be replaced

    shellString = 'curl -I -H "HOST:{}"'.format(host) + ' ' + final_url
    return shellString

# 0.2: Check if the redirection rule has already applied
def redirLogs(curl_string, dstURL):
    check = subprocess.run(curl_string, stdout=subprocess.PIPE, text=True, shell=True)
    output = check.stdout
    print(output)   #
    if output.find(dstURL) != -1:
        return False    # Redirection rule already applied
    else:
        return True     # Redirection rule has not been applied

### STEP 1: FIND THE CONFIG FILE (JSON)
    
# 1.1: Inside 'main()' function: cd / (root directory) -> cd m2log
# 1.2: Return "grep" command
def grepCommand(url):
    new_url = url.split('.com')[1]
    shellCommand = 'grep -rl ' + new_url + ' .'
    return shellCommand

# 1.3: After running the "grep" command, read the output log file names
# NEED TO CONSIDER EDGE CASE
def logFiles(grep):
    result = subprocess.run(grep, stdout=subprocess.PIPE, text=True, shell=True)
    log_files = result.stdout.splitlines()
    return log_files

# 1.4: Open the log file, find the virtual host name between "id=- -" and "HTTP" (from the bottom)
# Note: Assumed that "id=- -" and "HTTP" appears only once in each line
def hostName(log_file):
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

# 1.5: Find the configuration file in "setting.json".
# Configuration file location is next to the basehost under the virtual hostname you found.
def baseHost(host_name):
    json_file = "/usr/local/m2/setting.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")
    
    with open(json_file, 'r') as file:
        data = json.load(file)
        hosting = data["hosting"]

        for item in hosting:
            if item["name"] == host_name:
                return item["mode"]["basehost"]
        
        file.close()
    
### STEP 2: MODIFY JSON FILE
# 2.1: Open the configuration file


def main():
    # Global variable
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
    # https://www.kia.com/nl/dealers/sliedrecht/
    src = input("Type in the source URL:  ")
    
    src_url = validURL(src)
    ip = hostIP(ip_list, src)   # is_host -> Boolean value

    while (src_url == False) or (ip == False):
        print(f"\nSource {src} is not a valid URL or out of a valid IP range")
        src = input("Type in the source URL: ")
        src_url = validURL(src)
        ip = hostIP(ip_list, src)
        if (src_url == True) and (ip == True):
            break
    
    # User input: destination URL
    # redirection applied: https://www.kia.com/nl/dealers/auto-dewaard/
    # redirection not applied: https://www.kia.com/0/
    dst = input("Type in the destination URL:  ")
    dst_url = validURL(dst)
    
    while dst_url == False:
        print(f"\nDestination {dst} is not a valid URL")
        dst = input("Type in the destination URL: ")
        dst_url = validURL(dst)
        if dst_url == True:
            break

    # User input: [modify, add, delete]
    modes = ['modify', 'add', 'delete']
    mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()
    while mode not in modes:
        print(f"\nMode '{mode}' is not a valid request")
        mode = input("What do you want to do? (choose from 'modify', 'add', or 'delete'): ").lower()
        if (mode in modes):
            break
    print("\n")

    curlString = curl(ip_list, src)
    host_names = []
    configList = []
    
    check = redirLogs(curlString, dst)

    # check==False --> Redirection rule already applied
    # check==True --> Redirection rule has not been applied
    if (((mode=='modify' or mode=='add') and check==True) or (mode=='delete' and check==False)):
        print("\nChange work directory into root directory"); os.chdir("/")
        print("Change to m2log directory\n"); os.chdir("m2log")
        grepCommand = grepCommand(src)
        print(f"Run {grepCommand}\n")
        logLists = logFiles(grepCommand)    
        logLists = sorted(logLists, key=len)    # The log file with the simpliest name has the priority
        for log in logLists:
            hostname = hostName(log)
            # Need to remove redundant hostnames from host_names
            if hostname not in host_names:
                host_names.append(hostname)
            print(f"Hostname found from '{log}' is '{hostname}'")
        for host in host_names:
            config = baseHost(host)
            configList.append(config)   # Save it for STEP 2
            print(f"\nBasehost for '{host}' is '{config}'\n")
    elif ((mode=='modify' or mode=='add') and check==False): # modify / add -> location O (Stop)
        print(f"Redirection from '{src}' to '{dst}' has already applied.\n")
    elif (mode=='delete' and check==True):  # delete -> location X (Stop)
        print(f"Redirection from '{src}' to '{dst}' has already deleted.\n")


if __name__=='__main__':
    main()
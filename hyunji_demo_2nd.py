import os
import subprocess
import json
from urllib.parse import urlparse

# 0.0: Check if the URL is valid
def valid_url(url):
    try:
        check = urlparse(url)
        return all([check.scheme, check.netloc])
    except Exception:
        return False

def host_ip(lists, url):
    try:
        url_parts = url.split("://")[1]
        host = url_parts.split("/")[0]
        if host in lists:
            return True
        else:
            return False  
    except Exception:
        return False
    
# 0.1: Return 'curl -I -H "HOST:..." command
def curl(lists, url):
    ip = ''

    http = url.split("://")[0]  # change if 'https'
    url_parts = url.split("://")[1]
    host = url_parts.split("/")[0]

    # Assign IPs based on the documentation
    ip = lists[host]
    
    new_url = url.replace(http, "http", 1)
    final_url = new_url.replace(host, ip, 1) # 1 - only the first occurance will be replaced

    shellString = 'curl -I -H "HOST:{}"'.format(host) + ' ' + final_url
    return shellString

# 0.2: Check if the redirection rule has already applied
def RedirLogs(curl_string, dstURL):
    check = subprocess.run(curl_string, stdout=subprocess.PIPE, text=True, shell=True)
    output = check.stdout
    print(output)
    if output.find(dstURL) != -1:
        return False    # Redirection rule already applied
    else:
        return True     # Redirection rule has not been applied
    
# 1.1: Inside 'main()' function: sudo su - -> cd / (root directory) -> cd m2log
# 1.2: Return "grep" command
def GrepCommand(url):
    new_url = url.split('.com')[1]
    shellCommand = 'grep -rl ' + new_url + ' .'
    return shellCommand

# 1.3: After running the "grep" command, read the output log file names
def LogFiles(grep):
    result = subprocess.run(grep, stdout=subprocess.PIPE, text=True, shell=True)
    log_files = result.stdout.splitlines()
    return log_files

# 1.5: Open the log file, find the virtual host name between "id=- -" and "HTTP" (from the bottom)
# Note: Assumed that "id=- -" and "HTTP" appears only once in each line
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
def BaseHost(host_name):
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
# 2.1: Check if the config file has the source URL
def ConfigSrc(config, source):
    return 0


def modify():
    return 0

def add():
    return 0

def delete():
    return 0


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
    
    # User should run 'sudo su -' before they run the code
    
    # User input: source URL
    # https://www.kia.com/nl/dealers/sliedrecht/
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
    # https://www.kia.com/nl/dealers/auto-dewaard/
    # https://www.kia.com/0/
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

    curlString = curl(ip_list, src)
    host_names = []
    configList = []
    
    print("\nChange work directory into root directory"); os.chdir("/")
    print("Change to m2log directory\n"); os.chdir("m2log")
    grepCommand = GrepCommand(src)
    print(f"Run {grepCommand}\n")
    logLists = LogFiles(grepCommand)    
    logLists = sorted(logLists, key=len)    # The log file with the simpliest name has the priority
    for log in logLists:
        hostname = HostName(log)
        # Need to remove redundant hostnames from host_names
        if hostname not in host_names:
            host_names.append(hostname)
        print(f"Hostname found from '{log}' is '{hostname}'")
    for host in host_names:
        config = BaseHost(host)
        configList.append(config)   # Save it for STEP 2
        print(f"\nBasehost for '{host}' is '{config}'\n")

    
    for config_file in configList:
        ConfigSrc(config_file, src)
        if ConfigSrc:
            if mode=='modify':
                modify(config, src, dst)
            elif mode=='add':
                add(config, src, dst)
            elif mode=='delete':
                delete(config, src, dst)
        else:
            print(f"Source URL '{src}' is not found in '{config_file}'")


if __name__=='__main__':
    main()
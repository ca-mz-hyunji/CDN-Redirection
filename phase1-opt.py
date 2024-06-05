import os
import subprocess
import json

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

def splitURL(url):
    # https:// (protocol) www. (subdomain) kia.com (domain name) /hello/world/ (path/page)
    try:
        protocol = url.split("://")[0] # protocol = ['https', 'www.kia.com/hello/world/'][0] = 'https'
        domain_path = url.split("://")[1] # domain_path = 'www.kia.com/hello/world/'
        domain = domain_path.split("/")[0] # domain = ['www.kia.com', 'hello', 'world', ''][0] = 'www.kia.com'
        return protocol, domain
    except Exception:
        return False

# 0.0: Check if the URL is valid
def hostIP(lists, host):
    is_host = False
    if host in lists:
        is_host = True
    return is_host

def inputSrc():
    src = input("Type in the source URL:  ")
    protocol, domain = splitURL(src)
    is_host = hostIP(ip_list, domain)

    while is_host == False:
        print(f"\nSource {src} is out of a valid IP range")
        src = input("Type in the source URL: ")
        protocol, domain = splitURL(src)
        is_host = hostIP(ip_list, domain)
        if is_host == True:
            break
    return src, protocol, domain

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
    
# 0.1: Return 'curl -I -H "HOST:..." command
def curlString(lists, url, protocol, host):
    # Assign IPs based on the documentation
    ip = lists[host]
    
    http = url.replace(protocol, "http", 1)
    final_url = http.replace(host, ip, 1) # 1 - only the first occurance will be replaced

    shell_string = 'curl -I -H "HOST:{}"'.format(host) + ' ' + final_url
    return shell_string

# 0.2: Check if the redirection rule has already applied
def curlRun(curl_string, dstURL):
    check = subprocess.run(curl_string, stdout=subprocess.PIPE, text=True, shell=True)
    output = check.stdout
    print(output)
    if output.find(dstURL) != -1:
        return False    # Redirection rule already applied
    else:
        return True     # Redirection rule has not been applied

# 1.2: Return "grep" command
def grepString(url):
    new_url = url.split('.com')[1]
    shellCommand = 'grep -rl ' + new_url + ' .'
    return shellCommand

# 1.3: After running the "grep" command, read the output log file names
def grepRun(grep_string):
    result = subprocess.run(grep_string, stdout=subprocess.PIPE, text=True, shell=True)
    log_files = result.stdout.splitlines()
    return log_files

# 1.4: Open the log file, find the virtual host name between "id=- -" and "HTTP" (from the bottom)
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

# Configuration file location is next to the basehost under the virtual hostname you found in "setting.json".
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

def sub_sub_main(log_lists):
    host_names = []
    config_list = []    # Save it for STEP 2
    for log in log_lists:
        host_name = hostName(log)
        # Remove redundant hostnames from host_names
        if host_name not in host_names:
            host_names.append(host_name)
        print(f"Hostname found from '{log}' is '{host_name}'")
    for host in host_names:
        config_file = baseHost(host)
        config_list.append(config_file)
        print(f"\nBasehost for '{host}' is '{config_file}'\n")
    return config_list

def sub_main(src, dst, mode, is_redirected):
    # check==False --> Redirection rule already applied
    # check==True --> Redirection rule has not been applied
    if (((mode=='modify' or mode=='add') and is_redirected==True) or (mode=='delete' and is_redirected==False)):
        print("\nChange work directory into root directory"); os.chdir("/")
        print("Change to m2log directory\n"); os.chdir("m2log")
        grep_string = grepString(src)
        print(f"Run {grep_string}\n")

        log_lists = sorted(grepRun(grep_string), key=len)   # The log file with the simpliest name has the priority
        sub_sub_main(log_lists)

    elif ((mode=='modify' or mode=='add') and is_redirected==False): # modify / add -> location O (Stop)
        print(f"Redirection from '{src}' to '{dst}' has already applied.\n")

    elif (mode=='delete' and is_redirected==True):  # delete -> location X (Stop)
        print(f"Redirection from '{src}' to '{dst}' has already deleted.\n")

def main():
    # User input: source URL
    # https://www.kia.com/nl/dealers/sliedrecht/
    src, protocol, domain = inputSrc()
    
    # User input: destination URL
    # https://www.kia.com/nl/dealers/auto-dewaard/ + https://www.kia.com/0/
    dst = input("Type in the destination URL:  ")
    
    # User input: [modify, add, delete]
    mode = inputMode()

    curl_string = curlString(ip_list, src, protocol, domain)
    is_redirected = curlRun(curl_string, dst)

    sub_main(src, dst, mode, is_redirected) # return the list of configuration files

if __name__=='__main__':
    main()
import os
import subprocess
import sys
import json
from urllib.parse import urlparse


### STEP 0: RUN REDIRECTION LOG

# 0.0: Check if the URL is valid (Extra)
def valid_url(url):
    try:
        check = urlparse(url)
        return all([check.scheme, check.netloc])
    except Exception:
        return False

# 0.1: Return 'curl -I -H "HOST:..." command
def curl(url):
    # Ex. 'url = https://www.kia.com/hello/'
    if valid_url(url):
        url_parts = url.split("://")[1] # url_parts = ['https', 'www.kia.com/hello/'][1] == 'www.kia.com'
        host = url_parts.split("/")[0] # host = ['www.kia.com', 'hello', ''][0] == 'www.kia.com'

        host_parts = host.split('.')[1] # host_parts = ['www', 'kia', 'com'][1] == 'kia'
        ip = ''

        # Assign IPs based on the documentation
        ### EDGE CASES COVER
        if host_parts == 'kia':
            ip = '34.160.76.133'
        elif host_parts == 'hyunai':
            ip = '34.107.246.212'
        elif host_parts == 'genesis':
            ip = '34.149.135.209'

        new_url = url.replace(host, ip, 1) # 1 - only the first occurance will be replaced

        shellCommand = 'curl -I -H "HOST:{}"'.format(host) + ' ' + new_url
        return shellCommand # 'curl -I -H "HOST:www.kia.com"' https://34.160.76.133/hello
    else:
        print(f"{url} is not a valid URL")

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
def LogFiles(grep):
    try:
        result = subprocess.run(grep, stdout=subprocess.PIPE, text=True, shell=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, grep, output=result.stdout, stderr=result.stderr)
        log_files = result.stdout.splitlines()
        return log_files
    except subprocess.CalledProcessError as error:
        print(f"Error occurred: {error.stderr}", file=sys.stderr)
        return []
    
# 1.4: Return "vi [file name]" command
'''
def ViCommand(log_files):
    # Prioritize simpler naming conventions
    logDict = {}
    viCommand = []
    
    for log_file in log_files:
        logDict[log_file] = len(log_file)
    sortedLog = dict(sorted(logDict.items(), key=lambda item: item[1]))
    for log in sortedLog:
        shellCommand = 'vi {}'.format(log)
        viCommand.append(shellCommand)
    return viCommand
'''

# 1.5: Open the log file, find the virtual host name between "id=- -" and "HTTP" (from the bottom)
def HostName(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()
        json_data = ''.join(lines)
        try:
            json_object = json.loads(json_data)
            return json_object
        except json.JSONDecodeError:
            print("Error decoding JSON data")
            return None

def BaseHost():
    json_file = "/usr/local/m2/setting.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")

    with open(json_file, 'r') as file:
        data = json.load(file)

### STEP 2: MODIFY JSON FILE

def main():
    src = input("Type in the source URL:  ")
    dst = input("Type in the destination URL:  ")

    curlCommend = curl(src)
    HostNames = []
    if RedirLogs(curlCommend, dst):
        print("Switch to the user account"); subprocess.run('sudo su -', shell=True)
        print("Change work directory into root directory"); os.chdir("/")
        print("Change to m2log directory"); os.chdir("m2log")
        grepCommand = GrepCommand(src)
        logLists = RedirLogs(grepCommand)
        for log in logLists:
            hostname = HostName(log)
            HostNames.append(hostname)

if __name__=='__main__':
    main()

import os
import subprocess
import sys
import json
from urllib.parse import urlparse
import time

# 1.6: Find the configuration file in "setting.json".
# Configuration file location is next to the basehost under the virtual hostname you found.
def BaseHost(host_name):
    # json_file = "/usr/local/m2/setting.json"

    json_file = "C:\\Users\\Kim\\Desktop\\Assignments\\1_Hyundai_CDN\\setting.json"
    
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")
    else:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        file.close()

def main():
    configList = []
    HostNames = ["www.kia.com", "www.kia.com-origin-root-kr-80", "www.kia.com-org-www-443", "www.kia.com-org-www-8005"] # Assume LogFiles -> HostName done
    logLists = sorted(logLists, key=len)
    
    for host in HostNames:
        config = BaseHost(host)
        configList.append(config)

    for configs in configList:
        print(configs)

    
if __name__ == '__main__':
    main()
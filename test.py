import os
import subprocess
import sys
import json
from urllib.parse import urlparse
import time

def valid_url(url):
    try:
        check = urlparse(url)
        return all([check.scheme, check.netloc])
    except Exception:
        return False

def curl(url):
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
    ip = ''

    # Ex. 'url = https://www.kia.com/hello/'
    url_parts = url.split("://")[1] # url_parts = ['https', 'www.kia.com/hello/'][1] == 'www.kia.com'
    host = url_parts.split("/")[0] # host = ['www.kia.com', 'hello', ''][0] == 'www.kia.com'


    # Assign IPs based on the documentation
    if host in ip_list:
        ip = ip_list[host]
    else:
        print(f"{url} is not a valid URL")
        return -1

    new_url = url.replace(host, ip, 1) # 1 - only the first occurance will be replaced

    shellCommand = 'curl -I -H "HOST:{}"'.format(host) + ' ' + new_url
    print(shellCommand) # 'curl -I -H "HOST:www.kia.com"' https://34.160.76.133/hello


def HostName(log_file):
    with open(log_file, 'r') as file:
        # Read lines from the end of the file
        lines = file.readlines()  # Reverse the list to read from the bottom
        lines.reverse()
        for line in lines:
            if 'id=- -' in line:
                return 0
    return -1

def main():
    src = input("Type in the source URL:  ")
    #dst = input("Type in the destination URL:  ")

    url = valid_url(src)

    while url == False:
        print(f"{url} is not a valid URL")
        src = input("Type in the source URL:  ")
    else:
        curlCommend = curl(src)

    HostNames = []
    
    #file = HostName('example_log')

    
if __name__ == '__main__':
    main()
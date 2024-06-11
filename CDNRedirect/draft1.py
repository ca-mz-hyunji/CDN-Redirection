import os
import subprocess
import sys
import json
import re

IP_dict = {
    "www.kia.com": "34.160.76.133",
    "www.hyundai.com": "34.107.246.212",
    "www.hyundaiusa.com": "34.160.79.194",
    "www.genesis.com": "34.149.135.209",
    "www.casper.hyundai.com": "35.244.253.146",
    "casper.hyundai.com": "34.64.165.126 ",
    "sweb.hyundaiusa.com": "34.149.243.31",
    "sweb-owners.genesis.com": "34.117.224.125",
    "owners.genesis.com": "34.36.215.56",
    "owners-kia.com": "34.110.185.95",
    "preprod2-eu.kia.com": "34.102.172.183",
    "connectstore.kia.com": "34.49.88.90"
}

def splitURL(url):
    # https:// (protocol) www. (subdomain) kia.com (domain name) /hello/world/ (path/page)
    try:
        protocol = url.split("://")[0] # protocol = ['https', 'www.kia.com/hello/world/'][0] = 'https'
        domain_path = url.split("://")[1] # domain_path = 'www.kia.com/hello/world/'
        domain = domain_path.split("/")[0] # domain = ['www.kia.com', 'hello', 'world', ''][0] = 'www.kia.com'
        return protocol, domain
    except Exception:
        return None
    
# 1: Get inputs from User
def userInput():
    src_url = input("Enter <SOURCE URL>: ")
    protocol, domain = splitURL(src_url)
    if domain not in IP_dict:
        src_url = input("Enter <SOURCE URL>: ")
        protocol, domain = splitURL(src_url)


# hostIP + inputSrc + inputMode + destination URL -> input 한번에 받기
# 6개 possible cases 따로

# Non-csv file method
# Phase 1
# 1: Get inputs from User
# 2: Send Curl (check Destination & make a log if there wasn't)
# 3: Check the 6 cases (add, modify, delete) (destination = location ?: same, different)
# 4: Grep Command --> Find Log Files (sort into shortest first)
# 5: Open the (shortest) log file and find Virtual Hostname
# 6: Find JSON configuration file for the Virtual Hostname (from /usr/local/m2/setting.json)
# 7: Open the JSON config file and search for the redirect_from
# Phase 2
# 8: Check 2 cases (redirect_from exists? (modify, delete -> yes) (add -> no))
# *: Copy a backup file in a subdirectory



# csv file method (for multiple redirections)
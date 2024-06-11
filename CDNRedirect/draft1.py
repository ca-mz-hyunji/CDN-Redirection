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
        url = url.lower()
        domain_path = url.split("://")[1] # domain_path = ['https', 'www.kia.com/hello/world/'][1] = 'www.kia.com/hello/world/'
        domain = domain_path.split("/")[0] # domain = ['www.kia.com', 'hello', 'world', ''][0] = 'www.kia.com'
        path_from = domain_path.replace(domain, '')
        return domain, path_from
    except Exception:
        return None, None
    
# 1: Get inputs from User
def userInput():
    src_url = input("Enter <SOURCE URL>: ")
    domain, path_from = splitURL(src_url)
    while domain not in IP_dict:
        src_url = input("Enter <SOURCE URL>: ")
        domain, path_from = splitURL(src_url)
    ip = IP_dict[domain]

    dst_url = input("Enter <DESTINATION URL: ")
    action = input("Enter <ACTION> <add/change/delete>: ")
    while action.lower() not in ('add','change','delete'):
        action = input("Enter <ACTION> <add/change/delete>: ")

    return domain, ip, path_from, dst_url, action

def main():
    userInput()

if __name__=='__main__':
    main()
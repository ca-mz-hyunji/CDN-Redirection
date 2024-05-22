import os
import subprocess
import sys
import json
from urllib.parse import urlparse
import time

def HostName(log_file):
    with open(log_file, 'r') as file:
        # Read lines from the end of the file
        lines = file.readlines()  # Reverse the list to read from the bottom
        lines.reverse()
        for line in lines:
            if 'id=- -' in line:
                return 0
    return -1

    
if __name__ == '__main__':
    #src = input("Type in the source URL:  ")
    #dst = input("Type in the destination URL:  ")

    HostNames = []
    
    file = HostName('example_log')
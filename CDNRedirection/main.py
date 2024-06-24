import os
import subprocess
import sys
import json
import re

from modules.userInput import userInput
from modules.curlCommand import curlCommand
from modules.checkAction import checkAction
from modules.grepCommand import grepCommand
from modules.findVirtualHostname import findVirtualHostname
from modules.findBaseHost import findBaseHost
from modules.openConfigFile import openConfigFile
from modules.userConfirm import userConfirm
from modules.createBackup import createBackup
from modules.updateFile import updateFile


def main():
    ### Phase 1 ###
    # Step 1: Get inputs from User
    src_url, domain, ip, path_from, dst_url, action = userInput()

    # Step 2: Send Curl (check Destination & make a log if there wasn't)
    loc_eq_dst, location = curlCommand(domain, ip, path_from, dst_url, "single")
    
    # Step 3: Check the 8 cases (Add, Modify, Delete)
    action = checkAction(src_url, loc_eq_dst, location, action)

    if action == False:
        return 0
    
    # Step 4: Grep Command --> Find Log Files (sort into shortest first)
    log_files = grepCommand(path_from)
    
    # Step 5: Open the (shortest) log file (don't use /origin.log) and find Virtual Hostname for Path_from
    virt_hosts = findVirtualHostname(log_files, path_from)
    
    # Step 6: Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
    base_hosts = findBaseHost(virt_hosts, domain)   # dictionary
    
    # Step 7: Open the JSON config file (located at BaseHost) and search for redirection rule (using Path_from)
    config_pattern, config_location, config_file_loc, config_checked = openConfigFile(base_hosts, path_from, src_url, dst_url, action)

    if config_checked == False:
        return 0

    ### Phase 2 ###
    # Step 8: Show redirection rule (pattern) to Add/Modify/Delete and Check user's confirmation for updating the config file
    confirmed, rule = userConfirm(config_pattern, config_location, action, path_from, dst_url)

    if confirmed == 'no':
        return 0

    # Step 9: Copy a backup file in a subdirectory
    createBackup(config_file_loc)

    # Step 10: Update the Config File with redirection rule
    updateFile(path_from, dst_url, action, config_file_loc)


    # Step 11: Deploy


    # Step 12: Test the redirection change by using Curl (every 2 minutes, 5 times max)



if __name__=='__main__':
    main()
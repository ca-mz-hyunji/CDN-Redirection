import os
import subprocess
import sys
import json
import re

from modules.helpers import border_msg, userData
from modules.userInputcsv import userInputcsv
from modules.curlCommand import curlCommand
from modules.checkActionExcel import checkActionExcel
from modules.grepCommand import grepCommand
from modules.findVirtualHostname import findVirtualHostname
from modules.findBaseHost import findBaseHost
from modules.openConfigFileExcel import openConfigFileExcel
#from modules.userConfirm import userConfirm
from modules.createBackup import createBackup
from modules.updateFile import updateFile
from modules.helpers import userData, border_msg


def main():
    ### Phase 1 ###
    check_action_failed = {}
    check_config_failed = {}

    # Step 1: Get inputs from User
    #excel_file_path = input("Type in the Excel file path:  ")
    excel_file_path = "C:\\Users\\Kim\\Desktop\\GitHub\\Redirecting-Automation\\CDNRedirection\\testing_files\\kia_test.csv"

    if not os.path.exists(excel_file_path):
        border_msg(f"CSV file '{excel_file_path}' not found.")
        return
        
    user_input_dict, domain_failed = userInputcsv(excel_file_path)
    # user_input_dict = {{'src_url', 'domain', 'ip', 'path_from', 'dst_url', 'action'}}
    
    for user_input in user_input_dict:
        # Step 2: Send Curl (check Destination & make a log if there wasn't)
        # print(f'{user_input+1}: {user_input_dict[user_input]}\n')
        src_url, domain, ip, path_from, dst_url, action = userData(user_input_dict[user_input])

        loc_eq_dst, location = curlCommand(domain, ip, path_from, dst_url, "Excel")

        # For testing
        # print(f"[{user_input+1}]:\nsrc_url: {user_input_dict[user_input]['src_url']} --> dst_url: {user_input_dict[user_input]['dst_url']}\nCurr location: {location}")
    
        # Step 3: Check the 8 cases (Add, Modify, Delete)
        new_action = checkActionExcel(src_url, loc_eq_dst, location, action)

        if action != new_action:    # if new_action is different from the initial action or False
            if new_action == False:
                check_action_failed[user_input] = user_input_dict[user_input]
                continue
            else:
                user_input_dict[user_input]['action'] = new_action

    for action_failed_index in check_action_failed:
        user_input_dict.pop(action_failed_index)

    for new_user_input in user_input_dict:
        src_url, domain, ip, path_from, dst_url, action = userData(user_input_dict[new_user_input])

        # Step 4: Grep Command --> Find Log Files (sort into shortest first)
        # log_files = grepCommand(path_from, 'Excel')
        # For testing on Windows
        log_files = ['C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\testing_files\\m2log_copy\\www.kia.com\\access.log',
                     'C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\testing_files\\m2log_copy\\www.kia.com\\origin.log']
            
        # Step 5: Open the (shortest) log file (don't use /origin.log) and find Virtual Hostname for Path_from
        virt_hosts = findVirtualHostname(log_files, path_from, 'Excel')
            
        # Step 6: Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
        base_hosts = findBaseHost(virt_hosts, 'Excel')   # dictionary
            
        # Step 7: Open the JSON config file (located at BaseHost) and search for redirection rule (using Path_from)
        config_pattern, config_location, config_file_loc, config_checked = openConfigFileExcel(base_hosts, path_from, src_url, dst_url, action)

        if config_checked == False:
            check_config_failed[new_user_input] = user_input_dict[new_user_input]
            continue

        ### Phase 2 ###
        # Step 8: Show redirection rule (pattern) to Add/Modify/Delete and Check user's confirmation for updating the config file
        '''
        confirmed, rule = userConfirm(config_pattern, config_location, action, path_from, dst_url)
        if confirmed == 'no':
            continue
        '''
        # Step 9: Copy a backup file in a subdirectory
        # Note: Create backup only when it is the first redirection rule (no need to create multiple backup files)
        # createBackup(config_file_loc)

        # config_file_loc = "/home/hji_kim/automation/www.kia.com-acl-testing.json"
        config_file_loc = "C:\\Users\\Kim\\Desktop\\GitHub\\Redirecting-Automation\\CDNRedirection\\testing_files\\www.kia.com-acl-testing.json"

        # Step 10: Update the Config File with redirection rule
        updateFile(path_from, dst_url, action, config_file_loc)

    ### TESTING ###
    print("------------")
    for failed_index in domain_failed:
        print(f"Index {failed_index+1}: {domain_failed[failed_index]['src_url']} does not have a valid domain name. Try it again later.")
    print("------------")
    for action_failed_index in check_action_failed:
        print(f"ERROR: Index [{action_failed_index+1}] failed to check action. src_url: {check_action_failed[action_failed_index]['src_url']} & dst_url: {check_action_failed[action_failed_index]['dst_url']}")
    print("------------")
    for config_failed_index in check_config_failed:
        user_input_dict.pop(config_failed_index)
        print(f"ERROR: Index [{config_failed_index+1}] with src_url: {check_config_failed[config_failed_index]['src_url']} could not find the rule in any configuration file")
    print("------------")

    # Step 11: Deploy

    # Step 12: Test the redirection change by using Curl (every 2 minutes, 5 times max)

if __name__=='__main__':
    main()
    # C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\testing_files\\kia_test.xlsx
    # /home/hji_kim/automation/kia_test.csv
import os
import subprocess
import sys
import json
import re

from modules.userInputExcel import userInputExcel
from modules.curlCommand import curlCommand
from modules.checkActionExcel import checkActionExcel
from modules.grepCommand import grepCommand
from modules.findVirtualHostname import findVirtualHostname
from modules.findBaseHost import findBaseHost
from modules.openConfigFile import openConfigFile
from modules.userConfirm import userConfirm
from modules.createBackup import createBackup
from modules.updateFile import updateFile
from modules.helpers import userData, border_msg


def main():
    ### Phase 1 ###
    # Step 1: Get inputs from User
    excel_file_path = input("Type in the Excel file path:  ")
    check_action_failed = {}
    check_config_failed = {}
    user_confirm_failed = {}

    if not os.path.exists(excel_file_path):
        border_msg(f"Excel file '{excel_file_path}' not found.")
        
    else:
        user_input_dict, domain_failed = userInputExcel(excel_file_path)
        # user_input_dict = {{'src_url', 'domain', 'ip', 'path_from', 'dst_url', 'action'}}
        
        for user_input in user_input_dict:
            # Step 2: Send Curl (check Destination & make a log if there wasn't)
            # print(f'{user_input+1}: {user_input_dict[user_input]}')
            src_url, domain, ip, path_from, dst_url, action = userData(user_input_dict[user_input])

            loc_eq_dst, location = curlCommand(domain, ip, path_from, dst_url, "Excel")
    
            # Step 3: Check the 8 cases (Add, Modify, Delete)
            new_action = checkActionExcel(src_url, loc_eq_dst, location, action)

            if action != new_action:    # if new_action is different from the initial action or False
                if new_action == False:
                    check_action_failed[user_input] = user_input_dict[user_input]
                    continue
                else:
                    user_input_dict[user_input]['action'] = new_action

        for failed_index in check_action_failed:
            print(f"\nERROR: Index {failed_index+1} failed to check action. Try it again later: \nsrc_url: {check_action_failed[failed_index]['src_url']} & dst_url: {check_action_failed[failed_index]['dst_url']}")
            user_input_dict.pop(failed_index)
        
        print(user_input_dict)

        return 0
        for user_input in user_input_dict:
            # Step 4: Grep Command --> Find Log Files (sort into shortest first)
            log_files = grepCommand(path_from)
            
            # Step 5: Open the (shortest) log file (don't use /origin.log) and find Virtual Hostname for Path_from
            virt_hosts = findVirtualHostname(log_files, path_from)
            
            # Step 6: Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
            base_hosts = findBaseHost(virt_hosts)   # dictionary
            
            # Step 7: Open the JSON config file (located at BaseHost) and search for redirection rule (using Path_from)
            config_pattern, config_location, config_file_loc, config_checked = openConfigFile(base_hosts, path_from, src_url, dst_url, action)

            if config_checked == False:
                continue

            ### Phase 2 ###
            # Step 8: Show redirection rule (pattern) to Add/Modify/Delete and Check user's confirmation for updating the config file
            confirmed, rule = userConfirm(config_pattern, config_location, action, path_from, dst_url)

            if confirmed == 'no':
                continue

            # Step 9: Copy a backup file in a subdirectory
            createBackup(config_file_loc)

            # Step 10: Update the Config File with redirection rule
            updateFile(path_from, dst_url, action, config_file_loc)


            # Step 11: Deploy


            # Step 12: Test the redirection change by using Curl (every 2 minutes, 5 times max)



if __name__=='__main__':
    main()
    # C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\testing_files\\kia_test.xlsx
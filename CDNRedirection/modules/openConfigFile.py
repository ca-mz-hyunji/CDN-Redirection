import os
import json

# Step 7: Open the JSON config file (located at BaseHost) and search for redirection rule (using Path_from)
def openConfigFile(base_hosts, path_from, src_url, dst_url, action):
    # input: dictionary (loop)
    base_hosts_list = []
    config_pattern = None
    config_location = None
    config_file_loc = None
    config_checked = True
    count = 1

    for key in base_hosts:
        base_hosts_list.append(base_hosts[key])

    for config_file in base_hosts_list:
        if not os.path.exists(config_file):
            print(f"JSON file '{config_file}' not found.")
            break
        
        with open(config_file, 'r') as file:
            data = json.load(file)
            rules = data["functions"]["network"]["http"]["frontEnd"]["accessControl"]["matchingList"]
            for rule in rules:
                if rule["pattern"] == f"$URL[{path_from}]":
                    config_pattern = rule["pattern"]
                    config_location = rule["location"]
                    config_file_loc = config_file
                    break
        
        # Check the 6 Cases (in Handout: Coding Step-by-Step for Developers)
        if not config_pattern:
            print(f'Confg file {count}: [{config_file}]\ndoes not have the redirection rule for Source:\n[{src_url}]\n')
            if action == 'add': # Case 5
                print(f'Can ADD new redirection: \n[{src_url}]\n-->\n[{dst_url}]\n')
                config_file_loc = base_hosts_list[0]
                break
            else: # Case 2 & Case 4
                if config_file == base_hosts_list[-1]:
                    print("Searched the last Configuration File\n")
                    print("Cannot MODIFY or DELETE. Exiting the code.\n")
                    config_checked = False
                else:
                    print(f'Searching next Configuration File\n')                
        else:
            print(f'Config file {count}: [{config_file}]\nhas the redirection rule to Location:\n[{config_location}]\n')
            if action == 'modify': # Case 1
                print(f'Can MODIFY existing redirection: \n[{src_url}]\n-->[{config_location}]')
                print(f'to NEW redirection: \n[{src_url}]\n-->[{dst_url}]\n')
                break
            elif action == 'delete':
                if config_location == dst_url: # Case 3-1
                    print(f'Can DELETE existing redirection: \n[{src_url}]\n-->[{config_location}]\n')
                    break
                else: # Case 3-2
                    if config_file == base_hosts_list[-1]:
                        print("Searched the last Configuration File\n")
                        print("Cannot DELETE. Exiting the code.\n")
                        config_checked = False
                    else:
                        print("Searching next Configuration File\n")
        count += 1
        
        # [break] here for 1 config file (remove when we need to change to multiple config files)

    return config_pattern, config_location, config_file_loc, config_checked
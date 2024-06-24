import os
import json

from .helpers import removeDuplicates

# Step 6: Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
def findBaseHost(virt_hosts):
    # virt_hosts == list
    base_hosts = {}
    for virt_host in virt_hosts:
        base_hosts.setdefault(virt_host)

    json_file = "/usr/local/m2/setting.json"
    # json_file = "c:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\setting.json"

    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")

    with open(json_file, 'r') as file:
        data = json.load(file)
        hosting = data["hosting"]

        for item in hosting:
            if item["name"] in virt_hosts:
                base_hosts[item["name"]] = item["mode"]["basehost"]

    # Remove duplicates
    new_base_hosts = removeDuplicates(base_hosts)

    count = 1
    for base_host in new_base_hosts:
        print(f"Base Host {count}: [{new_base_hosts[base_host].split('/')[-1]}]")
        count += 1
    print('\n')

    return new_base_hosts
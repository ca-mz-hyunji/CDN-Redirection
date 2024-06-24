import json
import os

def updateFile(path_from, dst_url, action, config_file_loc):
    index = 0

    if not os.path.exists(config_file_loc):
        print(f"JSON file '{config_file_loc}' not found.")
        return
    
    with open(config_file_loc, 'r') as file:
        data = json.load(file)
        rules = data["functions"]["network"]["http"]["frontEnd"]["accessControl"]["matchingList"]
        if action == 'add':
            rule_add = {
                        "pattern":  f"$URL[{path_from}]",
                        "action": "redirect",
                        "location": dst_url,
                        "denialCode": 301
                        }
            print(f"Rule {rule_add} ADDED.")
            rules.append(rule_add)
        else:
            for rule in rules:
                if rule["pattern"] == f"$URL[{path_from}]":
                    if action == 'modify':
                        rule["location"] = dst_url
                        print(f"Rule {rule} MODIFIED.")
                        break
                    else:
                        if rule["location"] == dst_url:
                            print(f"Rule {rule} DELETED.")
                            del rules[index]
                            break
                index += 1
    
    with open(config_file_loc, 'w') as file:
        json.dump(data, file, indent=2)

'''
if __name__=='__main__':
    # ADD
    updateFile("/hello/world/0/", "https://www.kia.com/bye/world/", "add", "C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\www.kia.com-acl-testing.json")
    # MODIFY
    updateFile("/es/modelos/e-soul/", "https://www.kia.com/es/modelos/e-soul/0000/", "modify", "C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\www.kia.com-acl-testing.json")
    # DELETE
    updateFile("/hello/world/", "https://www.kia.com/bye/world/", "delete", "C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\www.kia.com-acl-testing.json")
'''
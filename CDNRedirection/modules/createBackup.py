import os
import json

from .helpers import dateTitle

def createBackup(json_path):
   if not os.path.exists(json_path):
      print(f"JSON file '{json_path}' not found.")
      return
   
   json_name = json_path.split("/")[-1]
   file_name = dateTitle(json_name)

   curr_path = str(os.getcwd())
   # Might need to change depending on the current path
   file_path = os.path.join(curr_path, "backups", file_name)

   with open(json_path, "r") as origin:
       data = json.load(origin)
   with open(file_path, "w") as copy:
       json.dump(data, copy, indent=3)
   
   print(f"Backup file {file_name} created in '{file_path}'")

'''
if __name__=='__main__':
   createBackup("C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\www.kia.com-acl.json")
'''
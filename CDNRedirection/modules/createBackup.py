import os
import shutil

from helpers import dateTitle

def createBackup(json_path):
   if not os.path.exists(json_path):
      print(f"JSON file '{json_path}' not found.")
      return
   
   json_name = json_path.split("\\")[-1]
   file_name = dateTitle(json_name)

   curr_path = str(os.getcwd())
   # Might need to change depending on the current path
   file_path = os.path.join(curr_path, "backups", file_name)

   shutil.copyfile(json_path, file_path)
   print(f"Backup file {file_name} created in 'backups' subdirectory")

'''
if __name__=='__main__':
   createBackup("C:\\Users\\Kim\\Desktop\\GitHub\\Automation\\CDNRedirection\\www.kia.com-acl.json")
'''
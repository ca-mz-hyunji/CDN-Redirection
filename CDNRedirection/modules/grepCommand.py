import subprocess

def grepCommand(path_from):
    print("Finding Redirection Log Files \n")

    ### For SSH ###
    log_files = subprocess.check_output(['grep', '-rl', path_from, '/m2log'], universal_newlines=True)
    
    log_files_list = log_files.strip().split('\n')
    log_files_list_sorted = sorted(log_files_list, key=len)

    # Remove origins
    for log_file in log_files_list_sorted:
        if log_file.find('origin') != -1:
            log_files_list_sorted.remove(log_file)
    
    # Print sorted log file lists
    count = 1
    for log_file in log_files_list_sorted:
        print(f"Log file {count}: [{log_file}]\n")
        count += 1

    return log_files_list_sorted
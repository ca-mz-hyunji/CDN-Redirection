import subprocess
import sys

# 1.3: After running the "grep" command, read the output log file names
### EDGE CASE
def LogFiles(grep):
    try:
        result = subprocess.run(grep, stdout=subprocess.PIPE, text=True, shell=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, grep, output=result.stdout, stderr=result.stderr)
        log_files = result.stdout.splitlines()
        return log_files
    except subprocess.CalledProcessError as error:
        print(f"Error occurred: {error.stderr}", file=sys.stderr)
        return []

# 1.4: Return "vi [file name]" command
def ViCommand(log_files):
    # Prioritize simpler naming conventions
    logDict = {}
    viCommand = []
    
    for log_file in log_files:
        logDict[log_file] = len(log_file)
    sortedLog = dict(sorted(logDict.items(), key=lambda item: item[1]))
    for log in sortedLog:
        shellCommand = 'vi {}'.format(log)
        viCommand.append(shellCommand)
    return viCommand
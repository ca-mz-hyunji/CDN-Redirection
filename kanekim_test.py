import os
import subprocess
import sys
import json

def search_directories(search_string, directory):
    #set to store unique virtual host name
    unique_substrings = set()

    # Execute grep command to search for the string in the specified directory and its subdirectories
    try:
        grep_output = subprocess.check_output(['grep', '-rl', search_string, directory], universal_newlines=True)
    except subprocess.CalledProcessError:
        print(f"No files found containing '{search_string}' in '{directory}'")
        return

    # Split grep output into lines and print the directory containing each file
    for line in grep_output.split('\n'):
        if line.strip():  # Skip empty lines
            print(os.path.abspath(line))
            with open(line, 'r') as f:
                for file_line in f:
                    if search_string in file_line:
                        http_index = file_line.find("HTTP")
                        if http_index != -1:
                            substring_before_http = file_line[:http_index].strip()
                            last_word_index = substring_before_http.rfind(" ")
                            if last_word_index != -1:
                                unique_substrings.add(substring_before_http[last_word_index+1:])
                                print(substring_before_http[last_word_index+1:])
    return unique_substrings

def find_basehosts(unique_substrings):
    json_file = "/usr/local/m2/setting.json"
    #Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"JSON file '{json_file}' not found.")
        return

    #Load the JSON data
    with open(json_file, 'r') as f:
        data=json.load(f)

    #Extract basehost values for names in unique_substrings
    for entry in data.get("hosting", []):
        name = entry.get("name", "")
        if name in unique_substrings:
            basehost = entry.get ("mode", {}).get("basehost", "")
            print(f"Basehost value for {name}: {basehost}")

# Main function
def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <search-string> <directory>")
        sys.exit(1)

    # Get command-line arguments
    search_string = sys.argv[1]
    directory = sys.argv[2]

    # Call the search_directories function with the provided arguments
    unique_substrings = search_directories(search_string, directory)

    #Find and print basehost values
    find_basehosts(unique_substrings)

# Entry point
if __name__ == "__main__":
    main()
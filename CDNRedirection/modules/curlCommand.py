import subprocess
import re

# Step 2: Send Curl (check Destination & make a log if there wasn't)
def curlCommand(domain, ip, path_from, dst_url, mode):

    curl_command = f'curl -I -H "HOST:{domain}" http://{ip}{path_from}'
    curl_output = subprocess.run(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if mode != 'Excel':
        print("Checking Redirection... \n")
        print(f'Running: {curl_command}\n')

        if curl_output.returncode == 0:
            print(f"Curl Command succeeded. \n")
            print(f"Output:\n{curl_output.stdout}")
        else:
            print("Curl Command failed with Error: \n")
            print(curl_output.stderr)

    # To Find the HTTP Protocol
    status_pattern = re.compile(r"HTTP/.*")
    # To Find the Redirection URL Location
    location_line = None
    loc_pattern = re.compile(r"location: .*")

    all_lines = curl_output.stdout.splitlines()

    for line in all_lines:
        if status_pattern.match(line):
            status_line = line

        if loc_pattern.match(line):
            location_line = line
            break
    
    status = status_line.split(" ")[1]

    if status == "404":
        location = None
    else:
        location = location_line.split(" ")[1]
        if mode != 'Excel':
            print("Currently Redirected to: [" + location + "]\n")
    
    if mode != 'Excel':
        print("HTTP Status: [" + status_line + "]\n")

    loc_eq_dst = False

    # If Redirection URL Location is same as dst_url
    if location == dst_url:
        loc_eq_dst = True
    
    return loc_eq_dst, location

'''
if __name__=='__main__':
    loc_eq_dst, location = httpRequest('www.kia.com','34.160.76.133','/hello/world/','https://www.kia.com/hello/world/0/')
'''
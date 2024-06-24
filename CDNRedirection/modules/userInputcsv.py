import csv
from .helpers import splitURL, IP_dict, border_msg

def userInputcsv(excel_file_path):
    user_input_dict = {}
    domain_failed = {}

    src_urls = []
    dst_urls = []
    
    with open(excel_file_path, mode='r') as file:
        lines = csv.reader(file)
        # skip header
        next(lines)
    
        # Assumme the first row is the header
        # Assume the first (A) column is the source URL
        # Assume the second (B) column is the Redirection code
        # Assume the third (C) column is the destination URL

        for line in lines:
            src_urls.append(line[0])
            dst_urls.append(line[2])

    index = 0
    while index < len(src_urls):
        domain, path_from = splitURL(src_urls[index])
        if domain not in IP_dict:
            domain = None
            ip = None
        else:
            ip = IP_dict[domain]
        
        user_input_dict[index] = {'src_url': src_urls[index],
                                    'domain': domain,
                                    'ip': ip,
                                    'path_from': path_from,
                                    'dst_url': dst_urls[index],
                                    'action': 'add'}
        index += 1

    count = 0
    for user_input in user_input_dict:
        if user_input_dict[user_input]['domain'] == None:
            domain_failed[count] = user_input_dict[user_input]
        count += 1
    
    for failed_index in domain_failed:
        # border_msg(f"Index {failed_index+1}: {domain_failed[failed_index]['src_url']} does not have a valid domain name. Try it again later.")
        user_input_dict.pop(failed_index)
    print("")

    ### For testing purpose
    '''
    for item in user_input_dict:
        print(f"[{item+1}]: {user_input_dict[item]}\n")
    '''

    return user_input_dict, domain_failed

'''
if __name__=='__main__':
    userInputcsv("C:\\Users\\Kim\\Desktop\\GitHub\\Redirecting-Automation\\CDNRedirection\\testing_files\\kia_test.csv")
'''
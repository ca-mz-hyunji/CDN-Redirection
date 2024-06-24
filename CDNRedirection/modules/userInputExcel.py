import pandas as pd
from helpers import splitURL, IP_dict, border_msg

def userInputExcel(excel_file_path):
    user_input_dict = {}
    domain_failed = {}
    
    df = pd.read_excel(excel_file_path)
    # Assumme the first row is the header
    # Assume the first (A) column is the source URL
    # Assume the second (B) column is the Redirection code
    # Assume the third (C) column is the destination URL

    src_urls = df[df.columns[0]]
    dst_urls = df[df.columns[2]]

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
            
    for index in domain_failed:
        border_msg(f"Index {index+1}: {domain_failed[index]['src_url']} does not have a valid domain name. Try it again later.")
        user_input_dict.pop(index)
    print("")

    return user_input_dict, domain_failed
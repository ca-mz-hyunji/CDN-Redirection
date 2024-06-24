from .helpers import splitURL, IP_dict

# Step 1: Get inputs from User
def userInput():
    src_url = input("\nEnter <SOURCE URL>: ")
    domain, path_from = splitURL(src_url)
    while domain not in IP_dict:
        src_url = input("Enter <SOURCE URL>: ")
        domain, path_from = splitURL(src_url)
    ip = IP_dict[domain]

    dst_url = input("Enter <DESTINATION URL>: ")
    action = input("Enter <ACTION> <add/modify/delete>: ").lower()
    while action not in ('add','modify','delete'):
        action = input("Enter <ACTION> <add/modify/delete>: ").lower()

    print("")

    return src_url, domain, ip, path_from, dst_url, action
# Step 3: Check the 8 cases (Add, Modify, Delete)
def checkAction(src_url, loc_eq_dst, location, action):
    action = action.lower()
    
    if location: 
        if action == 'add':
            if loc_eq_dst == False:
                if (location != src_url):
                    # Case 2. Add & Destination!=Location & Location!=SourceURL --> Did you mean MODIFY ?
                    print(f"{src_url} is redirected to {location}")
                    response = input("Do you want to modify instead of adding? (yes/no): ").lower()
                    while response not in ('yes','no'):
                        response = input("Do you want to modify instead of adding? (yes/no): ").lower()
                    if response == 'yes':
                        action = 'modify'
                        print(f"Current action: {action}")
                    else:
                        action = False
                        print("Cannot ADD. Exiting the code.")
            else:
                # Case 1. Add & Destination==Location --> No need to ADD
                action = False
                print("No need to ADD. Already Redirected to Destination. Exiting the code.")

        elif action == 'modify':
            if loc_eq_dst == False:
                if (location == src_url):
                    # Case 5. Modify & Destination!=Location & Location==SourceURL --> Did you mean ADD ?
                    print(f"{src_url} is redirected to {location}")
                    response = input("Do you want to add instead of modifying? (yes/no): ").lower()
                    while response not in ('yes','no'):
                        response = input("Do you want to add instead of modifying? (yes/no): ").lower()
                    if response == 'yes':
                        action = 'add'
                        print(f"Current action: {action}")
                    else:
                        action = False
                        print("Cannot MODIFY. Exiting the code.")
            else:
                # Case 4. Modify & Destination==Location --> No need to MODIFY
                action = False
                print("No need to MODIFY. Already Redirected to Destination. Exiting the code.")

        else:
            if loc_eq_dst == False:
                # Case 7. Delete & Destination!=Location --> No need to DELETE
                action = False
                print("No need to DELETE. Redirection to the Destination does not exist. Exiting the code.")
        # Case 3(add), Case 6(modify), Case 8(delete) --> Proceed with inital action    
        return action 
    else: # Case 9: 404 Error (location = None)
        return action


'''
    1. Add & Destination==Location
        * No need to ADD --> action = False
    2. Add & Destination!=Location & Location!=SourceURL
        * Need to check action again -> Did you mean MODIFY ?
    3. Add & Desitnation!=Location & Location==SourceURL
        * Good to ADD 
    4. Modify & Destination==Location
        * No need to MODIFY
    5. Modify & Destination!=Location & Location==SourceURL
        * Need to check action again -> Did you mean ADD ?
    6. Modify & Destination!=Location & Location!=SourceURL
        * Good to MODIFY
    7. Delete & Destination!=Location
        * Mo need to DELETE
    8. Delete & Destination==Location
        * Good to DELETE
'''

'''
if __name__=='__main__':
    # Case 1 --> False
    print(checkAction('http://www.kia.com/hello/world/', True, 'http://www.kia.com/hello/world/', 'ADD'))
    # Case 2 --> modify
    print(checkAction('http://www.kia.com/hello/world/', False, 'http://www.kia.ca/', 'ADD'))
    # Case 3 --> add
    print(checkAction('http://www.kia.com/hello/world/', False, 'http://www.kia.com/hello/world/', 'ADD'))
    # Case 4 --> False
    print(checkAction('http://www.kia.com/hello/world/', True, 'http://www.kia.ca/', 'MODIFY'))
    # Case 5 --> add
    print(checkAction('http://www.kia.com/hello/world/', False, 'http://www.kia.com/hello/world/', 'MODIFY'))
    # Case 6 --> modify
    print(checkAction('http://www.kia.com/hello/world/', False, 'http://www.kia.ca/', 'MODIFY'))
    # Case 7 --> False
    print(checkAction('http://www.kia.com/hello/world/', False, 'http://www.kia.ca/', 'Delete'))
    # Case 8 --> delete
    print(checkAction('http://www.kia.com/hello/world/', True, 'http://www.kia.ca/', 'Delete'))
'''
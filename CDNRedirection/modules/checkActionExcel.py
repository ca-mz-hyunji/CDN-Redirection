# Step 3: Check the 8 cases (Add, Modify, Delete)
def checkActionExcel(src_url, loc_eq_dst, location, action):
    action = action.lower()

    if location: 
        if action == 'add':
            if loc_eq_dst == False:
                if (location != src_url):
                    # Case 2. Add & Destination!=Location & Location!=SourceURL --> Did you mean MODIFY ?
                    action = 'modify'
            else:
                # Case 1. Add & Destination==Location --> No need to ADD
                action = False

        elif action == 'modify':
            if loc_eq_dst == False:
                if (location == src_url):
                    # Case 5. Modify & Destination!=Location & Location==SourceURL --> Did you mean ADD ?
                    action = 'add'
            else:
                # Case 4. Modify & Destination==Location --> No need to MODIFY
                action = False

        else:
            if loc_eq_dst == False:
                # Case 7. Delete & Destination!=Location --> No need to DELETE
                action = False
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
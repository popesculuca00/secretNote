import os
def load_user_data( user = None ):
    if user == None :
        return "" , {"nightmode" : "off"}

    try:
        f = open(user , "r")
        options = f.readline()
        text = f.read()
        f.close()
        return options , text
    except :
        f = open(user, "w")
        f.write("off\nYou don't have any previously saved text")
        f.close()
        return load_user_data(user)



def save_user_data( newtext , user = None , prefs = None ):

    if not prefs :
        prefs = "off"
    if "on" in prefs :
        prefs = "on"
    f = open(user , "w")
    savefile = f"{prefs}\n{newtext}"
    print("file saved")
    f.write(savefile)
    f.close()

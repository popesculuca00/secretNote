import os
def load_user_data( user = None ):
    if user == None :
        return "" , {"nightmode" : "off"}

    try:
        f = open(user , "r")
        options = f.readline()
        text = f.read()
        f.close()

        #print(user.split("\\")[-2])
        #enc = encoder(user.split("\\")[-2])
        #options = enc.get_dec_text(options)
        #text = enc.get_dec_text(text)


        return options , text
    except :
        f = open(user, "w")

        #enc = encoder(user.split("\\")[-2])
        #text = enc.get_enc_text("off\nYou don't have any previously saved text")
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

    #enc = encoder(user.split("\\")[-2])
    #savefile = enc.get_enc_text(savefile)

    f.write(savefile)
    f.close()

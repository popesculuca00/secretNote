import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from user_utils import load_user_data , save_user_data
from tkinter.messagebox import showinfo

def donothing():
    pass

class note_window:
    def __init__(self , width , height , user , root):
        self.user = user
        self.width = width
        self.height = height
        self.root = root
        self.root.title("secretNote" + " - " + user.split("\\")[-2])
        self.menu = Menu(self.root)
        self.textarea = Text(self.root)
        self.nmode , hist = load_user_data(self.user)

        if "on" in self.nmode :
            self.night_mode_on()

        self.textarea.insert(1.0 , hist)

        self.root.geometry('%dx%d+%d+%d' % (width,
                                            height,
                                            0, 0))

        self.textarea.grid(sticky=N + E + S + W )        # define text area
        self.root.grid_rowconfigure(0 , weight = 1 )    # and make it resizable
        self.root.grid_columnconfigure(0 , weight = 1)
        self.root.bind("<Control_L><s>" , func = lambda _:save_user_data(self.textarea.get(1.0 , "end-1c"),
                                                                         self.user,
                                                                         self.nmode ))
        self.root.bind("<Control_L><q>" , func = lambda _:self.root.quit() )
        self.root.bind("<Control_L><n>" , func = lambda _: self.night_mode_off() if self.nmode == "on"
                                                                                     else self.night_mode_on() )

        self.menubar = Menu(self.root)
        accmenu = Menu(self.menubar, tearoff=0)

        helpmenu = Menu(self.menubar, tearoff=0)
        prefmenu = Menu(self.menubar, tearoff=0)

        prefmenu.add_separator()

        nightmode = Menu(prefmenu , tearoff = 0)
        prefmenu.add_cascade(label = "Nightmode" , menu = nightmode)

        nightmode.add_command(label = "On" , command = lambda _:self.night_mode_on)
        nightmode.add_command(label = "Off" , command=lambda _: self.night_mode_off)

        fontsize = Menu(prefmenu , tearoff = 0)
        prefmenu.add_cascade(label = "Font size" , menu = fontsize)
        fontsize.add_command(label="Small font" ,  command = self.textarea.config(font = 10))
        fontsize.add_command(label="Medium font",  command = self.textarea.config(font = 20))
        fontsize.add_command(label="Big font"   ,  command = self.textarea.config(font = 30))
        fontsize.add_command(label="Very big font",command = self.textarea.config(font = 40))

        self.menubar.add_cascade(label = "Preferences" , menu = prefmenu)



        accmenu.add_separator()
        accmenu.add_command(label = "Save"   , command = lambda :save_user_data( self.textarea.get(1.0 , "end-1c") , self.user , self.nmode ))
        accmenu.add_command(label ="Log out" , command = lambda :self.logout())
        accmenu.add_command(label=     "Exit", command=self.root.quit)

        self.menubar.add_cascade(label="Account", menu=accmenu)


        helpmenu.add_command(label="About...", command=lambda :self.about_menu())
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=self.menubar)

    def logout(self):

        self.menubar.destroy()
        self.textarea.destroy()
        self.root.quit()
        return 0

    def night_mode_on(self):
        self.nmode = "on"
        self.root.config(bg="black" )
        self.textarea.config(bg = "black")
        self.textarea.config(fg = "green" )

    def night_mode_off(self):
        self.nmode = "off"
        self.root.config(bg = "white")
        self.textarea.config(bg = "white")
        self.textarea.config(fg = "black")

    def run(self):
        self.root.mainloop()

    def about_menu(self):
            showinfo("About this app", "App was created using Tkinter.")
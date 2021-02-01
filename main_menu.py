from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from face_detector import face_analyzer
import numpy as np
from user_utils import load_user_data
import os

class MainWindow():
    def __init__(self, window):

        self.auth = face_analyzer()
        self.login_showing = 0
        self.register_showing = 0
        self.user = None
        self.window = window
        self.window.geometry("1100x500")
        self.window.config(bg = "Black" )
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20 # Interval in ms to get the latest frame
        self.continue_feed = 0

        # Create canvas for image
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height , bg = "Black" )
        self.canvas.pack(side = RIGHT , fill = BOTH)
        self.canvas.create_text(320, 250, fill="darkgreen", font="Times 30 italic bold",
                                text="Welcome to secretNote!")
        self.exit   = Button(self.window , text = "Quit",
                             width=70, height = 2, padx=10, pady=10,
                             bg = "Green",
                             command=lambda: self.window.quit())
        self.exit.pack(side = BOTTOM)
        self.cancel = Button(self.window, text="Cancel",
                             width=70, height = 2, padx=10, pady=10,
                             bg="Green",
                             command=lambda: self.reinit())#self.cancel_button())
        self.cancel.pack(side=BOTTOM)

        self.register=Button( self.window , text = "Register" ,
                             width=70, height = 2, padx = 10, pady = 10 ,
                             bg = "Green" ,
                             command= lambda:self.register_menu())
        self.register.pack(side = BOTTOM)

        self.login = Button( self.window , text = "Log in" ,
                             width=70, height = 2, padx = 10, pady = 10 ,
                             bg = "Green" ,
                             command= lambda:self.login_pressed())
        self.login.pack(side = BOTTOM)


        self.canvas.create_window(900 ,400 )


    def reinit(self):
        self.kill_camera()
        self.register_showing = 0
        self.login_showing = 0

        for elem in self.window.winfo_children()[1:]:
            elem.destroy()
        self.exit   = Button(self.window , text = "Quit",
                             width=70, height = 2, padx=10, pady=10,
                             bg = "Green",
                             command=lambda: self.window.quit())
        self.exit.pack(side = BOTTOM)
        self.cancel = Button(self.window, text="Cancel",
                             width=70, height = 2, padx=10, pady=10,
                             bg="Green",
                             command=lambda: self.reinit())#self.cancel_button())
        self.cancel.pack(side=BOTTOM)

        self.register=Button( self.window , text = "Register" ,
                             width=70, height = 2, padx = 10, pady = 10 ,
                             bg = "Green" ,
                             command= lambda:self.register_menu())
        self.register.pack(side = BOTTOM)

        self.login = Button( self.window , text = "Log in" ,
                             width=70, height = 2, padx = 10, pady = 10 ,
                             bg = "Green" ,
                             command= lambda:self.login_pressed())
        self.login.pack(side = BOTTOM)

    def kill_camera(self):
        self.continue_feed = 0
        try:
            self.cap.release()
        except: pass



    def show_login(self):
        self.window.mainloop()
        self.reinit()
        self.canvas.destroy()
        self.login.destroy()
        self.register.destroy()
        self.exit.destroy()
        self.cancel.destroy()

    def login_pressed(self):
        if self.login_showing == 0:
            self.snapshot = Button(self.window, text="Authentificate",
                                   width=70, height=2, padx=10, pady=10,
                                   bg="Green",
                                   command=lambda: self.authentificate())
            self.login.destroy()
            self.register.destroy()
            self.snapshot.pack(side=BOTTOM)
            self.start_video()
            self.login_showing = 1


    def close_video(self):
        self.cap.release()
        self.continue_feed = 0

    def authentificate(self):
        cv2.imwrite("auth_pers.jpg" , np.float32(self.image_raw))
        self.user = self.auth.find_best_match()
        if self.user:
            self.window.quit()



    def get_user(self):
        return self.user

    def start_video(self):

        if self.continue_feed == 0:
            self.cap = cv2.VideoCapture(0)


        self.continue_feed = 1
        self.update_image()


    def update_image(self):


        if self.continue_feed != 0:



            self.image = cv2.flip(cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) , 1)


            self.image = Image.fromarray(self.image)
            self.image_raw = self.image
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0 , anchor = NW , image=self.image)
            self.window.after(self.interval, self.update_image)


        else :
            try:
                self.snapshot.destroy()
            except: pass
            self.image = 0


    def register_menu(self):
        if self.register_showing == 0 :
            self.login.forget()
            #self.new_user= Text(self.window , height = 1 , padx = 100)   ############################################3
            self.register.config(text = "Create account" , command = lambda: self.register_new_user())
            #self.new_user.config(font = 32)

            #self.new_user.pack(side = BOTTOM)

            self.new_user = Entry(self.window, width=40 , font = 32)
            self.new_user.pack(side = BOTTOM)
            self.new_user.insert(0, "Enter your name and take a photo")
            self.new_user.configure(state=DISABLED)

            def on_click(event):
                self.new_user.configure(state=NORMAL)
                self.new_user.delete(0, END)
                self.new_user.unbind('<Button-1>', on_click_id)
            on_click_id = self.new_user.bind('<Button-1>', on_click)
            self.start_video()
            self.register_showing = 1


    def register_new_user(self):
        v= self.new_user.get()
        os.mkdir(f"userdata//{v}")
        self.image_raw = cv2.cvtColor(np.float32(self.image_raw) , cv2.COLOR_BGR2RGB)
        cv2.imwrite(f"userdata//{v}//userface.jpg" , self.image_raw)
        f = open(f"userdata//{v}//text.txt" , "w")
        f.write("off\nYou don't have any previously saved text")
        f.close()
        self.reinit()

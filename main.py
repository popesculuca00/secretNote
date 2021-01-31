from main_window import note_window
from Loginpage import MainWindow
from tkinter.filedialog import *
class main:

    def __init__(self):
        self.root = Tk()
        self.person = "Luca"

    def login_page(self):
        login = MainWindow(self.root )
        login.show_login()
        login.kill_camera()
        self.person = login.get_user()
        if self.person != None :
            return self.user_page()

    def user_page(self):
        user_window = note_window(1100 , 500 , self.person , self.root)
        option = user_window.run()
        self.start_app()

    def start_app(self):
        self.login_page()

if __name__ == '__main__':
    app = main()
    app.start_app()




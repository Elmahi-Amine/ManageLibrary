import tkinter as tk
from controllers.app_controller import AppController
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LibManage")
        self.geometry("920x580")
        self.configure(bg="#f5f5f5")
        #self.iconbitmap("resoucres/icon.png")
        self.controller = AppController(self)

if __name__ == "__main__" :
    app = App()
    app.mainloop()
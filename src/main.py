import tkinter as tk
from controllers.app_controller import AppController
from tkinter import ttk
import tkinter.font as tkfont

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LibManage")
        self.geometry("920x580")
        self.configure(bg="#f5f5f5")
        tkfont.nametofont("TkDefaultFont").configure(size=11)

        # Define custom fonts
        font_small = ("Arial", 10)
        font_medium = ("Arial", 12)
        font_large = ("Arial", 16)

        # Use ttk.Style for specific widgets
        style = ttk.Style()
        style.configure("TLabel", font=font_medium)
        style.configure("Treeview", font=font_small)  # rows in treeview
        style.configure("Treeview.Heading", font=font_large)
        style.configure("TButton", font=font_medium)
        style.configure("TEntry", font=font_medium)
        self.controller = AppController(self)

if __name__ == "__main__" :
    app = App()
    app.mainloop()
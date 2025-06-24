import tkinter as tk
class HomeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dbdbdb")
        tk.Label(self, text="Home", font=("Arial", 18), bg="#dbdbdb").pack(pady=40)
        
   
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow library required

from controllers.livre_controller import LivreController
class LivreView(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent,bg="#dbdbdb")
        self.controller = LivreController(self)
        #self.label = tk.Label(self,text="Livres",font=("Arial",18))
        self.search_key = tk.StringVar()
        self.search_method = tk.StringVar(value="")

        self.search_bar = tk.Frame(self, bg="#dbdbdb", height=50)
        self.search_bar.pack(fill="x", side="top")

        # Style for the Combobox
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox",
                        fieldbackground="white",
                        background="white",
                        foreground="black",
                        borderwidth=0,
                        padding=5)
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])

        # Combobox for method
        self.method_choice = ttk.Combobox(
            self.search_bar,
            textvariable=self.search_method,
            values=["isbn", "copy-id", "titre", "auteur", "date"],
            state="readonly",
            width=10
        )
        self.method_choice.pack(side="left", padx=(0, 10), pady=5)

        # Entry for search key
        self.search_entry = tk.Entry(
            self.search_bar,
            textvariable=self.search_key,
            font=("Segoe UI", 12),
            bg="white",
            fg="black",
            relief="flat",
            insertbackground="black"
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)

        # Load and resize image
        img = Image.open("src/resources/search.png")
        img = img.resize((30, 30), Image.LANCZOS)
        self.search_icon = ImageTk.PhotoImage(img)

        # Image button
        self.search_button = tk.Button(
            self.search_bar,
            image=self.search_icon,
            command=self.controller.perform_search,
            bg="white",
            relief="flat",
            width=35,
            height=35
        )
        
        self.search_button.pack(side="right", pady=5)
        self.search_result_frame= tk.Frame(self,bg ="#ffffff")
        self.search_result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.search_entry.bind("<Return>", lambda event: self.controller.perform_search())



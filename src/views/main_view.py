import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.app_controller import AppController 
class MainView(tk.Frame):
    def __init__(self, root, controller:"AppController"):
        super().__init__(root, bg="#f5f5f5")
        self.controller = controller
        self.menu_width = 150
        self.pack(fill="both", expand=True)

        # Top bar
        self.top_bar = tk.Frame(self, height=40, bg="#ffffff", relief="raised", bd=1)
        self.top_bar.pack(fill="x", side="top")

        self.menu_button = tk.Button(
            self.top_bar, text="☰", font=("Arial", 18), bg="#ffffff", bd=0,
            command=self.controller.toggle_menu
        )
        self.menu_button.pack(side="left", padx=10, pady=5)

        self.current_view_label=tk.Label(self.top_bar,text="",font=("Arial",12),bg="#ffffff",bd=0)
        self.current_view_label.pack(side="left",padx=10,pady=5)

        # Content area (below top bar)
        self.content_area = tk.Frame(self, bg="#fafafa")
        self.content_area.pack(fill="both", expand=True)

        # Side menu (initially hidden)
        self.menu_frame = tk.Frame(root, bg="#333333", width=self.menu_width)
        self.menu_frame.place(x=-self.menu_width, y=0)

        self.create_menu_buttons()

    def create_menu_buttons(self):
        btn_style = {
            "font": ("Arial", 14),
            "bg": "#333333",
            "fg": "#ffffff",
            "activebackground": "#555555",
            "activeforeground": "#ffffff",
            "relief": "flat",
            "bd": 0,
            "anchor": "w",
            "padx": 20
        }
        home_btn = tk.Button(self.menu_frame, text="Home", **btn_style,
                            command=self.controller.show_Home_view)
        home_btn.place(x=0, y=50, width=self.menu_width, height=40)

        members_btn = tk.Button(self.menu_frame, text="Membres", **btn_style)
        members_btn.place(x=0, y=90, width=self.menu_width, height=40)

        livres_btn = tk.Button(self.menu_frame, text="Livres",**btn_style,
                            command=self.controller.show_livre_view)
        livres_btn.place(x=0,y=130,width=self.menu_width,height=40)
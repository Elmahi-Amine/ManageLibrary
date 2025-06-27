import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from typing import TYPE_CHECKING
if TYPE_CHECKING :
    from controllers.home_controller import HomeController

class HomeView(tk.Frame):
    def __init__(self, controller:"HomeController", parent):
        super().__init__(parent)
        self.controller = controller

        self.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self, text="Dashboard", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.button = ttk.Button(self, text="Emprunter" ,
                            command=self.controller.load_emprunt_view)
        self.button.pack(pady=10)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def display_charts(self, fig):
        # Clear existing charts
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        chart = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)
   
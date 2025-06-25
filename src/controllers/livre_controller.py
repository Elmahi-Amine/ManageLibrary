from typing import TYPE_CHECKING
from models.livre import LivreDAO

import tkinter as tk
from tkinter import ttk
if TYPE_CHECKING :
    from views.livre_view import LivreView
class LivreController :
    def __init__(self,view:"LivreView"):
        self.view = view
    def perform_search(self):
        _key=self.view.search_key.get()
        parameter = self.view.search_method.get()
        livredao = LivreDAO()
        print(f"[perform search]: parameter : {parameter} key : {_key}")
        print(f"[search] : value1.titre : {livredao.search(parameter,_key)[0].titre}")
        self.afficher_table_livres(self.view.search_result_frame,livredao.search(parameter,_key))

        


    def afficher_table_livres(self,parent, search_results):
        # Clear the parent widget (if anything exists)
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Create the Treeview (table)
        colonnes = ("isbn", "copy_id", "titre", "auteur", "annee", "genre","copie_id","statut","copies_count")
        table = ttk.Treeview(parent, columns=colonnes, show="headings")
        
        # Set column headings
        table.heading("isbn", text="ISBN")
        table.heading("copy_id", text="Copy ID")
        table.heading("titre", text="Titre")
        table.heading("auteur", text="Auteur")
        table.heading("annee", text="Année")
        table.heading("genre", text="Genre")
        table.heading("copie_id", text="Copie ID")
        table.heading("statut",text="statut")
        table.heading("copies_count",text="nbr copies")

        # Optional: Set column widths
        for col in colonnes:
            table.column(col, width=100)

        # Insert rows
        dao = LivreDAO()
        for item in search_results:
            livre = item
            count = dao.count_copies(item.isbn)
            print("result titre : ",livre.titre)
            table.insert("", "end", values=(
                livre.isbn,
                livre.copy_id,
                livre.titre,
                livre.auteur,
                livre.annee,
                livre.genre,
                livre.copy_id,
                livre.statut,
                count
            ))

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Make the table expandable inside the parent
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
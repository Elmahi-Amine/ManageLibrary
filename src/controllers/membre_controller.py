from typing import TYPE_CHECKING
from models.membre import Membre, MembreDAO  # You must define these
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

if TYPE_CHECKING:
    from views.membre_view import MembreView

class MembreController:
    def __init__(self, view: "MembreView"):
        self.view = view

    def perform_membre_search(self):
        _key = self.view.search_key.get()
        parameter = self.view.search_method.get()
        membre_dao = MembreDAO()
        print(f"[perform search]: parameter: {parameter}, key: {_key}")
        results = membre_dao.search(parameter, _key)
        self.afficher_table_membres(self.view.search_result_frame, results)

    def afficher_table_membres(self, parent, search_results):
        for widget in parent.winfo_children():
            widget.destroy()

        colonnes = ("id", "name")  # Adjust columns as needed
        table = ttk.Treeview(parent, columns=colonnes, show="headings")

        for col in colonnes:
            table.heading(col, text=col.capitalize())
            table.column(col, width=200)

        for membre in search_results:
            table.insert("", "end", values=(membre.id, membre.nom))

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        context_menu = tk.Menu(table, tearoff=0)
        context_menu.add_command(label="Supprimer", command=lambda: self._handle_action("supprimer", table))
        context_menu.add_command(label="Voir les livres empruntes", command=lambda: self._handle_action("voir_livres_emprnt",table))
        context_menu.add_command(label="Emprunter", command=lambda: self._handle_action("emprunter",table))


        def show_context_menu(event):
            selected_item = table.identify_row(event.y)
            if selected_item:
                if selected_item not in table.selection():
                    table.selection_set(selected_item)
                context_menu.tk_popup(event.x_root, event.y_root)

        table.bind("<Button-3>", show_context_menu)

    def _handle_action(self, action, table):
        selected_items = table.selection()
        print(f"[{action}] selected rows:")
        for item_id in selected_items:
            row_values = table.item(item_id, "values")
            print(f" - {row_values}")
        if action == "supprimer":
            if not messagebox.askyesno("Confirmation", "Are you sure you want to delete selected members?"):
                return
            dao = MembreDAO()
            for item_id in selected_items:
                values = table.item(item_id, "values")
                dao.supprimer(values[0])  # assuming ID is enough
            self.perform_membre_search()

    def create_add_membre_form(self):
        parent = self.view

        for widget in parent.winfo_children():
            widget.destroy()

        style = ttk.Style()
        style.theme_use("default")
        bg_color = "white"
        fg_color = "black"
        entry_bg = "#dbdbdb"
        button_color = "#dbdbdb"
        hover_color = "#c0c0c0"

        parent.configure(bg=bg_color)
        style.configure("TEntry", fieldbackground=entry_bg, background=entry_bg,
                        foreground=fg_color, borderwidth=0, padding=5)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("TButton", background=button_color, foreground=fg_color,
                        borderwidth=0, padding=(10, 5), font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", hover_color)])

        fields = {
            "ID": tk.StringVar(),
            "Name": tk.StringVar()
        }

        form_frame = tk.Frame(parent, bg=bg_color)
        form_frame.pack(padx=40, pady=40, anchor="center")

        for i, (label_text, var) in enumerate(fields.items()):
            label = ttk.Label(form_frame, text=label_text)
            entry = ttk.Entry(form_frame, textvariable=var)
            label.grid(row=i, column=0, sticky="e", padx=10, pady=8)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)

        form_frame.columnconfigure(1, weight=1)

        def restore_membre_view():
            from views.membre_view import MembreView
            for widget in parent.winfo_children():
                widget.destroy()
            membre_view = MembreView(parent)
            membre_view.pack(fill="both", expand=True)

        def ajouter_membre():
            membre = Membre(
                id=fields["ID"].get(),
                nom=fields["Name"].get()
            )
            if not (membre.id and membre.nom):
                messagebox.showerror("Erreur", "ID et Nom sont obligatoires.")
                return

            dao = MembreDAO()
            dao.ajouter(membre)
            messagebox.showinfo("Succès", "Membre ajouté avec succès.")
            restore_membre_view()

        def annuler():
            if messagebox.askyesno("Annuler", "Voulez-vous annuler l’ajout ?"):
                restore_membre_view()

        button_frame = tk.Frame(form_frame, bg=bg_color)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0))

        add_button = ttk.Button(button_frame, text="Ajouter", command=ajouter_membre)
        cancel_button = ttk.Button(button_frame, text="Annuler", command=annuler)

        add_button.pack(side="left", padx=10)
        cancel_button.pack(side="left", padx=10)

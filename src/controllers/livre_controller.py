from typing import TYPE_CHECKING
from models.livre import Livre, LivreDAO

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        search_result = livredao.search(parameter,_key)
        if not _key :
            search_result = livredao.get_all_livre()
        self.afficher_table_livres(self.view.search_result_frame,search_result)

    def afficher_table_livres(self, parent, search_results):
        for widget in parent.winfo_children():
            widget.destroy()

        colonnes = ("isbn", "copy_id", "titre", "auteur", "annee", "genre", "copie_id", "statut", "copies_count")
        table = ttk.Treeview(parent, columns=colonnes, show="headings", selectmode="extended")  # enable multiple selection

        for col in colonnes:
            table.heading(col, text=col.capitalize())
            table.column(col, width=100)

        dao = LivreDAO()
        for item in search_results:
            count = dao.count_copies(item.isbn)
            table.insert("", "end", values=(
                item.isbn, item.copy_id, item.titre, item.auteur,
                item.annee, item.genre, item.copy_id, item.statut, count
            ))

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Create context menu
        context_menu = tk.Menu(table, tearoff=0)
        context_menu.add_command(label="Supprimer", command=lambda: self._handle_action("supprimer", table))
        context_menu.add_command(label="Emprunter", command=lambda: self._handle_action("emprunter", table))
        context_menu.add_command(label="Retourner", command=lambda: self._handle_action("retourner", table))

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
            if not messagebox.askyesno("Confirmation", "Are you sure you want to delete selected items?"):
                return    
            dao = LivreDAO()
            for item_id in selected_items:
                values = table.item(item_id, "values")
                print(f"[handle action] {values[0]} , {values[1]}")
                dao.supprimer(values[0],values[1])
            self.perform_search() #refrech the table
        elif action == "retourner":
            if len(selected_items)==1:
                for itm in selected_items:
                    values= table.item(itm,"values")
                    if(values[7]=="disponible"):
                        messagebox.showerror("Erreur","Le livre et disponible")
                        return 
                    if not messagebox.askyesno("Confirmation","et ce que vous ete sure ?"):
                        return
                    ldao = LivreDAO()
                    from models.membre import MembreDAO
                    mdao = MembreDAO()
                    ldao.retourner(values[0],values[1])
                    mdao.retourner(values[0],values[1])
                self.perform_search()
        elif action == "emprunter":
            if len(selected_items)>1 or len(selected_items)==0:
                return 
            for item_id in selected_items:
                values = table.item(item_id,"values")
                self.open_emprunt_dialog(values[0],values[1])
            self.perform_search()
                    
                    
    def open_emprunt_dialog(self,isbn,copy_id):
        # Get the top-level window from the current view
        root_window = self.view.winfo_toplevel()

        # Create a new Toplevel window as a modal dialog
        dialog = tk.Toplevel(root_window)
        dialog.title("📘 Emprunt")
        dialog.geometry("600x400")
        dialog.configure(bg="white")
        dialog.transient(root_window)     # Show dialog on top of parent
        dialog.grab_set()                 # Make it modal (block interaction with root)
        
        # Create the Emprunt controller (will auto-create the view)
        from controllers.emprunt import EmpruntController
        EmpruntController(dialog,caller="Livre",var1=isbn,var2=copy_id)

        # Wait for the dialog to close
        root_window.wait_window(dialog)
        self.perform_search()
        # Code here continues only after dialog is closed
        print("Borrowing dialog closed.")


    def create_add_book_form(self):
        parent = self.view

        # Clear previous content
        for widget in parent.winfo_children():
            widget.destroy()

        # Apply modern styles
        style = ttk.Style()
        style.theme_use("default")

        bg_color = "white"
        fg_color = "black"
        entry_bg = "#dbdbdb"
        button_color = "#dbdbdb"
        hover_color = "#c0c0c0"

        parent.configure(bg=bg_color)

        style.configure("TEntry",
            fieldbackground=entry_bg,
            background=entry_bg,
            foreground=fg_color,
            borderwidth=0,
            padding=5
        )

        style.configure("TLabel",
            background=bg_color,
            foreground=fg_color,
            font=("Segoe UI", 10)
        )

        style.configure("TButton",
            background=button_color,
            foreground=fg_color,
            borderwidth=0,
            padding=(10, 5),
            font=("Segoe UI", 10, "bold")
        )
        style.map("TButton", background=[("active", hover_color)])

        fields = {
            "ISBN": tk.StringVar(),
            "Copy ID": tk.StringVar(),
            "Titre": tk.StringVar(),
            "Auteur": tk.StringVar(),
            "Année": tk.StringVar(),
            "Genre": tk.StringVar(),
            "Statut": tk.StringVar(value="disponible")
        }

        form_frame = tk.Frame(parent, bg=bg_color)
        form_frame.pack(padx=40, pady=40, anchor="center")

        for i, (label_text, var) in enumerate(fields.items()):
            label = ttk.Label(form_frame, text=label_text)
            entry = ttk.Entry(form_frame, textvariable=var)
            label.grid(row=i, column=0, sticky="e", padx=10, pady=8)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)

        form_frame.columnconfigure(1, weight=1)

        def restore_livre_view():
            from views.livre_view import LivreView
            for widget in parent.winfo_children():
                widget.destroy()
            livre_view = LivreView(parent)
            livre_view.pack(fill="both", expand=True)

        def ajouter_livre():
            livre = Livre(
                copy_id=fields["Copy ID"].get(),
                isbn=fields["ISBN"].get(),
                titre=fields["Titre"].get(),
                auteur=fields["Auteur"].get(),
                annee=fields["Année"].get(),
                genre=fields["Genre"].get(),
                statut=fields["Statut"].get()
            )

            if not (livre.copy_id and livre.isbn and livre.titre):
                messagebox.showerror("Erreur", "ISBN, Copy ID et Titre sont obligatoires.")
                return

            dao = LivreDAO()
            dao.ajouter(livre)
            messagebox.showinfo("Succès", "Livre ajouté avec succès.")
            restore_livre_view()  # ✅ Return to LivreView after adding

        def annuler():
            if messagebox.askyesno("Annuler", "Voulez-vous annuler l’ajout ?"):
                restore_livre_view()  # ✅ Return to LivreView after cancel

        # Add and Cancel buttons
        button_frame = tk.Frame(form_frame, bg=bg_color)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0))

        add_button = ttk.Button(button_frame, text="Ajouter", command=ajouter_livre)
        cancel_button = ttk.Button(button_frame, text="Annuler", command=annuler)

        add_button.pack(side="left", padx=10)
        cancel_button.pack(side="left", padx=10)

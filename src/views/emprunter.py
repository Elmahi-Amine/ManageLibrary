import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from models.livre import LivreDAO,Livre
from models.membre import MembreDAO,Membre
if TYPE_CHECKING :
    from controllers.emprunt import EmpruntController
class EmpruntView(tk.Frame):
    def __init__(self, parent, controller:"EmpruntController"):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        self.style = ttk.Style()
        self.configure_styles()

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.slide1 = tk.Frame(self.container, bg="white")
        self.slide2 = tk.Frame(self.container, bg="white")

        self.slide1.grid(row=0, column=0, sticky="nsew")
        self.slide2.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.search_key = ""
        self.search_param = ""

        self.create_slide1()
        self.create_slide2()

        self.show_slide(1)

    def configure_styles(self):
        self.style.theme_use("default")

        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=30,
                             fieldbackground="white",
                             borderwidth=0)
        self.style.map("Treeview", background=[("selected", "#dbdbdb")])

        self.style.configure("TButton",
                             background="#dbdbdb",
                             foreground="black",
                             padding=6,
                             relief="flat",
                             font=("Segoe UI", 11))
        self.style.map("TButton", background=[("active", "#c4c4c4")])

    def show_slide(self, num):
        # Reset search parameters on slide switch
        self.search_key = ""
        self.search_param = ""


        if num == 1:        
            if self.controller.caller == "Membre":
                self.search_key = self.controller.var1
                self.search_param = "id"
            self.update_table("membre")  # Just placeholder for now
            self.clear_search_slide1()
            self.slide1.tkraise()

            if self.controller.caller == "Membre":
                for itm_id in self.member_table.get_children():
                    values = self.member_table.item(itm_id,"values")
                    if(values[0]==self.controller.var1):
                        self.member_table.selection_set(itm_id)
        else:
            self.clear_search_slide2()
            self.slide2.tkraise()
            self.update_table("livre")
            if self.controller.caller=="Livre":
                self.search_key = self.controller.var1
                self.search_param = "isbn"
                print("[we reached update table livre ]")
                self.update_table("livre")
                for item_id in self.book_table.get_children():
                    values = self.book_table.item(item_id,"value")
                    print(f"[we reached the for loop: if param :{values[2]} ]")
                    if values[2]== self.controller.var2:
                        print(f"[we reached showlide 2 set selection ] isbn : {self.controller.var1} copy_id :{self.controller.var2}: selected item copy id:{values[2]}")
                        self.book_table.selection_set(item_id)
    
        
        

    def create_slide1(self):
        for widget in self.slide1.winfo_children():
            widget.destroy()

        wrapper = tk.Frame(self.slide1, bg="white", bd=2, relief="flat")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(wrapper, text="🔍 Rechercher Membre", font=("Segoe UI", 18, "bold"), bg="white", fg="black")
        label.pack(pady=(0, 20))

        # Search controls
        search_frame = tk.Frame(wrapper, bg="white")
        search_frame.pack(pady=(0, 15))

        self.member_search_var = tk.StringVar()
        self.member_search_entry = ttk.Entry(search_frame, textvariable=self.member_search_var, width=25)
        self.member_search_entry.grid(row=0, column=0, padx=5)

        self.member_param_var = tk.StringVar(value="ID")
        self.member_param_choice = ttk.Combobox(search_frame, textvariable=self.member_param_var, state="readonly", width=10)
        self.member_param_choice["values"] = ("id", "nom")
        self.member_param_choice.grid(row=0, column=1, padx=5)

        search_btn = ttk.Button(search_frame, text="Search", command=self.on_member_search)
        search_btn.grid(row=0, column=2, padx=5)

        self.member_table = ttk.Treeview(
            wrapper, columns=("ID", "Name"), show="headings", selectmode="browse", height=6
        )
        self.member_table.heading("ID", text="ID")
        self.member_table.heading("Name", text="Name")
        self.member_table.column("ID", width=100)
        self.member_table.column("Name", width=200)
        self.member_table.pack(pady=10)

        for i in range(5):
            self.member_table.insert("", "end", values=(f"M{i+1}", f"Member {i+1}"))

        self.selected_membre =self.member_table.selection()
        next_btn = ttk.Button(wrapper, text="➡ Next", command=self.controller.handle_next)
        next_btn.pack(pady=20)

    def create_slide2(self):
        for widget in self.slide2.winfo_children():
            widget.destroy()

        wrapper = tk.Frame(self.slide2, bg="white", bd=2, relief="flat")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(wrapper, text="📚 Selectionner le livre a emprunter", font=("Segoe UI", 18, "bold"), bg="white")
        label.pack(pady=(0, 20))

        # Search controls
        search_frame = tk.Frame(wrapper, bg="white")
        search_frame.pack(pady=(0, 15))

        self.book_search_var = tk.StringVar()
        self.book_search_entry = ttk.Entry(search_frame, textvariable=self.book_search_var, width=30)
        self.book_search_entry.grid(row=0, column=0, padx=5)

        self.book_param_var = tk.StringVar(value="ISBN")
        self.book_param_choice = ttk.Combobox(search_frame, textvariable=self.book_param_var, state="readonly", width=12)
        self.book_param_choice["values"] = ("isbn", "copy-id", "titre", "auteur","date")
        self.book_param_choice.grid(row=0, column=1, padx=5)

        search_btn = ttk.Button(search_frame, text="Search", command=self.on_book_search)
        search_btn.grid(row=0, column=2, padx=5)

        self.book_table = ttk.Treeview(
            wrapper,
            columns=("ISBN", "Title", "Copy ID", "Author", "Year", "Genre", "Status", "Count"),
            show="headings",
            selectmode="extended",
            height=6
        )
        for col in self.book_table["columns"]:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=100, anchor="center")
        self.book_table.pack(pady=10)

        for i in range(10):
            self.book_table.insert("", "end", values=(
                f"ISBN-{i+1}", f"Title {i+1}", f"CPY{i+1}", "Author A", "2020", "Fiction", "Available", 1
            ))

        btn_frame = tk.Frame(wrapper, bg="white")
        btn_frame.pack(pady=20)

        back_btn = ttk.Button(btn_frame, text="⬅ Back", command=self.controller.handle_back)
        back_btn.grid(row=0, column=0, padx=10)

        emprunter_btn = ttk.Button(btn_frame, text="✅ Emprunter", command=self.controller.handle_emprunter)
        emprunter_btn.grid(row=0, column=1, padx=10)

    def clear_search_slide1(self):
        self.member_search_var.set("")
        self.member_param_var.set("ID")

    def clear_search_slide2(self):
        self.book_search_var.set("")
        self.book_param_var.set("ISBN")

    def on_member_search(self):
        self.search_key = self.member_search_var.get().strip()
        self.search_param = self.member_param_var.get()
        print(f"Member search: param={self.search_param}, key={self.search_key}")
        self.update_table("membre")

    def on_book_search(self):
        self.search_key = self.book_search_var.get().strip()
        self.search_param = self.book_param_var.get()
        print(f"Book search: param={self.search_param}, key={self.search_key}")
        self.update_table("livre")

    def update_table(self, slide):
        key = self.search_key.strip().lower()
        param = self.search_param.strip().lower()

        if slide == "membre":
            # Clear member table
            for row in self.member_table.get_children():
                self.member_table.delete(row)

            # If no search key, show all members or empty
            if not key:
                dao = MembreDAO()
                results = dao.get_all_membres()
                for membre in results:
                    # Assuming membre has attributes id and nom
                    self.member_table.insert("", "end", values=(membre.id, membre.nom))
                return

            # Search members from DAO
            mdao = MembreDAO()
            results = mdao.search(param, key)  # Should return list of member objects

            # Insert results into member_table
            for membre in results:
                # Assuming membre has attributes id and nom
                self.member_table.insert("", "end", values=(membre.id, membre.nom))

        elif slide == "livre":
            # Clear book table
            for row in self.book_table.get_children():
                self.book_table.delete(row)

            # If no search key, show all books or empty
            if not key:
                # Show default static data or no rows
                dao = LivreDAO()
                results = dao.get_all_livre()
                for livre in results:
                    
                    count = dao.count_copies(livre.isbn)  # Get count copies
                    self.book_table.insert("", "end", values=(
                        livre.isbn,
                        livre.titre,
                        livre.copy_id,
                        livre.auteur,
                        livre.annee,
                        livre.genre,
                        livre.statut,
                        count
                    ))

                return

            # Search books from DAO
            ldao = LivreDAO()
            results = ldao.search(param, key)  # Should return list of livre objects

            # Insert results into book_table
            for livre in results:
                
                count = ldao.count_copies(livre.isbn)  # Get count copies
                self.book_table.insert("", "end", values=(
                    livre.isbn,
                    livre.titre,
                    livre.copy_id,
                    livre.auteur,
                    livre.annee,
                    livre.genre,
                    livre.statut,
                    count
                ))

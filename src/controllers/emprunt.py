from views.emprunter import EmpruntView
from tkinter import messagebox

class EmpruntController:
    def __init__(self, root,caller="Home",var1="",var2=""):
        self.root = root
        self.caller=caller
        self.var1 = var1
        self.var2 = var2
        self.view = EmpruntView(root, self)
        self.view.pack(fill="both", expand=True)

    def handle_next(self):
        selected = self.view.member_table.selection()
        if not selected:
            messagebox.showwarning("⚠ No Selection", "Please select a member first.")
            return
        self.view.selected_membre = self.view.member_table.item(selected[0],"value")

        self.view.show_slide(2)

    def handle_back(self):
        self.view.show_slide(1)

    def handle_emprunter(self):
        # Get selected member (single)
        selected_member = self.view.selected_membre
        if not selected_member:
            messagebox.showwarning("⚠ No Member", "Please select a member first.")
            self.view.show_slide(1)
            return
        print("before table.item call  the error is here ")
        
        member_id = selected_member[0]
        print(f"[handle emprunter ]: member id : {member_id}")
        # Get selected books (multiple)
        selected_books = self.view.book_table.selection()
        if len(selected_books) == 0:
            messagebox.showwarning("⚠ No Books", "Please select at least one book.")
            return
        if len(selected_books) > 7:
            messagebox.showerror("❌ Error", "You can select a maximum of 7 books.")
            return

        from models.membre import MembreDAO
        from models.livre import LivreDAO

        mdao = MembreDAO()
        ldao = LivreDAO()

        errors = []
        for book_id in selected_books:
            book_values = self.view.book_table.item(book_id, "values")
            isbn = book_values[0]
            copy_id = book_values[2]

            try:
                mdao.emprunter(member_id, isbn, copy_id)
                ldao.emprunter(isbn, copy_id)
            except Exception as e:
                errors.append(f"Failed to borrow {isbn} - {copy_id}: {str(e)}")

        if errors:
            messagebox.showerror("❌ Some errors occurred", "\n".join(errors))
        else:
            messagebox.showinfo("✅ Success", f"{len(selected_books)} book(s) borrowed successfully!")

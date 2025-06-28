import matplotlib.pyplot as plt
from models.livre import LivreDAO
from models.membre import MembreDAO
from views.home_view import HomeView
import tkinter as tk

class HomeController:
    def __init__(self, parent):
        self.view = HomeView(self, parent)
        
        self.update_charts()

    def update_charts(self):
        self.livre_dao = LivreDAO()
        self.membre_dao = MembreDAO()
        
        # Chart 1: Status Pie Chart (available vs borrowed)
        stats = {"disponible": 0, "emprunte": 0}
        for elem in self.livre_dao.get_all_livre_elm():
            status = elem.get("statut")
            if status in stats:
                stats[status] += 1

        # Chart 2: Top 10 Members with Most Borrowed Books
        member_books = {}
        for membre in self.membre_dao.get_all_membres():
            member_books[membre.id] = len(membre.copies)

        # Sort members by number of borrowed books in descending order and take top 10
        top_10_members = sorted(member_books.items(), key=lambda item: item[1], reverse=True)[:10]
        
        # Separate the keys and values for plotting
        top_member_ids = [member_id for member_id, count in top_10_members]
        top_borrow_counts = [count for member_id, count in top_10_members]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Pie chart: available vs borrowed books
        ax1.pie(stats.values(), labels=stats.keys(), autopct="%1.1f%%", startangle=90, colors=["#66b3ff", "#ff9999"])
        ax1.set_title("Répartition des livres")

        # Bar chart: top 10 members with most borrowed books
        ax2.bar(top_member_ids, top_borrow_counts, color="skyblue")
        ax2.set_title("Top 10 membres avec le plus de livres empruntés")
        ax2.set_xlabel("ID Membre")
        ax2.set_ylabel("Nombre de livres empruntés")
        ax2.set_xticklabels(top_member_ids, rotation=45, ha="right")

        plt.tight_layout()
        self.view.display_charts(fig)

    
    def load_emprunt_view(self):
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
        EmpruntController(dialog)

        # Wait for the dialog to close
        root_window.wait_window(dialog)
        self.update_charts()
        # Code here continues only after dialog is closed
        print("Borrowing dialog closed.")

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
        # Chart 1: Status Pie Chart
        stats = {"disponible": 0, "emprunte": 0}
        for elem in self.livre_dao.get_all_livre_elm():
            status = elem.get("statut")
            if status in stats:
                stats[status] += 1

        # Chart 2: Borrowed Books Per Member
        member_books = {}
        for membre in self.membre_dao.get_all_membres():
            member_books[membre.id] = len(membre.copies)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        # Pie chart
        ax1.pie(stats.values(), labels=stats.keys(), autopct="%1.1f%%", startangle=90)
        ax1.set_title("Répartition des livres")

        # Bar chart
        ax2.bar(member_books.keys(), member_books.values(), color="skyblue")
        ax2.set_title("Livres empruntés par membre")
        ax2.set_xlabel("ID Membre")
        ax2.set_ylabel("Nb Livres")

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

        # Code here continues only after dialog is closed
        print("Borrowing dialog closed.")

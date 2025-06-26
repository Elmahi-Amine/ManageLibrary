from controllers.membre_controller import MembreController
from .livre_view import LivreView  # Adjust import as needed based on your file structure

class MembreView(LivreView):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Replace controller with MembreController
        self.controller = MembreController(self)
        
        # Update button command to point to new controller method
        self.ajouter_btn.config(command=lambda: self.controller.create_add_membre_form())

        # Update combobox options
        self.method_choice.config(values=["id", "nom"])

        # Update search button command
        self.search_button.config(command=self.controller.perform_membre_search)

        # Update Enter key binding
        self.search_entry.bind("<Return>", lambda event: self.controller.perform_membre_search())

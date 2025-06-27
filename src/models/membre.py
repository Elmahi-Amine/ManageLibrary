import xml.etree.ElementTree as et
class Membre:
    __slots__ = ["id", "nom", "copies"]

    def __init__(self, id="", nom="", copies=None):
        self.id = id
        self.nom = nom
        self.copies = copies if copies is not None else []  # List of (isbn, copy_id) tuples


class MembreDAO:
    __storage_file_path = "data/membres.xml"

    def __init__(self):
        self.__tree = et.parse(MembreDAO.__storage_file_path)

    def ajouter(self, membre: Membre):
        root = self.__tree.getroot()
        membre_elem = et.Element("membre")
        membre_elem.set("id", membre.id)

        nom_elem = et.SubElement(membre_elem, "nom")
        nom_elem.text = membre.nom

        list_livres_elem = et.SubElement(membre_elem, "list-livres-empr")
        for copy_id, isbn in membre.copies:
            copy_elem = et.SubElement(list_livres_elem, "copy")
            copy_elem.set("id", copy_id)
            copy_elem.set("isbn", isbn)

        root.append(membre_elem)
        self.__tree.write(MembreDAO.__storage_file_path)

    def supprimer(self, membre_id: str):
        root = self.__tree.getroot()
        membre_elem = self._find_by_id(membre_id)
        root.remove(membre_elem)
        self.__tree.write(MembreDAO.__storage_file_path)

    def search(self, param, key):
        param = param.lower()
        key = key.lower()
        root = self.__tree.getroot()
        results = []

        for membre_elem in root.findall("membre"):
            membre = self.membre_from_element(membre_elem)
            value = ""

            if param == "id":
                value = membre.id
            elif param == "nom":
                value = membre.nom

            if key in value.lower():
                results.append(membre)

        return results

    def _find_by_id(self, membre_id):
        root = self.__tree.getroot()
        for membre_elem in root.findall("membre"):
            if membre_elem.get("id") == membre_id:
                return membre_elem

    def membre_from_element(self, elem):
        membre = Membre()
        membre.id = elem.get("id")
        membre.nom = elem.find("nom").text if elem.find("nom") is not None else ""
        membre.copies = []

        list_livres_elem = elem.find("list-livres-empr")
        if list_livres_elem is not None:
            for copy_elem in list_livres_elem.findall("copy"):
                copy_id = copy_elem.get("id")
                isbn = copy_elem.get("isbn")
                membre.copies.append((copy_id, isbn))
        return membre
    
    def emprunter(self,id,book_isbn, book_id):
        targeted_membre= self._find_by_id(id)
        if(targeted_membre!=None):
            list_livre_empr= targeted_membre.find("list-livres-empr")
            copy = et.SubElement(list_livre_empr,"copy")
            copy.set("id",book_id)
            copy.set("isbn",book_isbn)
        self.__tree.write(MembreDAO.__storage_file_path)
        
    def retourner(self,id,book_isbn,book_id):
        targeted_membre=self._find_by_id(id)
        list_livre_empr= targeted_membre.find("list-livres-empr")
        books = list_livre_empr.findall("copy")
        for item in books :
            item_isbn = item.get("isbn")
            item_id = item.get("id")
            if(book_isbn==item_isbn and book_id == item_id ):
                list_livre_empr.remove(item)
        self.__tree.write(MembreDAO.__storage_file_path)

    def get_all_membres(self):
        result = []
        root = self.__tree.getroot()
        list_membre_elm = root.findall("membre")
        for elm in list_membre_elm:
            result.append(self.membre_from_element(elm))
        return result
    def get_all_membres_elm(self):
        return self.__tree.getroot().findall("membre")
    
# class MembreDAO:
#     __storage_file_path ="data/membres.xml"
#     def __init__(self):
#         self.__tree = et.parse(MembreDAO.__storage_file_path)
#     @property 
#     def etree(self):
#         return self.__tree
    
#     def ajouter(self,membre: Membre):
#         root = self.__tree.getroot()
#         new_membre = et.Element("membre")
#         new_membre.set("id",membre.id)
#         # ajouter le nom de membre
#         new_memebre_nom = et.SubElement(new_membre,"nom")
#         new_memebre_nom.text = membre.nom
#         list_livre_empr = et.SubElement(new_membre,"list-livres-empr")
#         # ajouter la liste des livres empruntees
#         for c in membre.livres_empr:
#             copy= et.SubElement(list_livre_empr,"copy")
#             copy.set("id",c.copy_id)
#             copy.set("isbn",c.isbn)
#         # ajouter le tout dans root
#         root.append(new_membre)
#         self.__tree.write(MembreDAO.__storage_file_path)
#     # supprimer le membre avec le id donnee
#     def supprimer(self,id):
#         targeted_membre , root = self.rechercher(id)
#         if(targeted_membre !=None):
#             root.remove(targeted_membre)
#             return True
#         return False
    
#     def rechercher(self,id):
#         targeted_membre = None
#         root = self.__tree.getroot()
#         list_membre=root.findall("membre")
#         for mmbr in list_membre :
#             mmbr_id = mmbr.get("id")
#             if(mmbr_id == id):
#                 targeted_membre = mmbr
#         return targeted_membre,root
    
#     def rechercher(self,nom:str):
#         targeted_membre=None
#         root = self.__tree.getroot()
#         list_membre=root.findall("membre")
#         for mmbr in list_membre :
#             mmbr_nom = mmbr.find("nom")
#             if(mmbr_nom.text == id):
#                 targeted_membre = mmbr
#         return targeted_membre,root
#     def modifier(self,id,field,newValue):
#         targeted_membre,root=self.rechercher(id)
#         match field :
#             case "nom" : 
#                 targeted_membre.find("nom").text=newValue
#             case "id"   :
#                 targeted_membre.set("id",newValue)
#     def emprunter(self,id,livre:Livre):
#         targeted_membre,root= self.rechercher(id)
#         if(targeted_membre!=None):
#             list_livre_empr= targeted_membre.find("list-livres-empr")
#             copy = et.SubElement(list_livre_empr,"copy")
#             copy.set("id",livre.copy_id)
#             copy.set("isbn",livre.isbn)
            
import xml.etree.ElementTree as et
class Livre :
    __slots__ =["copy_id","isbn","titre","auteur","annee","genre","statut"]
    def __init__(self,copy_id="",isbn="",titre="",auteur="",annee="",genre="",statut="disponible"):
        self.copy_id = copy_id
        self.isbn=isbn
        self.titre=titre
        self.auteur=auteur
        self.annee=annee
        self.genre=genre
        self.statut=statut
    
class LivreDAO :
    __storage_file_path ="data/livres.xml"
    def __init__(self):
        self.__tree = et.parse(LivreDAO.__storage_file_path)
    def ajouter(self,livre:Livre):
        root = self.__tree.getroot()
        new_livre = et.Element("livre")
        new_livre.set("copy-id",livre.copy_id)
        new_livre.set("isbn",livre.isbn)
        new_livre.set("statut","disponible")
        
        titre = et.SubElement(new_livre,"titre")
        titre.text = livre.titre
        #
        auteur = et.SubElement(new_livre,"auteur")
        auteur.text = livre.auteur
        # 
        annee = et.SubElement(new_livre,"annee")
        annee .text = livre.annee
        #
        genre = et.SubElement(new_livre,"genre")
        genre.text = livre.genre
        #
        root.append(new_livre)
        self.__tree.write(LivreDAO.__storage_file_path)
    
    def rechercher_id_isbn(self,  isbn, copy_id):
        root = self.__tree.getroot()
        list_des_livres = root.findall("livre")
        for livre in list_des_livres :
            current_copy_id = livre.get("copy-id")
            current_isbn = livre.get("isbn")
            if current_copy_id== copy_id and current_isbn == isbn :
                return livre
    
    def supprimer(self,isbn,copy_id):
        root = self.__tree.getroot()
        targeted_livre = self.rechercher_id_isbn(isbn,copy_id)
        print(f"[supprimer] :{targeted_livre.get("isbn")} ")
        root.remove(targeted_livre)
        self.__tree.write(LivreDAO.__storage_file_path)


    def rechercher_titre(self, titre):
        
        root = self.__tree.getroot()
        list_des_livres = root.findall("livre")
        for livre in list_des_livres :
            current_titre = livre.find("titre")
            if current_titre.text == titre :
                targeted_livre = livre
                break
        return targeted_livre
    
    def count_copies(self, isbn):
        root = self.__tree.getroot()
        return sum(1 for livre in root.findall("livre") if livre.get("isbn") == isbn)
    
    def emprunter(self,isbn,copyid):
        targeted_livre = self.rechercher_id_isbn(isbn,copyid)
        targeted_livre.set("statut","emprunte")
        self.__tree.write(LivreDAO.__storage_file_path)

    def retourner(self,isbn,copy_id):
        targeted_livre= self.rechercher_id_isbn(isbn,copy_id)
        targeted_livre.set("statut","disponible")
        self.__tree.write(LivreDAO.__storage_file_path)

    def livre_from_element(self,elem):
        livre = Livre()
        livre.copy_id = elem.get("copy-id")
        livre.isbn = elem.get("isbn")
        livre.statut = elem.get("statut")
        livre.titre = elem.find("titre").text
        livre.auteur = elem.find("auteur").text
        livre.annee = elem.find("annee").text
        livre.genre = elem.find("genre").text
        return livre

    def search(self, param, key):
        param = param.lower()
        key = key.lower()
        root = self.__tree.getroot()
        results = []

        for elem in root.findall("livre"):
            livre = self.livre_from_element(elem)

            if param in ["titre", "auteur", "nom", "date"]:
                value = ""
                if param == "titre":
                    value = livre.titre
                elif param in ["auteur", "nom"]:
                    value = livre.auteur
                elif param == "date":
                    value = str(livre.annee)

                if key in value.lower():
                    results.append(livre)

            elif param == "isbn" and key == livre.isbn.lower():
                results.append(livre)

            elif param == "copy-id" and key == livre.copy_id.lower():
                results.append(livre)

        return results
    def emprunter(self,isbn,copy_id):
        targeted_livre=self.rechercher_id_isbn(isbn,copy_id)
        check_status=self.livre_from_element(targeted_livre).statut
        print (f'[wer are in livre emprunter ]status of livre is {targeted_livre.get("statut")}')
        if(check_status=="disponible"):
            targeted_livre.set("statut","emprunte")
        self.__tree.write(LivreDAO.__storage_file_path)
    def get_all_livre_elm(self):
        return self.__tree.getroot().findall("livre")
    def get_all_livre(self):
        result =[]
        for elm in self.get_all_livre_elm():
            result.append(self.livre_from_element(elm))
        return result
    def check_dispo(self,isbn,copyid):
        elm = self.rechercher_id_isbn(isbn,copy_id=copyid)
        return self.livre_from_element(elm).statut == "disponible"
            

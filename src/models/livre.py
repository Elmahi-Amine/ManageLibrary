import xml.etree.ElementTree as et
class Livre :
    __slots__ =["__copy_id","__isbn","__titre","__auteur","__annee","__genre"]
    def __init__(self):
        self.__copy_id
        self.__isbn
        self.__titre
        self.__auteur
        self.__annee
        self.__genre

    @property
    def copy_id(self):
        return f"{self.__copy_id}"
    @copy_id.setter 
    def copy_id(self,value):
        self.__copy_id=value
    @property
    def isbn(self):
        return f"{self.__isbn}"
    @isbn.setter
    def isbn(self,value):
        self.__isbn=value
    @property
    def titre(self):
        return f"{self.__titre}"
    @titre.setter
    def titre(self,value):
        self.__titre = value

    @property
    def auteur(self):
        return f"{self.__auteur}"
    @auteur.setter
    def auteur(self,value):
        self.__auteur=value
    @property
    def annee(self):
        return f"{self.annee}"
    def annee(self,value):
        self.__annee=value
    @property
    def genre (self):
        return f"{self.__genre}"
    @genre.setter
    def genre(self,value):
        self.__genre = value
    
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
    
    def rechercher(self, copy_id, isbn):
        targeted_livre = None
        root = self.__tree.getroot()
        list_des_livres = root.findall("livre")
        for livre in list_des_livres :
            current_copy_id = livre.get("copy-id")
            current_isbn = livre.get("isbn")
            if current_copy_id== copy_id and current_isbn == isbn :
                targeted_livre = livre
        return targeted_livre

    def rechercher(self, titre):
        targeted_livre = None
        root = self.__tree.getroot()
        list_des_livres = root.findall("livre")
        for livre in list_des_livres :
            current_titre = livre.find("titre")
            if current_titre.text == titre :
                targeted_livre = livre
        return targeted_livre
    

    def emprunter(self,id):
        targeted_livre = self.rechercher(id)
        targeted_livre.set("statut","emprunte")
        self.__tree.write(LivreDAO.__storage_file_path)
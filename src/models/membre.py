import xml.etree.ElementTree as et
from models.livre import Livre
class Membre:
    __slots__=["__nom","__id","livres_empr"]
    def __init__(self,nom ,id):
        self.__nom = nom
        self.__id =id
        self.livres_empr
    def __str__(self):
        return f"nom : {self.__nom} id : {self.__id}"
    @property
    def nom(self):
        return f"{self.__nom}"
    @nom.setter 
    def nom(self,value):
        self.__nom=value
    @property
    def id(self):
        return f"{self.__id}"
    @id.setter
    def id(self,value):
        self.__id =value
    @property
    def livres_empr(self):
        return self.livres_empr
    @livres_empr.setter
    def livres_empr(self,list: list[Livre]):
        self.livres_empr = list


class MembreDAO:
    __storage_file_path ="data/membres.xml"
    def __init__(self):
        self.__tree = et.parse(MembreDAO.__storage_file_path)
    @property 
    def etree(self):
        return self.__tree
    
    def ajouter(self,membre: Membre):
        root = self.__tree.getroot()
        new_membre = et.Element("membre")
        new_membre.set("id",membre.id)
        # ajouter le nom de membre
        new_memebre_nom = et.SubElement(new_membre,"nom")
        new_memebre_nom.text = membre.nom
        list_livre_empr = et.SubElement(new_membre,"list-livres-empr")
        # ajouter la liste des livres empruntees
        for c in membre.livres_empr:
            copy= et.SubElement(list_livre_empr,"copy")
            copy.set("id",c.copy_id)
            copy.set("isbn",c.isbn)
        # ajouter le tout dans root
        root.append(new_membre)
        self.__tree.write(MembreDAO.__storage_file_path)
    #supprimer le membre avec le id donnee
    def supprimer(self,id):
        targeted_membre , root = self.rechercher(id)
        if(targeted_membre !=None):
            root.remove(targeted_membre)
            return True
        return False
    
    def rechercher(self,id):
        targeted_membre = None
        root = self.__tree.getroot()
        list_membre=root.findall("membre")
        for mmbr in list_membre :
            mmbr_id = mmbr.get("id")
            if(mmbr_id == id):
                targeted_membre = mmbr
        return targeted_membre,root
    
    def rechercher(self,nom:str):
        targeted_membre=None
        root = self.__tree.getroot()
        list_membre=root.findall("membre")
        for mmbr in list_membre :
            mmbr_nom = mmbr.find("nom")
            if(mmbr_nom.text == id):
                targeted_membre = mmbr
        return targeted_membre,root
    def modifier(self,id,field,newValue):
        targeted_membre,root=self.rechercher(id)
        match field :
            case "nom" : 
                targeted_membre.find("nom").text=newValue
            case "id"   :
                targeted_membre.set("id",newValue)
    def emprunter(self,id,livre:Livre):
        targeted_membre,root= self.rechercher(id)
        if(targeted_membre!=None):
            list_livre_empr= targeted_membre.find("list-livres-empr")
            copy = et.SubElement(list_livre_empr,"copy")
            copy.set("id",livre.copy_id)
            copy.set("isbn",livre.isbn)
            
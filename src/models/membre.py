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
    def __init__(self):
        # TODO
        #parse membres.xml
        #return the element tree
        self.__tree = et.parse("data/membres.xml")
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
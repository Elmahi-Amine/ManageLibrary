class Livre :
    __slots__ =["__copy_id,__isbn,__auteur,__annee,__genre"]
    def __init__(self):
        self.__copy_id
        self.__isbn
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
__Author__ = "noeline"
__Filename__ = "litteral.py.py"
__Creationdate__ = "28/10/20"

import typing

class litteral:
    def __init__(self, litt):
        self.litt = litt

    @property
    def litt(self):
        return self.__litt

    @litt.setter
    def litt(self, x):
        #il n'y a pas de restriction sur les littérals, ca peut etre un prénom par exemple
        if isinstance(x, str) or isinstance(x, bool): # les litteraux True et False sont acceptés
            self.__litt = x

    def signe(self):
        #True si positif, False si négatif
        if isinstance(self.litt, bool):
            return None
        elif self.litt[0] == '-':
            return False
        return True

    def var(self):
        if self.signe() == True:
            return self.litt
        elif self.signe() == False:
            return self.litt[1:]
        else: #self.litt == True ou == False
            return self.litt


    def oppose(self):
        if self.litt == True: #importance du == true pck self.litt peut etre un str et "if str" rentre toujours dans le if
            return litteral(False)
        elif self.litt == False:
            return litteral(True)
        elif self.signe():
            return '-' + self.var()
        else:
            return self.var()

    def __str__(self):
        # ATTENTION : il faut que le non reste un - pour la fonction isThereLittPur
        return str(self.litt)

    def simplifie(self, val: 'Bool'):
        #met à val la valeure de la variable propositionnelle
        if self.signe() == True:
            return litteral(val)
        elif self.signe() == False:
            return litteral(val).oppose()
        else: #self est un booléen --> il se simplifie par lui même
            return self

    def __eq__(self, litt2: 'litteral'):
        if str(self) == str(litt2):
            return True
        return False
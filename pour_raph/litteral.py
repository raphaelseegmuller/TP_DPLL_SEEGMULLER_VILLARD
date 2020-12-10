__Author__ = "noeline"
__Filename__ = "litteral.py.py"
__Creationdate__ = "28/10/20"


class litteral:
    def __init__(self, litt):
        self.litt = litt

    @property
    def litt(self):
        return self.__litt

    @litt.setter
    def litt(self, x):
        # il n'y a pas de restriction sur les littéraux, ca peut être un prénom par exemple
        if isinstance(x, str) or isinstance(x, bool):  # les litteraux True et False sont acceptés
            self.__litt = x

    def signe(self):
        # True si positif, False si négatif
        if isinstance(self.litt, bool):
            return None  # Les littéraux True et False sont considérés sans signes.
        elif self.litt[0] == '-':
            return False
        return True

    def var(self):
        if self.signe() == True:
            return self.litt
        elif self.signe() == False:
            return self.litt[1:]
        else:  # self.litt == True/False
            return self.litt

    def var_neg(self):
        if self.signe() == True:
            return self.oppose().litt
        elif self.signe() == False:
            return self.litt
        else:  # self.litt == True/False
            return self.oppose().litt

    def oppose(self):
        if self.litt == True:  # importance du == true pck self.litt peut etre un str et "if str" rentre toujours dans le if
            return litteral(False)
        elif self.litt == False:
            return litteral(True)
        elif self.signe():
            return litteral('-' + self.var())
        else:
            return litteral(self.var())

    def __str__(self):
        # ATTENTION : il faut que le non reste un - pour la fonction isThereLittPur
        return str(self.litt)

    def __eq__(self, litt2: 'litteral'):
        if str(self) == str(litt2):
            return True
        return False
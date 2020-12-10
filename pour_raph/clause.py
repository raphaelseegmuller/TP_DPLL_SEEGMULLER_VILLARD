__Author__ = "noeline"
__Filename__ = "clause.py"
__Creationdate__ = "23/10/20"

from litteral import *


class clause():
    def __init__(self, litteraux):
        # litteraux est une liste de littéraux
        self.litteraux = litteraux

    @property
    def litteraux(self):
        return self.__litteraux

    @litteraux.setter
    def litteraux(self, x):
        if x == []:
            self.__litteraux = x
        elif isinstance(x, list):
            i = 0
            for elt in x:
                if not (isinstance(elt, litteral)):
                    i += 1
            if i == 0:
                self.__litteraux = x

    def isEmpty(self):
        if len(self.litteraux) > 0:
            return False
        return True

    def liste(self):
        # retourne la liste des littéraux
        liste = []
        for elt in self.litteraux:
            if elt == litteral(True):
                liste += [True]
            elif elt == litteral(False):
                liste += [False]
            else:
                liste += [str(elt)]
        return liste

    def __str__(self):
        if self.isEmpty():
            return ""
        chaine = str(self.litteraux[0])
        for elt in self.litteraux[1:]:
            chaine += ' ou ' + str(elt)
        return chaine

    def addLitteral(self, litt: 'litteral'):
        self.litteraux = self.litteraux + [litt]

    def __len__(self):
        return len(self.litteraux)

    def contientTrue(self):
        for litt in self.litteraux:
            if litt == True:
                return True
        return False

    def contientFalse(self):
        for litt in self.litteraux:
            if litt == False:
                return True
        return False

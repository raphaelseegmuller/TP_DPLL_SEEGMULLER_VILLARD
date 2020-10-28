__Author__ = "noeline"
__Filename__ = "clause.py"
__Creationdate__ = "23/10/20"

from litteral import *

class clause():
    def __init__(self, litteraux):
        #litteraux est une liste de littéraux
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
                if not(isinstance(elt, litteral)):
                    i += 1
            if i == 0:
                self.__litteraux = x

    def isEmpty(self):
        if len(self.litteraux) > 0:
            return False
        return True

    def isClauseUnitaire(self):
        if len(self.litteraux) == 1:
            return True
        return False

    def prop(self):
        #retourne la liste des variables propositionnelles d'une clause
        liste = []
        for elt in self.litteraux:
            if elt.var() not in liste:
                liste += [elt.var()]
        return liste

    def liste(self):
        #retourne la liste des littéraux
        liste = []
        for elt in self.litteraux:
            if elt == litteral(True):
                liste += [True]
            elif elt == litteral(False):
                liste += [False]
            else:
                liste += [str(elt)]
        return liste


    def isThereLitteralPur(self):
        #renvoie le premier litteral pur de la liste
        liste = []
        for elt in self.litteraux:
            if elt not in liste and elt.oppose() not in liste:
                liste += [str(elt)] # importance de mettre str(elt) et pas juste elt pck si on a litt1 = litteral('p')
                                    # et litt7 = litteral('p') alors on aura 2 fois p dans liste (mais en vrai c'est
                                    # pas très grave
            elif elt.oppose() in liste:
                liste.remove(str(elt.oppose()))
        if len(liste) > 0:
            return liste[0]
        return None

    def __str__(self):
        #if self.isEmpty():
        #    return str()
        chaine = str(self.litteraux[0])
        for elt in self.litteraux[1:]:
            chaine += ' ou ' + str(elt)
        return chaine

    def addLitteral(self, litt: 'litteral'):
        self.litteraux = self.litteraux + [litt]

    def removeLitteral(self, litt: 'litteral'):
        liste = []
        for elt in self.litteraux:
            if litt != elt:
                liste += [elt]
        return clause(liste)

    def simplifie(self, prop: 'litteral', val: 'Bool'):
        #la variable propositionnelle prend la valeur val
        #supprime aussi les doublons
        #ATTENTION prop doit etre positif
        ans = clause([])
        for elt in self.litteraux:
            if elt.var() == prop.var():
                ans.addLitteral(elt.simplifie(val))
            elif elt.litt not in ans.liste():
                ans.addLitteral(elt)
        if True in ans.liste():
            return clause([litteral(True)])
        elif False in ans.liste():
            return ans.removeLitteral(False)
        else:
            return ans


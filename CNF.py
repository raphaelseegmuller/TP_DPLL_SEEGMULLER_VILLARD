from litteral import litteral
from clause import clause


class CNF():

    def __init__(self, clauses):
        # clauses est une liste de liste
        self.clauses = clauses

    @property
    def clauses(self):
        return self.__clauses

    @clauses.setter
    def clauses(self, L):
        if L == []:
            self.__clauses = L
        elif isinstance(L, list):
            i = 0
            for cl in L:
                if not (isinstance(cl, clause)):
                    i += 1
            if i == 0:
                self.__clauses = L

    def __len__(self):
        # donne le nombre de clauses
        return len(self.clauses)

    def isEmpty(self):
        if len(self) == 1:
            if self.clauses[0].isEmpty():
                return True
        return False

    def __str__(self):
        if self.isEmpty():
            return ""
        chaine = "(" + str(self.clauses[0])
        for cl in self.clauses[1:]:
            chaine += ') et (' + str(cl)
        return chaine + ')'

    def liste(self):
        # retourne la liste des littéraux
        liste = []
        for elt in self.clauses:
            liste += [elt.liste()]
        return liste

    def addClause(self, cl: 'clause'):
        self.clauses = self.clauses + [cl]

    def removeClause(self, cl: 'clause'):
        liste = []
        for elt in self.clauses:
            if cl != elt:
                liste += [elt]
        return CNF(liste)

    def simplifie_resouds(self, prop: 'litteral', val: 'bool'):
        # la variable propositionnelle prend la valeur val
        # supprime aussi les doublons
        # ATTENTION prop doit etre positif
        if self.isEmpty():
            return self
        ans = CNF([])
        for i in range(len(self)):
            new_cl = self.clauses[i].simplifie_resouds(prop, val)
            if new_cl.isEqual(clause([litteral(False)])):
                return CNF([clause([litteral(False)])])
            elif not (new_cl.isEqual(clause([litteral(True)]))):
                ans.addClause(new_cl)
        L = ans.liste()
        surplus = []
        for j in range(len(L)):
            for k in range(j, len(L)):
                if j != k:
                    if ans.clauses[j].isEqual(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
            surplus = []
            L = ans.liste()
        for j in range(len(L)):
            for k in range(len(L)):
                if j != k:
                    if ans.clauses[j].comparaison(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            surplus = list(set(surplus))
            surplus.sort(reverse=True)
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
        return ans

    def simplifie(self):
        # Simplifie la forme clausale.
        if self.isEmpty():
            return self
        ans = CNF([])
        for i in range(len(self)):
            new_cl = self.clauses[i].simplifie()
            if new_cl.isEqual(clause([litteral(False)])):
                return CNF([clause([litteral(False)])])
            elif not (new_cl.isEqual(clause([litteral(True)]))):
                ans.addClause(new_cl)
        L = ans.liste()
        surplus = []
        for j in range(len(L)):
            for k in range(j, len(L)):
                if j != k:
                    if ans.clauses[j].isEqual(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
            surplus = []
            L = ans.liste()
        for j in range(len(L)):
            for k in range(len(L)):
                if j != k:
                    if ans.clauses[j].comparaison(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            surplus = list(set(surplus))
            surplus.sort(reverse=True)
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
        return ans

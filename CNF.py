__Author__ = "noeline"
__Filename__ = "CNF.py"
__Creationdate__ = "23/10/20"


class CNF():

    def __init__(self, clauses):
        #clauses est une liste de liste
        self.clauses = clauses
        
    @property
    def Lclauses(self):
        return self.__Lcauses

    @Lclauses.setter
    def Lclauses(self, L):
        if len(L) != 0:
            test = True
            for cl in L:
                if type(cl) != 'clause':
                    test = False
            if test == True:
                self.Lclauses = L

    def __len__(self):
        #donne le nombre de clauses
        return len(self.clauses)

    def isEmpty(self):
        if len(self) > 0:
            return False
        return True

    def clauses(self):
        return self.clauses


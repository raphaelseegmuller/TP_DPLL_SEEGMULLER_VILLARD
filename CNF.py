__Author__ = "noeline"
__Filename__ = "CNF.py"
__Creationdate__ = "23/10/20"


class CNF():

    def __init__(self, clauses):
        #clauses est une liste de liste
        self.clauses = clauses

    def __len__(self):
        #donne le nombre de clauses
        return len(self.clauses)

    def isEmpty(self):
        if len(self) > 0:
            return False
        return True

    def clauses(self):
        return self.clauses


__Author__ = "noeline"
__Filename__ = "clause.py"
__Creationdate__ = "23/10/20"


class clause():
    def __init__(self, litteraux):
        #litteraux est une miste de littéraux
        self.litteraux = litteraux

    def isEmpty(self):
        if len(self.litteraux) > 0:
            return False
        return True

    def isClauseUnitaire(self):
        if len(self.litteraux) == 1:
            return True
        return False


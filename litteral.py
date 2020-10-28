__Author__ = "noeline"
__Filename__ = "litteral.py.py"
__Creationdate__ = "28/10/20"

class litteral():
    def __init__(self, litt: 'str'):
        self.litt = litt

    @property
    def litt(self):
        return self.__litt

    @litt.setter
    def litt(self, x):
        #il n'y a pas de restriction sur les littérals, ca peut etre un prénom par exemple
        self.__litt = x

    def signe(self):
        #True si positif, False si négatif
        if self.litt[0] == '-':
            return False
        return True

    def var(self):
        if self.signe():
            return self.litt
        return self.litt[1:]
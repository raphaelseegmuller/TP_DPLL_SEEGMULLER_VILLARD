__Author__ = "noeline et raphaël"
__Filename__ = "testfonctions.py"
__Creationdate__ = "13/11/20"

from fonctions import *

n = 8

print(dames(n))
print('ans DPLL: ', dames(n).DPLL(ans=3, choice="first_fail", Time=True))


# "first_satisfy"
# "first_fail"


# si ans = 0 --> la méthode renvoie si la CNF est satisfaisable ou non (Booléen)
# si ans = 1 --> la méthode renvoie une valuation si la CNF est satisfaisable, None sinon
# si ans = 2 --> la méthode renvoie toutes les valuations de la CNF sous forme de liste (liste de liste)
# si ans = 3 --> la méthode renvoie le nombre de valuations (entier)
# si ans = 4 --> la méthode renvoie le nombre de noeuds de l'arbre (entier)

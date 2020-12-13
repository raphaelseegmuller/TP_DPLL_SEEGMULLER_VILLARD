__Author__ = "noeline"
__Filename__ = "graphs.py"
__Creationdate__ = "03/12/20"

import matplotlib.pyplot as plt
from CNF import *
from fonctions import *
from time import time

# ---------------------------------------------------------------------
n_min = 0
n_max = 8

Time = False  # affichage du temps pour chaque exécution de DPLL
graph = 'temps'  # graph du temps en fonction de n ou du nombre de noeuds en fonction de n
save = True  # sauvegarde de la figure
# ----------------------------------------------------------------------

generateurs = [dames, pigeons]
heuristiques = ["first_satisfy", "first_fail", None]
ans = 4
debut_total = time()
n = [i for i in range(n_min, n_max+1)]

for gen in generateurs:
    if gen == dames:
        gen_str = 'dames'
    elif gen == pigeons:
        gen_str = 'pigeons'
    print('-----', gen_str)
    for heur in heuristiques:
        print('---', heur)
        temps = []
        noeuds = []
        for i in range(n_min, n_max+1):
            print(i)
            debut = time()
            noeuds += [gen(i).DPLL(ans=ans, choice=heur, Time=Time)]
            fin = time()
            temps += [fin - debut]
        if graph == 'temps':
            if heur == None:
                plt.plot(n, temps, label='sans heuristique')
            else:
                plt.plot(n, temps, label=heur)
        if graph == 'noeuds':
            if heur == None:
                plt.plot(n, noeuds, label='sans heuristique')
            else:
                plt.plot(n, noeuds, label=heur)

    plt.xlabel('n')
    plt.ylabel(graph)
    plt.grid()
    plt.legend()

    plt.title(graph + ' de l\'algorithme DPLL pour le problème des ' + gen_str)
    if save:
        plt.savefig('DPLL_' + graph + '_' + gen_str)

    plt.show()

fin_total = time()
print("temps total : ", (fin_total - debut_total) / 60, "min")


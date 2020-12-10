__Author__ = "noeline"
__Filename__ = "graphs.py"
__Creationdate__ = "03/12/20"

import matplotlib.pyplot as plt
from CNF import *
from fonctions import *
from time import time

n_min = 0
n_max =7

debut_total = time()

n_max += 1
val_n = [i for i in range(n_min, n_max)]

val_temps_dames_fs = []
val_noeuds_dames_fs = []
for i in range(n_min, n_max):
    print()
    print(i)
    debut = time()
    val_noeuds_dames_fs += [dames(i).DPLL(ans=4, choice="first_satisfy", Time=False)]
    fin = time()
    val_temps_dames_fs += [fin - debut]

val_temps_dames_ff = []
val_noeuds_dames_ff = []
for i in range(n_min, n_max):
    print()
    print(i)
    debut = time()
    val_noeuds_dames_ff += [dames(i).DPLL(ans=4, choice="first_fail", Time=False)]
    fin = time()
    val_temps_dames_ff += [fin - debut]

val_temps_pigeons_fs = []
val_noeuds_pigeons_fs = []
for i in range(n_min, n_max):
    print()
    print(i)
    debut = time()
    val_noeuds_pigeons_fs += [pigeons(i).DPLL(ans=4, choice="first_satisfy", Time=False)]
    fin = time()
    val_temps_pigeons_fs += [fin - debut]

val_temps_pigeons_ff = []
val_noeuds_pigeons_ff = []
for i in range(n_min, n_max):
    print()
    print(i)
    debut = time()
    val_noeuds_pigeons_ff += [pigeons(i).DPLL(ans=4, choice="first_fail", Time=False)]
    fin = time()
    val_temps_pigeons_ff += [fin - debut]

print(len(val_n), len(val_temps_dames_ff))

plt.plot(val_n, val_temps_dames_fs, label='first satisfy')
plt.plot(val_n, val_temps_dames_ff, label='first fail')
plt.title('temps de l\'algorithme DPLL pour le problème des dames')
plt.xlabel('n')
plt.ylabel('temps')
plt.grid()
plt.legend()
#plt.savefig('DPLL_temps_dames')
plt.show()

plt.plot(val_n, val_temps_pigeons_fs, label='first satisfy')
plt.plot(val_n, val_temps_pigeons_ff, label='first fail')
plt.title('temps de l\'algorithme DPLL pour le problème des pigeons')
plt.xlabel('n')
plt.ylabel('temps')
plt.grid()
plt.legend()
#plt.savefig('DPLL_temps_pigeons')
plt.show()

plt.plot(val_n, val_noeuds_dames_fs, label='first satisfy')
plt.plot(val_n, val_noeuds_dames_ff, label='first fail')
plt.title('nombre de noeuds de l\'arbre DPLL pour le problème des dames')
plt.xlabel('n')
plt.ylabel('noeuds')
plt.grid()
plt.legend()
plt.savefig('DPLL_noeuds_dames')
plt.show()

plt.plot(val_n, val_noeuds_pigeons_fs, label='first satisfy')
plt.plot(val_n, val_noeuds_pigeons_ff, label='first fail')
plt.title('nombre de noeuds de l\'arbre DPLL pour le problème des pigeons')
plt.xlabel('n')
plt.ylabel('noeuds')
plt.grid()
plt.legend()
plt.savefig('DPLL_noeuds_pigeons')
plt.show()

fin_total = time()
print('temps total = ', (fin_total - debut_total)/60, ' minutes')
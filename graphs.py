__Author__ = "noeline"
__Filename__ = "graphs.py"
__Creationdate__ = "03/12/20"

import matplotlib.pyplot as plt
from CNF import *
from fonctions import *
from time import time

n_max = 9

debut_total = time()

val_n = [i for i in range(n_max)]

val_temps_dames_fs = []
for i in range(n_max):
    print(i)
    debut = time()
    dames(i).DPLL(ans=3, choice="first_satisfy", Time=True)
    fin = time()
    val_temps_dames_fs += [fin - debut]

val_temps_dames_ff = []
for i in range(n_max):
    print(i)
    debut = time()
    dames(i).DPLL(ans=3, choice="first_fail", Time=True)
    fin = time()
    val_temps_dames_ff += [fin - debut]

val_temps_pigeons_fs = []
for i in range(n_max):
    print(i)
    debut = time()
    pigeons(i).DPLL(ans=3, choice="first_satisfy", Time=True)
    fin = time()
    val_temps_pigeons_fs += [fin - debut]

val_temps_pigeons_ff = []
for i in range(n_max):
    print(i)
    debut = time()
    pigeons(i).DPLL(ans=3, choice="first_fail", Time=True)
    fin = time()
    val_temps_pigeons_ff += [fin - debut]

plt.plot(val_n, val_temps_dames_fs, label='first satisfy')
plt.plot(val_n, val_temps_dames_ff, label='first fail')
plt.title('temps de l\'algorithme DPLL pour le problème des dames')
plt.xlabel('n')
plt.ylabel('temps')
plt.legend()
plt.savefig('DPLL_dames')
plt.show()

plt.plot(val_n, val_temps_pigeons_fs, label='first satisfy')
plt.plot(val_n, val_temps_pigeons_ff, label='first fail')
plt.title('temps de l\'algorithme DPLL pour le problème des pigeons')
plt.xlabel('n')
plt.ylabel('temps')
plt.legend()
plt.savefig('DPLL_pigeons')
plt.show()

fin_total = time()
print('temps total = ', (fin_total - debut_total)/60, ' minutes')
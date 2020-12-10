__Author__ = "noeline"
__Filename__ = "testCNF.py"
__Creationdate__ = "23/10/20"

from CNF import *

# CNF aléatoires et cas limites

A = litteral("a")
B = litteral("-b")
C = litteral(True)
D = litteral("c")
E = litteral(False)
F = litteral("-d")
G = litteral("-a")

A1 = clause([A, B, B])
A2 = clause([])
A3 = clause([B, C, D])
A4 = clause([D, E, F])
A5 = clause([A, B, D, F, G])
A6 = clause([A])
A7 = clause([E])
A8 = clause([C, A, D, E])

B1 = CNF([A2])
B2 = CNF([A1, A1])
B3 = CNF([A1, A3])
B4 = CNF([A3, A4, A5])
B5 = CNF([A1, A5])
B6 = CNF([A1, A4, A6, A8])
B7 = CNF([A1, A6, A7])

# Exemples du cours

l1 = [['-c', 'd', '-b', '-a'], ['c', 'd', '-b', '-a']]
l2 = [['-p', 's'], ['q', 'r'], ['q', 'p', 's'], ['-r', '-p', '-q'], ['-r', '-s', '-q']]

l = l2
clauses = []
for cl in l:
    litteraux = []
    for litt in cl:
        litteraux += [litteral(litt)]
    clauses += [clause(litteraux)]
B8 = CNF(clauses)

# Testes

clause_a_tester = B8
print('clause : ', clause_a_tester)
print('reponse dpll : ', clause_a_tester.DPLL(ans=1, choice="first_satisfy", Time=True))



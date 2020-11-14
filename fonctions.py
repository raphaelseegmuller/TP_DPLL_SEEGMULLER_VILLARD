from litteral import litteral
from clause import clause
from CNF import CNF


def combinaison(n):
    # Retourne les combinaisons possibles
    C = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            C += [(i, j)]
    return C


def pigeons(n):
    G_CNF = CNF([clause([])])
    for i in range(n):
        new_cl = clause([])
        for j in range(n - 1):
            new_cl.addLitteral(litteral("p" + str(i) + str(j)))
        if G_CNF.isEmpty():  # PROBLEME AJOUT CLAUSE A CNF VIDE... PAS TIP TOP MAIS SINON IL FAUT REDEFINIR CNF.ISEMPTY()
            G_CNF = CNF([new_cl])
        else:
            G_CNF.addClause(new_cl)
    # print("Etape 1 : ", G_CNF)
    for i in range(n):
        for t in combinaison(n - 1):
            new_cl = clause([])
            for j in t:
                new_cl.addLitteral(litteral("-p" + str(i) + str(j)))
            G_CNF.addClause(new_cl)
    # print("Etape 2 : ", G_CNF)
    for i in range(n - 1):
        for t in combinaison(n):
            new_cl = clause([])
            for j in t:
                new_cl.addLitteral(litteral("-p" + str(j) + str(i)))
            G_CNF.addClause(new_cl)
    # print("Etape 3 : ", G_CNF)
    return G_CNF


def dames(n):
    G_CNF = CNF([clause([])])
    for i in range(n):
        new_cl = clause([])
        for j in range(n):
            new_cl.addLitteral(litteral("D" + str(j) + str(i)))
        if G_CNF.isEmpty():  # PROBLEME AJOUT CLAUSE A CNF VIDE... PAS TIP TOP MAIS SINON IL FAUT REDEFINIR CNF.ISEMPTY()
            G_CNF = CNF([new_cl])
        else:
            G_CNF.addClause(new_cl)
    for j in range(n):
        new_cl = clause([])
        for i in range(n):
            new_cl.addLitteral(litteral("D" + str(j) + str(i)))
        G_CNF.addClause(new_cl)
    print("Etape 1 : ", G_CNF)
    for i in range(n):
        for t in combinaison(n):
            new_cl = clause([])
            for j in t:
                new_cl.addLitteral(litteral("-D" + str(j) + str(i)))
            G_CNF.addClause(new_cl)
    for j in range(n):
        for t in combinaison(n):
            new_cl = clause([])
            for i in t:
                new_cl.addLitteral(litteral("-D" + str(j) + str(i)))
            G_CNF.addClause(new_cl)
    print("Etape 2 : ", G_CNF)
    # Diagonales
    for j in range(n - 1):
        for i in range(n - 1):
            for k in range(i + 1, n):
                new_cl = clause([(litteral("-D" + str(j) + str(i)))])
                if k - i + j < n:
                    new_cl.addLitteral(litteral("-D" + str(k - i + j) + str(k)))
                    G_CNF.addClause(new_cl)
    print("Etape 3 : ", G_CNF)
    # Anti-diagonales
    for j in range(1, n):
        for i in range(n - 1):
            for k in range(i + 1, n):
                new_cl = clause([(litteral("-D" + str(j) + str(i)))])
                if -k + i + j >= 0:
                    new_cl.addLitteral(litteral("-D" + str(-k + i + j) + str(k)))
                    G_CNF.addClause(new_cl)
    print("Etape 4 : ", G_CNF)
    return G_CNF

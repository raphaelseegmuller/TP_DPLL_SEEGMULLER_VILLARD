import CNF




#=====================================================================
# Question 1 :

# notation de la négation : -

def monolitteral(F):
    # retourne le premier monolitteral de F s'il en a, rien sinon
    for i in range(len(F)):
        if len(F[i]) == 1:
            return (F[i][0], i)
    return


def simplifie(F, var, val):
    # F : CNF
    # var : variable propositionnel
    # val = 0 ou 1 : valeure que la variable propositionnel doit prendre
    for i in range(len(F)):
        if len(F[i]) == 1 and F[i][0] == var:
            if var[0] == '-':
                if val == 1:
                    return [[0]]
                else:
                    F = F[:i] + F[i + 1:]
            else:
                if val == 0:
                    return [[0]]
                else:
                    F = F[:i] + F[i + 1:]
        ##PAS FINI !!!!!!!

    return F


def DPLL(F: list):
    # F : CNL
    # Retourne : satisfaisable et les modèles, ou insatisfaisable

    PROP = []  # liste des symboles propositionnels
    # ATTENTION : tout en positif
    for i in range(len(F)):
        for j in range(len(F[i])):
            if F[i][j] not in PROP:
                if F[i][j][0] == '-':
                    PROP += [F[i][j][1:]]
                else:
                    PROP += [F[i][j]]
    # return(PROP)
    I = [[]]  # ensemble des modèles

    if len(F) == 0:
        return ('satisfaisable', PROP)
    elif [] in F:
        return ('insatisfaisable')
    while len(I[0]) < len(PROP):
        if monolitteral(F) != None:
            # on le met a vrai
            i = monolitteral(F)[1]
            F = F[:i] + F[i + 1:]
            return F
        ##ATTENTUION PAS FINI !!!! BOUCLE INFINI!!!!


F = [['a', '-j', 'l'], ['-r'], ['z', 't']]
print(DPLL(F))


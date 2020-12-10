from litteral import litteral
from clause import clause
from CNF import CNF


def read_CNF(file):
    f = open(file, "r")
    res = CNF([])
    line = f.readline()
    clause_list = []
    T1 = False
    for i in range(len(line)):
        if line[i] == "(":
            T1 = True
            clause_list += [""]
        elif line[i] == ")":
            T1 = False
        else:
            if T1:
                clause_list[-1] += line[i]
    for cl in clause_list:
        litt_list = [""]
        k = 0
        while k < len(cl):
            if k + 4 >= len(cl):
                litt_list[-1] += cl[k]
                k += 1
            elif cl[k:k + 4] == " ou ":
                litt_list += [""]
                k = k + 4
            else:
                litt_list[-1] += cl[k]
                k += 1
        new_cl = clause([])
        for litt in litt_list:
            new_cl.addLitteral(litteral(litt))
        res.addClause(new_cl)
    return res


def write_CNF(cnf, file):
    f = open(file, "w")
    f.write(str(cnf))
    f.close()
    return "Fin"

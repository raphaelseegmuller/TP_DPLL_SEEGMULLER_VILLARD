__Author__ = "noeline"
__Filename__ = "CNF.py"
__Creationdate__ = "23/10/20"

from clause import *
from copy import copy
from time import time
import math


class CNF():

    def __init__(self, clauses):
        # clauses est une liste de clauses
        self.clauses = clauses

    @property
    def clauses(self):
        return self.__clauses

    @clauses.setter
    def clauses(self, L):
        if L == []:
            self.__clauses = L
        elif isinstance(L, list):
            i = 0
            for cl in L:
                if not (isinstance(cl, clause)):
                    i += 1
            if i == 0:
                self.__clauses = L

    def __len__(self):
        # donne le nombre de clauses
        return len(self.clauses)

    def isEmpty(self):
        if len(self) == 1:
            if self.clauses[0].isEmpty():
                return True
        return False

    def __str__(self):
        if self.isEmpty():
            return ""
        chaine = "(" + str(self.clauses[0])
        for cl in self.clauses[1:]:
            chaine += ') et (' + str(cl)
        return chaine + ')'

    def liste(self):
        # retourne la liste des littéraux
        liste = []
        for elt in self.clauses:
            liste += [elt.liste()]
        return liste

    def addClause(self, cl: 'clause'):
        self.clauses = self.clauses + [cl]

    def removeClause(self, cl: 'clause'):
        liste = []
        for elt in self.clauses:
            if cl != elt:
                liste += [elt]
        return CNF(liste)

    def simplifie_resouds(self, prop: 'litteral', val: 'bool'):
        # la variable propositionnelle prend la valeur val
        # supprime aussi les doublons
        # ATTENTION prop doit etre positif
        if self.isEmpty():
            return self
        ans = CNF([])
        for i in range(len(self)):
            new_cl = self.clauses[i].simplifie_resouds(prop, val)
            if new_cl.isEqual(clause([litteral(False)])):
                return CNF([clause([litteral(False)])])
            elif not (new_cl.isEqual(clause([litteral(True)]))):
                ans.addClause(new_cl)
        L = ans.liste()
        surplus = []
        for j in range(len(L)):
            for k in range(j, len(L)):
                if j != k:
                    if ans.clauses[j].isEqual(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
            surplus = []
            L = ans.liste()
        for j in range(len(L)):
            for k in range(len(L)):
                if j != k:
                    if ans.clauses[j].comparaison(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            surplus = list(set(surplus))
            surplus.sort(reverse=True)
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
        return ans

    def simplifie(self):
        # Simplifie la forme clausale.
        if self.isEmpty():
            return self
        ans = CNF([])
        for i in range(len(self)):
            new_cl = self.clauses[i].simplifie()
            if new_cl.isEqual(clause([litteral(False)])):
                return CNF([clause([litteral(False)])])
            elif not (new_cl.isEqual(clause([litteral(True)]))):
                ans.addClause(new_cl)
        L = ans.liste()
        surplus = []
        for j in range(len(L)):
            for k in range(j, len(L)):
                if j != k:
                    if ans.clauses[j].isEqual(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
            surplus = []
            L = ans.liste()
        for j in range(len(L)):
            for k in range(len(L)):
                if j != k:
                    if ans.clauses[j].comparaison(ans.clauses[k]):
                        surplus += [k]
        if surplus != []:
            surplus = list(set(surplus))
            surplus.sort(reverse=True)
            for elt in surplus:
                ans = ans.removeClause(ans.clauses[elt])
        return ans

    # --------------- rajouté par nono la meilleure ----------
    def prop(self):
        # retourne la liste des variables propositionnelles d'une CNF
        liste = []
        for cl in self.clauses:
            for litt in cl.litteraux:
                if litt.var() not in liste:
                    liste += [litt.var()]
        return liste

    def prop_neg(self):
        # retourne la liste des variables propositionnelles d'une CNF MAIS en négatifs
        liste = []
        for cl in self.clauses:
            for litt in cl.litteraux:
                if litt.var_neg() not in liste:
                    liste += [litt.var_neg()]
        return liste

    def isThereClauseUnitaire(self, ind=False, prop=None, etat_litt=None):
        # renvoie le litteral de la première clause unitaire s'il y en a
        # si ind=True, la fonction rencoir l'indice de la clause, utile pour DPLL
        # si prop = prop du DPLL alrors la fct renvoie le litteral que si il vaut 0 dans etat_litt
        liste = []
        for cl in self.clauses:
            if cl.isClauseUnitaire() and (prop == None or etat_litt[prop.index(cl.litteraux[0])] == 0):
                # if cl.isClauseUnitaire():  #juste "if" de quelque chose différent de None, ca rentre dans la boucle
                if ind == True:
                    return self.clauses.index(cl)
                return cl.litteraux[0]
        return None

    def isThereLitteralPur(self, all=False, prop=None, etat_litt=None):
        litt_pur = []
        for cl in self.clauses:
            litt_cl = cl.liste()
            for litt in litt_cl:
                if (litt not in litt_pur) and (litteral(litt).oppose() not in litt_pur) and (
                        prop == None or (prop != None and etat_litt[prop.index(cl.litteraux[0])] == 0)):
                    litt_pur += [litt]
                elif litteral(litt).oppose() in litt_pur:
                    litt_pur.remove(litteral(litt).oppose())
                    if litteral(litt) in litt_pur:
                        litt_pur.remove(litteral(litt))
        if len(litt_pur) > 0:
            if all == True:
                return litt_pur
            return litt_pur[0]
        return None

    # utiles pour DPLL ###################################
    @staticmethod
    def une_clause_est_fausse(clauses, n, pile_litteraux):
        for cl in clauses:
            if len(cl) == 0:
                continue
            val = 0  # est ce que ca clause est fausse ?
            for litt in cl:
                opp_litt = int((litt + (n / 2)) % n)  # littéral opposé de litt
                if opp_litt in pile_litteraux:
                    val += 1  # +1 littéral faux est a faux
            if val == len(
                    cl):  # si on a autant de littéraux faux dans la clause que de littéraux dans la clause (ie si tous les littéraux sont à faux)
                return True
        return False

    @staticmethod
    def contientClauseUnitaire(clauses, etat_clause,
                               pile_litteraux, len_prop):  # on veut savoir si il existe une clause contenant un seul littéral non vérifié
        #print('----------->')
        #print(clauses)
        #print(pile_litteraux)
        for i_cl in range(len(clauses)):
            # print(clauses[i_cl])
            if etat_clause[i_cl] == 0:
                val = 0  # nb de littéraux qui ne valent pas vrai
                for litt in clauses[i_cl]:
                    #print('-----', litt)
                    opp_litt = (litt + (len_prop / 2)) % len_prop
                    if litt not in pile_litteraux and opp_litt not in pile_litteraux:
                        # print('litt not in pile_litteraux')
                        val += 1
                        l = litt
                    #print(val)
                if val == 1:
                    # print('l : ', l)
                    return l
        return False

    @staticmethod
    def tout_est_verifie(etat_litteral):
        for litt in etat_litteral:
            if litt == 0:
                return False
        return True

    @staticmethod
    def heuristic(litt, ec, el, choice):
        """
        Choisit un littéral pour avancer dans DPLL.
        :param litt: ensemble de littéraux
        :param ec: liste des états des clauses
        :param el: liste des états des littéraux
        :param choice: choix de l'heuristique
        :return: indice du littéral choisit
        """
        # Heuristiques
        if choice == "first_satisfy":
            # Obtention du littéral ayant le plus d'occurences
            m = 0
            res = 0
            for l in range(math.ceil(len(el)/2)):
                counter = 0
                if el[l] == 0 and el[int((l + (len(el) / 2)) % len(el))] != 1:
                    for c in litt[l]:
                        if ec[c] == 0:
                            counter += 1
                if counter >= m:
                    m = counter
                    res = l
            return res
        elif choice == "first_fail":
            m = 0
            res = math.ceil(len(el)/2)
            for l in range(math.ceil(len(el)/2), len(el)):
                counter = 0
                if el[l] == 0 and el[int((l + (len(el) / 2)) % len(el))] != 1:
                    for c in litt[l]:
                        if ec[c] == 0:
                            counter += 1
                if counter >= m:
                    m = counter
                    res = l
            return res
        else:
            for i in range(len(el)):
                if el[i] == 0:
                    if el[int((i + (len(el) / 2)) % len(el))] != 1:  # pas forcément utile suivant DPLL.
                        return i

    @staticmethod
    def updateEtatClauses(clauses, etat_clause, pile_litteraux):
        for i_cl in range(len(etat_clause)):
            val = 0
            for litt in clauses[i_cl]:
                if litt not in pile_litteraux:
                    val += 1
            if val == len(clauses[i_cl]) and len(clauses[i_cl]) != 0:
                etat_clause[i_cl] = 0
            else:
                etat_clause[i_cl] = 1
        return etat_clause

    @staticmethod
    def toutes_var_prop_regarde(etat_litteral):
        for i in range(len(etat_litteral)):
            if etat_litteral[i] == 0 and etat_litteral[int((i + (len(etat_litteral) / 2)) % len(etat_litteral))] == 0:
                return False
        return True

    def DPLL(self, ans=0, choice=None, Time=False):
        """
        :param ans: entier dans {0, 1, 2, 3} --> la réponse souhaité
        :param choice: chaine de caractère --> choix de l'heuristique
        :param Time: Booléen --> option d'affichage du temps de l'algorithme
        :return:    si ans = 0 --> la méthode renvoie si la CNF est satisfaisable ou non (Booléen)
                    si ans = 1 --> la méthode renvoie une valuation si la CNF est satisfaisable, None sinon
                    si ans = 2 --> la méthode renvoie toutes les valuations de la CNF sous forme de liste (liste de liste)
                    si ans = 3 --> la méthode renvoie le nombre de valuations (entier)
                    si ans = 4 --> la méthode renvoie le nombre de noeuds de l'arbre (entier)
        """

        temps1 = time()
        # ------------------------- création et simplification -----------------------------
        # I) création :
        # I) 1) création de litteraux :
        litteraux = []
        prop_total = self.prop() + self.prop_neg()  # donne la numérotation des littéraux de la CNF
        prop = copy(prop_total)  # , ATTENTION ne contient ni True ni False
        for elt in prop:
            if elt == True or elt == False:
                prop.remove(elt)

        for i_litt in range(len(prop)):
            litteraux += [[]]
            for i_cl in range(len(self.clauses)):
                if prop[i_litt] in self.clauses[i_cl].liste():
                    litteraux[i_litt] += [i_cl]

        # I) 2) création de clauses :
        clauses = []
        for i_cl in range(len(self.clauses)):
            clauses += [[]]
            for i_litt in range(len(prop)):
                if prop[i_litt] in self.clauses[i_cl].liste():
                    clauses[i_cl] += [i_litt]
            if self.clauses[i_cl].contientTrue():
                clauses[i_cl] += [True]
            if self.clauses[i_cl].contientFalse():
                clauses[i_cl] += [False]

        # --> ici, clauses et litteraux ne sont pas simplifiés mais prop ne contient ni True ni false\
        prop1 = copy(prop)  # utile pour la fin, pour retrouver toutes les valuations

        # II) simplification :
        # II) 1) simplification de clauses :
        for i_cl in range(len(clauses)):
            if len(clauses[i_cl]) == 1 and clauses[i_cl][0] is False:
                # si la CNF contient une clause unitaire [False] alors la CNF est fausse
                if ans == 0:
                    return False
                elif ans == 1:
                    return None
                elif ans == 2:
                    return []
                elif ans == 3:
                    return 0
                elif ans == 4:
                    return 1
            else:
                for litt in clauses[i_cl]:
                    if litt is True:
                        # si une clause contient True alors cette clause est True
                        for litt2 in clauses[i_cl]:
                            if not (litt2 is True) and not (litt2 is False):
                                litteraux[litt2].remove(i_cl)
                        clauses[i_cl] = []
                        break
                    else:
                        if litt is False:
                            # si une clause contient False mais aussi d'autres littéraux, on peut le supprimer
                            # (importance du is et pas == pck pour python, 0 == False)
                            clauses[i_cl].remove(False)
                        opp_litt = (litt + (len(prop) / 2)) % len(prop)
                        if opp_litt in clauses[i_cl]:
                            # si une clause contient un littéral et son opposé, la clause est vrai
                            for litt2 in clauses[i_cl]:
                                if not (litt2 is True) and not (litt2 is False):
                                    litteraux[litt2].remove(i_cl)
                            clauses[i_cl] = []

        # II) 2) simplification de prop et littéraux
        # dans cette partie, on ne va garder que les littéraux utiles
        decalage = [0 for i in range(len(prop))]  # (utile pour la désimplification)
        litt = 0  # litt est le litteral qu'on regarde, on met pas for pck on veut la mise à jours ------------------------
        while litt < len(litteraux):  # tant qu'on a pas regardé tous les litteraux de litteraux
            opp_litt = int((litt + (len(prop) / 2)) % len(prop))
            if len(litteraux[litt]) == 0 and len(litteraux[opp_litt]) == 0:
                # si un litteral et son opposé n'apparaissemnt dans aucune clause
                del prop[min(litt, opp_litt)]
                del prop[max(litt, opp_litt) - 1]
                del litteraux[min(litt, opp_litt)]
                del litteraux[max(litt, opp_litt) - 1]
                for i_cl in range(len(clauses)):
                    for i_litt2 in range(len(clauses[i_cl])):
                        if clauses[i_cl][i_litt2] > min(litt, opp_litt) and clauses[i_cl][i_litt2] < max(litt, opp_litt):
                            clauses[i_cl][i_litt2] -= 1
                        elif clauses[i_cl][i_litt2] > max(litt, opp_litt):
                            clauses[i_cl][i_litt2] -= 2
                for i_dec in range(int(len(decalage))):
                    if i_dec > min(litt, opp_litt) and i_dec < max(litt, opp_litt):
                        decalage[i_dec] += 1
                    elif i_dec > max(litt, opp_litt):
                        decalage[i_dec] += 2
                del decalage[min(litt, opp_litt)]
                del decalage[max(litt, opp_litt) - 1]
            litt += 1

        len_prop = len(prop)
        len_clauses = len(clauses)

        temps2 = time()
        # ------------------------------ algo DPLL -------------------------------
        etat_clause = [0 for i in range(len_clauses)]
        etat_litteral = [0 for i in range(len_prop)]
        for i in range(len_clauses):
            if len(clauses[i]) == 0:
                etat_clause[i] = 1
        pile_litteraux = []
        clause_unitaire = []
        valuations = []

        nb_noeuds = 1

        # arbre du DPLL :
        while not (((ans == 0 or ans == 1) and len(valuations) > 0) or self.tout_est_verifie(etat_litteral)):
            val = len(valuations)

            # 1 branche du DPLL :
            while val == len(valuations):  # tant qu'on a rien rajouté dans valuations
                etat_clause = self.updateEtatClauses(clauses, etat_clause, pile_litteraux)
                # (soit on arrive a faux et y a beak, soit on a une valuation et ca coupe le boucle while)
                if etat_clause == [1 for i in range(len_clauses)]:
                    # si toutes les clauses sont à vrai
                    valuations += [pile_litteraux]
                    break
                elif self.une_clause_est_fausse(clauses, len_prop, pile_litteraux):
                    break
                elif self.toutes_var_prop_regarde(etat_litteral):
                    # toutes les variables propositionnels ont été regardé et la cnf n'est pas vraie, donc elle est fausse
                    break
                elif self.contientClauseUnitaire(clauses, etat_clause, pile_litteraux, len_prop) is not False:
                    l = self.contientClauseUnitaire(clauses, etat_clause, pile_litteraux, len_prop)  # (il faut que l prend la valeur VRAI !!)---------------
                    clause_unitaire += [True]
                else:
                    l = self.heuristic(clauses, litteraux, etat_clause, etat_litteral, choice)
                    clause_unitaire += [False]
                pile_litteraux += [l]
                etat_litteral[l] = 1
                nb_noeuds += 1


            # backtrack :
            dernier_litt = pile_litteraux[-1]  # dernier litteral visité
            pile_litteraux = pile_litteraux[:-1]  # on dépile
            opp_dernier_litt = int((dernier_litt + (len_prop / 2)) % len_prop)

            sortie = False  # (utile pour sortir de 2 while si on a fini)
            while etat_litteral[dernier_litt] == 1 and (etat_litteral[opp_dernier_litt] == 1 or clause_unitaire[-1] == True):
                # tant que un litt est visité et son oppose, on remonte l'arbre
                if (len(pile_litteraux) == 0 and clause_unitaire[0] == True) or (len(pile_litteraux) == 1 and etat_litteral[pile_litteraux[0]] == 1 and etat_litteral[int((pile_litteraux[0] + (len_prop / 2)) % len_prop)] == 1):
                    sortie = True
                    break
                etat_litteral[dernier_litt] = 0
                etat_litteral[opp_dernier_litt] = 0
                dernier_litt = pile_litteraux[-1]  # dernier litteral visité
                pile_litteraux = pile_litteraux[:-1]
                clause_unitaire = clause_unitaire[:-1]
                opp_dernier_litt = int((dernier_litt + (len_prop / 2)) % len_prop)

            if sortie == True:
                break
            nb_noeuds += 1

            pile_litteraux += [opp_dernier_litt]
            etat_litteral[opp_dernier_litt] = 1  # pb a la fin ??
            etat_clause = self.updateEtatClauses(clauses, etat_clause, pile_litteraux)

        # pour la dernière branche : --------------------------- utile ?
        #if etat_clause == [1 for i in range(len_clauses)]:  # si toutes les clauses sont à vrai
        #    valuations += [pile_litteraux]



        temps3 = time()
        # --------------------------------- désimplification --------------------------------------
        for i_val in range(len(valuations)):
            for i_prop in range(len(valuations[i_val])):
                valuations[i_val][i_prop] += decalage[valuations[i_val][i_prop]]

        len_prop1 = len(prop1)

        valuations_full = []
        for val in valuations:
            l = len(val)
            val_full = [val]
            if len(val) < len_prop1 / 2:  # si la valuation n'impose pas la valeur à toutes les prop
                for i in range(int(len_prop1 / 2)):
                    opp_i = int((i + (len_prop1 / 2)) % len_prop1)
                    if i not in val and opp_i not in val:
                        for elt in [v for v in val_full if len(v) < len_prop1 / 2]:
                            del val_full[val_full.index(elt)]
                            val_full += [elt + [i], elt + [opp_i]]
            valuations_full += val_full

        temps4 = time()

        valuations_lisible = []
        for i in range(len(valuations_full)):
            valuations_lisible += [[]]
            for litt in valuations_full[i]:
                valuations_lisible[i] += [prop1[litt]]

        nombre_valuations = len(valuations_full)

        temps_tot = temps4 - temps1
        if Time == True:
            print()
            print('---temps---')
            print('temps_tot = ', temps_tot)
            print('temps_simpl = ', 100*(temps2 - temps1) / temps_tot, ' %')
            print('temps_dpll = ', 100*(temps3 - temps2) / temps_tot, ' %')
            print('temps_remplissage = ', 100*(temps4 - temps3) / temps_tot, ' %')
            print('--- ---')
            print()

        if ans == 0:
            return len(valuations) == 0
        elif ans == 1:
            if len(valuations_full) == 0:
                return None
            return valuations_lisible[0]
        elif ans == 2:
            return valuations_lisible
        elif ans == 3:
            return nombre_valuations
        elif ans == 4:
            return nb_noeuds

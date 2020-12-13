from clause import *
from copy import copy

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
        #si ind=True, la fonction rencoir l'indice de la clause, utile pour DPLL
        # si prop = prop du DPLL alrors la fct renvoie le litteral que si il vaut 0 dans etat_litt
        liste = []
        for cl in self.clauses:
            if cl.isClauseUnitaire() and (prop == None or etat_litt[prop.index(cl.litteraux[0])] == 0):
            #if cl.isClauseUnitaire():  #juste "if" de quelque chose différent de None, ca rentre dans la boucle
                if ind == True:
                    return self.clauses.index(cl)
                return cl.litteraux[0]
        return None

    def isThereLitteralPur(self, all=False, prop=None, etat_litt=None):
        litt_pur = []
        for cl in self.clauses:
            litt_cl = cl.liste()
            for litt in litt_cl:
                if (litt not in litt_pur) and (litteral(litt).oppose() not in litt_pur) and (prop == None or (prop != None and etat_litt[prop.index(cl.litteraux[0])] == 0)):
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
            val = 0  #est ce que ca clause est fausse ?
            for litt in cl:
                opp_litt = int((litt + (n / 2)) % n) #littéral opposé de litt
                if opp_litt in pile_litteraux:
                    val += 1  # +1 littéral faux est a faux
            if val == len(cl):  # si on a autant de littéraux faux dans la clause que de littéraux dans la clause (ie si tous les littéraux sont à faux)
                return True
        return False

    @staticmethod
    def contientClauseUnitaire(clauses, etat_clause, pile_litteraux):  #on veut savoir si il existe une clause contenant un seul littéral non vérifié
        #print('----------->')
        #print(clauses)
        #print(pile_litteraux)
        for i_cl in range(len(clauses)):
            #print(clauses[i_cl])
            if etat_clause[i_cl] == 0:
                val = 0 #nb de littéraux qui ne valent pas vrai
                for litt in clauses[i_cl]:
                    if litt not in pile_litteraux:
                        #print('litt not in pile_litteraux')
                        val += 1
                        l = litt
                if val == 1:
                    #print('l : ', l)
                    return l
        return False

    @staticmethod
    def tout_est_verifie(etat_litteral):
        for litt in etat_litteral:
            if litt == 0:
                return False
        return True

    @staticmethod
    def heuristic(cl, litt, ec, el, choice):
        """
        Choisit un littéral pour avancer dans DPLL.
        :param cl: ensemble de clauses
        :param litt: ensemble de littéraux
        :param ec: liste des états des clauses
        :param el: liste des états des littéraux
        :param choice: choix de l'heuristique
        :return: indice du littéral choisit
        """
        '''
        # Clause unitaire ???
        for i in range(len(ec)):
            if ec[i] == 0:
                litt_list = cl[i]
                unwanted = []
                for j in litt_list:
                    if el[int((j + (len(el) / 2)) % len(el))] == 1:
                        unwanted += [j]
                for k in unwanted:
                    if k in litt_list:
                        litt_list = litt_list.remove(k)
                if len(litt_list) == 1:
                    return litt_list[0]
        '''
        # Heuristiques
        if choice == "first_satisfy" or choice == "first_fail":
            # Obtention du littéral ayant le plus d'occurences
            m = 0
            res = 0
            for l in range(len(el)):
                counter = 0
                if el[l] == 0 and el[int((l + (len(el) / 2)) % len(el))] != 1:
                    for c in litt[l]:
                        if ec[c] == 0:
                            counter += 1
                if counter >= m:
                    m = counter
                    res = l
            if choice == "first_satisfy":
                return res
            else:
                return int((res + (len(el) / 2)) % len(el))
        else:
            for i in range(len(el)):
                if el[i] == 0:
                    if el[int((i + (len(el) / 2)) % len(el))] != 1:  # pas forcément utile suivant DPLL.
                        return i

    @staticmethod
    def updateEtatClauses(clauses, etat_clause, pile_litteraux):
        #print('update etat clause')
        #print(clauses)
        #print(etat_clause)
        #print(pile_litteraux)
        for i_cl in range(len(etat_clause)):
            val = 0
            for litt in clauses[i_cl]:
                #print('litt', litt)
                if litt not in pile_litteraux:
                    #print('val += 1')
                    val += 1
            #print(val)
            if val == len(clauses[i_cl]) and len(clauses[i_cl]) != 0:
                etat_clause[i_cl] = 0
            else:
                etat_clause[i_cl] = 1
        return etat_clause

    @staticmethod
    def toutes_var_prop_regarde(etat_litteral):
        for i in range(len(etat_litteral)):
            if etat_litteral[i] == 0 and etat_litteral[int((i+(len(etat_litteral)/2))%len(etat_litteral))] == 0:
                return False
        return True



    def DPLL(self, ans=0, choice=None):

        # si ans = 0 alors la méthode renvoie si la CNF est satisfaisable ou non
        # si ans = 1 alors la méthode renvoie toutes les valuations de la CNF sous forme de liste (?)

        # -------- création de litteraux -------------
        # liste de liste qui, pour chaque litt (=liste dans la liste) donne les indices des clauses dans lesquel le
        # litt apparait. les littéraux sont alors représentés par des indices, celui de sa list
        litteraux = []
        prop_total = self.prop() + self.prop_neg()  # donne la numérotation des littéraux de la CNF
        prop = copy(prop_total)   #, ATTENTION ne contient ni True ni False
        for elt in prop:
            if elt == True or elt == False:
                prop.remove(elt)

        for i_litt in range(len(prop)):
            litteraux += [[]]
            for i_cl in range(len(self.clauses)):
                if prop[i_litt] in self.clauses[i_cl].liste():
                    litteraux[i_litt] += [i_cl]

        #  ----------------création de clauses----------------
        clauses = []
        #donne pour chaque chause l'indice du littéral qui est dans cette clause ET True et False si la clause contient True ou false
        for i_cl in range(len(self.clauses)):
            clauses += [[]]
            for i_litt in range(len(prop)):
                if prop[i_litt] in self.clauses[i_cl].liste():
                    clauses[i_cl] += [i_litt]
            if self.clauses[i_cl].contientTrue():
                clauses[i_cl] += [True]
            if self.clauses[i_cl].contientFalse():
                clauses[i_cl] += [False]

        #ICI, clauses et litteraux ne sont pas simplifiés mais prop ne contient ni True ni false
        # et on a pas de doublons


        # ------------------simplification-----------------

        # 1) simplification de clauses

        for i_cl in range(len(clauses)):
            if len(clauses[i_cl]) == 1 and clauses[i_cl][0] is False:  # clause unitaire [False] alors, la CNF est fausse
                return []
            else:
                for litt in clauses[i_cl]:
                    if litt is True:  # si une clause contient True alors cette clause est True
                        for litt2 in clauses[i_cl]:
                            if not (litt2 is True) and not (litt2 is False):
                                litteraux[litt2].remove(i_cl)
                        clauses[i_cl] = []
                        break
                    else:
                        opp_litt = (litt + (len(prop) / 2)) % len(prop)
                        if litt is False:  # si une clause fontient False mais aussi d'autres littéraux, on peut le supprimer
                            # important du is et pas == pck pour python, 0 == false
                            clauses[i_cl].remove(False)
                        if opp_litt in clauses[
                            i_cl]:  # si une clause contient un littéral et son opposé, la clause est vrai
                            for litt2 in clauses[i_cl]:
                                if not (litt2 is True) and not (litt2 is False):
                                    litteraux[litt2].remove(i_cl)
                            clauses[i_cl] = []

        # si on a le temps: faire une fct qui supprime les clauses qui sont uncuses dans d'autres

        # 2) simplification de prop et littéraux
        # on ne va garder que les littéraux utiles, exemple : si a n'apparait pas dans la clause simplifié, on va le
        # supprimer de prop et littéraux

        litt = 0  # litt est le litteral qu'on regarde, on met pas for pck ...
        while litt < len(litteraux):  # tant qu'on a pas regardé tous les litteraux de litteraux
            opp_litt = int((litt + (len(prop) / 2)) % len(prop))
            if len(litteraux[litt]) == 0 and len(litteraux[opp_litt]) == 0: # si un litteral et son opposé n'apparaissemnt dans aucune clause
                del prop[min(litt, opp_litt)]
                del prop[max(litt, opp_litt)-1]
                del litteraux[min(litt, opp_litt)]
                del litteraux[max(litt, opp_litt)-1]
                for i_cl in range(len(clauses)):
                    for i_litt2 in range(len(clauses[i_cl])):
                        if  clauses[i_cl][i_litt2] > min(litt, opp_litt) and clauses[i_cl][i_litt2] < max(litt, opp_litt):  #si le litteral qu'on regarde est entre litt et litt opp, n
                            clauses[i_cl][i_litt2] -= 1
                        elif clauses[i_cl][i_litt2] > max(litt, opp_litt):
                            clauses[i_cl][i_litt2] -= 2
                # litt ne change pas pck le prochain litteral a regardé à pris la place du précédent
            litt += 1  # on a rien enlevé donc on passe au littéral suivant

        print()
        print('prop : ', prop)
        print('litt : ', litteraux)
        print('clauses : ', clauses)
        print()



        # ---------algo DPLL------------------
        etat_clause = [0 for i in range(len(clauses))]  # dit si la clause a été regardé ou pas
        etat_litteral = [0 for i in range(len(litteraux))]  # dit si le littéral a été regardé ou pas : 0 si le
        # littéral n'a pas été regardé, 1 si on lui a atribué Vrai, a retenir : le littéral i vaut faut si le litteral
        # (i+(len(etat_litteral)/2))%len(etat_litteral) vaut vrai

        for i in range(len(etat_clause)):
            if len(clauses[i]) == 0:
                etat_clause[i] = 1

        pile_litteraux = [] #donne l'ordre de visite des littéraux
        valuations = []


        i = 0
        n = 50000000000000000000000000000000000000

        while not((ans == 0 and len(valuations) > 0) or self.tout_est_verifie(etat_litteral)) and i < n:
            i+=1
            val = len(valuations)
            #print('---------------dpll')

            j = 0

            #1 branche du DPLL
            while val == len(valuations) and j < n:  # tant qu'on a rien rajouté dans valuations
                #print('while branche')
                j+=1

                #print('prop : ', prop)
                #print('etat litteral : ', etat_litteral)

                etat_clause = self.updateEtatClauses(clauses, etat_clause, pile_litteraux)
                #print('etat litteral : ', etat_litteral)
                #print('etat clause : ', etat_clause)
                #soit on arrive a faut et y a beak, soit on a une valuation et ca coupe le boucle while
                if etat_clause == [1 for i in range(len(etat_clause))]:  # si toutes les clauses sont à vrai
                    #print('la CNF est vrai !!!!!!!!!!!!!!!!!!!')
                    valuations += [pile_litteraux]  #c'est la liste des littéraux qui doivent valoire Vrai pour que la CNF soit satisfaisable
                    break  #nécessaire, sinon l n'est pas définit

                elif self.une_clause_est_fausse(clauses, len(etat_litteral), pile_litteraux):
                    #print('une clause est fausse!!!!!!!!!!!!!')
                    #valuations = valuations #ne rien faire/ on ne rajoute rien a vation parce que la CNF est fausse
                    break  # dans ce cas la, on a arrété le while mais on a pas trouvé de valuation

                elif self.toutes_var_prop_regarde(etat_litteral):  # toutes les variables propositionnels ont été
                    # regardé et la cnf n'est pas vraie, donc elle est fausse
                    #print('toutes les litt one été regardé !!!!!!!!!!!!!')
                    break

                elif self.contientClauseUnitaire(clauses, etat_clause, pile_litteraux) is not False:
                    #print('clause unitaire')
                    l = self.contientClauseUnitaire(clauses, etat_clause, pile_litteraux)  # il faut que l prend la valeur VRAI !!

                else:
                    #print('heuristiques')
                    l = self.heuristic(clauses, litteraux, etat_clause, etat_litteral, choice)
                    # si toutes les var prop apparaissent le même nb de fois, il fait que heuristique en donne une quand meme

                #print('l : ', prop[l])

                pile_litteraux += [l]
                etat_litteral[l] = 1
                #for cl in litteraux[l]:
                    #print(cl)
                    #etat_litteral[cl] = 1
                #print('-->', etat_litteral)
                #etat_clause = self.updateEtatClauses(clauses, etat_clause, pile_litteraux)

            #print('fin while branche')

            #print('- pile : ', pile_litteraux)
            #print('- valuations : ', valuations)
            #print()



            #print(pile_litteraux)


            # on est arrivé au bout de la branche, maintenant, il faut dépiler la pile

            dernier_litt = pile_litteraux[len(pile_litteraux) - 1]  # dernier litteral visité
            pile_litteraux = pile_litteraux[: len(pile_litteraux) -1]  # on dépile
            opp_dernier_litt = int((dernier_litt+(len(etat_litteral)/2))%len(etat_litteral))
            #print('dernier litt : ', dernier_litt)

            #print('etat litt :', etat_litteral)

            sortie = False  #utile pour sortir de 2 while si on a fini

            while etat_litteral[dernier_litt] == 1 and etat_litteral[opp_dernier_litt] == 1:  # tant que un litt
                #print('while')
                #print(': ', pile_litteraux)
                # est visité et son oppose, on remonte l'arbre
                if len(pile_litteraux) == 1 and etat_litteral[pile_litteraux[0]] == 1 and etat_litteral[
                    int((pile_litteraux[0] + (len(etat_litteral) / 2)) % len(etat_litteral))] == 1:
                    sortie = True
                    break# pile_litteraux n'est jamais vide (sauf au début) !!!! a démontrer
                    # faux
                etat_litteral[dernier_litt] = 0
                etat_litteral[opp_dernier_litt] = 0
                dernier_litt = pile_litteraux[len(pile_litteraux) - 1]  # dernier litteral visité
                pile_litteraux = pile_litteraux[: len(pile_litteraux) - 1]  # on dépile
                opp_dernier_litt = int((dernier_litt + (len(etat_litteral) / 2)) % len(etat_litteral))

            if sortie == True:
                break


            #print('l : ', prop[opp_dernier_litt], 'back track')

            pile_litteraux += [opp_dernier_litt]
            etat_litteral[opp_dernier_litt] = 1  #pb a la fin ??
            etat_clause = self.updateEtatClauses(clauses, etat_clause, pile_litteraux)
            #print(etat_litteral)

        #pour la dernière branche :
        #utile ?
        #print(etat_clause)
        if etat_clause == [1 for i in range(len(etat_clause))]:  # si toutes les clauses sont à vrai
            #print('dernière branche : la CNF est vrai')
            valuations += [pile_litteraux]

        #print()
        #print('pile : ', pile_litteraux)

        if i == n or j == n:
            print('-----------trop long------------')



        valuations_lisible = []
        for i in range(len(valuations)):
            valuations_lisible += [[]]
            for litt in valuations[i]:
                valuations_lisible[i] += [prop[litt]]
        print(valuations_lisible)

        return valuations




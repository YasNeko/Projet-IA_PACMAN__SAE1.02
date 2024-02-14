# -*- coding: utf-8 -*-
"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module jeu.py
        Ce module contient l'implémentation du jeu qui sera exécuté par le serveur
"""
import random
import const


def _fonction_1(id_1=False, id_2=const.AUCUN, id_3=None, id_4=None):
    
    res = {'_ch_1': id_1, '_ch_2': id_2}
    if id_3 is None:
        res['_ch_3'] = set()
    else:
        res['_ch_3'] = id_3
    if id_3 is None:
        res['_ch_4'] = set()
    else:
        res['_ch_4'] = id_4
    return res


def _fonction_2(id_4):
    
    return id_4['_ch_1']




def _fonction_8(id_4):
    
    return id_4['_ch_2']


def _fonction_4(id_4):
    
    return id_4['_ch_3']

def _fonction_5(id_4):
    
    return id_4['_ch_4']


def _fonction_6(id_4):
    
    return len(id_4['_ch_3'])

def _fonction_7(id_4):
    
    return len(id_4['_ch_4'])

def _fonction_8(id_4):
    
    return id_4['_ch_2']

def _fonction_9(id_4, id_2):
    
    if not id_4['_ch_1']:
        id_4['_ch_2'] = id_2

def _fonction_10(id_4):
    
    res = id_4['_ch_2']
    id_4['_ch_2'] = const.AUCUN
    return res

def _fonction_11(id_4, id_5):
    
    id_4['_ch_3'].add(id_5)


def _fonction_12(id_4, id_5):
    
    if id_5 in id_4['_ch_3']:
        id_4['_ch_3'].remove(id_5)
        return True
    return False

def _fonction_13(id_4, id_6):
    
    if not id_4['_ch_1']:
        id_4['_ch_4'].add(id_6)


def _fonction_14(id_4, id_6):
    
    if id_6 in id_4['_ch_4']:
        id_4['_ch_4'].remove(id_6)
        return True
    return False


def _fonction_15(id_7, id_8, id_9, id_10, id_11, id_12, id_13):
    
    return {'_ch_5': id_7, '_ch_6': id_8, 
            '_ch_7': id_9, '_ch_8':id_10,
            '_ch_9': id_11, '_ch_10': id_12, '_ch_11': id_13}


def _fonction_16(id_15):
    
    couleur, nb_points, nb_faux_mvt, lin_p, col_p, lin_f, col_f, duree_glout, duree_immo, duree_mur ,nom = id_15.split(";")
    return _fonction_15(couleur, nom, int(nb_points), int(nb_faux_mvt), 
            (int(lin_p), int(col_p)), (int(lin_f), int(col_f)),
            {const.GLOUTON:int(duree_glout),
             const.IMMOBILITE:int(duree_immo),
             const.PASSEMURAILLE:int(duree_mur)})

def _fonction_17(id_16):
    
    return id_16['_ch_5']


def _fonction_18(id_16):
    
    return id_16['_ch_6']


def _fonction_19(id_16):
    
    return id_16['_ch_7']

def _fonction_20(id_16):
    
    return id_16['_ch_8']

def _fonction_21(id_16):
    
    res=[]
    for obj,duree in id_16['_ch_11'].items():
        if duree>0:
            res.append(obj)
    return res

def _fonction_22(id_16,id_2):
    
    if id_2 not in id_16['_ch_11']:
        return 0
    return id_16['_ch_11'][id_2]

def _fonction_23(id_16):
    
    return id_16['_ch_9']

def _fonction_24(id_16):
    
    return id_16['_ch_10']

def _fonction_25(id_16, id_17):
    
    id_16['_ch_9'] = id_17

def _fonction_26(id_16, id_17):
    
    id_16['_ch_10'] = id_17

def _fonction_27(id_16, id_18):
    
    id_16['_ch_7'] += id_18
    return id_16['_ch_7']

def _fonction_28(id_16):
    
    id_16['_ch_8'] -= 1
    return id_16['_ch_8']

def _fonction_29(id_16):
    
    id_16['_ch_8'] = const.NB_FAUX_MVT


def _fonction_30(id_16, id_2):
    
    points,duree=const.PROP_OBJET[id_2]
    if duree>0:   
        id_16['_ch_11'][id_2] += duree
    id_16['_ch_7'] += points


def _fonction_31(id_16):
    
    for id_2 in id_16['_ch_11']:
        if id_16['_ch_11'][id_2]>0:
            id_16['_ch_11'][id_2]-=1

# A NE PAS DEMANDER
def _fonction_32(id_16,id_17=";"):
        return str(id_16['_ch_5'])+id_17+str(id_16['_ch_7'])+\
            id_17+str(id_16['_ch_8'])+id_17+\
            str(id_16['_ch_9'][0])+id_17+str(id_16['_ch_9'][1])+\
            id_17+str(id_16['_ch_10'][0])+id_17+str(id_16['_ch_10'][1])+\
            id_17+str(id_16['_ch_11'][const.GLOUTON])+id_17+\
            str(id_16['_ch_11'][const.IMMOBILITE])+id_17+\
            str(id_16['_ch_11'][const.PASSEMURAILLE])+id_17+id_16['_ch_6']+'\n'


def _fonction_33(id_20):
    
    return id_20['_ch_12']


def _fonction_34(id_20):
    
    return id_20['_ch_13']

def _fonction_35(id_20, id_17):
    
    if id_17[1]<=0:
        return (id_17[0],id_20['_ch_13']-1)
    return (id_17[0],id_17[1]-1)

def _fonction_36(id_20, id_17):
    
    if id_17[1]>=id_20['_ch_13']-1:
        return (id_17[0],0)
    return (id_17[0],id_17[1]+1)

def _fonction_37(id_20, id_17):
    
    if id_17[0]<=0:
        return (id_20['_ch_12']-1,id_17[1])
    return (id_17[0]-1,id_17[1])

def _fonction_38(id_20, id_17):
    
    if id_17[0]>=id_20['_ch_12']-1:
        return (0,id_17[1])
    return (id_17[0]+1,id_17[1])

def _fonction_39(id_20,id_17,id_21):
    
    if id_21 == 'N':
        pos_arrivee = [id_17[0]-1, id_17[1]]
    elif id_21 == 'S':
        pos_arrivee = [(id_17[0]+1), id_17[1]]
    elif id_21 == 'O':
        pos_arrivee = [id_17[0], id_17[1]-1]
    elif id_21 == 'E':
        pos_arrivee = [id_17[0], id_17[1]+1]
    else:
        return None
    if pos_arrivee[0] < 0:
        pos_arrivee[0]=id_20['_ch_12']-1
    if pos_arrivee[0] >= id_20['_ch_12']:
        pos_arrivee[0]=0
    if pos_arrivee[1] < 0:
        pos_arrivee[1]=id_20['_ch_13']-1
    if pos_arrivee[1] >= id_20['_ch_13']:
        pos_arrivee[1]=0
    return tuple(pos_arrivee)

def _fonction_40(id_20, id_17):
    
    return id_20['_ch_14'][id_17[0] * id_20['_ch_13'] + id_17[1]]

def _fonction_41(id_20, id_17):
    
    return _fonction_8(id_20['_ch_14'][id_17[0] * id_20['_ch_13'] + id_17[1]])

def _fonction_42(id_20, id_5, id_17):
    
    _fonction_11(_fonction_40(id_20, id_17), id_5)

def _fonction_43(id_20, id_6, id_17):
    
    _fonction_13(_fonction_40(id_20, id_17), id_6)

def _fonction_44(id_20, id_2, id_17):
    
    _fonction_9(_fonction_40(id_20, id_17), id_2)

def _fonction_45(id_22, id_23=True):
    
    id_20 = {}
    les_lignes = id_22.split("\n")
    nb_lig, nb_col = les_lignes[0].split(";")
    nb_lig = int(nb_lig)
    nb_col = int(nb_col)
    id_20['_ch_12'] = nb_lig
    id_20['_ch_13'] = nb_col
    id_20['_ch_14'] = []
    for ind in range(1, nb_lig+1):
        for car in les_lignes[ind]:
            if car == '#':
                id_20['_ch_14'].append(_fonction_1(True))
            else:
                id_20['_ch_14'].append(_fonction_1(False,car))
    if not id_23:
        return id_20
    ind += 1
    nb_joueurs = int(les_lignes[ind])
    for ind in range(ind+1, ind+nb_joueurs+1):
        numj, lignej, colj = les_lignes[ind].split(";")
        _fonction_42(id_20, numj, (int(lignej), int(colj)))
    ind += 1
    nb_fantomes = int(les_lignes[ind])
    for ind in range(ind+1, ind+nb_fantomes+1):
        numf, lignef, colf = les_lignes[ind].split(";")
        _fonction_43(id_20, numf, (int(lignef), int(colf)))
    return id_20


def _fonction_46(id_24):
    
    return _fonction_45(id_24)


def _fonction_47(id_20, id_17, id_25):
    
    id_20['_ch_14'][id_17[0] * id_20['_ch_13'] + id_17[1]] = id_25




def _fonction_48(id_20, id_5, id_17):
    
    return _fonction_12(_fonction_40(id_20, id_17), id_5)


def _fonction_49(id_20, id_6, id_17):
    
    return _fonction_14(_fonction_40(id_20, id_17), id_6)


def _fonction_50(id_20, id_17):
    
    return _fonction_10(_fonction_40(id_20, id_17))

        
def _fonction_51(id_20, id_5, id_17, id_21, id_25=False):
    
    case_dep = _fonction_40(id_20, id_17)
    if id_5 not in _fonction_4(case_dep):
        return None
    pos_arr = _fonction_39(id_20,id_17,id_21)
    case_arr = _fonction_40(id_20, pos_arr)
    if _fonction_2(case_arr) and not id_25:
        return None
    _fonction_12(case_dep, id_5)
    _fonction_11(case_arr, id_5)
    return pos_arr

def _fonction_52(id_20, id_6, id_17, id_21):
    
    case_dep = _fonction_40(id_20, id_17)
    if id_6 not in _fonction_5(case_dep):
        return None
    pos_arr = _fonction_39(id_20,id_17,id_21)
    case_arr = _fonction_40(id_20, pos_arr)
    if _fonction_2(case_arr):
        return None
    _fonction_14(case_dep, id_6)
    _fonction_13(case_arr, id_6)
    return pos_arr

def _fonction_53(id_20):
    
    while(True):
        lin=random.randint(0,id_20['_ch_12']-1)
        col=random.randint(0,id_20['_ch_12']-1)
        la_case=_fonction_40(id_20,(lin,col))
        if not _fonction_2(la_case) and \
            _fonction_8(la_case) in [const.AUCUN,const.VITAMINE] and\
            len(_fonction_5(la_case))+len(_fonction_4(la_case))==0:
            return (lin,col)



def _fonction_54(id_20,id_17,id_25=False):
    
    if id_25:
        return const.DIRECTIONS
    res=''
    for dir in  const.DIRECTIONS:
        pos_arr=_fonction_39(id_20,id_17,dir)
        if not _fonction_2(_fonction_40(id_20,pos_arr)):
                res+=dir
    return res

#---------------------------------------------------------#


def _fonction_55(id_20, id_17, id_21, distance_max):
     
    def _fonction_56(la_case):
        id_2 = _fonction_8(la_case)
        if id_2 != const.AUCUN:
            res['_ch_11'].append((dist, id_2))
        les_pacmans = _fonction_4(la_case)
        for pac in les_pacmans:
            res['_ch_15'].append((dist, pac))
        les_fantomes = _fonction_5(la_case)
        for fan in les_fantomes:
            res['_ch_16'].append((dist, fan))
              
    res = {'_ch_11': [], '_ch_15': [], '_ch_16': []}
    nb_lignes = _fonction_33(id_20)
    nb_colonnes = _fonction_34(id_20)
    pos2 = _fonction_39(id_20,id_17,id_21)
    if _fonction_2(_fonction_40(id_20, pos2)):
        return None
    calque = []
    for _ in range(nb_lignes):
        calque.append([-1]*(nb_colonnes))
    calque[pos2[0]][pos2[1]] = 1
    dist = 1
    la_case = _fonction_40(id_20, pos2)
    if _fonction_2(la_case):
        return res
    _fonction_56(la_case)
    marque = True
    while marque and dist < distance_max:
        marque = False
        dist += 1
        for lin in range(nb_lignes):
            for col in range(nb_colonnes):
                if calque[lin][col] == dist-1:
                    for dir in 'NESO':
                        pos2=_fonction_39(id_20,(lin,col),dir)
                        if calque[pos2[0]][pos2[1]] == -1:
                            la_case = _fonction_40(id_20, pos2)
                            if not _fonction_2(la_case):
                                calque[pos2[0]][pos2[1]] = dist
                                _fonction_56(la_case)
                                marque = True
    return res

def _fonction_57(id_20,id_17,id_21):
    
    
    pos2=_fonction_39(id_20,id_17,id_21)
    dist=0
    dir_prec=id_21
    fini=False
    oppose={"N":"S","S":"N","E":"O","O":"E"}
    while not fini:
        dp=_fonction_54(id_20,pos2)
        if len(dp)==1:
            return -1
        if len(dp)>2:
            return dist
        if dist>len(id_20['_ch_14']):
            return -1
        if dp[0]==oppose[dir_prec]:
            dir_prec=dp[1]
        else:
            dir_prec=dp[0]
        dist+=1
        pos2=_fonction_39(id_20,pos2,dir_prec)



# A NE PAS DEMANDER
def _fonction_58(id_20):
        res = str(id_20['_ch_12'])+";"+str(id_20['_ch_13'])+"\n"
        pacmans = []
        fantomes = []
        for lig in range(id_20['_ch_12']):
            ligne = ""
            for col in range(id_20['_ch_13']):
                la_case = _fonction_40(id_20,(lig, col))
                if _fonction_2(la_case):
                    ligne += "#"
                    les_pacmans = _fonction_4(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = _fonction_8(la_case)
                    les_pacmans = _fonction_4(la_case)
                    les_fantomes= _fonction_5(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for id_6 in les_fantomes:
                        fantomes.append((id_6,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for id_6, lig, col in fantomes:
            res += str(id_6)+";"+str(lig)+";"+str(col)+"\n"
        return res

def _fonction_59(id_20,id_17):
    
    vois=[]
    for lin in range(-1,2):
        ligne=id_17[0]+lin
        if ligne<0:
            vois=[False,False,False]
            continue
        if ligne >= _fonction_33(id_20):
            vois.extend([False,False,False])
            continue
        for col in range(-1,2):
            if lin==0 and col==0:
                continue
            colonne=id_17[1]+col
            if colonne<0:
                vois.append(False)
            elif colonne>=_fonction_34(id_20):
                vois.append(False)
            else:
                vois.append(_fonction_2(_fonction_40(id_20,(ligne,colonne))))
    return vois

    
class Jeu(object):
    def __init__(self,nom_fic="",duree_totale=200):
        if nom_fic!="":
            with open(nom_fic) as fic:
                contenu=fic.read()
        else:
            return
        self.plateau= _fonction_45(contenu,False)
        self.les_joueurs={}
        self.duree_totale=duree_totale
        self.duree_actuelle=0
        self.nb_joueurs=0
        self.fantomes_repus=set()
        self.fantomes_repus_prec=set()

    def jeu_2_str(self,separateur=";"):
        res=str(self.duree_actuelle)+separateur+str(self.duree_totale)+'\n'
        res+="-"*20+'\n'+_fonction_58(self.plateau)+"-"*20+'\n'
        for un_joueur in self.les_joueurs.values():
            res+=_fonction_32(un_joueur,separateur)
        return res

    def jeu_from_str(self,chaine,separateur=';'):
        param,le_plateau,les_joueurs=chaine.split("-"*20+'\n')
        self.plateau=_fonction_45(le_plateau)
        self.les_joueurs={}
        for ligne in les_joueurs.split('\n'):
            if ligne!='':
                le_joueur=_fonction_16(ligne)
                self.les_joueurs[_fonction_17(le_joueur)]=le_joueur
        # il faut récupérer les paramètres
        duree_actuelle,duree_totale=param.split(separateur)
        self.duree_actuelle=int(duree_actuelle)
        self.duree_totale=int(duree_totale)
        
    def inscrire_joueur(self,nom):
        coul=chr(ord('A')+self.nb_joueurs)
        self.nb_joueurs+=1
        pos_pac=_fonction_53(self.plateau)
        _fonction_42(self.plateau,coul,pos_pac)
        pos_fan=_fonction_53(self.plateau)
        _fonction_43(self.plateau,coul.lower(),pos_fan)
        self.les_joueurs[coul]=_fonction_15(coul,nom,0,0,pos_pac,pos_fan,const.aucun_objet())

    def ajouter_objet(self):
        pos=_fonction_53(self.plateau)
        objet=random.choice(const.LES_OBJETS[1:])
        _fonction_44(self.plateau,objet,pos)
        return "L'objet @"+objet+"@ est apparu en "+str(pos)+"\n"

    def est_statufie(self,pos):
        nb_lig=_fonction_33(self.plateau)
        nb_col=_fonction_34(self.plateau)
        if pos[0]<const.DIST_MAX:
            debut_lig=nb_lig-(const.DIST_MAX-pos[0])
        else:
            debut_lig=pos[0]-const.DIST_MAX
        if pos[1]<const.DIST_MAX:
            debut_col=nb_col-(const.DIST_MAX-pos[1])
        else:
            debut_col=pos[1]-const.DIST_MAX
        for i in range(2*const.DIST_MAX+1):
            for j in range(2*const.DIST_MAX+1):
                les_pacmans=_fonction_4(_fonction_40(self.plateau,((debut_lig+i)%nb_lig,(debut_col+j)%nb_col)))
                for pac in les_pacmans:
                    if _fonction_22(self.les_joueurs[pac],const.IMMOBILITE)>0:
                        return True
        return False

    
    def executer_deplacer_pacman(self,couleur,direction):
        le_joueur=self.les_joueurs[couleur]
        pos_pac=_fonction_23(le_joueur)
        res=""
        if direction not in "NESO":
            res+="@"+couleur+"@"+" a donné une mauvaise direction "+direction+"\n"
            _fonction_27(le_joueur,-const.PENALITE)
            if _fonction_28(le_joueur)<=0:
                pos_arr=_fonction_53(self.plateau)
                res+="@"+couleur+"@"+" a été téléporté en"+str(pos_arr)+"\n"
                _fonction_48(self.plateau,couleur,pos_pac)
                _fonction_42(self.plateau,couleur,pos_arr)
                _fonction_25(le_joueur, pos_arr)
                _fonction_29(le_joueur)
            return res
        
        pos_arrivee=_fonction_51(self.plateau,couleur,
                                            pos_pac,direction, _fonction_22(le_joueur,const.PASSEMURAILLE)>0)
        
        if pos_arrivee==None:
            res+="@"+couleur+"@"+" a fait un faux mouvement\n"
            _fonction_27(le_joueur,-const.PENALITE)
            if _fonction_28(le_joueur)<=0:
                pos_arr=_fonction_53(self.plateau)
                res+="@"+couleur+"@"+" a été téléporté en"+str(pos_arr)+"\n"
                _fonction_48(self.plateau,couleur,pos_pac)
                _fonction_42(self.plateau,couleur,pos_arr)
                _fonction_25(le_joueur, pos_arr)
                _fonction_29(le_joueur)
            return res
        _fonction_48(self.plateau,couleur,pos_pac)
        _fonction_42(self.plateau,couleur,pos_arrivee)
        case_arrivee=_fonction_40(self.plateau,pos_arrivee)
        objet=_fonction_8(case_arrivee)
        if objet!=const.AUCUN:
            _fonction_30(le_joueur, objet)
            res+="@"+couleur+"@"+" a pris l'objet @"+objet+"@\n"
            _fonction_10(case_arrivee)
            if objet==const.TELEPORTATION:
                _fonction_48(self.plateau,couleur,pos_arrivee)
                pos_arrivee=_fonction_53(self.plateau)
                res+="@"+couleur+"@"+" a été téléporté en"+str(pos_arrivee)+"\n"
                _fonction_42(self.plateau,couleur,pos_arrivee)
        _fonction_25(le_joueur, pos_arrivee)

        fantomes=_fonction_5(case_arrivee)
        if _fonction_22(le_joueur,const.GLOUTON)>0:
            for fan in fantomes:
                res+="@"+couleur+"@"+" a attaqué le fantome @"+fan+"@\n"
                _fonction_27(le_joueur,const.POINTS_BATAILLE)
                _fonction_27(self.les_joueurs[fan.upper()],-const.POINTS_BATAILLE)
        else:
            for fan in fantomes:
                res+="@"+couleur+"@"+" a été attaqué par le fantome @"+fan+"@\n"
                _fonction_27(le_joueur,-const.POINTS_BATAILLE)
                _fonction_27(self.les_joueurs[fan.upper()],const.POINTS_BATAILLE)
                self.fantomes_repus.add(fan)
        return res

    def executer_deplacer_fantome(self,couleur,direction):
        le_joueur=self.les_joueurs[couleur]
        coul_fan=couleur.lower()
        pos_fan=_fonction_24(le_joueur)
        res=""
        if coul_fan in self.fantomes_repus_prec:
            return "@"+coul_fan+"@ digère\n"
        if self.est_statufie(pos_fan):
            return "@"+coul_fan+"@ est statufié\n"
        if direction not in "NESO":
            _fonction_27(le_joueur,-const.PENALITE)
            res+="@"+couleur+"@"+" a donné une mauvaise direction "+direction+"\n"
            if _fonction_28(le_joueur)<=0:
                pos_arr=_fonction_53(self.plateau)
                res+="@"+couleur+"@"+" a été téléporté en"+str(pos_arr)+"\n"
                _fonction_49(self.plateau,coul_fan,pos_fan)
                _fonction_43(self.plateau,coul_fan,pos_arr)
                _fonction_26(le_joueur, pos_arr)
                _fonction_29(le_joueur)
            return res
        
        pos_arrivee=_fonction_52(self.plateau,coul_fan,
                                            pos_fan,direction)

        if pos_arrivee==None:
            res+="@"+coul_fan+"@"+" a fait un faux mouvement\n"
            _fonction_27(le_joueur,const.PENALITE)
            if _fonction_28(le_joueur)<=0:
                pos_arr=_fonction_53(self.plateau)
                res+="@"+coul_fan+"@"+" a été téléporté en"+str(pos_arr)+"\n"
                _fonction_49(self.plateau,coul_fan,pos_fan)
                _fonction_43(self.plateau,coul_fan,pos_arr)
                _fonction_26(le_joueur, pos_arr)
                _fonction_29(le_joueur)
            return res
        _fonction_26(le_joueur,pos_arrivee)

        for pac in _fonction_4(_fonction_40(self.plateau,pos_arrivee)):
            if _fonction_22(self.les_joueurs[pac],const.GLOUTON)>0:
                res+="@"+coul_fan+"@"+" a été attaqué par le pacman @"+pac+"@\n"
                _fonction_27(le_joueur,-const.POINTS_BATAILLE)
                _fonction_27(self.les_joueurs[pac],const.POINTS_BATAILLE)
            else:
                res+="@"+couleur+"@"+" a attaqué le fantome @"+coul_fan+"@\n"
                _fonction_27(le_joueur,const.POINTS_BATAILLE)
                _fonction_27(self.les_joueurs[pac],-const.POINTS_BATAILLE)
                self.fantomes_repus.add(coul_fan)
        return res

    def fin_tour(self):
        self.duree_actuelle+=1
        self.fantomes_repus_prec=self.fantomes_repus
        self.fantomes_repus=set()
        msg=""
        if self.duree_actuelle>=self.duree_totale:
            self.duree_actuelle=self.duree_totale
            return "Partie terminée\n"
        for un_joueur in self.les_joueurs.values():
            _fonction_31(un_joueur)
    
        if random.randint(1,10)<3:
            msg=self.ajouter_objet()
        return msg
            

    def tour_de_jeu(self,actions):
        melange=actions.items()
        random.shuffle(melange)
        for couleur,act in melange:
            if len(act)==2:
                msg=self.executer_deplacer_pacman(couleur,act[0])
            else:
                msg=self.executer_deplacer_pacman(couleur," ")
        for couleur,act in melange:
            if len(act)==2:
                msg=self.executer_deplacer_fantome(couleur,act[1])
            else:
                msg=self.executer_deplacer_fantome(couleur," ")

        self.duree_actuelle+=1
        if self.duree_actuelle>=self.duree_totale:
            self.duree_actuelle=self.duree_totale
            return False
        return True

    def sauver_score(self,nom_fic):
        with open(nom_fic, "w") as fic:
            for ind_j in range(self.nb_joueurs):
                le_joueur = self.les_joueurs[chr(ord('A')+ind_j)]
                fic.write(
                _fonction_18(le_joueur).replace("~", ".").replace(";", ",") + ";" + \
                            str(_fonction_19(le_joueur)) + "\n")

    def classement(self):
        res=list(self.les_joueurs.values())
        res.sort(key=lambda x:_fonction_19(x),reverse=True)
        return res

    def get_duree_restante(self):
        return self.duree_totale-self.duree_actuelle
    
    def est_fini(self):
        return self.duree_actuelle==self.duree_totale
    

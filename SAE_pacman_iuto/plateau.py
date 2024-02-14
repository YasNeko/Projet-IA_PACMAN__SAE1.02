"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""
import const
import case
import random


# représentation du plateau:
# {"nb_lignes":int,"nb_colonnes":int,"cases":{(l,c):dict}}
# exemple cases:
# {(0,0):{"mur":bool,"objet":str,"pacmans_presents":set(str),"fantomes_presents":set(str)},
# {(0,1):{"mur":bool,"objet":str,"pacmans_presents":set(str),"fantomes_presents":set(str)}}

def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """
    if "nb_lignes" in plateau:
        return plateau["nb_lignes"]
    return None


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """
    if "nb_colonnes" in plateau:
        return plateau["nb_colonnes"]
    return None


def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    return pos[0], (pos[1] - 1) % get_nb_colonnes(plateau)


def pos_est(plateau, pos):
    """retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    return pos[0], (pos[1] + 1) % get_nb_colonnes(plateau)


def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    return (pos[0] - 1) % get_nb_lignes(plateau), pos[1]


def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    return (pos[0] + 1) % get_nb_lignes(plateau), pos[1]


def pos_arrivee(plateau, pos, direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None
    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """
    if "cases" not in plateau:
        return None
    directions = const.DIRECTIONS
    arrivee = None
    if direction == directions[0]:  # Nord
        arrivee = pos_nord(plateau, pos)
    elif direction == directions[1]:  # Est
        arrivee = pos_est(plateau, pos)
    elif direction == directions[2]:  # Sud
        arrivee = pos_sud(plateau, pos)
    elif direction == directions[3]:  # Ouest
        arrivee = pos_ouest(plateau, pos)
    if arrivee in plateau["cases"]:
        return arrivee
    return None


def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """
    if "cases" not in plateau:
        return None
    if pos in plateau["cases"]:
        return plateau["cases"][pos]
    else:
        return None


def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """
    case_select = get_case(plateau, pos)
    if case is not None:
        return case.get_objet(case_select)
    return None


def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """
    case_pos = get_case(plateau, pos)
    if case_pos is not None:
        case.poser_pacman(case_pos, pacman)


def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """
    case_pos = get_case(plateau, pos)
    if case_pos is not None:
        case.poser_fantome(case_pos, fantome)


def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (str): un str représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    case_pos = get_case(plateau, pos)
    if case_pos is not None:
        case.poser_objet(case_pos, objet)


def plateau_from_str(la_chaine, complet=True):
    """Construit un plateau à partir d'une chaine de caractère contenant les informations
        sur le contenu du plateau (voir sujet)

    Args:
        la_chaine (str): la chaine de caractères décrivant le plateau

    Returns:
        dict: le plateau correspondant à la chaine. None si l'opération a échoué
    """
    return Plateau(la_chaine)


def Plateau(plan):
    """Créer un plateau en respectant le plan donné en paramètre.
        Le plan est une chaine de caractères contenant
            '#' (mur)
            ' ' (couloir)
            une lettre majuscule (un couloir peint par le joueur représenté par la lettre)

    Args:
        plan (str): le plan sous la forme d'une chaine de caractères

    Returns:
        dict: Le plateau correspondant au plan
    """
    lignes = plan.split('\n')
    nb_lignes, nb_colonnes = lignes[0].split(";")  # récupéré le nombre de lignes et le nombre de colonnes
    lignes.pop(0)
    nb_lignes = int(nb_lignes)
    nb_colonnes = int(nb_colonnes)
    cases = dict()
    for l in range(nb_lignes):
        ligne = [*lignes[l]]
        for c in range(nb_colonnes):
            case_etudiee = ligne[c]
            if case_etudiee == "#":
                cases[(l, c)] = case.Case(True)
            else:
                if case_etudiee == ' ':
                    cases[(l, c)] = case.Case(False)
                else:
                    cases[(l, c)] = case.Case(False, case_etudiee)
    pacman_offset = nb_lignes
    nb_pacmans = int(lignes[pacman_offset])
    for i in range(1, nb_pacmans + 1):
        couleur, l, c = lignes[pacman_offset + i].split(";")
        l = int(l)
        c = int(c)
        cases[(l, c)]["pacmans_presents"].add(couleur)
    fantome_offset = pacman_offset + nb_pacmans + 1
    nb_fantomes = int(lignes[fantome_offset])
    for i in range(1, nb_fantomes + 1):
        couleur, l, c = lignes[fantome_offset + i].split(";")
        l = int(l)
        c = int(c)
        cases[(l, c)]["fantomes_presents"].add(couleur)
    plat = dict()
    plat["nb_lignes"] = nb_lignes
    plat["nb_colonnes"] = nb_colonnes
    plat["cases"] = cases
    return plat


def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """
    if pos in plateau["cases"]:
        plateau["cases"][pos] = une_case


def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    case_pos = get_case(plateau, pos)
    return case.prendre_pacman(case_pos, pacman)


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    case_pos = get_case(plateau, pos)
    return case.prendre_fantome(case_pos, fantome)


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    case_pos = get_case(plateau, pos)
    return case.prendre_objet(case_pos)


def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """
    case_pos = get_case(plateau, pos)
    if pacman in case.get_pacmans(case_pos):
        deplacement = pos_arrivee(plateau, pos, direction)
        if deplacement is not None:
            case_deplacement = get_case(plateau, deplacement)
            if not case.est_mur(case_deplacement):
                enlever_pacman(plateau, pacman, pos)
                poser_pacman(plateau, pacman, deplacement)
                return deplacement
            else:
                if passemuraille and 0 <= deplacement[0] < get_nb_lignes(plateau):
                    enlever_pacman(plateau, pacman, pos)
                    poser_pacman(plateau, pacman, deplacement)
                    return deplacement
    return None


def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """
    case_pos = get_case(plateau, pos)
    if fantome in case.get_fantomes(case_pos):
        deplacement = pos_arrivee(plateau, pos, direction)
        if deplacement is not None:
            case_deplacement = get_case(plateau, deplacement)
            if not case.est_mur(case_deplacement):
                enlever_fantome(plateau, fantome, pos)
                poser_fantome(plateau, fantome, deplacement)
                return deplacement
    return None


def case_vide(plateau):
    """choisi aléatoirement sur la plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    nb_lignes = get_nb_lignes(plateau)
    nb_colonnes = get_nb_colonnes(plateau)
    choisie = (random.randint(0, nb_lignes), random.randint(0, nb_colonnes))
    case_choisie = get_case(plateau, choisie)
    while case.est_mur(case_choisie) or case.get_nb_pacmans(case_choisie) > 0 or \
            case.get_nb_fantomes(case_choisie) or case.get_objet(case_choisie) is not None:
        choisie = (random.randint(0, nb_lignes), random.randint(0, nb_colonnes))
        case_choisie = get_case(plateau, choisie)
    return choisie


def directions_possibles(plateau, pos, passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """
    directions = const.DIRECTIONS
    directions_valides = ""
    for dir in directions:
        deplacement = pos_arrivee(plateau, pos, dir)
        case_deplacement = get_case(plateau, deplacement)
        if not case.est_mur(case_deplacement) or passemuraille:
            directions_valides += dir
    return directions_valides


# ---------------------------------------------------------#

def analyse_plateau(plateau, pos, direction, distance_max):
    """calcul les distances entre la position pos est les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        direction (str): direction choisie
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """
    res = {"objets": [], "pacmans": [], "fantomes": []}
    i = 1
    prev = [pos_arrivee(plateau, pos, direction)]
    if case.est_mur(get_case(plateau, prev[0])):
        return None
    curr = []
    deja_fait = set()
    deja_fait.add(pos_arrivee(plateau, pos, direction))
    case_depart = get_case(plateau, prev[0])
    pacmans_ajouter = [(i, x) for x in case.get_pacmans(case_depart)]
    fantomes_ajouter = [(i, x) for x in case.get_fantomes(case_depart)]
    objets_ajouter = case.get_objet(case_depart)
    if objets_ajouter != const.AUCUN:
        res["objets"] = [(i, objets_ajouter)]
    res["pacmans"] = pacmans_ajouter
    res["fantomes"] = fantomes_ajouter
    while i < distance_max:
        i += 1
        for position in prev:
            dirs_possibles = directions_possibles(plateau, position)
            voisins = [pos_arrivee(plateau, position, x) for x in dirs_possibles]
            for voisin in voisins:  # 4 maximum
                if voisin not in deja_fait:
                    case_voisin = get_case(plateau, voisin)
                    deja_fait.add(voisin)
                    if case.est_mur(case_voisin):
                        break
                    pacmans = case.get_pacmans(case_voisin)
                    fantomes = case.get_fantomes(case_voisin)
                    objet = case.get_objet(case_voisin)
                    if len(pacmans) > 0:
                        for pacman in pacmans:
                            res["pacmans"].append((i, pacman))
                    if len(fantomes) > 0:
                        for fantome in fantomes:
                            res["fantomes"].append((i, fantome))
                    if objet != const.AUCUN:
                        res["objets"].append((i, objet))

                    curr.append(voisin)
        prev = curr.copy()
        curr = []
    return res


def analyse_plateau_v2(plateau, pos, direction, distance_max, passemuraille=False):
    """calcul les distances entre la position pos est les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        passmuraille:
        direction (str): direction choisie
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes.
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist, (l,c),ident) où pos est la pos de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """
    res = {"objets": [], "pacmans": [], "fantomes": []}
    i = 1
    prev = [pos_arrivee(plateau, pos, direction)]
    if case.est_mur(get_case(plateau, prev[0])):
        return res
    curr = []
    deja_fait = set()
    deja_fait.add(pos_arrivee(plateau, pos, direction))
    case_depart = get_case(plateau, prev[0])
    pacmans_ajouter = [(i, prev[0], x) for x in case.get_pacmans(case_depart)]
    fantomes_ajouter = [(i, prev[0], x) for x in case.get_fantomes(case_depart)]
    objets_ajouter = case.get_objet(case_depart)
    if objets_ajouter != const.AUCUN:
        res["objets"] = [(i, pos, objets_ajouter)]
    res["pacmans"] = pacmans_ajouter
    res["fantomes"] = fantomes_ajouter
    while i < distance_max:
        i += 1
        for position in prev:
            dirs_possibles = directions_possibles(plateau, position, passemuraille)
            voisins = [pos_arrivee(plateau, position, x) for x in dirs_possibles]
            for voisin in voisins:  # 4 maximum
                if voisin not in deja_fait:
                    case_voisin = get_case(plateau, voisin)
                    deja_fait.add(voisin)
                    if case.est_mur(case_voisin):
                        break
                    pacmans = case.get_pacmans(case_voisin)
                    fantomes = case.get_fantomes(case_voisin)
                    objet = case.get_objet(case_voisin)
                    if len(pacmans) > 0:
                        for pacman in pacmans:
                            res["pacmans"].append((i, voisin, pacman))
                    if len(fantomes) > 0:
                        for fantome in fantomes:
                            res["fantomes"].append((i, voisin, fantome))
                    if objet != const.AUCUN:
                        res["objets"].append((i, voisin, objet))

                    curr.append(voisin)
        prev = curr.copy()
        curr = []
    return res


def prochaine_intersection(plateau, pos, direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """
    trouver = False
    curr = pos_arrivee(plateau, pos, direction)
    curr_direction = direction
    i = 0
    dir_inverse = {"N": "S", "S": "N", "E": "O", "O": "E"}
    while not trouver:
        dir_possibles = directions_possibles(plateau, curr)
        dir_possibles = dir_possibles.replace(curr_direction, "")
        # dir_possibles = dir_possibles.replace(dir_inverse[curr_direction], "")
        if case.est_mur(get_case(plateau, curr)):
            return -1
        if len(dir_possibles) == 2:
            dir_possibles = dir_possibles.replace(dir_inverse[curr_direction], "")
            curr_direction = dir_possibles[0]
            curr = pos_arrivee(plateau, curr, curr_direction)
            i += 1
        elif len(dir_possibles) > 2:
            return i

        curr = pos_arrivee(plateau, curr, curr_direction)
        i += 1


def fabrique_calque(plateau, pos, passemuraille=False):
    nb_lignes = get_nb_lignes(plateau)
    nb_colonnes = get_nb_colonnes(plateau)
    plan = str(nb_lignes) + ";" + str(nb_colonnes) + "\n"
    for _ in range(nb_lignes):
        plan += " " * nb_colonnes
        plan += "\n"
    plan += "0\n"
    plan += "0\n"
    calque = Plateau(plan)
    prev = [pos]
    curr = []
    deja_fait = set()
    deja_fait.add(pos)
    poser_objet(calque, 0, pos)
    i = 0
    while len(prev) > 0:
        i += 1
        for position in prev:
            dirs_possibles = directions_possibles(plateau, position, passemuraille)
            voisins = [pos_arrivee(plateau, position, x) for x in dirs_possibles]
            for voisin in voisins:
                if voisin not in deja_fait:
                    poser_objet(calque, i, voisin)
                    curr.append(voisin)
                    deja_fait.add(voisin)
        prev = curr.copy()
        curr = []

    return calque


def distance_entre_pos(plateau, pos1, pos2, pre_calc, passemuraille=False):
    """
    Renvoie la distance entre deux positions sur un plateau à partir de calques précalculés ou calcul un nouveau calque et l'ajoute aux calques précalculés
    Si l'endroit est innacessible, on renvoie -1
    Args:
        plateau (dict): plateau etudie
        pos1 (tuple): tuple (l,c) de la position 1
        pos2 (tuple): tuple (l,c) de la position 2
        pre_calc (dict): dictionnaire sous la forme suivante: {(l,c):calque}

    Returns:
        res (int): distance entre deux positions (ou -1 si innacessible)
    """
    res = None
    if pos1 in pre_calc:
        res = get_objet(pre_calc[pos1], pos2)
    else:
        calque = fabrique_calque(plateau, pos1, passemuraille)
        pre_calc[pos1] = calque
        res = get_objet(calque, pos2)
    if res == " ":
        return -1
    return res


def fabrique_chemin(plateau, pos_dep, pos_arr, pre_calc, passemuraille=False):
    if pos_dep == pos_arr:
        return []
    if pos_dep not in pre_calc:
        print("avant calque")
        pre_calc[pos_dep] = fabrique_calque(plateau, pos_dep, passemuraille=passemuraille)
        print("après calque")
    calque = pre_calc[pos_dep]
    if get_objet(calque, pos_dep) == " ":
        return []
    position = pos_arr
    direction = ""
    dir_inverse = {"N": "S", "S": "N", "E": "O", "O": "E"}
    res = []
    i = 0
    limite = 5000
    while position != pos_dep and i < limite:
        i += 1
        voisins = [pos_arrivee(plateau, position, x) for x in directions_possibles(plateau, position,passemuraille)]
        voisins_dir = [x for x in directions_possibles(plateau, position,passemuraille)]
        for i_vois in range(len(voisins)):
            val = get_objet(calque, voisins[i_vois])
            if val != " " and int(val) < int(get_objet(calque, position)):
                position = voisins[i_vois]
                direction = dir_inverse[voisins_dir[i_vois]]
        res.append((direction, position))
    if i == limite:
        return []
    return res[::-1]


# A NE PAS DEMANDER
def plateau_2_str(plateau):
    res = str(get_nb_lignes(plateau)) + ";" + str(get_nb_colonnes(plateau)) + "\n"
    pacmans = []
    fantomes = []
    for lig in range(get_nb_lignes(plateau)):
        ligne = ""
        for col in range(get_nb_colonnes(plateau)):
            la_case = get_case(plateau, (lig, col))
            if case.est_mur(la_case):
                ligne += "#"
                les_pacmans = case.get_pacmans(la_case)
                for pac in les_pacmans:
                    pacmans.append((pac, lig, col))
            else:
                obj = case.get_objet(la_case)
                les_pacmans = case.get_pacmans(la_case)
                les_fantomes = case.get_fantomes(la_case)
                ligne += str(obj)
                for pac in les_pacmans:
                    pacmans.append((pac, lig, col))
                for fantome in les_fantomes:
                    fantomes.append((fantome, lig, col))
        res += ligne + "\n"
    res += str(len(pacmans)) + '\n'
    for pac, lig, col in pacmans:
        res += str(pac) + ";" + str(lig) + ";" + str(col) + "\n"
    res += str(len(fantomes)) + "\n"
    for fantome, lig, col in fantomes:
        res += str(fantome) + ";" + str(lig) + ";" + str(col) + "\n"
    return res

"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module case.py
        Ce module contient l'implémentation des cases du plateau de jeu
"""
import const


# case = {"mur":bool,"objet":str,"pacmans_presents":set(str),"fantomes_presents":set(str)}
# exemple: Case(False,const.VALEUR,{"A","B"},{"c"})
def Case(mur=False, objet=const.AUCUN, pacmans_presents=None, fantomes_presents=None):
    """Permet de créer une case du plateau

    Args:
        mur (bool, optional): un booléen indiquant si la case est un mur ou un couloir.
                Defaults to False.
        objet (str, optional): un caractère indiquant l'objet qui se trouve sur la case.
                const.AUCUN indique qu'il n'y a pas d'objet sur la case. Defaults to const.AUCUN.
        pacmans_presents (set, optional): un ensemble indiquant la liste des pacmans
                se trouvant sur la case. Defaults to None.
        fantomes_presents (set, optional): un ensemble indiquant la liste des fantomes
                se trouvant sur la case. Defaults to None.

    Returns:
        dict: un dictionnaire représentant une case du plateau
    """
    case = dict()
    case["mur"] = mur
    case["objet"] = objet
    case["pacmans_presents"] = pacmans_presents if pacmans_presents is not None else set()
    case["fantomes_presents"] = fantomes_presents if fantomes_presents is not None else set()
    return case


def est_mur(case):
    """indique si la case est un mur ou non

    Args:
        case (dict): la case considérée

    Returns:
        bool: True si la case est un mur et False sinon
    """
    if "mur" in case:
        return case["mur"]
    return None


def get_pacmans(case):
    """retourne l'ensemble des pacmans qui sont sur la case

    Args:
        case (dict): la case considérée

    Returns:
        set: l'ensemble des identifiants de pacmans présents su la case.
    """
    if "pacmans_presents" in case:
        return case["pacmans_presents"]
    return None


def get_fantomes(case):
    """retourne l'ensemble des fantomes qui sont sur la case

    Args:
        case (dict): la case considérée

    Returns:
        set: l'ensemble des identifiants de fantomes présents su la case.
    """
    if "fantomes_presents" in case:
        return case["fantomes_presents"]
    return None


def get_nb_pacmans(case):
    """retourne le nombre de pacmans présents sur la case

    Args:
        case (dict): la case considérée

    Returns:
        int: le nombre de pacmans présents sur la case.
    """
    if "pacmans_presents" in case:
        return len(case["pacmans_presents"])
    return None


def get_nb_fantomes(case):
    """retourne le nombre de fantomes présents sur la case

    Args:
        case (dict): la case considérée

    Returns:
        int: le nombre de fantomes présents sur la case.
    """
    if "fantomes_presents" in case:
        return len(case["fantomes_presents"])
    return None


def get_objet(case):
    """retourne l'objet qui est sur la case.
        Si aucun objet ne s'y trouve la fonction retourne const.AUCUN

    Args:
        case (dict): la case considérée
    """
    if "objet" in case:
        return case["objet"]
    return None


def poser_objet(case, objet):
    """Pose un objet sur la case. Si un objet était déjà présent ce dernier disparait.
        Si la case est un mur, l'objet n'est pas mis dans la case.

    Args:
        case (dict): la case considérée
        objet (str): identifiant d'objet. const.AUCUN indiquant que plus aucun objet se
                trouve sur la case.
    """
    if "objet" in case and not est_mur(case):
        case["objet"] = objet


def prendre_objet(case):
    """Enlève l'objet qui se trouve sur la case et retourne l'identifiant de cet objet.
        Si aucun objet se trouve sur la case la fonction retourne const.AUCUN.

    Args:
        case (dict): la case considérée

    Returns:
        char: l'identifiant de l'objet qui se trouve sur la case.
    """
    if "objet" in case:
        objet = get_objet(case)
        if objet != const.AUCUN:
            poser_objet(case,const.AUCUN)
        return objet


def poser_pacman(case, pacman):
    """Pose un nouveau pacman sur la case.
    Si le pacman était déjà sur la case la fonction ne fait rien
    Si la case est un mur, le pacman est quand-même posé (pouvoir de passe-muraille)

    Args:
        case (dict): la case considérée
        pacman (str): identifiant du pacman à ajouter sur la case
    """
    if "pacmans_presents" in case:
        pacmans_presents = case["pacmans_presents"]
        if pacman not in pacmans_presents:
            pacmans_presents.add(pacman)


def prendre_pacman(case, pacman):
    """Enlève le pacman dont l'identifiant est passé en paramètre de la case.
        La fonction retourne True si le joueur était bien sur la case et False sinon.

    Args:
        case (dict): la case considérée
        pacman (str): l'identifiant du pacman à enlever

    Returns:
        bool: True si le joueur était bien sur la case et False sinon.
    """
    if "pacmans_presents" in case:
        pacmans_presents = case["pacmans_presents"]
        if pacman in pacmans_presents:
            pacmans_presents.remove(pacman)
            return True
        return False
    return None


def poser_fantome(case, fantome):
    """Pose un nouveau fantome sur la case
        si le fantome était déjà sur la case, la fonction ne fait rien
        si la case est un mur la fonction ne fait rien

    Args:
        case (dict): la case considérée
        fantome (str): identifiant du fantome à ajouter sur la case
    """
    if "fantomes_presents" in case and est_mur(case) is not None:
        fantomes_presents = case["fantomes_presents"]
        if fantome not in fantomes_presents and not est_mur(case):
            fantomes_presents.add(fantome)


def prendre_fantome(case, fantome):
    """Enlève le fantome dont l'identifiant est passé en paramètre de la case.
        La fonction retourne True si le fantome était bien sur la case et False sinon.

    Args:
        case (dict): la case considérée
        fantome (str): l'identifiant du fantome à enlever

    Returns:
        bool: True si le fantome était bien sur la case et False sinon.
    """
    if "fantomes_presents" in case:
        fantomes_presents = case["fantomes_presents"]
        if fantome in fantomes_presents:
            fantomes_presents.remove(fantome)
            return True
        return False
    return None

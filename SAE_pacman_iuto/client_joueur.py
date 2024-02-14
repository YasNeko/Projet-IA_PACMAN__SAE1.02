# coding: utf-8
"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module client_joueur.py
        Ce module contient le programme principal d'un joueur
        il s'occupe des communications avec le serveur
            - envois des ordres
            - recupération de l'état du jeu
        la fonction mon_IA est celle qui contient la stratégie de
        jeu du joueur.

"""
import argparse
import random
import client
import const
import plateau
import case
import joueur

prec = 'X'
last_dir = "N"


def fuir_fantome(le_plateau, pos_fantome, pos_pacman, passemuraille):
    """
    Détermine la direction dans laquelle le pacman doit se déplacer pour fuir le fantome.

    Args:
        le_plateau: L'état actuel du plateau de jeu.
        pos_fantome: La position actuelle du pacman.
        pos_pacman: La position actuelle du fantome ennemi.
        passemuraille: Booléen indiquant si le pacman peut passer à travers les murs.

    Returns:
        str: La direction dans laquelle le pacman doit se déplacer pour fuir.
    """
    directions_possibles = plateau.directions_possibles(le_plateau, pos_pacman, passemuraille)
    distance_max = -1
    direction_fuite = None

    for direction in directions_possibles:
        pos_future = plateau.pos_arrivee(le_plateau, pos_pacman, direction)
        distance = plateau.distance_entre_pos(le_plateau, pos_future, pos_fantome, dict(), passemuraille)

        if distance > distance_max:
            distance_max = distance
            direction_fuite = direction

    return direction_fuite if direction_fuite else random.choice(directions_possibles)

def direction_pacman_bete(plat, joueurs, couleur):
    precalc = dict()
    joueur = joueurs[couleur]  # Recuperer notre joueur
    pos = joueur["pos_pacman"]  # Recuperer la position de notre pacman
    passemuraille = joueur["objets"][const.PASSEMURAILLE] > 0
    glouton = joueur["objets"][const.GLOUTON] > 0

    dirs_possibles = plateau.directions_possibles(plat, pos, passemuraille)
    if len(dirs_possibles) == 0:
        return "N"
    analyse = plateau.analyse_plateau_v2(plat, pos, dirs_possibles[0],
                                         100, passemuraille)  # Analyser le plateau

    dir_inverse = {"N": "S", "S": "N", "E": "O", "O": "E"}
    objets = analyse["objets"]  # Recupère les objets issus de l'analyse
    objets = [x for x in objets if x[2] != const.VITAMINE]  # Retire toutes les vitamines
    fantomes = analyse["fantomes"]  # Recupère les fantomes issus de l'analyse

    objets = sorted(objets, key=lambda x: x[0])  # Filtrer les objets par leur distance (du plus proche au plus loins)
    fantomes = sorted(fantomes,
                      key=lambda x: x[0])  # Filtrer les fantomes par leur distance (du plus proche au plus loins)
    fantomes = [item for item in fantomes if item[2] != couleur]  # on retire notre fantome
    target = None
    fuite = False
    if len(objets) != 0:
        if len(fantomes) != 0:
            if objets[0][0] < fantomes[0][0]:
                target = objets[0]
            else:
                target = fantomes[0]
                fuite = True
        else:
            target = objets[0]
    elif len(fantomes) != 0:
        target = fantomes[0]
        fuite = True
    if target is None:
        return random.choice(dirs_possibles)
    chemin_target = plateau.fabrique_chemin(plat, pos, target[1], precalc, passemuraille)
    premieres_positions = {chemin_target[i][1] for i in range(len(chemin_target) if len(chemin_target) < 3 else 3)}
    for fantome in fantomes:
        if fantome[1] in premieres_positions or plateau.distance_entre_pos(plat, pos, fantome[1], dict()) < 3:
            fuite = True
            target = fantome
            break
    chemin_target = plateau.fabrique_chemin(plat, pos, target[1], precalc, passemuraille)
    if len(chemin_target) == 0:
        if len(objets) > 0:
            chemins = [plateau.fabrique_chemin(plat, pos, objets[i][1], precalc, passemuraille) for i in
                       range(len(objets))]
            chemins = [elem for elem in chemins if len(elem) != 0]
            chemins = sorted(chemins, key=len)
            if len(chemins) == 0:
                for direc in dirs_possibles:
                    arrivee = plateau.pos_arrivee(plat, pos, direc)
                    if arrivee == objets[0][1]:
                        return direc
                return random.choice(dirs_possibles)
            else:
                return chemins[0][0][0]
        elif len(fantomes) > 0:
            direction = fuir_fantome(plat, fantomes[0][1], pos, passemuraille)
            return direction
        else:
            return random.choice(dirs_possibles)
    dir_choisie = chemin_target[0][0]
    if glouton:
        fuite = False
    if fuite:
        return fuir_fantome(plat, target[1], pos, passemuraille)
    else:
        return dir_choisie


def determiner_direction_fantome(le_plateau, pos_fantome, ma_position_pacman, ma_couleur, joueurs):
 
    # Fabrique le chemin vers le pacman le plus proche
    Get_pacman_proche = plateau.analyse_plateau_v2(le_plateau, pos_fantome,
                                                   random.choice(plateau.directions_possibles(le_plateau, pos_fantome)),
                                                   100)

    liste_pacman_possible = Get_pacman_proche["pacmans"]
    # Trie en fonction de la distance
    liste_trier_pacman = sorted(liste_pacman_possible)
    # Selection du pacman cible a focus
    pacman_cible = None
    for pacman in liste_trier_pacman:
        if pacman[2] != ma_couleur and not joueurs[pacman[2]]["objets"][const.PASSEMURAILLE] > 0:
            pacman_cible = pacman
            break
        if pacman[2] != ma_couleur and joueurs[pacman[2]]["objets"][const.GLOUTON] > 0:
            pacman_glouton = pacman
            if (plateau.distance_entre_pos(le_plateau, pos_fantome, pacman_glouton[1], dict())) <= 2 and joueurs[pacman_glouton[2]]["objets"][const.GLOUTON] > 1:
                return fuir_pacman(le_plateau, pos_fantome, pacman_glouton[1])
            elif joueurs[pacman_glouton[2]]["objets"][const.GLOUTON] > 1:
                chemin = plateau.fabrique_chemin(le_plateau, pos_fantome, pacman_glouton[1], dict())
                return chemin[0][0]

    # Si aucun pacman approprie n'est trouve,choisit une direction aleatoire
    if pacman_cible is None:
        return random.choice(plateau.directions_possibles(le_plateau, pos_fantome))
    # Calculer le chemin vers le Pacman cible
    pos_enemie = pacman_cible[1]
    chemin = plateau.fabrique_chemin(le_plateau, pos_fantome, pos_enemie, dict())
    if len(chemin) == 0:
        return random.choice(plateau.directions_possibles(le_plateau, pos_fantome))
    # fait une liste des objets les plus proche sans les vitamine
    objet_possible = plateau.analyse_plateau_v2(le_plateau, pos_fantome, chemin[0][0], 100)
    liste_objet_possible = objet_possible["objets"]
    liste_trier_objet = sorted(liste_objet_possible)
    trier_objet_withoutvitamine = [item for item in liste_trier_objet if item[2] != const.VITAMINE]
    return Quel_item_focus(trier_objet_withoutvitamine, pos_fantome, chemin, le_plateau)


def fuir_pacman(le_plateau, pos_fantome, pos_pacman):
    """
    Détermine la direction dans laquelle le fantôme doit se déplacer pour fuir le Pacman.

    Args:
        le_plateau: L'état actuel du plateau de jeu.
        pos_fantome: La position actuelle du fantôme.
        pos_pacman: La position actuelle du Pacman ennemi.

    Returns:
        str: La direction dans laquelle le fantôme doit se déplacer pour fuir.
    """
    directions_possibles = plateau.directions_possibles(le_plateau, pos_fantome)
    distance_max = -1
    direction_fuite = None

    for direction in directions_possibles:
        pos_future = plateau.pos_arrivee(le_plateau, pos_fantome, direction)
        distance = plateau.distance_entre_pos(le_plateau, pos_future, pos_pacman, dict())
        if distance > distance_max:
            distance_max = distance
            direction_fuite = direction
    return direction_fuite if direction_fuite else random.choice(directions_possibles)


def Quel_item_focus(Objet_proche_sans_Vitamine, pos_fantome, chemin, le_plateau):
    # Verifie au alentour si y a des objet groupée proche du fantome
    objet_proche = False
    for i in range(1, len(Objet_proche_sans_Vitamine) - 1):
        distance_precedent = Objet_proche_sans_Vitamine[i - 1][1]
        distance_actuel = Objet_proche_sans_Vitamine[i][1]
        distance_prochaine= Objet_proche_sans_Vitamine[i+1][1]
        Objets_pack_TROIS= (plateau.distance_entre_pos(le_plateau, distance_precedent, distance_actuel, dict()) <=2) and (plateau.distance_entre_pos(le_plateau, distance_actuel, distance_prochaine, dict()) <=2)
        Objets_pack_DEUX= plateau.distance_entre_pos(le_plateau, distance_precedent, distance_actuel, dict()) <=2
        Objet_Cerise= Objet_proche_sans_Vitamine[i - 1][2] == const.VALEUR
        if Objets_pack_TROIS or Objets_pack_DEUX:
            objet_target = Objet_proche_sans_Vitamine[i-1][1]  # ptet un probleme futur
            objet_proche = True
            break  # Arrêter la boucle une fois qu'un groupe est trouvé

    # A trouver des objets groupée proche de lui & crée un chemin vers celuit ci
    if objet_proche is True:
        chemin = plateau.fabrique_chemin(le_plateau, pos_fantome, objet_target, dict())
        if pos_fantome == objet_target:
            # Lance le mode Campouse, reste a cotée des objets jusqu'a que le pacman vient les récuperer
            return Campouse(le_plateau, pos_fantome, objet_target)
        return chemin[0][0]
    return chemin[0][0]
        
        
def Campouse(le_plateau, pos_fantome, objet_target):
    if pos_fantome == objet_target:
        return random.choice(plateau.directions_possibles(le_plateau, pos_fantome))
    else:
        chemin = plateau.fabrique_chemin(le_plateau, pos_fantome, objet_target, dict())
        return chemin[0][0]


def mon_IA(ma_couleur, carac_jeu, plan, les_joueurs):
    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du jeur
        carac_jeu (str): une chaine de caractères contenant les caractéristiques
                                   de la partie séparées par des ;
             duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet
        plan (str): le plan du plateau comme comme indiqué dans le sujet
        les_joueurs (str): le liste des joueurs avec leur caractéristique (1 joueur par ligne)
        couleur;reserve;objet;duree_objet;ligne;colonne;nom_complet
    
    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement
    """
    # decodage des informations provenant du serveur
    joueurs = {}
    for ligne in les_joueurs.split('\n'):
        lejoueur = joueur.joueur_from_str(ligne)
        joueurs[joueur.get_couleur(lejoueur)] = lejoueur
    le_plateau = plateau.Plateau(plan)
    precalc = None
    # simu = simulateur.Simulateur(le_plateau,joueurs,ma_couleur,carac_jeu, 0,precalc)
    dir_p = direction_pacman_bete(le_plateau, joueurs, ma_couleur)
    if dir_p is None:
        dirs_p = plateau.directions_possibles(le_plateau, joueurs[ma_couleur]["pos_pacman"],
                                              joueurs[ma_couleur]["objets"][const.PASSEMURAILLE] > 0)
        dir_p = random.choice(dirs_p)
    # IA complètement aléatoire
    # dir_p = random.choice("NESO")
        
    dir_f = determiner_direction_fantome(le_plateau, joueurs[ma_couleur]["pos_fantome"],
                                         joueurs[ma_couleur]["pos_pacman"], ma_couleur, joueurs)
    
    return dir_p + dir_f


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)

    args = parser.parse_args()
    le_client = client.ClientCyber()
    le_client.creer_socket(args.serveur, args.port)
    le_client.enregistrement(args.nom_equipe, "joueur")
    ok = True
    while ok:
        ok, id_joueur, le_jeu = le_client.prochaine_commande()
        if ok:
            carac_jeu, le_plateau, les_joueurs = le_jeu.split("--------------------\n")
            actions_joueur = mon_IA(id_joueur, carac_jeu, le_plateau, les_joueurs[:-1])
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")

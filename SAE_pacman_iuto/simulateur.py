import random

import plateau
import case
import joueur
import const

NB_SIMULATIONS = 5


class Simulateur:
    def __init__(self, plat, joueurs, couleur, carac_jeu, iteration=0, precalc=None):
        if precalc is None:
            precalc = dict()
        self.couleur = couleur
        self.joueurs = joueurs
        # {"couleur":str,"nom":str,"nb_pooints":int,"nb_faux_mvt":int,"pos_pacman":tuple,"pos_fantome":tuple,
        # "objets":{"$":int,"@":int,"~":int}}
        self.plat_dep = plat
        self.plat_simul = plat
        self.carac_jeu = carac_jeu
        # duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet
        self.iteration = iteration
        self.precalc = precalc
        # {(l,c):calque}

    def simulate(self):
        plateau_etudie = self.plat_simul

    def update(self, plat, joueurs, carac_jeu, positions):
        self.plat_dep = plat
        self.plat_simul = plat
        self.joueurs = joueurs
        self.carac_jeu = carac_jeu
        self.iteration = 0


def pre_analyser(plat, joueurs):
    couleurs = joueurs.keys()
    analyse = dict()
    for couleur in couleurs:
        pos_pacman = joueurs[couleur]["pos_pacman"]
        pos_fantome = joueurs[couleur]["pos_fantome"]
        directions_pac = plateau.directions_possibles(plat, pos_pacman,
                                                      joueurs[couleur]["objets"][const.PASSEMURAILLE] > 0)
        directions_fant = plateau.directions_possibles(plat, pos_fantome)
        analyse[couleur] = dict()
        analyse[couleur]["p"] = dict()
        analyse[couleur]["f"] = dict()
        for dir in directions_pac:
            analyse[couleur]["p"][dir] = plateau.analyse_plateau_v2(plat, pos_pacman, dir, 4)
        for dir in directions_fant:
            analyse[couleur]["f"][dir] = plateau.analyse_plateau_v2(plat, pos_fantome, dir, 4)
    return analyse
    # analyse[couleur]["p"/"f"][dir] = {"objets": [(i,(l,c),id)], "pacmans": [(i,(l,c),id)], "fantomes": [(i,(l,c),id)]}


def choisi_direction(stats):
    directions = stats.keys()


def direction_pacman_bete_old(plat, joueurs, couleur, pre_analyse=None):
    joueur = joueurs[couleur]
    pos = joueur["pos_pacman"]
    directions = plateau.directions_possibles(plat, pos, joueur["objets"][const.PASSEMURAILLE] > 0)
    glouton = joueur["objets"][const.GLOUTON] > 0
    if pre_analyse is None:
        analyses = pre_analyser(plat, joueurs)
        pre_analyse = analyses
    analyses = pre_analyse[couleur]["p"]
    # analyses["A"]["p"]["N"] = {"objets": [(2,(5,6),"@"], "pacmans": [], "fantomes": []}
    stats = dict()
    for dir in directions:
        proch_inter = plateau.prochaine_intersection(plat, pos, dir)
        if proch_inter == -1:
            break
        nb_objets = len(analyses[dir]["objets"])
        nb_fantomes = len(analyses[dir]["fantomes"])
        if len(analyses[dir]["objets"]) > 0:
            min_dist_objet = min(analyses[dir]["objets"], key=lambda x: x[0])[0]
            max_dist_objet = max(analyses[dir]["objets"], key=lambda x: x[0])[0]
        else:
            min_dist_objet = 0
            max_dist_objet = 0
        if len(analyses[dir]["fantomes"]) > 0:
            min_dist_fantome = min(analyses[dir]["fantomes"], key=lambda x: x[0])[0]
            mas_dist_fantome = max(analyses[dir]["fantomes"], key=lambda x: x[0])[0]
        else:
            min_dist_fantome = 0
            max_dist_fantome = 0
        if min_dist_fantome > proch_inter:
            return dir
        if max_dist_objet < proch_inter:
            return dir

    return random.choice(directions)



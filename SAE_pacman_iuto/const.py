"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module const.py
        Ce module contient les constantes du jeu
"""
AUCUN = ' '
VITAMINE = '.'
GLOUTON = '$'
IMMOBILITE = '@'
PASSEMURAILLE = '~'
VALEUR = '&'
TELEPORTATION = '!'
NB_OBJETS = 6
LES_OBJETS = '.$@~&!'

DIRECTIONS = 'NESO'

NB_FAUX_MVT = 4
PENALITE = 1

DIST_MAX = 5

PROP_OBJET = {VITAMINE: (3, 0), GLOUTON: (50, 20), IMMOBILITE: (50, 10),
              PASSEMURAILLE: (50, 20), VALEUR: (100, 0), TELEPORTATION: (50, 0)}

POINTS_BATAILLE = 20


def aucun_objet():
    return {GLOUTON: 0, IMMOBILITE: 0, PASSEMURAILLE: 0}

"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module affichage.py
        Ce module contient l'afficheur du jeu en réseau.
"""

import pygame
import argparse
import os
import sys
import threading
import jeu_res as jeu
import client
import const


class JeuGraphique(object):
    """Classe simple d'affichage et d'interaction pour le labyrinthe."""

    def __init__(self, lecteur_jeu, nom_partie, titre="Pacman'IUT'O", size=(3000, 1600),
                 couleur=(209, 238, 238),
                 prefixe_image="./images"):
        """Method docstring."""
        self.lecteur_jeu = lecteur_jeu
        self.jeu = lecteur_jeu.get_jeu()
        self.nom_partie = nom_partie
        self.sauve = False
        self.message_info = None
        self.img_info = []
        self.fini = False
        self.couleur_texte = couleur
        self.plateau = self.jeu.plateau
        self.nb_lignes = jeu._fonction_33(self.plateau)
        self.nb_colonnes = jeu._fonction_34(self.plateau)
        self.couleur_texte = couleur
        self.titre = titre
        self.images_pacmans = {}
        self.images_fantomes = {}
        self.images_objets = {}
        self.surf_pacmans = {}
        self.surf_fantomes = {}
        self.surf_objets = {}
        self.surf_objets_min = {}
        self.icone = None
        self.hauteur = 0
        self.largeur = 0
        self.delta = 0
        self.finh = 0
        self.finl = 0
        self.taille_font = 0
        self.path_font = pygame.font.match_font("courier", True)
        self.get_images(prefixe_image)
        pygame.init()
        pygame.display.set_icon(self.icone)
        pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.maj_parametres()

    def get_images(self, prefixe_image="./images"):
        codage = "ABCDEFGH"
        for code in codage:
            if os.path.isfile(os.path.join(prefixe_image, 'fant' + code + '.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'fant' + code + '.png'))
                print('fant' + code + '.png')
            else:
                s = None
            self.images_fantomes[code.lower()] = s
            if os.path.isfile(os.path.join(prefixe_image, 'pac' + code + '.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'pac' + code + '.png'))
                print('pac' + code + '.png')
            else:
                s = None
            self.images_pacmans[code] = s

        for i in range(7):
            if os.path.isfile(os.path.join(prefixe_image, 'tresor' + str(i) + '.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'tresor' + str(i) + '.png'))
            else:
                s = None
            print('tresor' + str(i) + '.png')
            self.images_objets[const.LES_OBJETS[i - 1]] = s

        # lecture du logo de l'IUT'O
        icone_img = pygame.image.load(os.path.join(prefixe_image, 'logo.jpeg'))
        self.icone = pygame.transform.smoothscale(icone_img, (50, 50))

    def maj_surfaces(self, dico_entree, dico_sortie, taille):
        for (cle, img) in dico_entree.items():
            dico_sortie[cle] = pygame.transform.smoothscale(img, (taille, taille))

    def maj_parametres(self):
        """
        permet de mettre à jour les paramètres d'affichage en cas de redimensionnement de la fenêtre
        """
        self.surface = pygame.display.get_surface()
        self.hauteur = self.surface.get_height()
        self.largeur = self.surface.get_width()
        deltav = self.hauteur // (jeu._fonction_33(self.plateau) + 2)
        deltah = self.largeur // (jeu._fonction_34(self.plateau) + 12)
        self.delta = min(deltah, deltav)
        taille = round(self.delta * .8, 0)
        self.epaisseur = 8  # self.delta//10
        self.taille_font = int(round(self.delta * .7, 0))  # self.delta
        self.maj_surfaces(self.images_fantomes, self.surf_fantomes, taille)
        self.maj_surfaces(self.images_pacmans, self.surf_pacmans, taille)
        self.maj_surfaces(self.images_objets, self.surf_objets, taille)
        self.maj_surfaces(self.images_objets, self.surf_objets_min, taille // 2)

    def dessiner_case2(self, la_case, lin, col, voisinage, coul_bord=(131, 0, 101), coul_fond=None):
        x = col * self.delta + 20
        y = lin * self.delta + 20
        quart = self.delta // 4
        rayon = quart + 3
        demi = self.delta // 2
        fond = coul_fond != None
        if not jeu._fonction_2(la_case):
            return

        dessiner = False
        for v in voisinage:
            if not v:
                dessiner = True
                break

        if not dessiner:
            if fond:
                pygame.draw.rect(self.surface, coul_fond, (x, y, self.delta, self.delta))
            return

        # coin haut-gauche
        if voisinage[0]:
            if voisinage[1] and not voisinage[3]:
                pygame.draw.line(self.surface, coul_bord, (x + quart, y),
                                 (x + quart, y + demi), self.epaisseur)
            elif voisinage[3] and not voisinage[1]:
                pygame.draw.line(self.surface, coul_bord, (x, y + quart),
                                 (x + demi, y + quart), self.epaisseur)
        else:
            if voisinage[1] and voisinage[3]:
                pygame.draw.circle(self.surface, coul_bord, (x, y),
                                   rayon + 2, self.epaisseur, draw_bottom_right=True)
            elif voisinage[1]:
                pygame.draw.line(self.surface, coul_bord, (x + quart, y),
                                 (x + quart, y + demi), self.epaisseur)
            elif voisinage[3]:
                pygame.draw.line(self.surface, coul_bord, (x, y + quart),
                                 (x + demi, y + quart), self.epaisseur)
            else:
                pygame.draw.circle(self.surface, coul_bord, (x + demi, y + demi),
                                   rayon, self.epaisseur, draw_top_left=True)

        # coin haut-droit
        if voisinage[2]:
            if voisinage[1] and not voisinage[4]:
                pygame.draw.line(self.surface, coul_bord, (x + 3 * quart - 1, y),
                                 (x + 3 * quart - 1, y + demi), self.epaisseur)
            elif voisinage[4] and not voisinage[1]:
                pygame.draw.line(self.surface, coul_bord, (x + demi, y + quart),
                                 (x + self.delta, y + quart), self.epaisseur)
        else:
            if voisinage[1] and voisinage[4]:
                pygame.draw.circle(self.surface, coul_bord, (x + self.delta, y),
                                   rayon + 2, self.epaisseur, draw_bottom_left=True)
            elif voisinage[1]:
                pygame.draw.line(self.surface, coul_bord, (x + 3 * quart - 1, y),
                                 (x + 3 * quart - 1, y + demi), self.epaisseur)
            elif voisinage[4]:
                pygame.draw.line(self.surface, coul_bord, (x + demi, y + quart),
                                 (x + self.delta, y + quart), self.epaisseur)
            else:
                pygame.draw.circle(self.surface, coul_bord, (x + demi, y + demi),
                                   rayon, self.epaisseur, draw_top_right=True)

        # coin bas-droit
        if voisinage[7]:
            if voisinage[6] and not voisinage[4]:
                pygame.draw.line(self.surface, coul_bord, (x + 3 * quart - 1, y + self.delta),
                                 (x + 3 * quart - 1, y + demi), self.epaisseur)
            elif voisinage[4] and not voisinage[6]:
                pygame.draw.line(self.surface, coul_bord, (x + demi, y + 3 * quart - 1),
                                 (x + self.delta, y + 3 * quart - 1), self.epaisseur)
        else:
            if voisinage[6] and voisinage[4]:
                pygame.draw.circle(self.surface, coul_bord, (x + self.delta, y + self.delta),
                                   rayon + 2, self.epaisseur, draw_top_left=True)
            elif voisinage[6]:
                pygame.draw.line(self.surface, coul_bord, (x + 3 * quart - 1, y + self.delta),
                                 (x + 3 * quart - 1, y + demi), self.epaisseur)
            elif voisinage[4]:
                pygame.draw.line(self.surface, coul_bord, (x + demi, y + 3 * quart - 1),
                                 (x + self.delta, y + 3 * quart - 1), self.epaisseur)
            else:
                pygame.draw.circle(self.surface, coul_bord, (x + demi, y + demi),
                                   rayon, self.epaisseur, draw_bottom_right=True)

        # coin bas-gauche
        if voisinage[5]:
            if voisinage[6] and not voisinage[3]:
                pygame.draw.line(self.surface, coul_bord, (x + quart, y + self.delta),
                                 (x + quart, y + demi), self.epaisseur)
            elif voisinage[3] and not voisinage[6]:
                pygame.draw.line(self.surface, coul_bord, (x + demi, y + 3 * quart - 1),
                                 (x, y + 3 * quart - 1), self.epaisseur)
        else:
            if voisinage[6] and voisinage[3]:
                pygame.draw.circle(self.surface, coul_bord, (x, y + self.delta),
                                   rayon + 2, self.epaisseur, draw_top_right=True)
            elif voisinage[6]:
                pygame.draw.line(self.surface, coul_bord, (x + quart, y + self.delta),
                                 (x + quart, y + demi), self.epaisseur)
            elif voisinage[3]:
                pygame.draw.line(self.surface, coul_bord, (x + demi, y + 3 * quart - 1),
                                 (x, y + 3 * quart - 1), self.epaisseur)
            else:
                pygame.draw.circle(self.surface, coul_bord, (x + demi, y + demi),
                                   rayon, self.epaisseur, draw_bottom_left=True)

    def dessiner_plateau(self, le_plateau):
        self.surface.fill((0, 0, 0))
        for ligne in range(jeu._fonction_33(le_plateau)):
            for colonne in range(jeu._fonction_34(le_plateau)):
                voisinage = jeu._fonction_59(le_plateau, (ligne, colonne))
                self.dessiner_case2(jeu._fonction_40(le_plateau, (ligne, colonne)),
                                    ligne, colonne, voisinage)

    def surface_case(self, la_case):
        """
        transforme une case en une surface (image 2D) avec les pions et trésor associés
        """
        pacmans = jeu._fonction_4(la_case)
        fantomes = jeu._fonction_5(la_case)
        objet = jeu._fonction_8(la_case)
        surf_carte = pygame.Surface((self.delta, self.delta))
        dist = 5
        coord = [(dist, dist), (dist, self.delta - (self.delta // 2 + dist)),
                 (self.delta - (self.delta // 2 + dist), self.delta - (self.delta // 2 + dist)),
                 (self.delta - (self.delta // 2 + dist), dist), (self.delta // 4 + dist, dist),
                 (self.delta // 4 + dist, self.delta - (self.delta // 2 + dist))]

        if objet != ' ':
            surf_carte.blit(self.surf_objets[objet], (self.delta // 4, self.delta // 4))
        for pac in pacmans:
            surf_carte.blit(self.surf_pacmans[pac], coord.pop(0))
        for fant in fantomes:
            surf_carte.blit(self.surf_fantomes[fant], coord.pop(0))
        return surf_carte

    def dessiner_contenu(self):
        self.dessiner_plateau(self.plateau)
        for lig in range(self.nb_lignes):
            for col in range(self.nb_colonnes):
                la_case = jeu._fonction_40(self.plateau, (lig, col))
                if not jeu._fonction_2(la_case):
                    self.surface.blit(self.surface_case(la_case),
                                      (col * self.delta + 20, lig * self.delta + 20))
                else:
                    voisinage = jeu._fonction_59(self.plateau, (lig, col))
                    self.dessiner_case2(jeu._fonction_40(self.plateau, (lig, col)),
                                        lig, col, voisinage)
                    if len(jeu._fonction_4(la_case)) > 0:
                        for pac in jeu._fonction_4(la_case):
                            self.surface.blit(self.surf_pacmans[pac],
                                              (col * self.delta + 20, lig * self.delta + 20))

    def affiche_message(self, ligne, texte, images=[], couleur=None):
        """
        affiche un message en mode graphique à l'écran
        """
        posx = (self.nb_colonnes + 1) * self.delta + 30
        posy = ligne * self.delta + 20

        font = pygame.font.Font(self.path_font, self.taille_font)
        if couleur is None:
            couleur = self.couleur_texte
        liste_textes = texte.split('@img@')
        for msg in liste_textes:
            if msg != '':
                texte = font.render(msg, True, couleur)
                textpos = texte.get_rect()
                textpos.y = posy
                textpos.x = posx
                self.surface.blit(texte, textpos)
                posx += textpos.width
            if images != []:
                surface = pygame.transform.smoothscale(images.pop(0),
                                                       (round(self.taille_font * 1.5), round(self.taille_font * 1.5)))
                debuty = posy - (self.taille_font // 2)
                self.surface.blit(surface, (posx, debuty))
                posx += surface.get_width()

    def affiche_joueurs(self, ligne, couleur=None):
        font = pygame.font.Font(self.path_font, self.taille_font)
        if couleur is None:
            couleur = self.couleur_texte
        posx = (self.nb_colonnes + 1) * self.delta + 30
        posy = ligne * self.delta + 20

        classement = self.jeu.classement()
        for le_joueur in classement:
            nom = jeu._fonction_18(le_joueur)
            points = jeu._fonction_19(le_joueur)
            contenu = "{} {}"
            surfp = self.surf_pacmans[jeu._fonction_17(le_joueur)]
            self.surface.blit(surfp, (posx, posy))
            nb_obj = -1
            for un_obj in jeu._fonction_21(le_joueur):
                self.surface.blit(self.surf_objets_min[un_obj],
                                  (posx - self.delta // 2, posy + (nb_obj * self.delta // 2)))
                nb_obj += 1
            texte = font.render(
                contenu.format(nom[:15].ljust(15), str(points).rjust(5)), True,
                couleur)
            textpos = texte.get_rect()
            textpos.y = posy
            textpos.x = posx + surfp.get_width() + 3
            self.surface.blit(texte, textpos)
            textpos.x += texte.get_width()
            textpos.y = posy - self.delta // 3
            # self.surface.blit(surfo, textpos)
            posy += texte.get_height() * 2

    def affiche_message_info(self, num_ligne=4):
        """
        affiche un message d'information aux joueurs
        """
        if self.message_info is not None:
            self.affiche_message(num_ligne, self.message_info, self.img_info)
        self.img_info = []
        pygame.display.flip()

    def affiche_info(self):
        """
        affiche l'ensemble du jeu du labyrinthe
        """
        efface = pygame.Surface((11 * self.delta, self.nb_lignes * self.delta))
        self.surface.blit(efface, (self.delta * (self.nb_colonnes + 1), 2))

        if self.jeu.est_fini():
            self.affiche_message(2, "La partie est terminée")
        nb_tours = self.jeu.get_duree_restante()
        pluriel = "s"
        if nb_tours <= 1:
            pluriel = ""
        self.affiche_message(3, "il reste " + str(nb_tours) + " tour" + pluriel + " de jeu", [])
        self.affiche_joueurs(5)
        pygame.display.flip()

    def demarrer(self):
        """
        démarre l'environnement graphique et la boucle d'écoute des événements
        """
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)
        en_cours = False
        sauver = False
        clock = pygame.time.Clock()
        self.dessiner_plateau(self.plateau)
        while (True):
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            # if ev.type == pygame.KEYDOWN
            #     en_cours = True
            # if not en_cours:
            #     continue
            if ev.type == pygame.USEREVENT + 1:
                le_jeu = self.lecteur_jeu.get_jeu()
                if le_jeu is not None:
                    self.jeu = le_jeu
                    self.plateau = le_jeu.plateau
                self.dessiner_contenu()
                self.affiche_info()
            if ev.type == pygame.VIDEORESIZE:
                self.maj_parametres()
                self.dessiner_plateau(self.plateau)
                pygame.display.flip()
        pygame.quit()


class LecteurThread(threading.Thread):
    def __init__(self, serveur="", port=1111):
        super().__init__()
        self.client = client.ClientCyber()
        self.client.creer_socket(serveur, port)
        self.client.enregistrement("affichage principal", "afficheur")
        self.ok = True
        self.verrou = threading.Lock()
        ok, _, le_jeu = self.client.prochaine_commande()
        if not ok:
            sys.exit(0)
        self.le_jeu = jeu.Jeu()
        self.le_jeu.jeu_from_str(le_jeu)
        self.change = True

    def get_jeu(self):
        self.verrou.acquire()
        res = None
        if self.change:
            res = self.le_jeu
            self.change = False
        self.verrou.release()
        return res

    def lire_jeu(self):
        ok, _, le_jeu = self.client.prochaine_commande()
        if not ok:
            self.ok = ok
            return
        self.verrou.acquire()
        self.le_jeu = jeu.Jeu()
        self.le_jeu.jeu_from_str(le_jeu)
        self.change = True
        self.verrou.release()

    def arreter(self):
        self.ok = False

    def run(self):
        while self.ok:
            self.lire_jeu()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--nom_partie", dest="nom_partie", help="nom de la partie", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    args = parser.parse_args()
    print("Bienvenue dans le jeu de Pacman@IUT'O")
    id_joueur = 1
    lecteur = LecteurThread(args.serveur, args.port)
    lecteur.start()
    jg = JeuGraphique(lecteur, [], args.nom_partie)
    jg.demarrer()
    lecteur.arreter()

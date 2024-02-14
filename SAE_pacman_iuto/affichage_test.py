"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module affichage_test.py
        Ce module permet d'afficher le contenu d'un plateau
        pour tester si le contenu des structures de données
        est conforme à ce qui est décodé par le serveur
"""
import pygame
import os
import const
import case
import plateau
from math import pi
class JeuGraphique(object):
    """Classe simple d'affichage d'une case."""

    def __init__(self, le_plateau, titre="PacIUT'O", size=(500, 500),
                 couleur=(209, 238, 238),
                 prefixe_image="./images"):
        """Method docstring."""
        #self.la_case=la_case
        self.le_plateau=le_plateau
        self.nb_lignes=plateau.get_nb_lignes(le_plateau)
        self.nb_colonnes=plateau.get_nb_colonnes(le_plateau)
        self.couleur_texte = couleur
        self.titre = titre
        self.images_pacmans = {}
        self.images_fantomes = {}
        self.images_objets = {}
        self.surf_pacmans = {}
        self.surf_fantomes = {}
        self.surf_objets = {}
        self.icone = None
        self.hauteur = 0
        self.largeur = 0
        self.delta = 0
        self.finh = 0
        self.finl = 0
        self.taille_font = 0
        self.get_images(prefixe_image)
        pygame.init()
        pygame.display.set_icon(self.icone)
        pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.maj_parametres()

    def get_images(self, prefixe_image="./images"):
        codage="ABCDEFGH"
        for code in codage:
            if os.path.isfile(os.path.join(prefixe_image, 'fant' + code + '.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'fant' + code + '.png'))
                print('fant' + code + '.png')
            else:
                s = None
            self.images_fantomes[code.lower()]=s
            if os.path.isfile(os.path.join(prefixe_image, 'pac' + code + '.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'pac' + code + '.png'))
                print('pac' + code + '.png')
            else:
                s = None
            self.images_pacmans[code]=s
            
        for i in range(7):
            if os.path.isfile(os.path.join(prefixe_image, 'tresor' + str(i) + '.png')):
                s = pygame.image.load(os.path.join(prefixe_image, 'tresor' + str(i) + '.png'))
            else:
                s = None
            print('tresor' + str(i) + '.png')
            self.images_objets[const.LES_OBJETS[i-1]]=s

        # lecture du logo de l'IUT'O
        icone_img = pygame.image.load(os.path.join(prefixe_image, 'logo.png'))
        self.icone = pygame.transform.smoothscale(icone_img, (50, 50))

    def maj_surfaces(self,dico_entree,dico_sortie, taille):
        for (cle,img) in dico_entree.items():
            dico_sortie[cle]=pygame.transform.smoothscale(img, (taille, taille))
    
    def maj_parametres(self):
        """
        permet de mettre à jour les paramètres d'affichage en cas de redimensionnement de la fenêtre
        """
        self.surface = pygame.display.get_surface()
        self.hauteur = self.surface.get_height()
        self.largeur = self.surface.get_width()
        deltav=self.hauteur//(plateau.get_nb_lignes(self.le_plateau)+2)
        deltah=self.largeur//(plateau.get_nb_colonnes(self.le_plateau)+2)
        self.delta = min(deltah,deltav)
        taille=self.delta//2
        self.epaisseur= 8#self.delta//10
        self.taille_font = self.delta// 2
        self.maj_surfaces(self.images_fantomes,self.surf_fantomes,taille)
        self.maj_surfaces(self.images_pacmans,self.surf_pacmans,taille)
        self.maj_surfaces(self.images_objets,self.surf_objets,taille)
        


    def dessiner_case2(self, la_case, lin,col, voisinage,coul_bord=(131,0,101),coul_fond=None):
        x=col*self.delta+20
        y=lin*self.delta+20
        quart=self.delta//4
        rayon=quart+3
        demi=self.delta//2
        fond=coul_fond != None
        if not case.est_mur(la_case):
            return
        
        dessiner=False
        for v in voisinage:
            if not v:
                dessiner=True
                break

        if not dessiner:
            if fond:
                pygame.draw.rect(self.surface,coul_fond,(x,y,self.delta,self.delta))
            return
        
        #coin haut-gauche
        if voisinage[0]:
            if voisinage[1] and not voisinage[3]:
                pygame.draw.line(self.surface,coul_bord,(x+quart,y),
                             (x+quart,y+demi),self.epaisseur)
            elif voisinage[3] and not voisinage[1]: 
                pygame.draw.line(self.surface,coul_bord,(x,y+quart),
                             (x+demi,y+quart),self.epaisseur)
        else:
            if voisinage[1] and voisinage[3]:
                pygame.draw.circle(self.surface,coul_bord,(x,y),
                               rayon+2,self.epaisseur,draw_bottom_right=True)
            elif voisinage[1]:
                pygame.draw.line(self.surface,coul_bord,(x+quart,y),
                             (x+quart,y+demi),self.epaisseur)
            elif voisinage[3]:
                pygame.draw.line(self.surface,coul_bord,(x,y+quart),
                             (x+demi,y+quart),self.epaisseur)
            else:
                pygame.draw.circle(self.surface,coul_bord,(x+demi,y+demi),
                               rayon,self.epaisseur,draw_top_left=True)

        #coin haut-droit
        if voisinage[2]:
            if voisinage[1] and not voisinage[4]:
                pygame.draw.line(self.surface,coul_bord,(x+3*quart-1,y),
                             (x+3*quart-1,y+demi),self.epaisseur)
            elif voisinage[4] and not voisinage[1]:
                pygame.draw.line(self.surface,coul_bord,(x+demi,y+quart),
                             (x+self.delta,y+quart),self.epaisseur)
        else:
            if voisinage[1] and voisinage[4] :
                pygame.draw.circle(self.surface,coul_bord,(x+self.delta,y),
                               rayon+2,self.epaisseur,draw_bottom_left=True)
            elif voisinage[1]:
                pygame.draw.line(self.surface,coul_bord,(x+3*quart-1,y),
                             (x+3*quart-1,y+demi),self.epaisseur)
            elif voisinage[4]:
                pygame.draw.line(self.surface,coul_bord,(x+demi,y+quart),
                             (x+self.delta,y+quart),self.epaisseur)
            else:
                pygame.draw.circle(self.surface,coul_bord,(x+demi,y+demi),
                               rayon,self.epaisseur,draw_top_right=True)

        #coin bas-droit
        if voisinage[7]:
            if voisinage[6] and not voisinage[4]:
                pygame.draw.line(self.surface,coul_bord,(x+3*quart-1,y+self.delta),
                             (x+3*quart-1,y+demi),self.epaisseur)
            elif voisinage[4] and not voisinage[6]:
                pygame.draw.line(self.surface,coul_bord,(x+demi,y+3*quart-1),
                             (x+self.delta,y+3*quart-1),self.epaisseur)
        else:
            if voisinage[6] and voisinage[4]:
                pygame.draw.circle(self.surface,coul_bord,(x+self.delta,y+self.delta),
                               rayon+2,self.epaisseur,draw_top_left=True)
            elif voisinage[6]:
                pygame.draw.line(self.surface,coul_bord,(x+3*quart-1,y+self.delta),
                             (x+3*quart-1,y+demi),self.epaisseur)
            elif voisinage[4]:
                pygame.draw.line(self.surface,coul_bord,(x+demi,y+3*quart-1),
                             (x+self.delta,y+3*quart-1),self.epaisseur)
            else:
                pygame.draw.circle(self.surface,coul_bord,(x+demi,y+demi),
                               rayon,self.epaisseur,draw_bottom_right=True)

        #coin bas-gauche
        if voisinage[5]:
            if voisinage[6] and not voisinage[3]:
                pygame.draw.line(self.surface,coul_bord,(x+quart,y+self.delta),
                             (x+quart,y+demi),self.epaisseur)
            elif voisinage[3] and not voisinage[6]:
                pygame.draw.line(self.surface,coul_bord,(x+demi,y+3*quart-1),
                             (x,y+3*quart-1),self.epaisseur)
        else:
            if voisinage[6] and voisinage[3]:
                pygame.draw.circle(self.surface,coul_bord,(x,y+self.delta),
                               rayon+2,self.epaisseur,draw_top_right=True)
            elif voisinage[6]:
                pygame.draw.line(self.surface,coul_bord,(x+quart,y+self.delta),
                             (x+quart,y+demi),self.epaisseur)
            elif voisinage[3]:
                pygame.draw.line(self.surface,coul_bord,(x+demi,y+3*quart-1),
                             (x,y+3*quart-1),self.epaisseur)
            else:
                pygame.draw.circle(self.surface,coul_bord,(x+demi,y+demi),
                               rayon,self.epaisseur,draw_bottom_left=True)


    def dessiner_plateau(self,le_plateau):
        self.surface.fill((0,0,0))
        for ligne in range(plateau.get_nb_lignes(le_plateau)):
            for colonne in range(plateau.get_nb_colonnes(le_plateau)):
                voisinage=plateau.directions_possibles(le_plateau,(ligne,colonne))
                self.dessiner_case2(plateau.get_case(le_plateau,(ligne,colonne)),
                                    ligne,colonne,voisinage)

         
    def surface_case(self, la_case):
        """
        transforme une case en une surface (image 2D) avec les pions et trésor associés
        """
        pacmans=case.get_pacmans(la_case)
        fantomes=case.get_fantomes(la_case)
        objet=case.get_objet(la_case)
        surf_carte = pygame.Surface((self.delta, self.delta))
        dist = 5
        coord = [(dist, dist), (dist, self.delta - (self.delta // 2 +dist)),
                 (self.delta - (self.delta // 2 +dist), self.delta - (self.delta // 2 +dist)),
                 (self.delta - (self.delta // 2 +dist), dist), (self.delta//4+dist,dist),
                 (self.delta//4+dist,self.delta - (self.delta // 2 +dist))]
        
        for pac in pacmans:
            surf_carte.blit(self.surf_pacmans[pac], coord.pop(0))
        for fant in fantomes:
            surf_carte.blit(self.surf_fantomes[fant], coord.pop(0))
        if objet != ' ':
            surf_carte.blit(self.surf_objets[objet], (self.delta // 4 , self.delta // 4 ))
        return surf_carte

    def dessiner_contenu(self):
        for lig in range(self.nb_lignes):
            for col in range(self.nb_colonnes):
                la_case=plateau.get_case(self.le_plateau,(lig,col))
                if not case.est_mur(la_case):
                    self.surface.blit(self.surface_case(la_case),
                                      (col*self.delta+20,lig*self.delta+20))
        pygame.display.flip()

    def demarrer(self):
        #self.surface.blit(self.surface_carte(self.la_case),(0,0))
        # voisinage=[False,False,False,False,False,False,False,False,False]
        # self.dessiner_case2(self.la_case,1,1,voisinage)
        self.dessiner_plateau(self.le_plateau)
        pygame.display.flip()
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)
        la_pos=(1,2)
        while (True):
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.KEYDOWN:
                if ev.__dict__["unicode"].upper()=='Q':
                    break
            if ev.type == pygame.VIDEORESIZE:
                self.maj_parametres()
                self.dessiner_plateau(self.le_plateau)
                pygame.display.flip()
            if ev.type == pygame.USEREVENT + 1:
                self.dessiner_contenu()
        pygame.quit()

if __name__ == '__main__':
    la_case=case.Case(mur=True)
    plan1="4;6\n"+\
                    "#   # \n"+\
                    "    ##\n"+\
                    " ##   \n"+\
                    " #  ##\n"
    
    plan2="4;6\n"+\
                    "##### \n"+\
                    "  ### \n"+\
                    "#####  \n"+\
                    "  ####\n"
    
    plan3="7;16\n"+\
                " # # # ### # ###\n"+\
                " # # #  #  # # #\n"+\
                " # ###  #    ###\n"+\
                "                \n"+\
                " # # # ### ###  \n"+\
                " # ### ##  # #  \n"+\
                " # # # #   ###  \n"
    plan4=""
    with open("./cartes/test1.txt") as fic:
        plan4=fic.read()
    plat=plateau.plateau_from_str(plan4,True)
    print(plateau.get_nb_colonnes(plat),plateau.get_nb_lignes(plat))
    affichage=JeuGraphique(plat,prefixe_image="./images")
    affichage.demarrer()

import unittest
import const
import joueur

class test_joueur(unittest.TestCase):  
    def setUp(self):
        self.chaine1="A;152;3;28;0;0;12;5;0;9;Greedy"
        self.chaine2="B;-8;0;1;3;6;4;0;0;0;iut'o"
        self.chaine3="C;14;2;12;21;23;1;3;2;1;Ghost"
    
    def test_joueur(self):
        le_joueur=joueur.Joueur('A',"test1",53,2,(12,27),(2,14),
                                {const.GLOUTON:3,const.IMMOBILITE:0,const.PASSEMURAILLE:1})
        self.assertEqual(joueur.get_couleur(le_joueur),'A')
        self.assertEqual(joueur.get_nom(le_joueur),'test1')
        self.assertEqual(joueur.get_nb_points(le_joueur),53)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),2)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),(12,27))
        self.assertEqual(joueur.get_pos_fantome(le_joueur),(2,14))
        self.assertEqual(joueur.get_duree(le_joueur,const.GLOUTON),3)
        self.assertEqual(joueur.get_duree(le_joueur,const.IMMOBILITE),0)
        self.assertEqual(joueur.get_duree(le_joueur,const.PASSEMURAILLE),1)

        le_joueur=joueur.Joueur('B',"test2",-22,0,(17,3),(8,4),
                                {const.GLOUTON:0,const.IMMOBILITE:1,const.PASSEMURAILLE:2})
        self.assertEqual(joueur.get_couleur(le_joueur),'B')
        self.assertEqual(joueur.get_nom(le_joueur),'test2')
        self.assertEqual(joueur.get_nb_points(le_joueur),-22)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),0)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),(17,3))
        self.assertEqual(joueur.get_pos_fantome(le_joueur),(8,4))
        self.assertEqual(joueur.get_duree(le_joueur,const.GLOUTON),0)
        self.assertEqual(joueur.get_duree(le_joueur,const.IMMOBILITE),1)
        self.assertEqual(joueur.get_duree(le_joueur,const.PASSEMURAILLE),2)
 
    def test_joueur_from_str(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        self.assertEqual(joueur.get_couleur(le_joueur),'A')
        self.assertEqual(joueur.get_nom(le_joueur),'Greedy')
        self.assertEqual(joueur.get_nb_points(le_joueur),152)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),3)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),(28,0))
        self.assertEqual(joueur.get_pos_fantome(le_joueur),(0,12))
        self.assertEqual(joueur.get_duree(le_joueur,const.GLOUTON),5)
        self.assertEqual(joueur.get_duree(le_joueur,const.IMMOBILITE),0)
        self.assertEqual(joueur.get_duree(le_joueur,const.PASSEMURAILLE),9)

        le_joueur=joueur.joueur_from_str(self.chaine2)
        self.assertEqual(joueur.get_couleur(le_joueur),'B')
        self.assertEqual(joueur.get_nom(le_joueur),"iut'o")
        self.assertEqual(joueur.get_nb_points(le_joueur),-8)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),0)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),(1,3))
        self.assertEqual(joueur.get_pos_fantome(le_joueur),(6,4))
        self.assertEqual(joueur.get_duree(le_joueur,const.GLOUTON),0)
        self.assertEqual(joueur.get_duree(le_joueur,const.IMMOBILITE),0)
        self.assertEqual(joueur.get_duree(le_joueur,const.PASSEMURAILLE),0)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        self.assertEqual(joueur.get_couleur(le_joueur),'C')
        self.assertEqual(joueur.get_nom(le_joueur),"Ghost")
        self.assertEqual(joueur.get_nb_points(le_joueur),14)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),2)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),(12,21))
        self.assertEqual(joueur.get_pos_fantome(le_joueur),(23,1))
        self.assertEqual(joueur.get_duree(le_joueur,const.GLOUTON),3)
        self.assertEqual(joueur.get_duree(le_joueur,const.IMMOBILITE),2)
        self.assertEqual(joueur.get_duree(le_joueur,const.PASSEMURAILLE),1)

    def test_get_objets(self):

        l1=[const.GLOUTON,const.PASSEMURAILLE]
        l1.sort()
        l3=[const.GLOUTON,const.IMMOBILITE,const.PASSEMURAILLE]
        l3.sort()

        le_joueur=joueur.joueur_from_str(self.chaine1)
        l_res1=joueur.get_objets(le_joueur)
        l_res1.sort()
        self.assertEqual(l_res1,l1)
        le_joueur=joueur.joueur_from_str(self.chaine2)
        l_res2=joueur.get_objets(le_joueur)
        self.assertEqual(l_res2,[])
        le_joueur=joueur.joueur_from_str(self.chaine3)
        l_res3=joueur.get_objets(le_joueur)
        l_res3.sort()
        self.assertEqual(l_res3,l3)

    def test_set_pos_pacman(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        pos=(10,12)
        joueur.set_pos_pacman(le_joueur,pos)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),pos)
        le_joueur=joueur.joueur_from_str(self.chaine2)
        pos=(28,5)
        joueur.set_pos_pacman(le_joueur,pos)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),pos)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        pos=(17,25)
        joueur.set_pos_pacman(le_joueur,pos)
        self.assertEqual(joueur.get_pos_pacman(le_joueur),pos)

    def test_set_pos_fantome(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        pos=(53,2)
        joueur.set_pos_fantome(le_joueur,pos)
        self.assertEqual(joueur.get_pos_fantome(le_joueur),pos)
        le_joueur=joueur.joueur_from_str(self.chaine2)
        pos=(2,63)
        joueur.set_pos_fantome(le_joueur,pos)
        self.assertEqual(joueur.get_pos_fantome(le_joueur),pos)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        pos=(37,12)
        joueur.set_pos_fantome(le_joueur,pos)
        self.assertEqual(joueur.get_pos_fantome(le_joueur),pos)

    def test_add_points(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        self.assertEqual(joueur.add_points(le_joueur,25),177)
        le_joueur=joueur.joueur_from_str(self.chaine2)
        self.assertEqual(joueur.add_points(le_joueur,-12),-20)
        le_joueur=joueur.joueur_from_str(self.chaine3)
        self.assertEqual(joueur.add_points(le_joueur,-5),9)
        self.assertEqual(joueur.add_points(le_joueur,20),29)

    def test_faux_mouvement(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        self.assertEqual(joueur.faux_mouvement(le_joueur),2)
        self.assertEqual(joueur.faux_mouvement(le_joueur),1)
        le_joueur=joueur.joueur_from_str(self.chaine2)
        self.assertEqual(joueur.faux_mouvement(le_joueur),-1)
        le_joueur=joueur.joueur_from_str(self.chaine3)
        self.assertEqual(joueur.faux_mouvement(le_joueur),1)

        
    def test_ajouter_objet(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)        
        for objet in const.LES_OBJETS:
            nb_points=joueur.get_nb_points(le_joueur)
            duree=joueur.get_duree(le_joueur,objet)
            joueur.ajouter_objet(le_joueur,objet)
            self.assertEqual(joueur.get_nb_points(le_joueur),nb_points+const.PROP_OBJET[objet][0])
            self.assertEqual(joueur.get_duree(le_joueur,objet),duree+const.PROP_OBJET[objet][1])
            
       
        le_joueur=joueur.joueur_from_str(self.chaine2)
        for objet in const.LES_OBJETS:
            nb_points=joueur.get_nb_points(le_joueur)
            duree=joueur.get_duree(le_joueur,objet)
            joueur.ajouter_objet(le_joueur,objet)
            self.assertEqual(joueur.get_nb_points(le_joueur),nb_points+const.PROP_OBJET[objet][0])
            self.assertEqual(joueur.get_duree(le_joueur,objet),duree+const.PROP_OBJET[objet][1])

        le_joueur=joueur.joueur_from_str(self.chaine3)
        for objet in const.LES_OBJETS:
            nb_points=joueur.get_nb_points(le_joueur)
            duree=joueur.get_duree(le_joueur,objet)
            joueur.ajouter_objet(le_joueur,objet)
            self.assertEqual(joueur.get_nb_points(le_joueur),nb_points+const.PROP_OBJET[objet][0])
            self.assertEqual(joueur.get_duree(le_joueur,objet),duree+const.PROP_OBJET[objet][1])

    def test_reinit_faux_mouvements(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        joueur.reinit_faux_mouvements(le_joueur)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),const.NB_FAUX_MVT)
        le_joueur=joueur.joueur_from_str(self.chaine2)
        joueur.reinit_faux_mouvements(le_joueur)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),const.NB_FAUX_MVT)
        le_joueur=joueur.joueur_from_str(self.chaine3)
        joueur.reinit_faux_mouvements(le_joueur)
        self.assertEqual(joueur.get_nb_faux_mvt(le_joueur),const.NB_FAUX_MVT)
        

    def test_maj_duree(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        for objet in const.LES_OBJETS:
            if const.PROP_OBJET[objet][1]!=0:
                duree=joueur.get_duree(le_joueur,objet)
                joueur.maj_duree(le_joueur)
                self.assertEqual(joueur.get_duree(le_joueur,objet),max(0,duree-1))
        le_joueur=joueur.joueur_from_str(self.chaine2)
        for objet in const.LES_OBJETS:
            if const.PROP_OBJET[objet][1]!=0:
                duree=joueur.get_duree(le_joueur,objet)
                joueur.maj_duree(le_joueur)
                self.assertEqual(joueur.get_duree(le_joueur,objet),max(0,duree-1))
        le_joueur=joueur.joueur_from_str(self.chaine3)
        for objet in const.LES_OBJETS:
            if const.PROP_OBJET[objet][1]!=0:
                duree=joueur.get_duree(le_joueur,objet)
                joueur.maj_duree(le_joueur)
                self.assertEqual(joueur.get_duree(le_joueur,objet),max(0,duree-1))
        
        

if __name__ == '__main__':
    unittest.main()       
       
        
        
        
        
        
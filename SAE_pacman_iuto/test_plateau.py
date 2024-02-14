import unittest
import const
import plateau
import case


class test_case(unittest.TestCase):
    def setUp(self):
        with open("cartes/test1.txt") as fic:
            self.plateau1 = fic.read()
        with open("cartes/test2.txt") as fic:
            self.plateau2 = fic.read()
        with open("cartes/test3.txt") as fic:
            self.plateau3 = fic.read()

    def verif(self, plan, le_plateau):
        les_lignes = plan.split("\n")
        [nb_lignes, nb_colonnes] = les_lignes[0].split(";")
        nb_lignes = int(nb_lignes)
        nb_colonnes = int(nb_colonnes)
        nbli = plateau.get_nb_lignes(le_plateau)
        if nb_lignes != nbli:
            return "Le nombre de lignes est incorrect. Attendu: " + str(nb_lignes) + \
                "Obtenu: " + str(nbli)
        nbco = plateau.get_nb_colonnes(le_plateau)
        if nb_colonnes != nbco:
            return "Le nombre de colonnes est incorrect. Attendu: " + str(nb_colonnes) + \
                "Obtenu: " + str(nbco)
        for lin in range(nb_lignes):
            la_ligne = les_lignes[lin + 1]
            for col in range(nb_colonnes):
                la_case = plateau.get_case(le_plateau, (lin, col))
                if la_ligne[col] == ' ':
                    if case.est_mur(la_case):
                        return "La case " + str(lin) + "," + str(col) + \
                            " devrait être un couloir alors que c'est un mur dans votre plateau"
                    obj = case.get_objet(la_case)
                    if obj != ' ':
                        return "La case " + str(lin) + "," + str(col) + \
                            " devrait être vide alors qu'elle a l'objet " + \
                            str(obj) + " dans votre plateau"
                elif la_ligne[col] == '#':
                    if not case.est_mur(la_case):
                        return "La case " + str(lin) + "," + str(col) + \
                            " devrait être un mur alors que c'est un couloir dans votre plateau"
                    coul = case.get_objet(la_case)
                    if coul != ' ':
                        return "La case " + str(lin) + "," + str(col) + \
                            " devrait être vide alors qu'elle a l'objet " + \
                            str(obj) + " dans votre plateau"
                elif la_ligne[col] in const.LES_OBJETS:
                    if case.est_mur(la_case):
                        return "La case " + str(lin) + "," + str(col) + \
                            " devrait être un couloir alors que c'est un mur dans votre plateau"
                    obj = case.get_objet(la_case)
                    if obj != la_ligne[col]:
                        return "La case " + str(lin) + "," + str(col) + \
                            " devrait être contenir l'objet " + la_ligne[col] + " alors qu'elle contient l'objet " + \
                            str(obj) + " dans votre plateau"

        nb_pacmans = int(les_lignes[nb_lignes + 1])
        for ind in range(nb_lignes + 2, nb_lignes + 2 + nb_pacmans):
            pacman, lin, col = les_lignes[ind].split(';')
            lin = int(lin)
            col = int(col)
            pacmans = case.get_pacmans(plateau.get_case(le_plateau, (lin, col)))
            if pacman not in pacmans:
                return "La case " + str(lin) + "," + str(col) + \
                    " devrait contenir le pacman " + pacman + \
                    " alors qu'elle contient cet ensemble de pacmans " + \
                    str(pacmans)
        nb_fantomes = int(les_lignes[nb_lignes + 2 + nb_pacmans])
        for ind in range(nb_lignes + 3 + nb_pacmans, nb_lignes + 3 + nb_pacmans + nb_fantomes):
            fantome, lin, col = les_lignes[ind].split(';')
            lin = int(lin)
            col = int(col)
            fantomes = case.get_fantomes(plateau.get_case(le_plateau, (lin, col)))
            if fantome not in fantomes:
                return "La case " + str(lin) + "," + str(col) + \
                    " devrait contenir le fantome " + fantome + \
                    " alors qu'elle contient cet ensemble de fantomes " + \
                    str(fantomes)
        return None

    def test_Plateau(self):
        res = self.verif(self.plateau1, plateau.Plateau(self.plateau1))
        self.assertIsNone(res, res)
        res = self.verif(self.plateau2, plateau.Plateau(self.plateau2))
        self.assertIsNone(res, res)
        res = self.verif(self.plateau3, plateau.Plateau(self.plateau3))
        self.assertIsNone(res, res)

    def test_pos_nord(self):
        p1 = plateau.Plateau(self.plateau1)
        res = plateau.pos_nord(p1, (0, 12))
        self.assertEqual(res,
                         (plateau.get_nb_lignes(p1) - 1, 12),
                         "La position au nord de la case (0,12) devrait être (" + \
                         str(plateau.get_nb_lignes(p1) - 1) + ",12)" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_nord(p1, (18, 0))
        self.assertEqual(res, (17, 0),
                         "La position au nord de la case (28,0) devrait être (27,0)" + \
                         " alors que vous retournez " + str(res))
        p2 = plateau.Plateau(self.plateau2)
        res = plateau.pos_nord(p2, (0, 5))
        self.assertEqual(res,
                         (plateau.get_nb_lignes(p2) - 1, 5),
                         "La position au nord de la case (0,5) devrait être (" + \
                         str(plateau.get_nb_lignes(p2) - 1) + ",5)" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_nord(p2, (3, 0))
        self.assertEqual(res, (2, 0),
                         "La position au nord de la case (3,0) devrait être (2,0)" + \
                         " alors que vous retournez " + str(res))

    def test_pos_sud(self):
        p1 = plateau.Plateau(self.plateau1)
        res = plateau.pos_sud(p1, (plateau.get_nb_lignes(p1) - 1, 10))
        self.assertEqual(res,
                         (0, 10),
                         "La position au sud de la case (" + str(plateau.get_nb_lignes(p1) - 1) + \
                         ",10) devrait être (0,10)" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_sud(p1, (14, 0))
        self.assertEqual(res, (15, 0),
                         "La position au sud de la case (14,0) devrait être (15,0)" + \
                         " alors que vous retournez " + str(res))
        p2 = plateau.Plateau(self.plateau2)
        res = plateau.pos_sud(p2, (plateau.get_nb_lignes(p2) - 1, 7))
        self.assertEqual(res,
                         (0, 7),
                         "La position au sud de la case (" + \
                         str(plateau.get_nb_lignes(p2) - 1) + \
                         ",7) devrait être (0,7)" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_sud(p2, (3, 0))
        self.assertEqual(res, (4, 0),
                         "La position au sud de la case (3,0) devrait être (4,0)" + \
                         " alors que vous retournez " + str(res))

    def test_pos_ouest(self):
        p1 = plateau.Plateau(self.plateau1)
        res = plateau.pos_ouest(p1, (12, 0))
        self.assertEqual(res,
                         (12, plateau.get_nb_colonnes(p1) - 1),
                         "La position à l'ouest de la case (12,0) devrait être (12," + \
                         str(plateau.get_nb_colonnes(p1) - 1) + ")" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_ouest(p1, (0, 28))
        self.assertEqual(res, (0, 27),
                         "La position à l'ouest de la case (0,28) devrait être (0,27)" + \
                         " alors que vous retournez " + str(res))
        p2 = plateau.Plateau(self.plateau2)
        res = plateau.pos_ouest(p2, (5, 0))
        self.assertEqual(res,
                         (5, plateau.get_nb_colonnes(p2) - 1),
                         "La position à l'ouest de la case (5,0) devrait être (5," + \
                         str(plateau.get_nb_colonnes(p2) - 1) + ")" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_ouest(p2, (0, 3))
        self.assertEqual(res, (0, 2),
                         "La position à l'ouest de la case (0,3) devrait être (0,2)" + \
                         " alors que vous retournez " + str(res))

    def test_pos_est(self):
        p1 = plateau.Plateau(self.plateau1)
        res = plateau.pos_est(p1, (15, plateau.get_nb_colonnes(p1) - 1))
        self.assertEqual(res,
                         (15, 0),
                         "La position à l'est de la case (15" + \
                         str(plateau.get_nb_colonnes(p1) - 1) + \
                         ") devrait être (15,0) alors que vous retournez " + str(res))
        res = plateau.pos_est(p1, (0, 26))
        self.assertEqual(res, (0, 27),
                         "La position à l'est de la case (0,26) devrait être (0,27)" + \
                         " alors que vous retournez " + str(res))
        p2 = plateau.Plateau(self.plateau2)
        res = plateau.pos_est(p2, (0, 5))
        self.assertEqual(res,
                         (0, 6),
                         "La position à l'est de la case (0,5) devrait être (0,6)" + \
                         " alors que vous retournez " + str(res))
        res = plateau.pos_est(p2, (0, plateau.get_nb_colonnes(p2) - 1))
        self.assertEqual(res, (0, 0),
                         "La position à l'est de la case (0," + \
                         str(plateau.get_nb_colonnes(p2) - 1) + \
                         ") devrait être (0,0) alors que vous retournez " + str(res))

    def test_pos_arrivee(self):
        p1 = plateau.Plateau(self.plateau1)
        nb_lig = plateau.get_nb_lignes(p1)
        nb_col = plateau.get_nb_colonnes(p1)
        directions = "NSOE"
        pos_test = [(0, 12), (nb_lig - 1, 7), (7, 0), (11, nb_col - 1), (6, 5), (6, 5), (6, 5), (6, 5)]
        pos_attendues = [(nb_lig - 1, 12), (0, 7), (7, nb_col - 1), (11, 0), (5, 5), (7, 5), (6, 4), (6, 6)]
        for i in range(len(pos_test)):
            res = plateau.pos_arrivee(p1, pos_test[i], directions[i % 4])
            self.assertEqual(res, pos_attendues[i],
                             "L'appel de pos_arrivee sur la plateau test1.txt" + \
                             " à partir de la case " + str(pos_test[i]) + \
                             " en direction de " + str(directions[i % 4]) + \
                             " devrait retourner " + str(pos_attendues[i]) + \
                             " or vous retournez " + str(res)
                             )

    def test_enlever_pacman(self):
        p1 = plateau.Plateau(self.plateau1)
        res = plateau.enlever_pacman(p1, 'A', (1, 2))
        self.assertTrue(res, "Le pacman A devrait être sur la case (1,2) du plateau test1.txt")
        self.assertFalse('A' in case.get_pacmans(plateau.get_case(p1, (1, 2))),
                         "après avoir enlevé le pacman A de la case (1,2) il ne devrait " + \
                         "plus être sur cette case")
        res = plateau.enlever_pacman(p1, 'C', (3, 6))
        self.assertTrue(res, "Le pacman C devrait être sur la case (3,6) du plateau test1.txt")
        self.assertFalse('C' in case.get_pacmans(plateau.get_case(p1, (3, 6))),
                         "après avoir enlevé le pacman C de la case (3,6) il ne devrait " + \
                         "plus être sur cette case")
        self.assertFalse(plateau.enlever_pacman(p1, 'B', (1, 1)),
                         "Le pacman B ne se trouve pas sur la case (1,1) du plateau 1 or vous le détectez")

    def test_enlever_fantome(self):
        p1 = plateau.Plateau(self.plateau1)
        res = plateau.enlever_fantome(p1, 'a', (7, 5))
        self.assertTrue(res, "Le fantome a devrait être sur la case (7,5) du plateau test1.txt")
        self.assertFalse('a' in case.get_fantomes(plateau.get_case(p1, (7, 5))),
                         "après avoir enlevé le fantome a de la case (7,5) il ne devrait " + \
                         "plus être sur cette case")
        self.assertTrue('d' in case.get_fantomes(plateau.get_case(p1, (7, 5))),
                        "après avoir enlevé le fantome a de la case (7,5) le fantome d devrait " + \
                        "toujours y être or il semble avoir disparu")
        res = plateau.enlever_fantome(p1, 'e', (3, 6))
        self.assertTrue(res, "Le fantome e devrait être sur la case (3,6) du plateau test1.txt")
        self.assertFalse('e' in case.get_fantomes(plateau.get_case(p1, (3, 6))),
                         "après avoir enlevé le fantome e de la case (3,6) il ne devrait " + \
                         "plus être sur cette case")

        self.assertFalse(plateau.enlever_pacman(p1, 'b', (10, 12)),
                         "Le fantome b ne se trouve pas sur la case (10,12) du plateau 1 or vous le détectez")

    def test_prendre_objet(self):
        p2 = plateau.Plateau(self.plateau2)
        res = plateau.prendre_objet(p2, (1, 1))
        self.assertEqual(res, const.VITAMINE,
                         "La case (1,1) du plateau test2.txt contient une vitamine " + \
                         "or vous retournez la valeur [" + str(res) + "]")
        res = plateau.prendre_objet(p2, (1, 1))
        self.assertEqual(res, const.AUCUN,
                         "Après avoir pris l'objet de la case (1,1) du plateau test2.txt " + \
                         "il ne devrait plus y avoir d'objet or vous retournez la valeur " + str(res))
        res = plateau.prendre_objet(p2, (8, 1))
        self.assertEqual(res, const.VALEUR,
                         "La case (8,1) du plateau test2.txt contient " + const.VALEUR + \
                         "or vous trouvez l'objet " + str(res))
        res = plateau.prendre_objet(p2, (8, 1))
        self.assertEqual(plateau.prendre_objet(p2, (8, 1)), const.AUCUN,
                         "Après avoir pris un objet en (8,1) cette case devrait être vide " + \
                         "or vous trouvez l'objet " + str(res))

    def verif_deplacement(self, plat, pos_d, pos_a, pacman, dir, present=True, passemuraille=False):
        res = plateau.deplacer_pacman(plat, pacman, pos_d, dir, passemuraille)
        self.assertEqual(res, pos_a,
                         "Le déplacement du pacman " + pacman + " de la position " + str(pos_d) + \
                         " en direction de " + dir + " devrait retourner " + str(pos_a) + \
                         " or votre fonction trouve " + str(res)
                         )
        if pos_a is None:
            if present:
                self.assertTrue(pacman in case.get_pacmans(plateau.get_case(plat, pos_d)),
                                "Le déplacement du pacman " + str(pacman) + " de la position " + str(pos_d) + \
                                " en direction de " + dir + " n'ayant pas pu se faire " + \
                                str(pacman) + " devrait toujours être en " + str(pos_d) + \
                                " or dans votre implémentation il n'y est plus"
                                )
        else:
            self.assertFalse(pacman in case.get_pacmans(plateau.get_case(plat, pos_d)),
                             "Le déplacement du pacman " + str(pacman) + " de la position " + str(pos_d) + \
                             " en direction de " + dir + " a réussi" + \
                             " or dans votre implémentation " + pacman + " est toujours dans cette case"
                             )
            self.assertTrue(pacman in case.get_pacmans(plateau.get_case(plat, pos_a)),
                            "Le déplacement du pacman " + str(pacman) + " de la position " + str(pos_d) + \
                            " en direction de " + dir + " arrive en " + str(pos_d) + \
                            " or dans votre implémentation " + pacman + " n'est pas dans cette case"
                            )

    def test_deplacer_pacman(self):
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 1), (1, 0), 'A', 'O')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 1), None, 'A', 'E')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 1), (2, 1), 'A', 'S')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 1), None, 'A', 'N')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 2), None, 'A', 'N', False)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 2), None, 'A', 'E', False)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (8, 6), (8, 7), 'C', 'E')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (8, 6), (8, 5), 'C', 'O')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (8, 6), (7, 6), 'C', 'N')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (8, 6), None, 'C', 'S')

    def test_deplacer_pacman_passemuraille(self):
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 8), (1, 7), 'B', 'O', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 8), (1, 9), 'B', 'E', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 8), (0, 8), 'B', 'N', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 8), (2, 8), 'B', 'S', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 2), None, 'B', 'N', False, passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (1, 2), None, 'B', 'E', False, passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (6, 6), (6, 7), 'D', 'E', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (6, 6), (6, 5), 'D', 'O', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (6, 6), (5, 6), 'D', 'N', passemuraille=True)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement(p2, (6, 6), (7, 6), 'D', 'S', passemuraille=True)

    def verif_deplacement_f(self, plat, pos_d, pos_a, fantome, dir, present=True):
        res = plateau.deplacer_fantome(plat, fantome, pos_d, dir)
        self.assertEqual(res, pos_a,
                         "Le déplacement du fantome " + fantome + " de la position " + str(pos_d) + \
                         " en direction de " + dir + " devrait retourner " + str(pos_a) + \
                         " or votre fonction trouve " + str(res)
                         )
        if pos_a is None:
            if present:
                self.assertTrue(fantome in case.get_fantomes(plateau.get_case(plat, pos_d)),
                                "Le déplacement du fantome " + str(fantome) + " de la position " + str(pos_d) + \
                                " en direction de " + dir + " n'ayant pas pu se faire " + \
                                str(fantome) + " devrait toujours être en " + str(pos_d) + \
                                " or dans votre implémentation il n'y est plus"
                                )
        else:
            self.assertFalse(fantome in case.get_fantomes(plateau.get_case(plat, pos_d)),
                             "Le déplacement du fantome " + str(fantome) + " de la position " + str(pos_d) + \
                             " en direction de " + dir + " a réussi" + \
                             " or dans votre implémentation " + fantome + " est toujours dans cette case"
                             )
            self.assertTrue(fantome in case.get_fantomes(plateau.get_case(plat, pos_a)),
                            "Le déplacement du fantome " + str(fantome) + " de la position " + str(pos_d) + \
                            " en direction de " + dir + " arrive en " + str(pos_d) + \
                            " or dans votre implémentation " + fantome + " n'est pas dans cette case"
                            )

    def test_deplacer_fantome(self):
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (1, 9), (1, 8), 'c', 'O')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (1, 9), (1, 0), 'c', 'E')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (1, 9), None, 'c', 'S')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (1, 9), None, 'c', 'N')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (1, 2), None, 'c', 'N', False)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (1, 2), None, 'c', 'E', False)
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (6, 4), None, 'd', 'E')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (6, 4), None, 'd', 'O')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (6, 4), (5, 4), 'd', 'N')
        p2 = plateau.Plateau(self.plateau2)
        self.verif_deplacement_f(p2, (6, 4), (7, 4), 'd', 'S')

    def test_directions_possibles(self):
        p2 = plateau.Plateau(self.plateau2)
        attendus = {(0, 0): {"S"}, (5, 6): {"N", "S", "E", "O"}, (7, 8): set(),
                    (8, 5): {'O', 'E'}, (5, 0): {'O', 'E'}, (7, 1): {"N", "S"}}
        for pos in attendus:
            res = plateau.directions_possibles(p2, pos)
            self.assertEqual(set(res), attendus[pos],
                             "Sur le plateau test2.txt, l'ensemble des directions possibles à partir de " + \
                             str(pos) + " est " + str(attendus[pos]) + " or votre fonction retourne " +
                             str(res))
        res = plateau.directions_possibles(p2, (3, 2), True)
        self.assertEqual(set(res), {"N", "S", "E", "O"},
                         "Sur le plateau test2.txt, l'ensemble des directions possibles à partir de " + \
                         " (3,2) est NSEO or votre fonction retourne " +
                         str(res))

    def test_analyse_plateau(self):
        p2 = plateau.Plateau(self.plateau2)
        pos = (5, 6)
        dist = 5

        attendus = {'N': {
            'objets': [(2, '@'), (3, '!'), (3, '.'), (3, '.'), (4, '.'), (4, '.'), (4, '.'), (5, '.'), (5, '.'),
                       (5, '.'), (5, '~')], 'pacmans': [(3, 'D'), (5, 'C')], 'fantomes': [(3, 'b'), (5, 'd')]},
                    'S': {'objets': [(2, '@'), (3, '.'), (3, '.'), (3, '~'), (4, '.'), (4, '.'), (4, '.'), (5, '!'),
                                     (5, '.'), (5, '.')], 'pacmans': [(1, 'D'), (3, 'C')],
                          'fantomes': [(5, 'b'), (5, 'd')]},
                    'E': {'objets': [(1, '.'), (2, '.'), (2, '@'), (3, '.'), (4, '.'), (5, '!'), (5, '.'), (5, '.'),
                                     (5, '~')], 'pacmans': [(3, 'D'), (5, 'C')], 'fantomes': [(5, 'b'), (5, 'd')]},
                    'O': {'objets': [(1, '.'), (2, '@'), (2, '.'), (3, '.'), (3, '.'), (4, '.'), (4, '.'), (5, '!'),
                                     (5, '.'), (5, '~')], 'pacmans': [(3, 'D'), (5, 'C')],
                          'fantomes': [(3, 'd'), (5, 'b')]}
                    }
        for dir in attendus:
            res = plateau.analyse_plateau(p2, pos, dir, dist)
            for cle in attendus[dir]:
                attendus[dir][cle].sort()
                res[cle].sort()
                self.assertEqual(res[cle], attendus[dir][cle],
                                 "Les distances à partir de la position " + str(pos) + \
                                 " en allant vers " + dir + " pour les " + cle + " ne sont pas correctes")
        self.assertEqual(plateau.analyse_plateau(p2, (1, 6), 'N', 5), None,
                         "Le déplacement vers N à partir de (1,6) n'est pas possible or " + \
                         "votre fonction retourne " + str(res) + " au lieu de None")

    def test_prochaine_intersection(self):
        p2 = plateau.Plateau(self.plateau2)
        attendus = {'N': 1, 'S': 2, 'E': 4, 'O': 4}
        pos = (5, 6)
        for dir in attendus:
            res = plateau.prochaine_intersection(p2, pos, dir)
            self.assertEqual(res, attendus[dir],
                             "La prochaine intersection quand on part de " + \
                             str(pos) + " en allant vers le " + dir + \
                             " devrait être à une distance de " + str(attendus[dir]) + \
                             " or votre fonction retourne " + str(res))


if __name__ == '__main__':
    unittest.main()


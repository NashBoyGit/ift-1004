from unittest import TestCase
from pymafia.joueur import Joueur
from pymafia.de import Dé


class TestJoueur(TestCase):

    def test_joueur(self):
        joueur = Joueur(1)
        self.assertEqual(len(joueur), 2)
        self.assertEqual(type(joueur.identifiant), type(1))
        self.assertIsInstance(joueur.dés[0], Dé)

    def test_rouler_dés(self):
        joueur = Joueur(1)
        joueur.dés = [Dé(2), Dé(4), Dé(6), Dé(1), Dé(5)]
        joueur.rouler_dés()
        état_dés_1 = joueur.__repr__()
        joueur.rouler_dés()
        état_dés_2 = joueur.__repr__()
        self.assertNotEqual(état_dés_1, état_dés_2)
        # Il est possible que les 5 dés, de nouveau roulés, donnent le même résultat. Il s'agit d'une possibilité sur 7776

    def test_calculer_points(self):
        joueur = Joueur(1)
        joueur.dés = [Dé(2), Dé(4), Dé(6), Dé(1), Dé(5)]
        self.assertEqual(joueur.calculer_points(), 18)

    def test_ajuster_score_en_fin_de_tour(self):
        joueur = Joueur(1)
        joueur.dés = [Dé(5), Dé(4)]

        # Situation testée 1: les points à retirer (9) sont supérieures au score du joueur (6)
        joueur.score = 6
        self.assertEqual(joueur.ajuster_score_en_fin_de_tour(), 6)
        self.assertEqual(joueur.score, 0)

        # Situation testée 2: les points à retirer (9) sont inférieures au score du joueur (12)
        joueur.score = 12
        self.assertEqual(joueur.ajuster_score_en_fin_de_tour(), 9)
        self.assertEqual(joueur.score, 3)

    def test_compter_1_et_6(self):
        joueur = Joueur(1)

        joueur.dés = [Dé(1), Dé(2), Dé(6), Dé(3), Dé(5)]
        self.assertEqual(joueur.compter_1_et_6(), (1, 1))

        joueur.dés = [Dé(1), Dé(1), Dé(6), Dé(6), Dé(5)]
        self.assertEqual(joueur.compter_1_et_6(), (2, 2))

        # Cas: pas de 6
        joueur.dés = [Dé(1), Dé(1), Dé(5), Dé(5), Dé(5)]
        self.assertEqual(joueur.compter_1_et_6(), (2, 0))

        # Cas: pas de 1
        joueur.dés = [Dé(4), Dé(2), Dé(6), Dé(6), Dé(6)]
        self.assertEqual(joueur.compter_1_et_6(), (0, 3))

        # Cas: pas de 1 ni de 6
        joueur.dés = [Dé(4), Dé(5), Dé(5), Dé(3), Dé(5)]
        self.assertEqual(joueur.compter_1_et_6(), (0, 0))

    def test_retirer_dé(self):
        joueur = Joueur(1)

        # Cas 1: Un seul dé ayant la valeur à retirer
        joueur.dés = [Dé(2), Dé(4), Dé(6), Dé(1), Dé(5)]
        joueur.retirer_dé(4)
        self.assertEqual(str(joueur.dés), str([Dé(2), Dé(6), Dé(1), Dé(5)]))

        # Cas 2: Plus d'un dé ayant la valeur à retirer
        joueur.dés = [Dé(2), Dé(4), Dé(6), Dé(1), Dé(4)]
        joueur.retirer_dé(4)
        self.assertEqual(str(joueur.dés), str([Dé(2), Dé(6), Dé(1)]))

        # Cas 3: Tous les dés ayant la valeur à retirer
        joueur.dés = [Dé(4), Dé(4), Dé(4), Dé(4), Dé(4)]
        joueur.retirer_dé(4)
        self.assertEqual(joueur.dés, [])

    def test_retirer_dés(self):
        joueur = Joueur(1)

        # Cas 1: Le joueur a plusieurs dés
        joueur.dés = [Dé(2), Dé(4), Dé(6), Dé(1), Dé(5)]
        joueur.retirer_dés()
        self.assertEqual(len(joueur), 0)

        # Cas 2: Le jouer n'a déjà plus de dés
        joueur.retirer_dés()
        self.assertEqual(len(joueur), 0)

    def test_ajouter_dé(self):
        joueur = Joueur(1)

        # Cas 1: Le joueur a plusieurs dés
        joueur.dés = [Dé(2), Dé(4), Dé(6), Dé(1)]
        joueur.ajouter_un_dé()
        self.assertEqual(len(joueur.dés), 5)

        # Cas 2: Le joueur n'a aucun dés
        joueur.dés = []
        joueur.ajouter_un_dé()
        self.assertEqual(len(joueur.dés), 1)

    def test_reinitialiser_dés(self):
        joueur = Joueur(1)
        joueur.reinitialiser_dés()
        self.assertEqual(len(joueur.dés), 5)



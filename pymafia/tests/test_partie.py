from unittest import TestCase
from pymafia.partie import Partie
from pymafia.de import Dé
from pymafia.joueur import Joueur
from pymafia.joueur_humain import JoueurHumain
from pymafia.joueur_ordinateur import JoueurOrdinateur


class TestPartie(TestCase):

    def test_creer_joueurs(self):

        partie = Partie(5, 2)
        self.assertEqual(len(partie.joueurs), 5)

        nombre_joueurs_humains = 0
        nombre_joueurs_ordinateurs = 0

        for i in range(5):
            if isinstance(partie.joueurs[i], JoueurHumain):
                nombre_joueurs_humains += 1
            else:
                nombre_joueurs_ordinateurs += 1

        self.assertEqual(2, nombre_joueurs_humains)
        self.assertEqual(3, nombre_joueurs_ordinateurs)

    def test_trouver_joueurs_au_plus_haut_total(self):
        partie = Partie(5, 4)
        joueurs = [Joueur(1), Joueur(2), Joueur(3), Joueur(4), Joueur(5)]
        # Initialisation de leurs dés
        joueurs[0].dés = [Dé(5), Dé(2)]
        joueurs[1].dés = [Dé(1), Dé(2)]
        joueurs[2].dés = [Dé(3), Dé(5)]
        joueurs[3].dés = [Dé(6), Dé(6)]
        joueurs[4].dés = [Dé(2), Dé(4)]

        # Cas 1: Un seul joueur a le plus haut total
        self.assertEqual([joueurs[3]], partie.trouver_joueurs_au_plus_haut_total(joueurs))

        # Cas 2: Deux joueurs sont à égalité avec le plus haut total
        joueurs[1].dés = [Dé(6), Dé(5)]
        joueurs[3].dés = [Dé(6), Dé(5)]
        liste_joueurs_plus_haut_total = partie.trouver_joueurs_au_plus_haut_total(joueurs)
        self.assertIn(joueurs[1], liste_joueurs_plus_haut_total)
        self.assertIn(joueurs[3], liste_joueurs_plus_haut_total)

        # Cas 3: Trois joueurs sont à égalité avec le plus haut total
        joueurs[1].dés = [Dé(4), Dé(6)]
        joueurs[3].dés = [Dé(6), Dé(4)]
        joueurs[4].dés = [Dé(6), Dé(4)]
        liste_joueurs_plus_haut_total = partie.trouver_joueurs_au_plus_haut_total(joueurs)
        self.assertIn(joueurs[1], liste_joueurs_plus_haut_total)
        self.assertIn(joueurs[3], liste_joueurs_plus_haut_total)
        self.assertIn(joueurs[4], liste_joueurs_plus_haut_total)

    def test_trouver_indices_max(self):

        self.assertEqual([1], Partie.trouver_indices_max([5, 11, 9, 10, 6]))
        self.assertEqual([2], Partie.trouver_indices_max([1, 2, 3]))
        self.assertEqual([2, 3, 4], Partie.trouver_indices_max([1, 2, 3, 3, 3]))

    def test_determiner_joueur_suivant(self):

        partie = Partie(7, 6)
        partie.joueur_courant = partie.joueurs[5]

        # Cas 1: Sens horaire, on passe au prochain avec un retour au premier joueur
        partie.sens = 1
        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[6], partie.joueur_suivant)

        partie.joueur_courant = partie.joueurs[6]
        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[0], partie.joueur_suivant)

        # Cas 2: Sens anti-horaire, on passe au joueur précédent
        partie.sens = -1
        partie.joueur_courant = partie.joueurs[1]
        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[0], partie.joueur_suivant)

        partie.joueur_courant = partie.joueurs[0]
        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[6], partie.joueur_suivant)

        # Cas 3: Sens horaire, avec seulement quelques joueurs actifs.
        partie.sens = 1
        partie.joueurs_actifs = [partie.joueurs[1], partie.joueurs[4], partie.joueurs[6]]
        partie.joueur_courant = partie.joueurs[4]

        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[6], partie.joueur_suivant)

        partie.joueur_courant = partie.joueurs[6]
        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[1], partie.joueur_suivant)

        # Cas 4: Sens anti-horaire, avec seulement quelques joueurs actifs
        partie.sens = -1

        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[4], partie.joueur_suivant)

        partie.joueur_courant = partie.joueurs[1]
        partie.determiner_joueur_suivant()
        self.assertEqual(partie.joueurs[6], partie.joueur_suivant)

    def test_reinitialiser_des_joueurs(self):

        partie = Partie(5, 4)
        partie.reinitialiser_dés_joueurs()
        for joueur in partie.joueurs:
            self.assertEqual(5, len(joueur))

    def test_verifier_des_joueur_courant_pour_1_et_6(self):

        partie = Partie(2, 2)
        partie.joueurs[0].dés = [Dé(1), Dé(2), Dé(3), Dé(4), Dé(5), Dé(6)]
        partie.joueur_courant = partie.joueurs[0]
        self.assertEqual((1, 1), partie.verifier_dés_joueur_courant_pour_1_et_6())

        partie.joueurs[0].dés = [Dé(2), Dé(2), Dé(3), Dé(4), Dé(5), Dé(5)]
        self.assertEqual((0, 0), partie.verifier_dés_joueur_courant_pour_1_et_6())

        partie.joueurs[0].dés = [Dé(2), Dé(2), Dé(3), Dé(4), Dé(5), Dé(6)]
        self.assertEqual((0, 1), partie.verifier_dés_joueur_courant_pour_1_et_6())

        partie.joueurs[0].dés = [Dé(1), Dé(1), Dé(1), Dé(1), Dé(1), Dé(1)]
        self.assertEqual((6, 0), partie.verifier_dés_joueur_courant_pour_1_et_6())

    def test_deplacer_les_dés_1_et_6(self):
        partie = Partie(2, 2)
        partie.sens = 1
        partie.joueur_courant = partie.joueurs[0]
        partie.determiner_joueur_suivant()

        # Cas 1: 1 dé de valeur 1 et 1 dé de valeur 6
        partie.joueurs[0].dés = [Dé(1), Dé(2), Dé(3), Dé(4), Dé(5), Dé(6)]
        partie.joueurs[1].dés = [Dé(2), Dé(2), Dé(4)]
        partie.deplacer_les_dés_1_et_6(1, 1)

        self.assertEqual(str([Dé(2), Dé(3), Dé(4), Dé(5)]), str(partie.joueurs[0].dés))
        self.assertEqual(4, len(partie.joueurs[1]))

        # Cas 2: 5 dé de valeur 1 et 0 dé de valeur 6
        partie.joueurs[0].dés = [Dé(1), Dé(1), Dé(1), Dé(1), Dé(1)]
        partie.joueurs[1].dés = [Dé(2), Dé(2), Dé(4)]
        partie.deplacer_les_dés_1_et_6(5, 0)

        self.assertEqual(str([]), str(partie.joueurs[0].dés))
        self.assertEqual(3, len(partie.joueurs[1]))

        # Cas 3: 0 dé de valeur 1 et 5 dé de valeur 6
        partie.joueurs[0].dés = [Dé(6), Dé(6), Dé(6), Dé(6), Dé(6)]
        partie.joueurs[1].dés = [Dé(2), Dé(2), Dé(4)]
        partie.deplacer_les_dés_1_et_6(0, 5)

        self.assertEqual(str([]), str(partie.joueurs[0].dés))
        self.assertEqual(8, len(partie.joueurs[1]))

    def test_verifier_si_fin_de_ronde(self):

        partie = Partie(6, 3)
        partie.joueur_courant = partie.joueurs[4]
        self.assertFalse(partie.verifier_si_fin_de_ronde())

        partie.joueurs[4].dés = []
        self.assertTrue(partie.verifier_si_fin_de_ronde())

    def test_passer_au_prochain_joueur(self):

        partie = Partie(5, 1)
        partie.joueur_courant = partie.joueurs[0]
        partie.sens = 1

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 2)
        self.assertEqual(partie.joueur_suivant.identifiant, 3)

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 3)
        self.assertEqual(partie.joueur_suivant.identifiant, 4)

        partie.passer_au_prochain_joueur()
        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 5)
        self.assertEqual(partie.joueur_suivant.identifiant, 1)

        partie.joueurs_actifs = [partie.joueurs[0], partie.joueurs[2], partie.joueurs[4]]
        partie.joueur_suivant = partie.joueurs[0]

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 1)
        self.assertEqual(partie.joueur_suivant.identifiant, 3)

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 3)
        self.assertEqual(partie.joueur_suivant.identifiant, 5)

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 5)
        self.assertEqual(partie.joueur_suivant.identifiant, 1)

        partie.sens = -1

        partie.joueur_suivant = partie.joueurs[2]

        self.assertEqual(partie.joueur_courant.identifiant, 5)
        self.assertEqual(partie.joueur_suivant.identifiant, 3)

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 3)
        self.assertEqual(partie.joueur_suivant.identifiant, 1)

        partie.passer_au_prochain_joueur()
        self.assertEqual(partie.joueur_courant.identifiant, 1)
        self.assertEqual(partie.joueur_suivant.identifiant, 5)

    def test_passer_a_la_ronde_suivante(self):

        partie = Partie(4, 4)

        partie.passer_a_la_ronde_suivante()
        self.assertEqual(2, partie.ronde)

        partie.ronde = 8
        partie.passer_a_la_ronde_suivante()
        self.assertEqual(9, partie.ronde)

    def test_jouer_dés_en_fin_de_ronde(self):

        partie = Partie(3, 2)

        partie.joueurs[0].dés = [Dé(4), Dé(5), Dé(6)]
        partie.joueurs[1].dés = [Dé(1), Dé(2)]
        partie.joueurs[2].dés = []
        partie.joueur_courant = partie.joueurs[2]

        dés_joueur0 = [Dé(4), Dé(5), Dé(6)]
        dés_joueur1 = [Dé(1), Dé(2)]

        partie.jouer_dés_en_fin_de_ronde()

        # Les dés des deux joueurs à qui il reste des dés doivent changer (petite possibilité de dés identiques)
        self.assertNotEqual(str(dés_joueur0), str(partie.joueurs[0].dés))
        self.assertNotEqual(str(dés_joueur1), str(partie.joueurs[1].dés))
        self.assertEqual([], partie.joueurs[2].dés)

    def test_ajuster_points_des_perdants_en_fin_de_ronde(self):

        partie = Partie(4, 2)
        partie.joueur_courant = partie.joueurs[0]
        partie.joueurs[0].dés = []
        partie.joueurs[1].dés = [Dé(5), Dé(3)]
        partie.joueurs[2].dés = [Dé(2)]
        partie.joueurs[3].dés = [Dé(4), Dé(1), Dé(6)]

        partie.joueurs[1].score = 10
        partie.joueurs[2].score = 35
        partie.joueurs[3].score = 8

        points_au_gagnant = partie.ajuster_points_des_perdants_en_fin_de_ronde()

        self.assertEqual(18, points_au_gagnant)
        self.assertEqual(2, partie.joueurs[1].score)
        self.assertEqual(33, partie.joueurs[2].score)
        self.assertEqual(0, partie.joueurs[3].score)

    def test_ajuster_points_du_gagnant(self):

        partie = Partie(3, 2)

        partie.joueur_courant = partie.joueurs[2]
        partie.joueur_courant.score = 40

        partie.ajuster_points_du_gagnant(15)

        self.assertEqual(55, partie.joueur_courant.score)

    def test_retirer_joueurs_sans_points(self):

        partie = Partie(8, 2)

        # Deux joueurs n'ont plus de points
        partie.joueurs[3].score = partie.joueurs[6].score = 0

        liste_joueurs_retires = partie.retirer_joueurs_sans_points()
        liste_joueurs_toujours_actifs = partie.joueurs[:3] + partie.joueurs[4:6] + [partie.joueurs[7]]

        # Les deux joueurs retirés sont listés dans la valeur de retour de partie.retirer_joueurs_sans_points()
        self.assertEqual([partie.joueurs[3], partie.joueurs[6]], liste_joueurs_retires)
        # La liste de joueurs actifs ne contient plus joueurs[3] et joueurs[6]
        self.assertEqual(liste_joueurs_toujours_actifs, partie.joueurs_actifs)

    def test_determiner_liste_gagnants(self):

        partie = Partie(7, 2)

        partie.joueurs[0].score = 10
        partie.joueurs[1].score = 20
        partie.joueurs[2].score = 30
        partie.joueurs[3].score = 40
        partie.joueurs[4].score = 35
        partie.joueurs[5].score = 20
        partie.joueurs[6].score = 5

        self.assertEqual([3], partie.determiner_liste_gagnants())

        partie.joueurs[6].score = partie.joueurs[0].score = 40
        self.assertEqual([0, 3, 6], partie.determiner_liste_gagnants())







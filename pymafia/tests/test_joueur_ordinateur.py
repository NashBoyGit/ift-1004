from unittest import TestCase
from pymafia.joueur_ordinateur import JoueurOrdinateur


class TestJoueurOrdinateur(TestCase):

    def test_demander_sens(self):

        joueur_ordinateur = JoueurOrdinateur(1)
        frequence_choix = {1: 0, -1: 0}
        nombre_choix = 10000
        for i in range(nombre_choix):
            frequence_choix[joueur_ordinateur.demander_sens()[0]] += 1
        # Sur 10 000 choix, s'assurer que la fréquence de 1 et -1 s'approche de 50%,
        # avec une marge d'erreur inférieure à 1%.
        for key in frequence_choix:
            self.assertLess(frequence_choix[key]/nombre_choix - 0.5, 0.02)

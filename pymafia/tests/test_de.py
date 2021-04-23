from unittest import TestCase
from pymafia.de import Dé


class TestDé(TestCase):

    def test_rouler_Dé(self):
        dé = Dé()
        frequence_lancer = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        nombre_lancers = 50000

        for i in range(nombre_lancers):
            dé.rouler()
            self.assertTrue(1 <= dé.valeur <= 6)  # Vérifie qu'un lancer donne toujours une valeur entre 1 et 6
            frequence_lancer[dé.valeur] += 1

        # Vérifie la nature aléatoire du lancer.
        # La fréquence d'une valeur ne doit pas dévier de 0,5% pour 50 000 lancers
        for i in range(1, 7):
            self.assertLess(abs(frequence_lancer[i]/nombre_lancers - 1/6), 0.02)

    def test_str(self):
        dé = Dé()
        for valeur_test in range(1, 7):
            dé.valeur = valeur_test
            self.assertEqual(dé.__repr__(), chr(9855+dé.valeur))

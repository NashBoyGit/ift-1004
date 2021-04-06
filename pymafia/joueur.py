"""
Module de la classe Joueur
"""

from pymafia.dé import Dé


class Joueur:
    """
    Classe pour un joueur du jeu pymafia

    Attributes:
        identifiant (int): Numéro d'identification du joueur
        dés (liste): liste contenant les dés du joueur
        score (int): nombre de points du joueur
    """
    identifiant = 0
    dés = []
    score = 0

    def __init__(self, identifiant):
        """
        Constructeur de la classe Joueur.
        Note: Lorsqu'un joueur est créé en début de partie, on lui donne deux dés.
        Args:
            identifiant (int): Identifiant du joueur à être instancié
        """
        self.identifiant = identifiant
        self.dés = [] 
        self.ajouter_un_dé()
        self.ajouter_un_dé()

    def rouler_dés(self):
        """
        Méthode qui modifie aléatoirement la valeur de tous les dés du joueur.
        """
        for de in self.dés:
            de.rouler()

    def compter_1_et_6(self):
        """
        Méthode qui fait le décompte des dés du joueur qui ont la valeur 1 et la valeur 6.
        Returns:
            nombre_1 (int): Nombre de dés du joueur ayant la valeur 1
            nombre_6 (int): Nombre de dés du joueur ayant la valeur 6
        """
        nombre_6 = 0
        nombre_1 = 0
        valeurs = [de.valeur for de in self.dés]
        nombre_6 = sum(map(lambda valeur : valeur == 6, valeurs))
        nombre_1 = sum(map(lambda valeur : valeur == 1, valeurs))
        return nombre_1, nombre_6
        

    def retirer_dé(self, valeur):
        """
        Méthode qui retire tous les dés du joueur ayant une certaine valeur.
        Args:
            valeur (int): Nombre entre 1 et 6 du ou des dés à retirer
        """
        for de in self.dés:
            if (de.valeur == valeur):
                self.dés.remove(de)

    def retirer_dés(self):
        """
        Méthode qui retire tous les dés du joueurs
        """
        self.dés.clear()

    def ajouter_un_dé(self):
        """
        Méthode qui ajoute un dé de valeur 6 aux dés du joueur
        """
        self.dés.append(Dé(6))

    def reinitialiser_dés(self):
        """
        Méthode qui réinitialise les dés du joueur en lui remettant 5 dés en main.
        """
        self.retirer_dés()
        for de in range(5):
            self.ajouter_un_dé()

    def calculer_points(self):
        """
        Méthode qui calcule le total de la valeur des dés du joueur.
        Returns:
            int: Total de la valeur des dés
        """
        return sum(de.valeur for de in self.dés)


    def ajuster_score_en_fin_de_tour(self):
        """
        Méthode qui modifie le score du joueur selon la valeurs des dés du joueur.
        Si la valeur des dés est inférieure ou égale au score actuel du joueur, le score du joueur est
        réduit de cette valeur, qui est aussi retournée. Autrement, le score est mis à 0 et la valeur du
        score qui restait est retournée.
        Returns:
            int: Nombre de points perdus par le joueur en fin de tour et donnés au gagnant.
        """
        if self.calculer_points > self.score:
            nbr_points_perdus=self.calculer_points-self.score
            self.score = 0
            return nbr_points_perdus
        else:
            self.score = self.score - self.calculer_points
            return self.calculer_points
        

    def __eq__(self, other):
        """
        Méthode qui définit l'opérateur == pour la classe joueur
        Args:
            other (Joueur): autre objet joueur pour la comparaison
        Returns:
            bool: True si c'est le même joueur, False autrement
        """
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Méthode qui définit l'opérateur != pour la classe joueur
        Args:
            other (Joueur): autre objet joueur pour la comparaison
        Returns:
            bool: True si ce n'est pas le même joueur, False autrement
        """
        return not self == other

    def __len__(self):
        """
        Méthode qui retourne le nombre de dés du joueur.
        Returns:
            int: Nombre de dés du joueur
        """
        return len(self.dés)

    def __str__(self):
        """
        Méthode qui retourne une chaîne de caractères représentant les dés du joueur. Celle-ci prend la forme d'une
        chaîne composée des dés. Par exemple, '⚀ ⚃ ⚃'.
        Returns:
            str: Représentation des dés du joueur.
        """
        return ' '.join(str(d) for d in self.dés)


"""
Module principal du package pymafia.
C'est ici le point d'entrée du programme.
Ce module définit 3 fonctions ainsi que les commandes principales qui lancent le jeu.
"""
from pymafia.partie import Partie


def demander_nombre_joueurs():
    """
    Fonction qui demande à l'utilisateur combien de joueurs entre 2 et 8 vont jouer une partie de pymafia.
    Les validations sont faites sur la valeur entrée par l'utilisateur et le programme redemande un nombre
    si la valeur entrée est invalide.
    Returns:
        int: le nombre de joueurs choisi par l'utilisateur
    """
    pass


def demander_nombre_joueurs_humains(nombre_joueurs):
    """
    Fonction qui demande le nombre de joueurs humains qui seront parmi les joueurs. Les autres joueurs
    seront contrôlés par l'ordinateur. Les validations sont faites sur la valeur entrée par l'utilisateur
    et le programme redemande un nombre si la valeur entrée est invalide. Cette valeur doit bien sûr être
    inférieure ou égale au nombre de joueurs.
    Args:
        nombre_joueurs (int): nombre de joueurs voulu par l'utilisateur.
    Returns:
        int: le nombre de joueurs humains choisi par l'utilisateur
    """
    pass


def afficher_instructions():
    """
    Fonction qui affiche les instructions du jeu.
    """
    pass


if __name__ == '__main__':

    print("Jouons une partie de pyMafia!\n")

    partie = Partie(4, 3)


    # Afficher les instruction

    # Demander le nombre de joueurs voulu par l'utilisateur

    # Demander le nombre de joueurs humains

    # Création de l'objet partie avec le nombre de joueurs spécifiés

    # Démarrage de cette partie.

    input('Appuyer sur ENTER pour quitter.')

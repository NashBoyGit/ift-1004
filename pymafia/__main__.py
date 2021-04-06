"""
Module principal du package pymafia.
C'est ici le point d'entrée du programme.
Ce module définit 3 fonctions ainsi que les commandes principales qui lancent le jeu.
"""
from pymafia.partie import Partie
from pymafia.joueur import Joueur

def demander_nombre_joueurs():
    """
    Fonction qui demande à l'utilisateur combien de joueurs entre 2 et 8 vont jouer une partie de pymafia.
    Les validations sont faites sur la valeur entrée par l'utilisateur et le programme redemande un nombre
    si la valeur entrée est invalide.
    Returns:
        int: le nombre de joueurs choisi par l'utilisateur
    """
    valeur_entrée=False
    while valeur_entrée == False:
        nbrs_de_joueurs = input("Combien de joueur entre 2 et 8 aller vous être")
        if nbrs_de_joueurs.isdigit():
            nbrs_de_joueurs=int(nbrs_de_joueurs)
            if nbrs_de_joueurs<=8 and nbrs_de_joueurs>=2:
                valeur_entrée=True
    return nbrs_de_joueurs


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
    valeur_entrée=False
    while valeur_entrée == False:
        nbrs_de_joueurs_humain = input("Combien de joueur humain voulez-vous avoir")
        if nbrs_de_joueurs_humain.isdigit():
            nbrs_de_joueurs_humain=int(nbrs_de_joueurs_humain)
            if nbrs_de_joueurs_humain<=nombre_joueurs and nbrs_de_joueurs_humain>=0:
                valeur_entrée=True
    return nbrs_de_joueurs_humain


def afficher_instructions():
    """
    Fonction qui affiche les instructions du jeu.

    
    """
    print("Le jeu dont vous vous apprêter à jouer ce nomme Pymafia\n")
    print("Vous pouvez jouer entre 2 et 8 joueur ordinateur y compris\n")
    print("Au départ chaque joueur dispose de 5 dés traditionnels à 6 faces et un nombre de points choisis au préalable\n")
    print("Les régles sont simples\n")
    print("Pour commencer, tout le monde lance les dés. Celui qui a le plus haut résultat décide dans qu'elle sens va le jeu et peut commencer\n")
    print("À son tour, le joueur lance les dés\n")
    print("Les dés avec une valeur 6 sont passé au prochain joueur alors que les dés avec une valeur de 1 sont retirés du jeu\n")
    print("Le but est simple, ne plus avoir de dés en sa possession avant les autres joueurs\n")
    print("Lorsqu'un joueur n'a plus de dés, les autres joueurs lance leur dés restant pour déterminer les points qu'ils perderont et donneront au gagnant du round\n")
    print("Si par malheur un joueur n'a pas assez de point, il ne donne que ce qu'il lui reste et doit quitter le jeu\n")
    print("Par la suite tout le monde récupère 5 dés et une manche est reparti\n")
    print("La partie se terminer lorsqu'il n'y a plus qu'un joueur dans le jeu\n")
    



if __name__ == '__main__':

    print("Jouons une partie de pyMafia!\n")

    # Afficher les instruction

    afficher_instructions()
    

    # Demander le nombre de joueurs voulu par l'utilisateur
    nbr_joueurs=demander_nombre_joueurs()

    # Demander le nombre de joueurs humains
    nbr_joueur_humain=demander_nombre_joueurs_humains(nbr_joueurs)
    # Création de l'objet partie avec le nombre de joueurs spécifiés
    partie=Partie(nbr_joueurs, nbr_joueur_humain)
    # Démarrage de cette partie.
    partie.jouer()
    #input('Appuyer sur ENTER pour quitter.')

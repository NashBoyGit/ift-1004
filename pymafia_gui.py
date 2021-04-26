"""
Module contenant la description d'une classe pour la fenêtre du jeu Pymafia et de classes secondaires.
"""

from pymafia.partie import Partie
from tkinter import Tk, Frame, Button, Label, StringVar, DISABLED, NORMAL


class FrameJoueur(Frame):
    """
    Classe pour les frames de tous les joueurs qui prévoit les widgets communs.
    """

    def __init__(self, joueur, parent):
        super().__init__(parent)
        self.joueur = joueur
        self.nom_joueur = StringVar()
        self.nom_joueur.set("Joueur {}".format(self.joueur.identifiant))
        self.label_nom_joueur = Label(self, textvariable=self.nom_joueur, padx=10)
        self.bouton_rouler_dés = Button(self, command=self.rouler_dés, text="Rouler\nles\ndés")

    def rouler_dés(self):
        self.joueur.rouler_dés()
        self.mettre_label_dés_a_jour()

    def mettre_label_dés_a_jour(self):
        # Méthode à être redéfinie dans les classes filles
        pass

    def activer_bouton(self):
        self.bouton_rouler_dés['state'] = NORMAL

    def inactiver_bouton(self):
        self.bouton_rouler_dés['state'] = DISABLED


class FrameJoueurGauche(FrameJoueur):
    """
    Classe pour un joueur situé à gauche du plateau de jeu
    """

    def __init__(self, joueur, parent):
        super().__init__(joueur, parent)

        self.label_nom_joueur.grid(row=0, column=0)

        self.dés_joueur1 = StringVar()
        self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
        self.dés_joueur2 = StringVar()

        self.label_dés_joueur1 = Label(self, textvariable=self.dés_joueur1, font=("Courier", 32), height=5)
        self.label_dés_joueur1.grid(row=0, column=1)
        self.label_dés_joueur2 = Label(self, textvariable=self.dés_joueur2, font=("Courier", 32), width=1)
        self.label_dés_joueur2.grid(row=0, column=2)

        self.bouton_rouler_dés.grid(row=0, column=3)

    def mettre_label_dés_a_jour(self):
        if len(self.joueur.dés) <= 5:
            self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
            self.dés_joueur2.set("")
        else:
            self.dés_joueur1.set(str(self.joueur)[0:9].replace(" ", "\n"))
            self.dés_joueur2.set(str(self.joueur)[10:].replace(" ", "\n"))


class FrameJoueurDroite(FrameJoueur):
    """
    Classe pour un joueur situé à droite du plateau de jeu
    """

    def __init__(self, joueur, parent):
        super().__init__(joueur, parent)

        self.label_nom_joueur.grid(row=0, column=3)

        self.dés_joueur1 = StringVar()
        self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
        self.dés_joueur2 = StringVar()
        self.label_dés_joueur1 = Label(self, textvariable=self.dés_joueur1, font=("Courier", 32), height=5)
        self.label_dés_joueur1.grid(row=0, column=2)
        self.label_dés_joueur2 = Label(self, textvariable=self.dés_joueur2, font=('Courier', 32), width=1)
        self.label_dés_joueur2.grid(row=0, column=1)

        self.bouton_rouler_dés.grid(row=0, column=0)

    def mettre_label_dés_a_jour(self):
        if len(self.joueur.dés) <= 5:
            self.dés_joueur1.set(str(self.joueur).replace(" ", "\n"))
            self.dés_joueur2.set("")
        else:
            self.dés_joueur1.set(str(self.joueur)[0:9].replace(" ", "\n"))
            self.dés_joueur2.set(str(self.joueur)[10:].replace(" ", "\n"))


class FrameJoueurHaut(FrameJoueur):
    """
    Classe pour un joueur situé en haut du plateau de jeu
    """

    def __init__(self, joueur, parent):
        super().__init__(joueur, parent)

        self.label_nom_joueur.grid(row=0, column=0)

        self.dés_joueur = StringVar()
        self.dés_joueur.set(str(self.joueur).replace(" ", ""))
        self.label_dés_joueur = Label(self, textvariable=self.dés_joueur, font=("Courier", 32), width=8)
        self.label_dés_joueur.grid(row=1, column=0)

        self.bouton_rouler_dés.grid(row=2, column=0)

    def mettre_label_dés_a_jour(self):
        self.dés_joueur.set(str(self.joueur).replace(" ", ""))


class FrameJoueurBas(FrameJoueur):
    """
    Classe pour un joueur situé en bas du plateau de jeu
    """

    def __init__(self, joueur, parent):
        super().__init__(joueur, parent)

        self.label_nom_joueur.grid(row=2, column=0)

        self.dés_joueur = StringVar()
        self.dés_joueur.set(str(self.joueur).replace(" ", ""))
        self.label_dés_joueur = Label(self, textvariable=self.dés_joueur, font=("Courier", 32), width=8)
        self.label_dés_joueur.grid(row=1, column=0)

        self.bouton_rouler_dés.grid(row=0, column=0)

    def mettre_label_dés_a_jour(self):
        self.dés_joueur.set(str(self.joueur).replace(" ", ""))


class FenetrePymafia(Tk):
    """
    Classe principale du module pour l'interface du jeu pymafia
    Attributes:
        partie (Partie): Données d'une partie du jeu Pymafia
        frames_joueurs (list): Liste contenant les frames des 4 joueurs de la partie. Les index sont:
        0, joueur à gauche; 1, joueur en haut; 2, joueur à droite; 3, joueur en bas
    """

    def __init__(self):

        super().__init__()
        self.title("Jeu de pymafia")
        self.resizable(0, 0)
        self.partie = Partie(4, 4)

        self.partie.reinitialiser_dés_joueurs()

        self.frames_joueurs = []

        frame_joueur_gauche = FrameJoueurGauche(self.partie.joueurs[0], self)
        self.frames_joueurs.append(frame_joueur_gauche)
        frame_joueur_haut = FrameJoueurHaut(self.partie.joueurs[1], self)
        self.frames_joueurs.append(frame_joueur_haut)
        frame_joueur_droite = FrameJoueurDroite(self.partie.joueurs[2], self)
        self.frames_joueurs.append(frame_joueur_droite)
        frame_joueur_bas = FrameJoueurBas(self.partie.joueurs[3], self)
        self.frames_joueurs.append(frame_joueur_bas)

        frame_joueur_gauche.grid(row=1, column=0)
        frame_joueur_haut.grid(row=0, column=1)
        frame_joueur_droite.grid(row=1, column=2)
        frame_joueur_bas.grid(row=2, column=1)


if __name__ == '__main__':

    fenetre_pymafia = FenetrePymafia()
    fenetre_pymafia.mainloop()


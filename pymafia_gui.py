"""
Module contenant la description d'une classe pour la fenêtre du jeu Pymafia et de classes secondaires.
"""
from tkinter.constants import NONE
from pymafia.partie import Partie
from tkinter import Tk, Frame, Button, Label, StringVar, DISABLED, NORMAL, Toplevel, Menu,simpledialog, messagebox, Checkbutton
from pymafia.partie import RONDEMAX

def demander_nombre_joueur():
    answer = simpledialog.askstring("Input", "Combien de joueurs serez-vous?",
                                parent=pymafia_fenetre)
    if (isinstance(answer, int)):
        nombre_joueurs = answer

def shows_instructions():
    messagebox.showinfo("title", "Le jeu dont vous vous apprêter à jouer ce nomme Pymafia\nVous pouvez jouer entre 2 et 4 joueur\nAu départ chaque joueur dispose de 5 dés traditionnels à 6 faces et un nombre de points choisis au préalable\n")
    messagebox.showinfo("title","Les régles sont simples\nPour commencer, tout le monde lance les dés. Celui qui a le plus haut résultat décide dans qu'elle sens va le jeu et peut commencer\nÀ son tour, le joueur lance les dés\n")
    messagebox.showinfo("title","Les dés avec une valeur 6 sont passé au prochain joueur alors que les dés avec une valeur de 1 sont retirés du jeu\nLe but est simple, ne plus avoir de dés en sa possession avant les autres joueurs\nLorsqu'un joueur n'a plus de dés, les autres joueurs lance leur dés restant pour déterminer les points qu'ils perderont et donneront au gagnant du round\n")
    messagebox.showinfo("title","Si par malheur un joueur n'a pas assez de point, il ne donne que ce qu'il lui reste et doit quitter le jeu\nPar la suite tout le monde récupère 5 dés et une manche est reparti\nLa partie se terminer lorsqu'il n'y a plus qu'un joueur dans le jeu\n")

def recommencer():
    if messagebox.askquestion("ALERTE", "Voulez-vous vraiment recommencer une partie\n Cette étape sera irréversible") == "yes":
        pymafia_fenetre.frames_joueurs[pymafia_fenetre.partie.joueur_courant.identifiant-1].inactiver_bouton()
        pymafia_fenetre.partie.preparer_une_partie()
        pymafia_fenetre.partie.reinitialiser_dés_joueurs()
        for frame in pymafia_fenetre.frames_joueurs:
            frame.mettre_label_dés_a_jour()
        pymafia_fenetre.frames_joueurs[pymafia_fenetre.partie.premier_joueur.identifiant-1].activer_bouton()

        #pymafia_fenetre.frames_joueurs[pymafia_fenetre.partie.joueur_courant.identifiant-1].mettre_label_dés_a_jour()

        # pymafia_fenetre.partie.trouver_premier_joueur()
        # print(pymafia_fenetre.partie.premier_joueur.identifiant)
        # pymafia_fenetre.frames_joueurs[pymafia_fenetre.partie.premier_joueur.identifiant-1].activer_bouton()
        # pymafia_fenetre.mainloop()

def quitter():
    if messagebox.askquestion("ALERTE", "Voulez-vous vraiment quitter le jeu\n Cette étape sera irréversible") == "yes":
        pymafia_fenetre.quit()
            

        
        
        


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
        nombre_1, nombre_6 = pymafia_fenetre.partie.verifier_dés_joueur_courant_pour_1_et_6()
        messagebox.showinfo("", f"{pymafia_fenetre.partie.message_pour_dé_1(nombre_1)}\n{pymafia_fenetre.partie.message_pour_dé_6(nombre_6)}")
        pymafia_fenetre.partie.gerer_dés_1_et_6()
        pymafia_fenetre.partie.retirer_joueurs_sans_points()
        self.inactiver_bouton()
        if pymafia_fenetre.partie.verifier_si_fin_de_ronde() == True:
            pymafia_fenetre.partie.terminer_ronde()
            if len(pymafia_fenetre.partie.joueurs_actifs) == 1 or pymafia_fenetre.partie.ronde == RONDEMAX:
                pymafia_fenetre.partie.terminer_une_partie()
            else:
                pymafia_fenetre.partie.preparer_une_partie()
                pymafia_fenetre.partie.reinitialiser_dés_joueurs()
    
                                                                         
        else:
            pymafia_fenetre.partie.passer_au_prochain_joueur()
            pymafia_fenetre.frames_joueurs[pymafia_fenetre.partie.joueur_courant.identifiant-1].activer_bouton()
            pymafia_fenetre.frames_joueurs[pymafia_fenetre.partie.joueur_courant.identifiant-1].mettre_label_dés_a_jour()
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
        self.partie.preparer_une_partie()
        #self.partie.reinitialiser_dés_joueurs()

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

        for frame in self.frames_joueurs:
            frame.inactiver_bouton()
        
        index = 0
        self.title(f"Jeu de pymafia (Ronde #{self.partie.ronde})")
        for joueur in self.partie.joueurs_actifs:
            label = Label(self, text = f"Joueur {joueur.identifiant} : {joueur.score}")
            label.place(x=0, y=index)
            index += 15


        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Démarrer", command=demander_nombre_joueur)
        filemenu.add_command(label="Recommencer", command=recommencer)
        filemenu.add_command(label="Instructions", command=shows_instructions)
        
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=quitter)
        menubar.add_cascade(label="Fichier", menu=filemenu)

        self.config(menu=menubar)

        self.frames_joueurs[self.partie.premier_joueur.identifiant-1].activer_bouton()
                    
if __name__ == '__main__':
    pymafia_fenetre = FenetrePymafia()
    pymafia_fenetre.mainloop()

"""
Module de la classe Partie
"""

from pymafia.joueur import Joueur
from pymafia.joueur_humain import JoueurHumain
from pymafia.joueur_ordinateur import JoueurOrdinateur
from random import normalvariate, shuffle

# Variable globale spécifiant le nombre maximale de rondes d'une partie du jeu pymafia
RONDEMAX = 10


class Partie:
    """
    Documentation de la classe Partie
    Attributes:
        joueurs (list): Liste des joueurs au départ de la partie
        joueurs_actifs (list): Liste des joueurs qui ont encore des points (score supérieur à 0)
        premier_joueur (Joueur): Premier joueur de la ronde
        joueur_courant (Joueur): Joueur dont c'est le tour
        joueur_suivant (Joueur): Joueur dont ce sera le tour lorsque le joueur_courant aura joué (prochain joueur actif)
        ronde (int): Nombre de la ronde actuelle
        sens (int): Nombre qui indique le sens du tour (1, croissant; -1, décroissant)
        gagnant (Joueur): Joueur qui sera déclaré gagnant de la partie, initialisé à None
    """

    joueurs = []
    joueurs_actifs = []
    premier_joueur = None
    premier_joueur = None
    joueur_courant = None
    joueur_suivant = None
    ronde = 1
    sens = 1
    gagnant = None

    def __init__(self, nombre_joueurs, nombre_joueurs_humains):
        """
        Constructeur de la classe Partie
        Args:
            nombre_joueurs (int): Nombre de joueurs de la partie
            nombre_joueurs_humains (int): Nombre de joueurs humains de la partie
        """
        self.joueurs_actifs = self.joueurs = Partie.creer_joueurs(nombre_joueurs, nombre_joueurs_humains)
        self.ronde = 1

    @staticmethod
    def creer_joueurs(nombre_joueurs, nombre_joueurs_humains):
        """
        Méthode statique qui crée la liste de joueurs de la partie.
        Dans le cas où des joueurs ordinateurs sont permis, les joueurs humains et ordinateurs sont
        mélangés au hasard dans la liste de joueurs.
        Args:
            nombre_joueurs (int): Nombre de joueurs de la partie
            nombre_joueurs_humains (int): Nombre de joueurs humains de la partie

        Returns:
            list: Liste des joueurs
        """
        joueurs = []
        for identifiant in range(nombre_joueurs):
            if identifiant < nombre_joueurs_humains: 
                joueurs.append(JoueurHumain(identifiant + 1))
            else: 
                joueurs.append(JoueurOrdinateur(identifiant + 1))
            
        #shuffle(joueurs)
        return joueurs

    def preparer_une_partie(self):
        """
        Méthode qui accomplit les actions nécessaires pour débuter une partie.
        """
        # Afficher les joueurs.
        self.afficher_joueurs()
        # Trouver le premier joueur.
        self.trouver_premier_joueur()
        # Déterminer le sens de la partie voulue par le premier joueur.
        self.determiner_sens()
        # Affecter à l'attribut du joueur_courant le premier joueur.
        self.joueur_courant = self.premier_joueur
        # Déterminer qui est le joueur suivant.
        self.determiner_joueur_suivant()
        # Réinitialiser les dés des joueurs pour que chaque joueur ait 5 dés.
        self.reinitialiser_dés_joueurs()

    def afficher_joueurs(self):
        """
        Méthode qui affiche quels joueurs sont humains et quels joueurs sont l'ordinateur.
        La version simple de cette méthode peut se limiter à lister les joueurs.
        Par exemple, "Le joueur 6 est prêt à jouer!"
        """
        # Lister l'identifiant des joueurs humains
        identifiants_joueurs_humains = []
        for joueur in self.joueurs:
            if isinstance(joueur, JoueurHumain):
                identifiants_joueurs_humains.append(str(joueur.identifiant))

        # Afficher les identifiants des joueurs humains (la chaîne est différente selon le nombre)
        if len(identifiants_joueurs_humains) == 1:
            print("Le joueur {} est le joueur humain.".format(identifiants_joueurs_humains[0]))
        elif len(identifiants_joueurs_humains) == len(self.joueurs):
            print('Tous les joueurs sont des joueurs humains!')
        elif len(identifiants_joueurs_humains) == 2:
            print("Les joueurs {} et {} sont des joueurs humains.".format(identifiants_joueurs_humains[0],
                                                                          identifiants_joueurs_humains[1]))
        else:
            liste_joueurs_humains = ", ".join(identifiants_joueurs_humains[:-1])
            print("Les joueurs {} et {} sont des joueurs humains.".format(liste_joueurs_humains,
                                                                          identifiants_joueurs_humains[-1]))
        # Si nécessaire, indiquer que l'autre joueur ou les autres joueurs sont des ordinateurs.
        nombre_joueurs_ordinateur = len(self.joueurs) - len(identifiants_joueurs_humains)
        if nombre_joueurs_ordinateur == 1:
            print("L'autre joueur est un ordinateur.\n")
        elif nombre_joueurs_ordinateur > 1:
            print("Les autres joueurs sont des ordinateurs.\n")

    def trouver_premier_joueur(self):
        """
        Méthode qui sert à déterminer qui sera le premier joueur de la première ronde. Ce joueur est celui qui obtient
        le plus haut score lorsque les joueurs lancent deux dés. En cas d'égalité, les joueurs à égalité relancent
        leurs dés jusqu'à ce qu'un seul joueurs aient le plus haut résultat.
        """
      
        joueurs_restants = self.joueurs

        while (len(joueurs_restants) > 1):
            for joueur in joueurs_restants:
                joueur.rouler_dés()
            joueurs_restants = self.trouver_joueurs_au_plus_haut_total(joueurs_restants)

        self.premier_joueur = joueurs_restants[0]

    def trouver_joueurs_au_plus_haut_total(self, liste_joueurs):
        """
        Cette méthode trouve le ou les joueurs ayant le plus haut score à leurs dés.
        Args:
            liste_joueurs (list): Liste des joueurs parmi lesquels il faut identifier ceux qui ont le plus score aux dés

        Returns:
            list: Liste des joueurs ayant eu le plus haut score. Cette liste contient plus qu'un joueur s'il y a eu
            égalité lors du lancer.
        """
        
        indices = self.trouver_indices_max([x.calculer_points() for x in liste_joueurs])
        return [self.joueurs[i] for i in indices]

    @staticmethod
    def trouver_indices_max(vecteur):
        """
        Méthode statique qui trouve les index des nombres d'un vecteur d'entiers correspondants à la valeur maximale du
        vecteur.
        Args:
            vecteur (list): Vecteur de nombre d'entiers dont il faut trouver les index des maximum
        Returns:
            list: Liste des index des éléments du vecteur ayant la valeur la plus élevée
        """
        valeur_max = max(vecteur)
        index_avec_plus_haute_valeur = []
        for i, j in enumerate(vecteur):
            if j == valeur_max:
                index_avec_plus_haute_valeur.append(i)
        return index_avec_plus_haute_valeur

    def determiner_sens(self):
        """
        Méthode qui demande au premier joueur le sens dans lequel il souhaite bouger. Cette méthode vérifie si le
        premier joueur est un humain ou l'ordinateur. Dans le cas de l'humain, une demande est faite à la console.
        L'attribut sens de la partie est modifié selon la réponse. Dans le cas de l'ordinateur, on affiche son choix.
        """
        print(f"Le premier joueur est un {'ordinateur' if isinstance(self.premier_joueur, JoueurOrdinateur) else 'humain'} (Joueur #{self.premier_joueur.identifiant})")

        if isinstance(self.premier_joueur, JoueurHumain):
            while (True):
                print("Quel sens désirez-vous?")
                sens = input("1 (Horaire)\n2 (Anti-Horaire)\nChoix : ")
                if (sens == "1" or sens == "2"): 
                    self.sens = 1 if sens == "1" else -1
                    break
                print("\nChoix invalide!\n")
        else: 
            sens = self.premier_joueur.demander_sens()
            print(f"\nEt il a choisit { 'Horaire' if self.sens == 1  else 'Anti-Horaire'}")

    def determiner_joueur_suivant(self):
        """
        Méthode qui trouve qui est le joueur suivant et qui modifie l'attribut joueur_suivant de la partie.
        """
        indice_joueur_courant = self.joueurs_actifs.index(self.joueur_courant)
        self.joueur_suivant = self.joueurs_actifs[(indice_joueur_courant+1)%len(self.joueurs)]

    def reinitialiser_dés_joueurs(self):
        """
        Méthode qui réinitialise les dés des joueurs actifs en leur donnant 5 dés chacun.
        """
        for joueur in self.joueurs_actifs:
            joueur.reinitialiser_dés()

    def jouer_une_partie(self):
        """
        Méthode qui accomplit les actions pour jouer une partie de pymafia.
        """
        # Cette méthode contient une grande boucle qui vérifie que le numéro de la ronde actuelle est inférieure ou
        # égale au nombre maximal de ronde. Chacune des itérations de la boucle permet de jouer une ronde.
        # Les étapes pour une ronde sont:
        # 1. Jouer une ronde.
        while (self.ronde <= RONDEMAX):
            self.jouer_une_ronde()
        # 2. Terminer la ronde.
            self.terminer_ronde()
        # 3. Afficher un message donnant les points en fin de ronde.
            print(self.messages_pour_points_fin_de_ronde())
        # 4. Réinitialiser les dés des joueurs.
            self.reinitialiser_dés_joueurs()
        # 5. Passer à la prochaine ronde.
            self.passer_a_la_ronde_suivante()
        


    def jouer_une_ronde(self):
        """
        Méthode qui permet de jouer une ronde. Un message de début de ronde est affiché. Ensuite faire une boucle pour
        jouer une succession de tour. On sort de la boucle lorsqu'un joueur gagne le tour.
        """
        joueur_gagnant = None
        print(f"Ronde #{self.ronde}")
        while joueur_gagnant == None:
            joueur_gagnant = self.jouer_un_tour()
        

    def jouer_un_tour(self):
        """
        Méthode qui permet à un joueur de jouer un tour:
        Returns:
            Joueur: Le joueur gagnant, si le joueur courant gagne le tour, None autrement.
        """
        # Les étapes pour jouer un tour sont:
        
        # 1) Le joueur courant roule ses dés.
        self.joueur_courant.rouler_dés()
        # 2) Le résultat du lancer est affiché.
        print(f"Joueur #{self.joueur_courant.identifiant} : {self.joueur_courant}")
        # 3) On gère les dés de valeur 1 et 6.
        self.gerer_dés_1_et_6()
        # 4) On vérifie si le joueur courant a gagné la ronde en n'ayant plus de dé. S'il gagne, on affiche un message
        # qui indique qu'il n'a plus de dé. Sinon, on passe au joueur suivant.

        if (len(self.joueur_courant.dés) == 0):
            print(f"Joueur #{self.joueur_courant.identifiant} a gagné la ronde")
            return self.joueur_courant
        else:           
            self.passer_au_prochain_joueur()
            return None
            
    def gerer_dés_1_et_6(self):
        """
        Méthode qui gère le contenu des dés du joueur courant suite à un lancer pour traiter la présence de 1 et de 6
        selon les étapes suivantes:
        """
        # Les étapes de cette méthode sont:
        # 1. Vérifier si les dés du joueur courant contiennent des 1 et des 6 et obtenir le nombre de 1 et de 6.
        nombre_1, nombre_6 = self.verifier_dés_joueur_courant_pour_1_et_6()
        # 2. Afficher les messages pour ces dés.
        self.afficher_messages_dés_1_et_6(nombre_1, nombre_6)
        # 3. Déplacer les dés 1 et 6.
        self.deplacer_les_dés_1_et_6(nombre_1, nombre_6)

    def verifier_dés_joueur_courant_pour_1_et_6(self):
        """
        Méthode qui vérifie le nombre de dés de valeur 1 et 6 du joueur courant.
        Returns:
            int, int: nombre de dés de valeur 1 et 6
        """
        nombre_6 = 0
        nombre_1 = 0
        valeurs = [de.valeur for de in self.joueur_courant.dés]
        nombre_6 = sum(map(lambda valeur : valeur == 6, valeurs))
        nombre_1 = sum(map(lambda valeur : valeur == 1, valeurs))
        return nombre_1, nombre_6

    def afficher_messages_dés_1_et_6(self, nombre_1, nombre_6):
        """
        Méthode qui affiche les messages de la présence de dés de valeur 1 et de dés de valeur 6 dans les dés du joueur
        courant. On affiche les messages que si le joueur a un dé de la valeur désignée.
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
            nombre_6 (int): Nombre de dé(s) de valeur 6
        """
        if nombre_1:
            print(self.message_pour_dé_1(nombre_1))
        if nombre_6:
            print(self.message_pour_dé_6(nombre_6))
        if nombre_1 or nombre_6:
            print()  # Affiche un ligne vide si le joueur a des 1 ou des 6

    def message_pour_dé_1(self, nombre_1):
        """
        Méthode qui retourne le message sur le nombre de dé(s) de valeur 1. Par exemple, "Le joueur 2 a roulé 2 dés de
        valeur 1 et les retire du jeu."
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
        Returns:
            str: Message contenant le nombre de dé(s) retiré
        """
        return 'Le joueur {} a roulé {} dé{} de valeur 1 et le{} retire du jeu.'.format(
                self.joueur_courant.identifiant, nombre_1, 's' if nombre_1 > 1 else '', 's' if nombre_1 > 1 else '')

    def message_pour_dé_6(self, nombre_6):
        """
        Méthode qui retourne le message sur le nombre de dé(s) de valeur 6. Par exemple, "Le joueur 4 a roulé 1 dé de
        valeur 6 et le passe au joueur suivant."
        Args:
            nombre_6 (int): Nombre de dé(s) de valeur 6
        Returns:
            str: Message contenant le nombre de dé(s) passé au suivant
        """
        return 'Le joueur {} a roulé {} dé{} de valeur 6 et le{} passe au joueur suivant.'.format(
                self.joueur_courant.identifiant, nombre_6, 's' if nombre_6 > 1 else '', 's' if nombre_6 > 1 else '')

    def deplacer_les_dés_1_et_6(self, nombre_1, nombre_6):
        """
        Méthode qui déplace les dés de valeur 1 et de valeur 6 roulés par le joueur courant. Les dés de valeur 1 sont
        retirés du jeu (penser à une méthode de la classe joueur). Les dés de valeur 6 sont passés au joueur suivant.
        Args:
            nombre_1 (int): Nombre de dé(s) de valeur 1
            nombre_6 (int): Nombre de dé(s) de valeur 6
        """
        self.joueur_courant.retirer_dé(1)
        for nombre_de in range(nombre_6):
            self.passer_dé_joueur_suivant()

    def passer_dé_joueur_suivant(self):
        """
        Méthode qui passe un dé en ajoutant un dé au joueur suivant et en retirant un dé de valeur 6 du joueur courant.
        """
        self.joueur_courant.retirer_dé(6)
        self.joueur_suivant.ajouter_un_dé()

    def verifier_si_fin_de_ronde(self):
        """
        Méthode qui vérifie si le joueur courant n'a plus de dé. Ceci signifie la fin de la ronde.
        Returns:
            bool: True, si le joueur courant n'a plus de dé. False autrement.
        """
        if (len(self.joueur_courant.dés == 0)):
            return True
        else:
            return False

    def passer_au_prochain_joueur(self):
        """
        Méthode qui change la valeur de l'attribut du joueur_courant et qui détermine le joueur suivant.
        """
        self.joueur_courant = self.joueur_suivant
        self.determiner_joueur_suivant()

    def passer_a_la_ronde_suivante(self):
        """
        Méthode qui incrémente le numéro de la ronde.
        
        """
        self.ronde += 1


    def terminer_ronde(self):
        """
        Méthode qui accomplit les actions de jeu en fin de ronde à l'aide d'autres méthodes de la classe.
        """
        # 1. Tous les joueurs qui n'ont pas gagné la ronde jouent les dés qui leur restent.
        self.jouer_dés_en_fin_de_ronde()
        # 2. Afficher les messages des points donnés par les joueurs.
        print(self.messages_pour_points_fin_de_ronde())
        # 3. Ajuster les points de perdants de la ronde et compter la somme des points destinés au gagnant.
        points_donne_par_perdants = self.ajuster_points_des_perdants_en_fin_de_ronde()
        # 4. Ajuster les points du gagnant avec les points des perdants.
        self.ajuster_points_du_gagnant(points_donne_par_perdants)
        # 5. Afficher le message qui annonce le nouveau score du gagnant.
        print(self.message_pour_points_du_gagnant(points_donne_par_perdants))
        

    def jouer_dés_en_fin_de_ronde(self):
        """
        Méthode qui fait rouler les dés des joueurs qui sont encore actifs (sauf le gagnant)
        """
        for joueur in self.joueurs_actifs:
            if len(joueur.dés) != 0:
                joueur.rouler_dés


    def messages_pour_points_fin_de_ronde(self):
        """
        Méthode qui assemble le message qui informe de la quantité de points donnés par chacun des joueurs qui ont perdu
        la ronde. Si la somme des dés donne un nombre de points inférieurs au score actuel du joueur, le nombre de
        points donnés correspond au résultat du lancer. Sinon, le nombre des points donnés correspond au score du
        joueur. Dans le premier cas, le message pourrait être : "Le joueur 2 joue les dés suivants: ⚅ ⚁ . Il donne 8
        points au gagnant de la ronde." Dans le deuxième cas, le message pourrait être: "Le joueur 5 joue les dés
        suivants: ⚅ ⚃ . La somme des dés est égale ou supérieure à son nombre de points. Il donne 7 points au gagnant
        de la ronde et se retire de la partie.
        Returns:
            str: Le message qui indique le nombre de points par chaque joueur perdant de la ronde.
        """
        message = ""
        for joueur in self.joueurs:
            message += f"Le joueur {joueur.identifiant} joue les dés {joueur.dés}."
            if joueur.calculer_points() < joueur.score:
                message += f"Il donne {joueur.calculer_points()} points au gagnant de la ronde\n"
            else: 
                message += f"La somme des dés est égale ou supérieure à son nombre de points. Il donne {joueur.score} \
                points au gagnant de la ronde et se retire de la partie.\n"
        return message


    def ajuster_points_des_perdants_en_fin_de_ronde(self):
        """
        Méthode qui ajuste les points des perdants en fin de ronde. (en utilisant la méthode appropriée de la classe
        joueur). La méthode fait aussi la somme des points ainsi retirés à ces joueurs.
        Returns:
            int: Somme des points retirés aux joueurs.
        """
        somme_points = 0
        for joueur in self.joueurs_actifs:
            somme_points += joueur.ajuster_score_en_fin_de_tour()
        
        return somme_points

    def ajuster_points_du_gagnant(self, score):
        """
        Méthode qui ajuste le score du gagnant de la ronde (le joueur courant).
        Args:
            score (int): Le nombre de points à ajouter au score du joueur courant.
        """
        self.joueur_courant.score += score



    def message_pour_points_du_gagnant(self, points_au_gagnant):
        """
        Méthode qui retourne un message annonçant le nombre de points donnés au gagnant. Par exemple: "Le joueur 3
        obtient 18 points.
        Args:
            points_au_gagnant (int): Nombre de points donnés au gagnant.
        Returns:
            str: Chaîne de caractères contenant le message.
        """
        return f"Le joueur {self.joueur_courant.identifiant} obtient {points_au_gagnant} points."

    def retirer_joueurs_sans_points(self):
        """
        Méthode qui vérifie si des joueurs actifs ont maintenant un score de 0. Seuls les joueurs ayant un score plus
        grand que zéro demeurent actifs. Advenant que le joueur suivant ne soit plus actif, le prochain joueur actif
        devient le nouveau joueur suivant.
        Returns:
            list: La liste des joueurs à retirer. (Cette valeur de retour ne devrait pas être utilisée dans le TP3, mais
            sera utile pour le TP4.
        """
        joueur_a_retire=[]
        for joueur in self.joueurs_actifs:
            if joueur.score == 0:
                joueur_a_retire.append(joueur)
        

    def terminer_une_partie(self):
        """
        Méthode qui fait les affichages de fin de partie en déterminant le gagnant.
        """
        # On informe les joueurs que le nombre maximal de rondes est atteint.
        # Ensuite, on affiche le bilan des points des joueurs de la partie.
        # On détermine le gagnant et on en informe les utilisateurs
        print(f"La ronde {RONDEMAX} vient de finir ce qui met fin a la partie")
        for joueur in self.joueurs:
            print(f"Le joueur{joueur.identifiant} a accumule un score de {joueur.score}")
        joueur_gagnant = 0

        print("Merci d'avoir joué à pymafia!")

    def message_points_en_fin_de_partie(self):
        """
        Méthode qui assemble un message sur les points des joueurs en fin de partie. Par exemple, "À la fin de la partie
        ronde, les joueurs ont les points suivants: Le joueur 1 a 16 points. ..." Et ainsi de suite pour tous les
        joueurs.
        Returns:
            str: Le message qui donne les points en fin de partie.
        """
        message = "À la fin de la partie, les joueurs ont les points suivants:\n"
        message += self.message_points_des_joueurs()
        return message

    def message_points_des_joueurs(self):
        """
        Méthode qui assemble un message indiquant les points de tous les joueurs. Par exemple, "Le joueur 1 a 16
        points. ..." Et ainsi de suite pour tous les joueurs.
        Returns:
            str: Les message donnant les points des joueurs.
        """
        message = ""
        for joueur in self.joueurs:
            message += "Le joueur {} a {} point{}.\n".format(
                joueur.identifiant, joueur.score, 's' if joueur.score > 0 else '')
        return message

    def determiner_liste_gagnants(self):
        """
        Méthode qui détermine l'index des joueurs ayant le score le plus élevé.
        Returns:
            list: Liste contenant les indices des joueurs ayant le plus haut score. Il y a plus d'un joueur dans cette
            liste seulement s'il y a égalité.
        """
        liste_points_joueurs = []
        for joueur in self.joueurs:
            liste_points_joueurs.append(joueur.score)
        return Partie.trouver_indices_max(liste_points_joueurs)

    def message_gagnants(self, liste_index_gagnants):
        """
        Méthode qui assemble le message annonçant le gagnant (ou les gagnant en cas d'égalité). Par exemple, "Le joueur
        3 a gagné la partie!"
        Args:
            liste_index_gagnants (list): Liste contenant l'index (qui est l'identifiant) du ou des joueurs gagnants
        Returns:
            str: Message annonçant le gagnant.
        """
        if len(liste_index_gagnants) == 1:
            message = "Le joueur {} a gagné à la partie!\n".format(self.joueurs[liste_index_gagnants[0]].identifiant)
        else:
            message = "Il y a égalité entre les joueurs {}.\n".format(" et ").join(
                str(self.joueurs[gagnant].identifiant) for gagnant in liste_index_gagnants)
        return message

    def jouer(self):
        """
        Méthode principale de la classe qui spécifie le déroulement d'une partie.
        """
        # Les étapes sont:
        # 1) préparer une partie;
        self.preparer_une_partie()
        # 2) jouer une partie et
        self.jouer_une_partie()
        # 3) terminer une partie.
        self.terminer_une_partie()

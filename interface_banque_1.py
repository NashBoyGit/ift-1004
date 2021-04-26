"""Un module d'interface pour la banque.

"""
from tkinter import Tk, Toplevel, Label, Listbox, Frame, Entry, Button, END, NORMAL, E, DISABLED
from banque import Banque, Client


class BanqueGraphique(Tk):
    """Classe principale de l'interface de la banque. Nous héritons de "Tk", la classe représentant la fenêtre principale
    d'une application tkinter.

    Attributes:
        banque (Banque): La banque liée à l'interface
        compte_selectionne (Compte): Référence vers le compte actuellement sélectionnée dans l'interface.

    """
    def __init__(self):
        # On appelle le constructeur de la classe Tk.
        super().__init__()

        # On crée une instance de la banque. On pourra donc utiliser ses attributs et méthodes avec self.banque.attribut, self.banque.methode, etc.
        self.banque = Banque()

        # On crée également un attribut qui servira à se "rappeler" du compte sélectionné.
        self.compte_selectionne = None

        # Manière intéressante de changer la police de caractères pour tous les widgets de l'interface.
        self.option_add("*Font", "DejaVu")

        # On change le titre de la fenêtre. La méthode "title" est une méthode de la classe mère (Tk).
        self.title("Banque")

        # Liste des clients. Mettre à jour en appelant la méthode mise_a_jour_interface().
        Label(self, text="Clients").grid(row=0, column=0, padx=10, pady=10)
        self.widget_clients = Listbox(self, exportselection=False)
        self.widget_clients.grid(row=1, column=0, padx=10, pady=10)

        # On lie l'événement de sélection à la méthode qui affiche les comptes du client.
        self.widget_clients.bind('<<ListboxSelect>>', self.mettre_a_jour_comptes)

        # Liste des comptes pour un client donné.
        Label(self, text="Comptes").grid(row=0, column=1, padx=10, pady=10)
        self.widget_comptes = Listbox(self, exportselection=False)
        self.widget_comptes.grid(row=1, column=1, padx=10, pady=10)

        # On lie l'événement de sélection à la méthode qui affiche le contenu du compte.
        self.widget_comptes.bind('<<ListboxSelect>>', self.mettre_a_jour_info_compte)

        # Contenu d'un compte.
        Label(self, text="Gestion du compte").grid(row=0, column=3, padx=10, pady=10)
        cadre_compte = Frame(self)
        cadre_compte.grid(row=1, column=3, padx=10, pady=10)
        Label(cadre_compte, text="Numéro: ").grid(row=0, column=0, padx=10, sticky=E)
        Label(cadre_compte, text="Type: ").grid(row=1, column=0, padx=10, sticky=E)
        Label(cadre_compte, text="Solde: ").grid(row=2, column=0, padx=10, sticky=E)
        self.entree_numero = Entry(cadre_compte, state="readonly")
        self.entree_numero.grid(row=0, column=1)
        self.entree_type = Entry(cadre_compte, state="readonly")
        self.entree_type.grid(row=1, column=1)
        self.entree_solde = Entry(cadre_compte, state="readonly")
        self.entree_solde.grid(row=2, column=1)

        # Boutons de dépôt et retrait. Non disponibles tant que nous n'avons pas sélectionné un compte.
        cadre_boutons = Frame(cadre_compte)
        cadre_boutons.grid(row=3, column=1, pady=10)
        self.bouton_depot = Button(cadre_boutons, text="Dépôt", state=DISABLED, command=self.deposer)
        self.bouton_depot.grid(row=3, column=0)
        self.bouton_retrait = Button(cadre_boutons, text="Retrait", state=DISABLED, command=self.retirer)
        self.bouton_retrait.grid(row=3, column=1)

        # On ajoute les clients de la banque (pour tests seulement).
        # Dans la "vraie vie", on pourrait par exemple avoir un fichier (ou une base de données) contenant
        # ces informations et les charger à l'ouverture de la fenêtre.
        self.initialiser_clients_bidons()

        # On remplit l'interface avec des clients bidon.
        self.mettre_a_jour_interface()

    def initialiser_clients_bidons(self):
        """Ajoute des clients bidon à la banque. Dans la "vraie vie", on ajouterait la
        possiblité de sauvegarder et charger les informations d'une banque à partir d'un
        fichier, par exemple.

        """
        c_1 = Client("Jane Doe")
        c_1.ajouter_compte(1)
        c_1.ajouter_compte(2)
        c_1.deposer_dans_compte(1, 1000)
        c_1.retirer_dans_compte(2, 500)
        c_1.deposer_dans_compte(2, 250.25)

        c_2 = Client("John Doe")
        c_2.ajouter_compte(1)
        c_2.deposer_dans_compte(1, 10000)

        self.banque.ajouter_client(c_1)
        self.banque.ajouter_client(c_2)
        self.banque.recuperer_client("Jane Doe").ajouter_compte_sans_dette(3)
        self.banque.recuperer_client("Jane Doe").deposer_dans_compte(3, 1000)

    def mettre_a_jour_interface(self):
        """Méthode appelée pour mettre à jour les différents éléments de l'interface en fonction
        du contenu de la banque, puis de ce qui est sélectionné dans l'interface.

        """
        # Mise à jour de la liste de clients.
        self.widget_clients.delete(0, END)

        for client in self.banque.clients:
            self.widget_clients.insert(END, client.nom)

        # On déselectionne.
        self.widget_clients.selection_clear(0, END)

        # On vide la liste des comptes.
        self.widget_comptes.delete(0, END)

        # On vide le contenu de la gestion du compte
        self.desactiver_gestion_compte()

    def mettre_a_jour_comptes(self, evenement=None):
        """Met à jour la liste des comptes affichés. Réinitialise le compte affiché.

        Args:
            evenement (Event): Objet reçu de la part de tkinter. Nous n'en avons pas besoin, alors on
                met sa valeur par défaut à None.

        """
        # On récupère quel client est sélectionné.
        index_clique = int(self.widget_clients.curselection()[0])
        valeur = self.widget_clients.get(index_clique)

        # Mise à jour de la liste de comptes (en fonction du client sélectionné)
        self.widget_comptes.delete(0, END)

        client = self.banque.recuperer_client(valeur)
        for numero, compte in client.comptes.items():
            self.widget_comptes.insert(END, str(numero))

        # On désactive la gestion du compte.
        self.desactiver_gestion_compte()

    def desactiver_gestion_compte(self):
        """Désactive les éléments d'interface liés à la gestion du compte, et remet à None
        le compte sélectionné.

        """
        self.compte_selectionne = None

        self.entree_numero['state'] = NORMAL
        self.entree_type['state'] = NORMAL
        self.entree_solde['state'] = NORMAL

        self.entree_numero.delete(0, END)
        self.entree_type.delete(0, END)
        self.entree_solde.delete(0, END)

        self.entree_numero['state'] = 'readonly'
        self.entree_type['state'] = 'readonly'
        self.entree_solde['state'] = 'readonly'
        self.bouton_depot['state'] = DISABLED
        self.bouton_retrait['state'] = DISABLED

    def mettre_a_jour_info_compte(self, evenement=None):
        """En fonction des autres éléments d'interface, met à jour le contenu lié au compte
        sélectionné. Met à jour l'attribut self.compte_selectionne pour usage futur.

        Args:
            evenement (Event): Objet reçu de la part de tkinter. Nous n'en avons pas besoin, alors on
                met sa valeur par défaut à None.

        """
        # On récupère quel client et quel compte est sélectionné.
        index_client = self.widget_clients.curselection()[0]
        nom_client = self.widget_clients.get(index_client)
        index_compte = int(self.widget_comptes.curselection()[0])
        numero_compte = int(self.widget_comptes.get(index_compte))

        # On récupère l'objet de type Compte, et on place sa référence dans L'attribut
        # self.compte_selectionne. Note: modifier le compte via cet attribut modifiera
        # également le compte dans la hiérarchie d'objets de la banque!
        objet_compte = self.banque.recuperer_client(nom_client).comptes[numero_compte]
        self.compte_selectionne = objet_compte

        # Gestion des éléments d'interface.
        self.entree_numero['state'] = NORMAL
        self.entree_type['state'] = NORMAL
        self.entree_solde['state'] = NORMAL

        self.entree_numero.delete(0, END)
        self.entree_type.delete(0, END)
        self.entree_solde.delete(0, END)
        self.entree_numero.insert(END, numero_compte)
        self.entree_type.insert(END, objet_compte.__class__.__name__)
        self.entree_solde.insert(END, objet_compte.solde)

        self.entree_numero['state'] = 'readonly'
        self.entree_type['state'] = 'readonly'
        self.entree_solde['state'] = 'readonly'

        # On active les boutons de dépôt et de retrait
        self.bouton_depot['state'] = NORMAL
        self.bouton_retrait['state'] = NORMAL

    def deposer(self):
        """Effectue un dépôt dans le compte sélectionné.

        """
        # On demande le montant à l'utilisateur.
        fenetre_depot = FenetreDepotRetrait(self, sorte="dépôt")
        self.wait_window(fenetre_depot)

        # On fait le dépôt dans le compte sélectionné.
        if self.compte_selectionne is not None:
            # TODO: Lorsque nous connaîtrons la gestion des erreurs,
            # TODO: nous pourrons faire des validations supplémentaires ici.
            self.compte_selectionne.deposer(fenetre_depot.valeur)

        # On met à jour l'interface.
        self.mettre_a_jour_info_compte(evenement=None)

    def retirer(self):
        """Effectue un retrait dans le compte sélectionné.

        """
        # On demande le montant à l'utilisateur.
        fenetre_retrait = FenetreDepotRetrait(self, sorte="retrait")
        self.wait_window(fenetre_retrait)

        # On fait le dépôt dans le compte sélectionné.
        if self.compte_selectionne is not None:
            # TODO: Lorsque nous connaîtrons la gestion des erreurs,
            # TODO: nous pourrons faire des validations supplémentaires ici.
            self.compte_selectionne.retirer(fenetre_retrait.valeur)

        # On met à jour l'interface.
        self.mettre_a_jour_info_compte(evenement=None)


class FenetreDepotRetrait(Toplevel):
    """Un exemple de fenêtre qui "popup", utilisée pour les dépôts et les retraits.

    Args:
        master (widget): Le "master" de la fenêtre.
        sorte (str): Sorte d'opération ('dépôt' ou 'retrait').

    Attributes:
        valeur (float): La valeur du dépôt/retrait.

    """
    def __init__(self, master, sorte="dépôt"):
        super().__init__(master)

        # On prend le contrôle de l'application
        self.master = master
        self.transient(master)
        self.grab_set()

        Label(self, text="Entrez le montant du {}".format(sorte)).grid()
        self.entree = Entry(self)
        self.entree.grid()

        self.bouton_ok = Button(self, text="OK", command=self.fermer)
        self.bouton_ok.grid(padx=10, pady=10)

    def fermer(self):
        """Affecte l'attribut "valeur" à la valeur choisie, et fermer la fenêtre.

        """
        # TODO: Lorsque nous connaîtrons la gestion des erreurs,
        # TODO: nous pourrions valider le contenu de l'entrée
        # TODO: avant de fermer.

        # On sauvegarde le résultat.
        self.valeur = float(self.entree.get())

        # On redonne le contrôle au parent.
        self.grab_release()
        self.master.focus_set()
        self.destroy()


if __name__ == '__main__':
    # Instanciation de la fenêtre et démarrage de sa boucle principale.
    fenetre = BanqueGraphique()
    fenetre.mainloop()

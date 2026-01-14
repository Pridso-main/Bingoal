import customtkinter as ctk
import json
from datetime import datetime

class BingoTile(ctk.CTkButton):
    """
    Une case de Bingo. C'est un bouton qui change de couleur quand on clique dessus.
    """
    def __init__(self, master, index, data, on_click_callback):
        self.index = index
        self.data = data
        self.callback = on_click_callback
        
        # Définition de la couleur selon la difficulté (Poids)
        # 1 étoile = Vert, 2 étoiles = Jaune/Or, 3 étoiles = Rouge
        colors = {1: "#27ae60", 2: "#f39c12", 3: "#c0392b"}
        base_color = colors.get(data['poids'], "#3498db")

        # Texte du bouton : Titre + Etoiles
        texte_bouton = f"{data['titre']}\n{'★' * data['poids']}"
        
        # Si la case est déjà validée, on la grise
        etat = "normal"
        couleur = base_color
        if data['valide']:
            etat = "disabled"
            couleur = "#2c3e50" # Gris foncé
            texte_bouton = f"✅\n{data['titre']}"

        super().__init__(
            master,
            text=texte_bouton,
            font=("Arial", 12, "bold"),
            fg_color=couleur,
            height=80, # Hauteur de la case
            command=self.action_clic,
            state=etat
        )

    def action_clic(self):
        """Quand on clique, on appelle la fonction de validation du parent"""
        self.callback(self.index)


class GridScreen(ctk.CTkFrame):
    """
    L'écran principal du jeu avec la grille 5x5
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.config_file = "data/bingo_config.json"
        
        # 1. Chargement des données
        with open(self.config_file, "r", encoding="utf-8") as f:
            self.data_global = json.load(f)
            self.objectifs = self.data_global["objectifs"]

        # 2. Barre de titre et progression (Simplifié pour ce test)
        self.label_info = ctk.CTkLabel(self, text="Mon Bingoal 2026", font=("Arial", 24, "bold"))
        self.label_info.pack(pady=20)

        # 3. La Grille
        self.frame_grille = ctk.CTkFrame(self)
        self.frame_grille.pack(fill="both", expand=True, padx=20, pady=20)

        # Configuration de la grille 5x5 (poids égal pour centrer)
        for i in range(5):
            self.frame_grille.grid_columnconfigure(i, weight=1)
            self.frame_grille.grid_rowconfigure(i, weight=1)

        # Création des 25 boutons
        self.boutons = []
        for i, obj in enumerate(self.objectifs):
            row = i // 5
            col = i % 5
            
            btn = BingoTile(self.frame_grille, i, obj, self.valider_case)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.boutons.append(btn)

    def valider_case(self, index):
        """Marque une case comme validée et sauvegarde"""
        print(f"✅ Case {index} validée !")
        
        # Mise à jour des données en mémoire
        self.objectifs[index]['valide'] = True
        self.objectifs[index]['date_validation'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Mise à jour visuelle du bouton (on le désactive)
        self.boutons[index].configure(fg_color="#2c3e50", state="disabled", text=f"✅\n{self.objectifs[index]['titre']}")

        # Sauvegarde immédiate dans le JSON
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.data_global, f, indent=4, ensure_ascii=False)
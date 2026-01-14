import customtkinter as ctk
import json
import os

class GoalRow(ctk.CTkFrame):
    """
    Composant IHM représentant une ligne d'objectif dans la grille.
    Chaque ligne permet de définir un titre et une difficulté (poids).
    """
    def __init__(self, master, index, default_text="", default_weight=1):
        super().__init__(master, fg_color="transparent")
        
        # Index de la case (1 à 25)
        self.label = ctk.CTkLabel(self, text=f"{index+1:02d}.", width=40, font=("Helvetica", 12, "bold"))
        self.label.pack(side="left", padx=5)

        # Champ de saisie pour l'objectif
        self.entry = ctk.CTkEntry(self, placeholder_text="Ex: Finir mon projet Python...", height=35)
        self.entry.insert(0, default_text)
        self.entry.pack(side="left", padx=5, fill="x", expand=True)

        # Sélecteur de difficulté (Poids de 1 à 3)
        # On mappe les étoiles aux valeurs numériques
        self.diff_map = {1: "★", 2: "★★", 3: "★★★"}
        self.reverse_map = {v: k for k, v in self.diff_map.items()}
        
        self.difficulty_selector = ctk.CTkSegmentedButton(
            self, 
            values=["★", "★★", "★★★"],
            selected_color="#3b8ed0",
            selected_hover_color="#36719f"
        )
        self.difficulty_selector.set(self.diff_map.get(default_weight, "★"))
        self.difficulty_selector.pack(side="right", padx=5)

    def get_data(self):
        """Récupère les informations saisies sur la ligne."""
        return {
            "titre": self.entry.get(),
            "poids": self.reverse_map.get(self.difficulty_selector.get(), 1),
            "valide": False,
            "date_validation": None
        }

class SetupScreen(ctk.CTkFrame):
    """
    IHM de la Phase 1 : Configuration du Bingoal.
    Permet de valider les objectifs issus du CSV et de fixer les récompenses.
    """
    def __init__(self, master, initial_data=None, on_save_callback=None):
        super().__init__(master)
        self.on_save_callback = on_save_callback
        
        # Configuration du layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. En-tête
        self.header = ctk.CTkLabel(
            self, 
            text="🎯 Configuration de votre Bingoal 2026", 
            font=("Helvetica", 24, "bold")
        )
        self.header.pack(pady=20)

        # 2. Zone défilante pour les 25 objectifs
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            label_text="Vérifiez vos 25 objectifs et ajustez la difficulté",
            label_font=("Helvetica", 14, "bold"),
            fg_color="gray15"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.goal_rows = []
        for i in range(25):
            # On récupère les données si elles existent (via le parser CSV)
            txt = ""
            poids = 1
            if initial_data and i < len(initial_data['objectifs']):
                txt = initial_data['objectifs'][i].get('titre', "")
                poids = initial_data['objectifs'][i].get('poids', 1)
            
            row = GoalRow(self.scroll_frame, i, default_text=txt, default_weight=poids)
            row.pack(fill="x", pady=5, padx=10)
            self.goal_rows.append(row)

        # 3. Section des Récompenses (Paliers)
        self.rewards_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.rewards_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(
            self.rewards_frame, 
            text="🎁 Vos Récompenses par Palier", 
            font=("Helvetica", 16, "bold"),
            text_color="#e67e22"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        self.reward_entries = {}
        paliers = [
            ("🥉 Bronze (25%)", "bronze"),
            ("🥈 Argent (50%)", "argent"),
            ("🥇 Or (75%)", "or"),
            ("💎 Platine (100%)", "platine")
        ]

        for i, (label, key) in enumerate(paliers):
            ctk.CTkLabel(self.rewards_frame, text=label, font=("Helvetica", 12)).grid(row=i+1, column=0, padx=20, pady=5, sticky="e")
            entry = ctk.CTkEntry(self.rewards_frame, width=500, placeholder_text=f"Récompense pour le palier {key}...")
            # Pré-remplissage si data dispo
            if initial_data and key in initial_data['recompenses']:
                entry.insert(0, initial_data['recompenses'][key])
            entry.grid(row=i+1, column=1, padx=20, pady=5, sticky="w")
            self.reward_entries[key] = entry

        # 4. Bouton de validation final
        self.start_button = ctk.CTkButton(
            self, 
            text="CRÉER MON BINGOAL 🚀", 
            font=("Helvetica", 16, "bold"),
            height=50,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.save_configuration
        )
        self.start_button.pack(pady=20)

    def save_configuration(self):
        """Récupère toutes les données et les sauvegarde dans data/bingo_config.json"""
        final_data = {
            "version": "1.0",
            "objectifs": [row.get_data() for row in self.goal_rows],
            "recompenses": {k: v.get() for k, v in self.reward_entries.items()},
            "stats": {
                "total_poids": sum(row.get_data()['poids'] for row in self.goal_rows),
                "date_creation": "2026-01-14"
            }
        }

        # Création du dossier data s'il n'existe pas
        if not os.path.exists("data"):
            os.makedirs("data")

        # Sauvegarde JSON
        with open("data/bingo_config.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

        print("✅ Phase 1 terminée : Configuration enregistrée dans data/bingo_config.json")
        
        # Appel du callback pour dire au main.py de changer de vue
        if self.on_save_callback:
            self.on_save_callback()
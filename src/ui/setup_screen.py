import customtkinter as ctk
import json

class GoalRow(ctk.CTkFrame):
    """Composant personnalisé pour une ligne d'objectif"""
    def __init__(self, master, index, default_text=""):
        super().__init__(master)
        
        # Numéro de la case (1 à 25)
        self.label = ctk.CTkLabel(self, text=f"{index+1:02d}.", width=30)
        self.label.pack(side="left", padx=5)

        # Champ de texte pour l'objectif
        self.entry = ctk.CTkEntry(self, placeholder_text="Titre de l'objectif...", width=300)
        self.entry.insert(0, default_text)
        self.entry.pack(side="left", padx=5, fill="x", expand=True)

        # Sélecteur de difficulté (Poids)
        self.difficulty = ctk.CTkSegmentedButton(self, values=["★", "★★", "★★★"])
        self.difficulty.set("★") # Par défaut
        self.difficulty.pack(side="right", padx=5)

    def get_data(self):
        """Récupère les infos de la ligne"""
        mapping = {"★": 1, "★★": 2, "★★★": 3}
        return {
            "titre": self.entry.get(),
            "poids": mapping[self.difficulty.get()],
            "valide": False,
            "date_validation": None
        }

class SetupScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        # --- TITRE ---
        ctk.CTkLabel(self, text="⚙️ Configuration du Bingoal", font=("Helvetica", 20, "bold")).pack(pady=10)

        # --- ZONE D'OBJECTIFS (Scrollable) ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Les 25 Objectifs (Colonnes B, I, N, G, O)", height=400)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.goal_rows = []
        for i in range(25):
            row = GoalRow(self.scroll_frame, i)
            row.pack(fill="x", pady=2, padx=5)
            self.goal_rows.append(row)

        # --- RÉCOMPENSES ---
        self.recompenses_frame = ctk.CTkFrame(self)
        self.recompenses_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.recompenses_frame, text="🎁 Paliers de Récompenses", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        self.rewards = {}
        paliers = [("🥉 Bronze (25%)", "bronze"), ("🥈 Argent (50%)", "argent"), 
                   ("🥇 Or (75%)", "or"), ("💎 Platine (100%)", "platine")]
        
        for i, (label, key) in enumerate(paliers):
            ctk.CTkLabel(self.recompenses_frame, text=label).grid(row=i+1, column=0, padx=10, sticky="e")
            entry = ctk.CTkEntry(self.recompenses_frame, width=400)
            entry.grid(row=i+1, column=1, padx=10, pady=2, sticky="w")
            self.rewards[key] = entry

        # --- BOUTON FINAL ---
        self.btn_save = ctk.CTkButton(self, text="Lancer le Bingoal ! 🚀", 
                                      command=self.save_and_start, 
                                      fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_save.pack(pady=20)

    def save_and_start(self):
        """Compile toutes les données et crée le fichier JSON"""
        config = {
            "objectifs": [row.get_data() for row in self.goal_rows],
            "recompenses": {k: v.get() for k, v in self.rewards.items()},
            "date_creation": "2026-01-14" # On pourra ajouter un sélecteur de date ici
        }
        
        with open("data/bingo_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print("Configuration sauvegardée ! Passage à la Phase 2...")
        # Ici on appellera la fonction pour changer de vue
import customtkinter as ctk
import json
from datetime import datetime

class BingoTile(ctk.CTkButton):
    """
    Une tuile de Bingo intelligente (Switch ON/OFF).
    """
    def __init__(self, master, index, data, on_click_callback):
        self.index = index
        self.poids = data['poids']
        self.titre = data['titre']
        self.callback = on_click_callback
        
        self.colors = {1: "#27ae60", 2: "#f39c12", 3: "#c0392b"}
        self.base_color = self.colors.get(self.poids, "#3498db")

        super().__init__(
            master,
            font=("Arial", 11, "bold"),
            border_width=2,
            border_color="#34495e",
            hover_color="#34495e",
            command=self.on_click
        )
        
        self.update_visuals(data['valide'])

    def on_click(self):
        self.callback(self.index)

    def update_visuals(self, is_valid):
        if is_valid:
            self.configure(fg_color="#2c3e50", text=f"✅\n{self.titre}")
        else:
            self.configure(fg_color=self.base_color, text=f"{self.titre}\n{'★' * self.poids}")


class GridScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.config_file = "data/bingo_config.json"
        
        # Chargement des données
        with open(self.config_file, "r", encoding="utf-8") as f:
            self.full_data = json.load(f)
        
        self.objectifs = self.full_data['objectifs']
        self.recompenses = self.full_data['recompenses']
        self.total_weight = sum(obj['poids'] for obj in self.objectifs)

        self.setup_ui()
        self.update_progress_display()

    def get_days_remaining(self):
        """Calcule le nombre de jours restants jusqu'à la fin de 2026."""
        # Date cible : 31 Décembre 2026
        target_date = datetime(2026, 12, 31)
        now = datetime.now()
        
        delta = target_date - now
        return max(0, delta.days) # On ne retourne pas de négatif

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        # --- HEADER AMÉLIORÉ ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
        
        # On divise le header en 2 colonnes : Gauche (Progression), Droite (Temps)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # 1. Label Progression (Gauche)
        self.lbl_progress = ctk.CTkLabel(self.header_frame, text="Progression : 0%", font=("Arial", 20, "bold"))
        self.lbl_progress.grid(row=0, column=0, sticky="w")

        # 2. Label Compte à rebours (Droite)
        jours_restants = self.get_days_remaining()
        self.lbl_timer = ctk.CTkLabel(
            self.header_frame, 
            text=f"⏳ J-{jours_restants}", 
            font=("Arial", 20, "bold"),
            text_color="#e74c3c" if jours_restants < 100 else "#3498db" # Rouge si urgence (<100 jours)
        )
        self.lbl_timer.grid(row=0, column=1, sticky="e")

        # 3. Barre de progression (Dessous, prend toute la largeur)
        self.progress_bar = ctk.CTkProgressBar(self.header_frame, height=20)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        # --- GRILLE ---
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        for i in range(5):
            self.grid_frame.grid_columnconfigure(i, weight=1)
            self.grid_frame.grid_rowconfigure(i, weight=1)

        self.tiles = []
        for i, obj in enumerate(self.objectifs):
            tile = BingoTile(self.grid_frame, i, obj, self.toggle_objective)
            tile.grid(row=i//5, column=i%5, padx=5, pady=5, sticky="nsew")
            self.tiles.append(tile)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, fg_color="gray20", corner_radius=15)
        self.sidebar.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="🏆 Paliers & Cadeaux", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.reward_widgets = {}
        paliers_order = ["bronze", "argent", "or", "platine"]
        emojis = {"bronze": "🥉", "argent": "🥈", "or": "🥇", "platine": "💎"}
        
        for key in paliers_order:
            container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            container.pack(fill="x", padx=10, pady=10)
            
            lbl_title = ctk.CTkLabel(container, text=f"{emojis[key]} {key.capitalize()}", font=("Arial", 14, "bold"), text_color="gray")
            lbl_title.pack(anchor="w")
            
            lbl_reward = ctk.CTkLabel(container, text=self.recompenses.get(key, "???"), font=("Arial", 12), text_color="gray60", wraplength=180, justify="left")
            lbl_reward.pack(anchor="w", padx=10)
            
            self.reward_widgets[key] = (lbl_title, lbl_reward)

    def toggle_objective(self, index):
        current_state = self.objectifs[index]['valide']
        new_state = not current_state
        self.objectifs[index]['valide'] = new_state
        
        if new_state:
            self.objectifs[index]['date_validation'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.objectifs[index]['date_validation'] = None

        self.tiles[index].update_visuals(new_state)
        self.save_data()
        self.update_progress_display()

    def update_progress_display(self):
        current_weight = sum(obj['poids'] for obj in self.objectifs if obj['valide'])
        ratio = (current_weight / self.total_weight) if self.total_weight > 0 else 0
        percent = int(ratio * 100)
        
        self.progress_bar.set(ratio)
        self.lbl_progress.configure(text=f"Progression : {percent}% (XP: {current_weight}/{self.total_weight})")

        thresholds = {"bronze": 0.25, "argent": 0.50, "or": 0.75, "platine": 1.0}
        for key, limit in thresholds.items():
            title_lbl, reward_lbl = self.reward_widgets[key]
            if ratio >= limit:
                title_lbl.configure(text_color="#2ecc71")
                reward_lbl.configure(text_color="white")
            else:
                title_lbl.configure(text_color="gray")
                reward_lbl.configure(text_color="gray60")

    def save_data(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.full_data, f, indent=4, ensure_ascii=False)
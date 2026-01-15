import customtkinter as ctk
import json
from datetime import datetime

# --- DÉFINITION DES COULEURS ET FONTS (THEME) ---
THEME = {
    "bg_main": "transparent",       # Fond principal
    "bg_container": "#2b2b2b",      # Fond des panneaux (sidebar)
    "accent_gold": "#F5C518",       # Couleur Or pour la progression
    "accent_green": "#27ae60",      # Vert validation
    "accent_red": "#e74c3c",        # Rouge urgence
    "accent_purple": "#8e44ad",     # Violet bouton historique
    "text_light": "#ffffff",        # Texte blanc
    "text_gray": "#bdc3c7",         # Texte gris clair
    "tile_valid_bg": "#1e3d2f",     # Fond case validée (vert sombre)
    "tile_border_hover": "#F5C518", # Bordure dorée au survol
}

FONT_TITLE = ("Roboto", 24, "bold")  # Police plus grande pour titres
FONT_HEADER = ("Roboto", 18, "bold") # Pour le header
FONT_NORMAL = ("Roboto", 12)         # Texte standard
FONT_TILE = ("Roboto", 11, "bold")   # Texte des tuiles

class BingoTile(ctk.CTkButton):
    def __init__(self, master, index, data, on_click_callback):
        self.index = index
        self.poids = data['poids']
        self.titre = data['titre']
        self.callback = on_click_callback
        
        # Couleurs de base (Non validé) - Un peu plus pastels/modernes
        self.colors = {
            1: "#2ecc71", # Emerald
            2: "#f1c40f", # Sunflower
            3: "#e67e22"  # Carrot
        }
        self.base_color = self.colors.get(self.poids, "#3498db")

        super().__init__(
            master,
            font=FONT_TILE,
            border_width=2,
            border_color=THEME["bg_container"], # Bordure discrète par défaut
            corner_radius=12, # Angles plus arrondis
            hover_color=self.base_color, # Reste sur la couleur de base au survol si non validé
            command=self.on_click
        )
        
        # Effet de survol personnalisé : Bordure dorée
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.update_visuals(data['valide'])

    # --- Effets de survol ---
    def on_enter(self, event):
        if self._state != "disabled":
            self.configure(border_color=THEME["tile_border_hover"])
            
    def on_leave(self, event):
        if self._state != "disabled":
             # Retour à la couleur selon l'état
            color = THEME["accent_gold"] if self.cget("text").startswith("✅") else THEME["bg_container"]
            self.configure(border_color=color)

    def on_click(self):
        if self._state != "disabled":
            self.callback(self.index)

    def update_visuals(self, is_valid):
        if is_valid:
            # Look Validé : Fond vert sombre, texte doré, bordure dorée
            self.configure(
                fg_color=THEME["tile_valid_bg"], 
                text_color=THEME["accent_gold"],
                border_color=THEME["accent_gold"],
                text=f"✅\n{self.titre}"
            )
        else:
            # Look Non Validé : Couleur de difficulté, bordure discrète
            self.configure(
                fg_color=self.base_color,
                text_color=THEME["text_light"],
                border_color=THEME["bg_container"],
                text=f"{self.titre}\n{'★' * self.poids}"
            )


class GridScreen(ctk.CTkFrame):
    def __init__(self, master, on_recap_callback=None):
        super().__init__(master, fg_color=THEME["bg_main"])
        self.on_recap_callback = on_recap_callback
        
        self.config_file = "data/bingo_config.json"
        self.game_over = False
        
        with open(self.config_file, "r", encoding="utf-8") as f:
            self.full_data = json.load(f)
        
        self.objectifs = self.full_data['objectifs']
        self.recompenses = self.full_data['recompenses']
        self.total_weight = sum(obj['poids'] for obj in self.objectifs)

        self.days_remaining = self.get_days_remaining()
        if self.days_remaining == 0:
            self.game_over = True

        self.setup_ui()
        self.update_progress_display()
        
        if self.game_over:
            self.disable_grid()

    def get_days_remaining(self):
        target_date = datetime(2026, 12, 31)
        now = datetime.now()
        delta = target_date - now
        return max(0, delta.days)

    def setup_ui(self):
        # Ajout de padding global autour de tout l'écran
        self.pack(padx=20, pady=20)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header ne prend que la place nécessaire
        self.grid_rowconfigure(1, weight=1) # Le reste prend tout l'espace

        # --- HEADER (Design plus aéré) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # 1. Label Progression (Plus gros)
        self.lbl_progress = ctk.CTkLabel(self.header_frame, text="Progression : 0%", font=FONT_TITLE, text_color=THEME["accent_gold"])
        self.lbl_progress.grid(row=0, column=0, sticky="w")

        # 2. Label Compte à rebours (Plus gros)
        txt_timer = f"⏳ J-{self.days_remaining}" if not self.game_over else "🏁 TERMINE"
        color_timer = THEME["accent_red"] if self.days_remaining < 100 or self.game_over else THEME["text_light"]
        
        self.lbl_timer = ctk.CTkLabel(self.header_frame, text=txt_timer, font=FONT_TITLE, text_color=color_timer)
        self.lbl_timer.grid(row=0, column=1, sticky="e")

        # 3. Bouton Historique (Plus moderne)
        self.btn_history = ctk.CTkButton(
            self.header_frame, text="📜 Historique", width=120, height=35,
            fg_color=THEME["accent_purple"], hover_color="#9b59b6",
            font=FONT_NORMAL, corner_radius=8,
            command=self.open_recap
        )
        self.btn_history.grid(row=0, column=2, sticky="e", padx=(20, 0))

        # 4. Barre de progression (Dorée et plus épaisse)
        self.progress_bar = ctk.CTkProgressBar(self.header_frame, height=15, corner_radius=8)
        self.progress_bar.set(0)
        self.progress_bar.configure(progress_color=THEME["accent_gold"]) # Couleur OR
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(15, 0))

        # --- GRILLE ---
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Ajout de padding à droite pour séparer de la sidebar
        self.grid_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20))
        
        for i in range(5):
            self.grid_frame.grid_columnconfigure(i, weight=1)
            self.grid_frame.grid_rowconfigure(i, weight=1)

        self.tiles = []
        for i, obj in enumerate(self.objectifs):
            tile = BingoTile(self.grid_frame, i, obj, self.toggle_objective)
            # Plus d'espace entre les tuiles (padx/pady 5 -> 8)
            tile.grid(row=i//5, column=i%5, padx=8, pady=8, sticky="nsew")
            self.tiles.append(tile)

        # --- SIDEBAR (Nouveau look "Carte flottante") ---
        self.sidebar = ctk.CTkFrame(self, fg_color=THEME["bg_container"], corner_radius=20, border_width=1, border_color="#333333")
        self.sidebar.grid(row=1, column=1, sticky="nsew")
        
        # Titre sidebar avec une icône et couleur or
        header_sidebar = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_sidebar.pack(pady=(20, 10))
        ctk.CTkLabel(header_sidebar, text="🏆", font=("Arial", 28)).pack()
        ctk.CTkLabel(header_sidebar, text="PALIERS & CADEAUX", font=FONT_HEADER, text_color=THEME["accent_gold"]).pack()
        
        self.reward_widgets = {}
        paliers_order = ["bronze", "argent", "or", "platine"]
        emojis = {"bronze": "🥉", "argent": "🥈", "or": "🥇", "platine": "💎"}
        
        for key in paliers_order:
            # Conteneur de récompense plus aéré
            container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            container.pack(fill="x", padx=15, pady=12) # Plus d'espace vertical
            
            lbl_title = ctk.CTkLabel(container, text=f"{emojis[key]} {key.capitalize()}", font=FONT_HEADER, text_color=THEME["text_gray"])
            lbl_title.pack(anchor="w")
            
            lbl_reward = ctk.CTkLabel(container, text=self.recompenses.get(key, "???"), font=FONT_NORMAL, text_color=THEME["text_gray"], wraplength=180, justify="left")
            lbl_reward.pack(anchor="w", padx=(25,0), pady=(5,0)) # Décalage du texte
            
            self.reward_widgets[key] = (lbl_title, lbl_reward)

    def open_recap(self):
        if self.on_recap_callback:
            self.on_recap_callback()

    def toggle_objective(self, index):
        if self.game_over: return

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
        
        if new_state: self.check_victory()

    def update_progress_display(self):
        current_weight = sum(obj['poids'] for obj in self.objectifs if obj['valide'])
        ratio = (current_weight / self.total_weight) if self.total_weight > 0 else 0
        percent = int(ratio * 100)
        
        self.progress_bar.set(ratio)
        self.lbl_progress.configure(text=f"Progression : {percent}%") # Simplifié

        thresholds = {"bronze": 0.25, "argent": 0.50, "or": 0.75, "platine": 1.0}
        for key, limit in thresholds.items():
            title_lbl, reward_lbl = self.reward_widgets[key]
            if ratio >= limit:
                # Palier atteint : Or brillant
                title_lbl.configure(text_color=THEME["accent_gold"])
                reward_lbl.configure(text_color=THEME["text_light"])
            else:
                # Non atteint : Gris discret
                title_lbl.configure(text_color=THEME["text_gray"])
                reward_lbl.configure(text_color=THEME["text_gray"])
        return ratio

    def disable_grid(self):
        for tile in self.tiles:
            tile.configure(state="disabled")
        
        victory_label = ctk.CTkLabel(self.grid_frame, text="🔒 BINGO TERMINÉ\nDate limite dépassée", 
                                     font=FONT_TITLE, text_color=THEME["accent_red"], fg_color=THEME["bg_container"], corner_radius=20)
        victory_label.place(relx=0.5, rely=0.5, anchor="center")

    def check_victory(self):
        ratio = self.update_progress_display()
        if ratio >= 1.0:
            self.show_victory_popup()

    def show_victory_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("FÉLICITATIONS !")
        popup.geometry("450x350")
        popup.attributes("-topmost", True)
        popup.configure(fg_color=THEME["bg_container"]) # Fond sombre
        
        ctk.CTkLabel(popup, text="🎉", font=("Arial", 70)).pack(pady=(20,10))
        ctk.CTkLabel(popup, text="BINGO COMPLET !", font=FONT_TITLE, text_color=THEME["accent_gold"]).pack()
        ctk.CTkLabel(popup, text="Vous avez atteint le niveau PLATINE.\nL'année 2026 est un succès total.", 
                     font=FONT_NORMAL, text_color=THEME["text_gray"]).pack(pady=10)
        
        recompense_platine = self.recompenses.get("platine", "Inconnu")
        ctk.CTkLabel(popup, text=f"Récompense débloquée :\n✨ {recompense_platine} ✨", 
                     font=FONT_HEADER, text_color=THEME["accent_green"]).pack(pady=20)
                     
        ctk.CTkButton(popup, text="Je suis une légende 😎", command=popup.destroy, 
                      fg_color=THEME["accent_gold"], hover_color="#d4a915", 
                      text_color=THEME["bg_container"], font=FONT_HEADER, height=40, corner_radius=20).pack(pady=10)

    def save_data(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.full_data, f, indent=4, ensure_ascii=False)
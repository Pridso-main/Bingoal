import customtkinter as ctk
import json
from datetime import datetime

class BingoTile(ctk.CTkButton):
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
        # On ne déclenche l'action que si le bouton n'est pas désactivé (disabled)
        if self._state != "disabled":
            self.callback(self.index)

    def update_visuals(self, is_valid):
        if is_valid:
            self.configure(fg_color="#2c3e50", text=f"✅\n{self.titre}")
        else:
            self.configure(fg_color=self.base_color, text=f"{self.titre}\n{'★' * self.poids}")


class GridScreen(ctk.CTkFrame):
    def __init__(self, master, on_recap_callback=None):
        super().__init__(master)
        self.on_recap_callback = on_recap_callback
        
        self.config_file = "data/bingo_config.json"
        self.game_over = False # ### NOUVEAU : Pour savoir si le jeu est fini (Temps écoulé)
        
        # Chargement
        with open(self.config_file, "r", encoding="utf-8") as f:
            self.full_data = json.load(f)
        
        self.objectifs = self.full_data['objectifs']
        self.recompenses = self.full_data['recompenses']
        self.total_weight = sum(obj['poids'] for obj in self.objectifs)

        # Vérification du temps AVANT de créer l'interface
        self.days_remaining = self.get_days_remaining()
        if self.days_remaining == 0:
            self.game_over = True

        self.setup_ui()
        self.update_progress_display()
        
        # ### NOUVEAU : Si le temps est fini, on bloque tout dès le début
        if self.game_over:
            self.disable_grid()

    def get_days_remaining(self):
        target_date = datetime(2026, 12, 31)
        now = datetime.now()
        delta = target_date - now
        return max(0, delta.days)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        # HEADER
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.lbl_progress = ctk.CTkLabel(self.header_frame, text="Progression : 0%", font=("Arial", 20, "bold"))
        self.lbl_progress.grid(row=0, column=0, sticky="w")

        # Label Timer avec gestion "FINI"
        txt_timer = f"⏳ J-{self.days_remaining}" if not self.game_over else "🏁 TERMINE"
        color_timer = "#e74c3c" if self.days_remaining < 100 or self.game_over else "#3498db"
        
        self.lbl_timer = ctk.CTkLabel(
            self.header_frame, 
            text=txt_timer, 
            font=("Arial", 20, "bold"),
            text_color=color_timer
        )
        self.lbl_timer.grid(row=0, column=1, sticky="e")

        self.btn_history = ctk.CTkButton(
            self.header_frame, text="📜 Historique", width=100,
            fg_color="#8e44ad", hover_color="#9b59b6",
            command=self.open_recap
        )
        self.btn_history.grid(row=0, column=2, sticky="e", padx=10)

        self.progress_bar = ctk.CTkProgressBar(self.header_frame, height=20)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        # GRILLE
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

        # SIDEBAR
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

    def open_recap(self):
        if self.on_recap_callback:
            self.on_recap_callback()

    def toggle_objective(self, index):
        # ### NOUVEAU : On empêche de cliquer si le jeu est fini
        if self.game_over:
            return

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
        
        # ### NOUVEAU : On vérifie si c'est la victoire !
        if new_state: # Seulement si on vient de cocher (pas décocher)
            self.check_victory()

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
        
        return ratio # Retourne le ratio pour check_victory

    # ### NOUVEAU : Méthode pour désactiver la grille
    def disable_grid(self):
        """Désactive tous les boutons de la grille (Mode Lecture Seule)"""
        for tile in self.tiles:
            tile.configure(state="disabled")
        
        # On affiche un petit message
        victory_label = ctk.CTkLabel(self.grid_frame, text="🔒 BINGO TERMINÉ\nDate limite dépassée", 
                                     font=("Arial", 30, "bold"), text_color="#e74c3c", fg_color="#2c3e50", corner_radius=20)
        victory_label.place(relx=0.5, rely=0.5, anchor="center")

    # ### NOUVEAU : Popup de Victoire
    def check_victory(self):
        """Vérifie si on a atteint 100%"""
        ratio = self.update_progress_display()
        if ratio >= 1.0:
            self.show_victory_popup()

    def show_victory_popup(self):
        # Création d'une fenêtre secondaire (Toplevel)
        popup = ctk.CTkToplevel(self)
        popup.title("FÉLICITATIONS !")
        popup.geometry("400x300")
        popup.attributes("-topmost", True) # Reste au dessus
        
        # Design Festif
        ctk.CTkLabel(popup, text="🎉", font=("Arial", 60)).pack(pady=10)
        ctk.CTkLabel(popup, text="BINGO COMPLET !", font=("Arial", 24, "bold"), text_color="#f1c40f").pack()
        ctk.CTkLabel(popup, text="Vous avez atteint le niveau PLATINE.\nL'année 2026 est un succès total.", 
                     font=("Arial", 14), text_color="gray80").pack(pady=10)
        
        recompense_platine = self.recompenses.get("platine", "Inconnu")
        ctk.CTkLabel(popup, text=f"Récompense débloquée :\n✨ {recompense_platine} ✨", 
                     font=("Arial", 16, "bold"), text_color="#2ecc71").pack(pady=20)
                     
        ctk.CTkButton(popup, text="Je suis une légende 😎", command=popup.destroy, fg_color="#e74c3c").pack(pady=10)

    def save_data(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.full_data, f, indent=4, ensure_ascii=False)
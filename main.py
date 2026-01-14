import customtkinter as ctk
import os
from src.logic.data_manager import extraire_donnees_csv
from src.ui.setup_screen import SetupScreen
from src.ui.grid_screen import GridScreen

class BingoalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuration de la fenêtre ---
        self.title("Bingoal 2026 - Atteignez vos sommets")
        self.geometry("1000x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- État de l'application ---
        self.current_frame = None
        self.config_path = "data/bingo_config.json"
        self.csv_path = "data/Bingo 2026 - Feuille 1.csv"

        # --- Lancement ---
        self.verifier_etat_initial()

    def verifier_etat_initial(self):
        """Vérifie si une config existe déjà ou s'il faut passer par le setup."""
        if os.path.exists(self.config_path):
            print("📅 Config trouvée. Lancement de la Phase 2...")
            self.lancer_phase_jeu()
        else:
            print("🆕 Aucune config. Lancement de la Phase 1 (Setup)...")
            self.lancer_phase_setup()

    def lancer_phase_setup(self):
        """Affiche l'écran de configuration (Phase 1)."""
        # On tente d'extraire les données du CSV fourni
        donnees_csv = extraire_donnees_csv(self.csv_path)
        
        if self.current_frame:
            self.current_frame.destroy()

        # On passe le callback pour lancer le jeu après la sauvegarde
        self.current_frame = SetupScreen(
            master=self, 
            initial_data=donnees_csv,
            on_save_callback=self.lancer_phase_jeu
        )
        self.current_frame.pack(fill="both", expand=True)

    def lancer_phase_jeu(self):
        """Affiche la grille de Bingo (Phase 2)."""
        print("🎮 Lancement de la Phase 2 : Grille")
        
        if self.current_frame:
            self.current_frame.destroy()

        # C'est ici qu'on appelle la VRAIE grille
        self.current_frame = GridScreen(master=self)
        self.current_frame.pack(fill="both", expand=True)

    def reset_config(self):
        """Supprime la config pour revenir au setup (utile pour le débug)."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
            print("🗑️ Configuration supprimée.")
        self.lancer_phase_setup()

if __name__ == "__main__":
    # On s'assure que le dossier data existe
    if not os.path.exists("data"):
        os.makedirs("data")
        
    app = BingoalApp()
    app.mainloop()
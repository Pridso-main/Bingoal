import customtkinter as ctk
import os
from src.logic.data_manager import extraire_donnees_csv
from src.ui.setup_screen import SetupScreen
from src.ui.grid_screen import GridScreen
from src.ui.recap_screen import RecapScreen  # <--- Vérifie que cette ligne est bien là

class BingoalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bingoal 2026 - Atteignez vos sommets")
        self.geometry("1100x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_frame = None
        self.config_path = "data/bingo_config.json"
        
        # Choix du fichier source (Fun ou Sérieux)
        # self.csv_path = "data/bingo_fun.csv" 
        self.csv_path = "data/Bingo 2026 - Feuille 1.csv"

        self.verifier_etat_initial()

    def verifier_etat_initial(self):
        """Si une config existe, on lance le jeu, sinon le setup."""
        if os.path.exists(self.config_path):
            self.lancer_phase_jeu()
        else:
            self.lancer_phase_setup()

    def lancer_phase_setup(self):
        """Phase 1 : Configuration"""
        donnees_csv = extraire_donnees_csv(self.csv_path)
        
        if self.current_frame: 
            self.current_frame.destroy()
            
        self.current_frame = SetupScreen(
            master=self, 
            initial_data=donnees_csv, 
            on_save_callback=self.lancer_phase_jeu
        )
        self.current_frame.pack(fill="both", expand=True)

    def lancer_phase_jeu(self):
        """Phase 2 : La Grille"""
        if self.current_frame: 
            self.current_frame.destroy()
            
        # C'est ICI que la magie opère pour le bouton historique 👇
        self.current_frame = GridScreen(
            master=self, 
            on_recap_callback=self.lancer_phase_recap
        )
        self.current_frame.pack(fill="both", expand=True)

    def lancer_phase_recap(self):
        """Phase 3 : L'Historique"""
        print("📜 Lancement de l'historique...") # Petit debug pour voir si ça marche
        
        if self.current_frame: 
            self.current_frame.destroy()
            
        self.current_frame = RecapScreen(
            master=self, 
            on_back_callback=self.lancer_phase_jeu
        )
        self.current_frame.pack(fill="both", expand=True)

    def reset_config(self):
        """Pour réinitialiser (debug)"""
        if os.path.exists(self.config_path): 
            os.remove(self.config_path)
        self.lancer_phase_setup()

if __name__ == "__main__":
    if not os.path.exists("data"): 
        os.makedirs("data")
    app = BingoalApp()
    app.mainloop()
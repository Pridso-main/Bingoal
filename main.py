import customtkinter as ctk
import os
import sys
from src.logic.data_manager import extraire_donnees_csv
from src.ui.setup_screen import SetupScreen
from src.ui.grid_screen import GridScreen
from src.ui.recap_screen import RecapScreen

# --- DONNÉES PAR DÉFAUT (INTEGRÉES DANS L'APP) ---
CSV_DEFAULT_CONTENT = """IGNORE,B,I,N,G,O,IGNORE,IGNORE,IGNORE,IGNORE,IGNORE,RECOMPENSES
IGNORE,Manger une pizza ananas,Parler à un pigeon,Survivre à un Lundi,Faire un commit sans bug,Caresser un chien,,,,
IGNORE,Voir un OVNI,Boire 3L d'eau,Ignorer un appel spam,Nettoyer sa souris,Sortir les poubelles (en pyjama),,,,
IGNORE,Gagner au loto (facile),Toucher son nez avec sa langue,CASE GRATUITE (Triche),Lire un livre (sans images),Ne pas scroller TikTok pendant 1h,,,,
IGNORE,Inventer un mot,Faire la vaisselle tout de suite,Crier 'Bingo' dans la rue,Dormir 10h d'affilée,Rire tout seul,,,,
IGNORE,Adopter un caillou,Marcher pieds nus dans l'herbe,Chanter sous la douche,Faire 1 pompe (juste une),Finir ce Bingo stupide,,,,
IGNORE,,,,,,,,,,,
IGNORE,🥉 Niveau BRONZE : Une sucette,,,,,,,,,
IGNORE,🥈 Niveau ARGENT : Un Kebab complet (Chef),,,,,,,,,
IGNORE,🥇 Niveau OR : Une nouvelle Carte Graphique,,,,,,,,,
IGNORE,💎 Niveau PLATINE : Un voyage sur Mars (Aller simple),,,,,,,,,
"""

class BingoalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bingoal 2026 - Atteignez vos sommets")
        self.geometry("1100x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_frame = None
        
        # Définition des chemins
        self.data_dir = "data"
        self.config_path = os.path.join(self.data_dir, "bingo_config.json")
        self.csv_path = os.path.join(self.data_dir, "bingo_default.csv")

        # --- AUTO-RÉPARATION ---
        # L'application vérifie et crée son environnement si nécessaire
        self.initialiser_environnement()

        self.verifier_etat_initial()

    def initialiser_environnement(self):
        """Crée le dossier data et le CSV par défaut si absents."""
        # 1. Créer le dossier 'data' s'il n'existe pas
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
                print("📁 Dossier 'data' créé.")
            except Exception as e:
                print(f"Erreur création dossier: {e}")

        # 2. Créer le fichier CSV par défaut s'il n'existe pas
        if not os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, "w", encoding="utf-8") as f:
                    f.write(CSV_DEFAULT_CONTENT)
                print("📄 CSV par défaut généré.")
            except Exception as e:
                print(f"Erreur création CSV: {e}")

    def verifier_etat_initial(self):
        """Si une config existe, on lance le jeu, sinon le setup."""
        if os.path.exists(self.config_path):
            self.lancer_phase_jeu()
        else:
            self.lancer_phase_setup()

    def lancer_phase_setup(self):
        """Phase 1 : Configuration"""
        # On lit le CSV qu'on vient potentiellement de générer
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
            
        self.current_frame = GridScreen(
            master=self, 
            on_recap_callback=self.lancer_phase_recap
        )
        self.current_frame.pack(fill="both", expand=True)

    def lancer_phase_recap(self):
        """Phase 3 : L'Historique"""
        if self.current_frame: 
            self.current_frame.destroy()
            
        self.current_frame = RecapScreen(
            master=self, 
            on_back_callback=self.lancer_phase_jeu
        )
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = BingoalApp()
    app.mainloop()
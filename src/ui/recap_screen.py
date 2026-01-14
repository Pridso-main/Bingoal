import customtkinter as ctk
import json
from datetime import datetime

class RecapRow(ctk.CTkFrame):
    """Une ligne de la timeline : Date à gauche, Succès à droite"""
    def __init__(self, master, data):
        super().__init__(master, fg_color="transparent")
        
        # Formatage de la date (ex: 2026-01-14 -> 14 Jan 2026)
        try:
            date_obj = datetime.strptime(data['date_validation'], "%Y-%m-%d %H:%M:%S")
            date_str = date_obj.strftime("%d %b")
            heure_str = date_obj.strftime("%H:%M")
        except:
            date_str = "??"
            heure_str = ""

        # Conteneur Date (Cercle ou encadré)
        self.date_frame = ctk.CTkFrame(self, width=80, fg_color="#34495e", corner_radius=10)
        self.date_frame.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(self.date_frame, text=date_str, font=("Arial", 14, "bold"), text_color="white").pack(pady=(5,0))
        ctk.CTkLabel(self.date_frame, text=heure_str, font=("Arial", 10), text_color="gray80").pack(pady=(0,5))

        # Conteneur Détails
        self.info_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        self.info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Couleur du titre selon poids
        colors = {1: "#2ecc71", 2: "#f1c40f", 3: "#e74c3c"}
        poids_color = colors.get(data['poids'], "white")

        ctk.CTkLabel(self.info_frame, text=data['titre'], font=("Arial", 14, "bold"), text_color="white", anchor="w").pack(fill="x", padx=10, pady=(5,0))
        ctk.CTkLabel(self.info_frame, text=f"Difficulté : {'★'*data['poids']}", font=("Arial", 12), text_color=poids_color, anchor="w").pack(fill="x", padx=10, pady=(0,5))


class RecapScreen(ctk.CTkFrame):
    def __init__(self, master, on_back_callback):
        super().__init__(master)
        self.callback = on_back_callback
        
        # Header avec bouton retour
        self.header = ctk.CTkFrame(self, height=60, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        self.btn_back = ctk.CTkButton(self.header, text="⬅ Retour", width=100, command=self.callback, fg_color="gray30", hover_color="gray40")
        self.btn_back.pack(side="left")
        
        ctk.CTkLabel(self.header, text="📜 Mon Histoire 2026", font=("Arial", 24, "bold")).pack(side="left", padx=20)

        # Zone de défilement pour la timeline
        self.scroll = ctk.CTkScrollableFrame(self, label_text="Chronologie des succès", label_font=("Arial", 16, "bold"))
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.charger_donnees()

    def charger_donnees(self):
        try:
            with open("data/bingo_config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                objectifs = data.get("objectifs", [])
                
                # On ne garde que ceux qui sont validés ET qui ont une date
                succes = [obj for obj in objectifs if obj['valide'] and obj.get('date_validation')]
                
                # On trie par date (du plus récent au plus vieux)
                succes.sort(key=lambda x: x['date_validation'], reverse=True)

                if not succes:
                    ctk.CTkLabel(self.scroll, text="Aucun objectif validé pour l'instant.\nAu travail ! 💪", font=("Arial", 16)).pack(pady=50)
                
                for obj in succes:
                    row = RecapRow(self.scroll, obj)
                    row.pack(fill="x", pady=5)

        except Exception as e:
            ctk.CTkLabel(self.scroll, text=f"Erreur de lecture : {e}").pack()
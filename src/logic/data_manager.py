import pandas as pd
import os
import re

def extraire_donnees_csv(chemin_fichier):
    """
    Analyse le CSV pour extraire les objectifs et les récompenses.
    Capable de gérer différents formats de fichiers (Colonnes fixes ou texte libre).
    """
    if not os.path.exists(chemin_fichier):
        return None

    try:
        # Lecture sans header
        df = pd.read_csv(chemin_fichier, header=None)
        
        # 1. Extraction des objectifs (Grille 5x5 - Lignes 1 à 5, Cols 1 à 5)
        # On sécurise au cas où le fichier est plus petit
        try:
            objectifs_raw = df.iloc[1:6, 1:6].values.flatten()
        except:
            # Si le fichier est mal formaté, on renvoie une liste vide
            objectifs_raw = ["Case vide"] * 25

        liste_objectifs = []
        for obj in objectifs_raw:
            titre = str(obj) if pd.notna(obj) else ""
            titre = titre.replace("\n", " ").strip()
            # Si le titre est vide, on met un placeholder
            if not titre or titre.lower() == "nan":
                titre = "Objectif Libre"
            liste_objectifs.append({"titre": titre, "poids": 1})

        # 2. Extraction des Récompenses (Intelligence améliorée)
        recompenses = {
            "bronze": "", "argent": "", "or": "", "platine": ""
        }

        def nettoyer_texte_recompense(texte):
            """Enlève les mots clés pour ne garder que le cadeau."""
            # Liste des mots parasites à supprimer
            parasites = [
                "Niveau", "BRONZE", "ARGENT", "OR", "PLATINE", 
                "🥉", "🥈", "🥇", "💎", ":", "(", ")", 
                "%", "Etoiles", "de", "la", "grille"
            ]
            for p in parasites:
                texte = texte.replace(p, "")
                texte = texte.replace(p.lower(), "") # Majuscules et minuscules
            return texte.strip()

        # On parcourt chaque ligne du fichier
        for index, row in df.iterrows():
            # On convertit toute la ligne en une seule chaîne de texte majuscule pour chercher
            ligne_str = " ".join(str(val) for val in row.values if pd.notna(val)).upper()
            
            # On définit les mots clés à chercher
            map_paliers = {
                "BRONZE": "bronze",
                "ARGENT": "argent", 
                "OR": "or",    # Attention à ne pas matcher "DOOR" ou "PORT"
                "PLATINE": "platine"
            }

            for mot_cle, cle_dict in map_paliers.items():
                # Si on trouve "PLATINE" dans la ligne
                if mot_cle in ligne_str:
                    # STRATÉGIE 1 : Regarder la colonne 11 (Format GSheet original)
                    if len(row) > 11 and pd.notna(row[11]) and str(row[11]).strip() != "":
                        recompenses[cle_dict] = str(row[11]).strip()
                    
                    # STRATÉGIE 2 : Chercher dans la ligne entière (Format Test/Fun)
                    else:
                        # On cherche la cellule exacte qui contient le mot clé
                        for cell in row.values:
                            cell_str = str(cell)
                            if mot_cle in cell_str.upper():
                                # On nettoie cette cellule
                                cadeau = nettoyer_texte_recompense(cell_str)
                                # Si après nettoyage il reste du texte, c'est le cadeau !
                                if len(cadeau) > 2: 
                                    recompenses[cle_dict] = cadeau

        return {"objectifs": liste_objectifs, "recompenses": recompenses}

    except Exception as e:
        print(f"⚠️ Erreur lors de l'analyse du CSV : {e}")
        return None
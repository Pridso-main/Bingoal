import pandas as pd
import os

def extraire_donnees_csv(chemin_fichier):
    """
    Analyse le CSV pour extraire les 25 objectifs et les 4 paliers.
    """
    if not os.path.exists(chemin_fichier):
        return None

    # Lecture sans header pour garder le contrôle total sur les indices
    df = pd.read_csv(chemin_fichier, header=None)

    # 1. Extraction des objectifs (Grille 5x5)
    # Les colonnes B,I,N,G,O correspondent aux colonnes d'index 1 à 5
    # Les objectifs commencent généralement à la ligne d'index 1 (juste après BINGO)
    objectifs_raw = df.iloc[1:6, 1:6].values.flatten()
    
    liste_objectifs = []
    for obj in objectifs_raw:
        titre = str(obj) if pd.notna(obj) else "Objectif vide"
        # Nettoyage simple des sauts de ligne Excel (\n)
        titre = titre.replace("\n", " ")
        liste_objectifs.append({"titre": titre, "poids": 1}) # Poids 1 par défaut

    # 2. Extraction des Récompenses (Recherche par mot-clé)
    recompenses = {
        "bronze": "Non défini",
        "argent": "Non défini",
        "or": "Non défini",
        "platine": "Non défini"
    }

    # On parcourt tout le fichier pour trouver les lignes de paliers
    for index, row in df.iterrows():
        ligne_str = " ".join(str(cell) for cell in row.values)
        if "BRONZE" in ligne_str.upper():
            recompenses["bronze"] = row[11] if len(row) > 11 else "Lot Bronze"
        elif "ARGENT" in ligne_str.upper():
            recompenses["argent"] = row[11] if len(row) > 11 else "Lot Argent"
        elif "OR" in ligne_str.upper():
            recompenses["or"] = row[11] if len(row) > 11 else "Lot Or"
        elif "PLATINE" in ligne_str.upper():
            recompenses["platine"] = row[11] if len(row) > 11 else "Lot Platine"

    return {"objectifs": liste_objectifs, "recompenses": recompenses}
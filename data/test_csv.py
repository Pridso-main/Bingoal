import pandas as pd
import os

chemin = "data/Bingo 2026 - Feuille 1.csv"

if os.path.exists(chemin):
    print("✅ Fichier trouvé !")
    df = pd.read_csv(chemin, header=None)
    print("✅ Lecture réussie. Voici les premières lignes :")
    print(df.head())
else:
    print(f"❌ Erreur : Le fichier est introuvable à l'adresse {chemin}")
    print(f"Fichiers présents dans data/ : {os.listdir('data') if os.path.exists('data') else 'Dossier data absent'}")
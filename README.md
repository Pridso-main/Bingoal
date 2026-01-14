# 🎯 Bingoal 2026

> **Transformez vos résolutions annuelles en un jeu captivant.** > *Bingoal* est une application de bureau moderne développée en Python pour suivre, gamifier et atteindre vos objectifs personnels.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![UI](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)
![Status](https://img.shields.io/badge/Status-Stable-green)

## 🌟 Le Concept

Fini les listes de tâches ennuyeuses. **Bingoal** utilise le principe d'une grille de Bingo 5x5 pour visualiser votre année. 
L'application ne se contente pas de compter les cases : elle calcule un score pondéré (XP) et débloque des récompenses réelles que vous définissez.

## 🚀 Fonctionnalités Clés

### 🎮 Expérience Utilisateur
* **Grille Interactive 5x5** : Cochez (et décochez) vos succès.
* **Système de Difficulté (XP)** : Chaque objectif a un poids :
    * ★ **Easy** (1 pt)
    * ★★ **Medium** (2 pts)
    * ★★★ **Hard** (3 pts)
* **Progression Pondérée** : La barre de progression reflète l'effort réel, pas juste le nombre de cases.
* **Récompenses Dynamiques** : Les paliers (Bronze, Argent, Or, Platine) s'illuminent en temps réel dès qu'ils sont atteints.
* **Compte à Rebours** : Un timer "J-XXX" pour garder la motivation jusqu'au 31 décembre.

### 💾 Technique & Data
* **Import CSV Intelligent** : Chargez vos objectifs depuis un simple tableur (compatible Google Sheets).
* **Persistance JSON** : Sauvegarde automatique à chaque clic.
* **Timeline Historique** : Un écran "Bilan" trace la chronologie exacte de vos validations.
* **Zero Config** : Si aucun fichier n'est fourni, l'application lance un formulaire de configuration assisté.

## 🛠️ Installation

1.  **Cloner le projet**
    ```bash
    git clone [https://github.com/Pridso-main/Bingoal](https://github.com/Pridso-main/Bingoal.git)
    cd Bingoal
    ```

2.  **Installer les dépendances**
    ```bash
    pip install customtkinter pandas
    ```

3.  **Lancer l'application**
    ```bash
    python main.py
    ```

## 📂 Structure du Projet

L'architecture respecte les standards modernes (séparation Vue/Logique) :

```text
Bingoal/
│
├── data/                  # Stockage (CSV source & JSON config)
├── src/
│   ├── logic/             # Parsing de données
│   └── ui/                # Interface Graphique (CustomTkinter)
│       ├── grid_screen.py # Grille de jeu
│       ├── setup_screen.py# Formulaire de départ
│       └── recap_screen.py# Historique / Timeline
│
└── main.py                # Point d'entrée & Gestionnaire de vues
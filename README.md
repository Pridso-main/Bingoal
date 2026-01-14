# 🎯 Bingoal

**Bingoal** est une application de suivi d'objectifs personnels sous forme de Bingo dynamique. Développée en Python avec `CustomTkinter`, elle permet de visualiser sa progression réelle grâce à un système de pondération par difficulté.

## 🚀 Fonctionnalités
- **Grille 5x5 dynamique** générée via CSV.
- **Difficulté pondérée** : 
  - ★ Easy (Poids 1)
  - ★★ Medium (Poids 2)
  - ★★★ Hard (Poids 3)
- **Système de paliers** : Débloquez des récompenses Bronze (25%), Argent (50%), Or (75%) et Platine (100%).
- **Sauvegarde automatique** de la progression en JSON.

## 🛠️ Installation
1. Clonez le dépôt : `git clone https://github.com/ton-pseudo/Bingoal.git`
2. Installez les dépendances : `pip install customtkinter pandas`
3. Lancez l'app : `python main.py`

## 📊 Calcul du score
La progression n'est pas linéaire. Elle est calculée selon le poids total des cases validées par rapport au poids total disponible.
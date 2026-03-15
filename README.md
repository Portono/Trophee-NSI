# CHAMP DE MARS

Survival Shooter Roguelike (Pygame)

# Description du projet

Ce projet est un jeu développé en **Python avec la bibliothèque Pygame**.
Le joueur contrôle un personnage qui doit survivre face à des vagues d’ennemis apparaissant autour de lui.

En éliminant les ennemis, le joueur gagne de l’**expérience (XP)** qui lui permet d’obtenir différentes **améliorations (upgrades)**. Ces améliorations peuvent modifier les statistiques du joueur ou ajouter des effets spéciaux aux armes (électricité en chaîne, ralentissement, explosions, etc.).

Le jeu comprend plusieurs types d’ennemis avec des comportements différents ainsi qu’un **système de difficulté qui augmente progressivement** au cours de la partie.

# Pour commencer

Si vous consultez ce projet sur GitHub, téléchargez la **dernière Release** disponible.
Si vous voyez ce projet depuis une autre plateforme, nous vous recommandons de vous rendre sur notre dépôt GitHub (lien ci-dessous).

# Pré-requis

Ce qui est nécessaire pour exécuter le projet :

* **Python 3.13**
* La bibliothèque **pygame**
* La bibliothèque **pygame_widgets**

Installation de pygame :

```
pip install pygame
```
et
```
pip install pygame_widgets
```

ou alors:

```
pip install -r requirements.txt
```

afin d'installer toutes les bibliothèques nécessaires.

# Installation

Les étapes pour installer le projet :

1. Télécharger la **dernière Release** du projet depuis GitHub.
2. Extraire le fichier **.zip** téléchargé.
3. Ouvrir le dossier du projet extrait.
4. Installer les bibliothèques requises si nécessaire.

# Démarrage

Le jeu doit être lancé **depuis le dossier principal du projet**.
Certaines ressources (sprites, musiques, fichiers JSON, etc.) sont chargées à l’aide de **chemins relatifs**. Si le programme est exécuté depuis un autre dossier, ces fichiers ne pourront pas être trouvés.

Avant de lancer le jeu, assurez-vous que votre terminal se trouve dans le dossier principal du projet :

```bash
cd Champ-de-Mars
```

Puis lancez le jeu avec :

```bash
python sources/main.py
```

Exécuter directement `main.py` depuis un autre dossier ou depuis certains IDE sans définir le bon **working directory** peut provoquer des erreurs de type :

```
FileNotFoundError: No file found
```


# Fabriqué avec

* **Python** — Langage de programmation
* **Pygame** — Bibliothèque utilisée pour le moteur du jeu
* **JSON** — Utilisé pour la sauvegarde de certaines données
* **Sprites 2D**

Sprites réalisés avec **Pixilart**.
Musiques et sons réalisés avec **UltraaBox**

# Versions

Version actuelle : **1.0**

# Auteurs

**Alias :**

* Evan Miniscloux = Portono
* Evan Berthelin  = Enma-EB
* Mael Barbaro    = Oltorc/Kolkien

**Développeurs :**

* Evan Miniscloux
* Evan Berthelin
* Mael Barbaros

**Design graphique :**

* Evan Berthelin
* Mael Barbaros

**Sound Designer :**

* Evan Berthelin

# Dépôt GitHub officiel

Le code source complet du projet, ainsi que l'historique des versions et les mises à jour, sont disponibles sur GitHub :

```
https://github.com/Portono/Champ-de-Mars
```

# License

Ce projet est sous licence **MIT** — voir le fichier `LICENSE` pour plus d'informations.

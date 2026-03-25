# Docs

Notre projets est structurés en differents scripts, certains plus long que d'autres qui sont classes par fonctions par exemple les fonctions de sauvegarde dans save_load.py


# Sources :

**1. Main_game.py :**
C'est là où est codé le jeu principal.
Exemples : 
- Les déplacements du joueur
- Toutes les classes
- Les sprites et animations des personnages
- La carte du jeu
- La logique des projectiles
- La logique des armes
- La logique des ennemis
- plus bien d'autres...

**2. Menu.py :**  
C'est là où le jeu commence, on peut accéder aux parametres, quitter et à l'astropedia.

**3. Main.py :**  
C'est là où les scripts sont assemblés.

**4. Sounddesign.py :**  
C'est là où sont chargés les sons et leur volume modifié.

**5. menu_pause.py :**  
Il s'agit du script qui appel le menu avec des paramètres précis, on y accède avec la touche escape.  
On peut : 
- reprendre la partie
- accéder aux parametres (modification du volume et de la résolution)
- quitter le jeu (va automatiquement créer un fichier de sauvegarde en .Json)
- accéder à l'astropedia

**6. random_module.py :**  
Là où les améliorations du personnage sont définis.  
Elles sont organisées en dictionnaires selon leur catégorie (statistiques, pour les différentes armes, améliorations uniques...).

**7. gameover.py :**  
Là où l'écran de mort est créé avec l'affichage, la police d'ériture et le son.

**8. save_load :**  
Fichier contenant les deux fonctions permettant la sauvegarde et le chargement du jeu.  
La sauvegarde se fait automatiquement en quittant le jeu depuis la menu pause.  
La fonction fait appel à un dictionnaire dans lequel nous avons regroupé tout ce qui nécessite une sauvegarde(nombre de jours, améliorations, niveau, etc).

**9. paths.py :**  
C'est là où est créée la fonction pour trouver le chemin des fichiers dans d'autre dossiers

# Data :

**1. .png :**

*Les : "(1)" ou avec d'autres nombres sont là pour programmer les animations.*

Ce sont pour les sprites :
- des personnages
- pour certaines upgrades (comme l'arc électrique)
- le fond d'écran du menu

**2 .ttf :**

Le format pour les 2 polices d'écritures utilisés dans le jeu (ex : fontgameover.ttf juste pour l'écran de game over).

**3. .mp3 :**

Pour les musiques et les sons présents dans le jeu.  
Les musiques : 1-3, 2-3 et 3-3 sont les 3 en rotation aléatoire pour Main_game.

**4. .json :**

Le format pour la carte de Mars avec la base.
Aussi le format du fichier de sauvegarde

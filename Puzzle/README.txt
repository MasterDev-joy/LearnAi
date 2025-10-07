Jeu de Taquin avec Solveur A*
Ce projet est une implémentation du classique jeu de taquin (Sliding Puzzle) en Python à l'aide de la bibliothèque Pygame. Il propose un mode de jeu manuel pour le joueur ainsi qu'un solveur automatique basé sur l'algorithme de recherche A* qui trouve la solution la plus courte.
[Image d'un jeu de taquin]
Fonctionnalités
* Grille Dynamique : La taille du puzzle s'adapte automatiquement aux dimensions de l'image choisie.
* Personnalisation : Utilisez n'importe quelle image pour créer un puzzle unique.
* Double Mode de Jeu :
   * Mode Humain : Jouez et résolvez le puzzle vous-même à l'aide de la souris.
   * Mode IA : Regardez l'intelligence artificielle résoudre le puzzle de manière optimale grâce à l'algorithme A*.
* Interface Intuitive : Un menu simple pour choisir le mode de jeu et un panneau d'information affichant les mouvements et les contrôles.
* Contrôle de l'IA : Mettez en pause et reprenez l'animation de la solution de l'IA à tout moment.
Prérequis
Pour faire fonctionner ce jeu, vous devez avoir Python et la bibliothèque Pygame installés sur votre machine.
* Python 3 : Télécharger Python
* Pygame : Vous pouvez l'installer via pip :


pip install pygame

Comment Lancer le jeu
1. Structure des Fichiers : Assurez-vous d'avoir les trois fichiers Python dans le même répertoire :
   * main.py : Le point d'entrée principal du jeu.
   * game_ui.py : Gère l'interface graphique et l'état du puzzle.
   * puzzle_astar.py : Contient la logique de l'algorithme A* pour le solveur.
2. Dossier assets : Créez un dossier nommé assets dans le même répertoire que les fichiers Python. Placez-y l'image que vous souhaitez utiliser pour le puzzle. Par défaut, le jeu cherche l'image c-o-champion-sett-mk-splash.jpg.
3. Exécution : Ouvrez un terminal ou une invite de commande, naviguez jusqu'au répertoire du projet et lancez le jeu avec la commande suivante :
python main.py

Comment Jouer
   * Menu Principal :
   * Cliquez sur "Jouer (Humain)" pour commencer une partie manuelle.
   * Cliquez sur "Résoudre (IA)" pour que l'IA trouve et montre la solution.
   * Contrôles en Jeu :
   * Mode Humain : Cliquez sur une tuile adjacente à la case vide pour la déplacer.
   * Mode IA :
   * Appuyez sur la barre d'espace pour mettre en pause ou reprendre l'animation de la solution.
   * Touche Échap : Appuyez à tout moment pour revenir au menu principal.
Personnalisation
Vous pouvez facilement modifier le puzzle en éditant le fichier main.py :
   * Changer l'image : Modifiez la variable IMAGE_PATH pour pointer vers votre fichier image dans le dossier assets.

IMAGE_PATH = pathlib.Path("assets") / "votre-image.jpg"

   * Changer la taille de la grille : Modifiez la variable BASE_TILES. Cette valeur définit le nombre de tuiles sur le plus grand côté de l'image (par exemple, 3 pour un puzzle 3x2, 4 pour un 4x3, etc.).
BASE_TILES = 4
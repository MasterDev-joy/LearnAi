import pygame
import sys
import pathlib
import time
import os

# Import des classes depuis les autres fichiers
from game_ui import Puzzle, BACKGROUND_COLOR, TEXT_COLOR, MARGIN
from puzzle_astar import AStarSolver

# --- Constantes ---
FPS = 60  # Fréquence d'images par seconde
BUTTON_COLOR = (80, 80, 80)  # Couleur des boutons dans le menu
BUTTON_HOVER_COLOR = (110, 110, 110)  # Couleur des boutons au survol


def main():
    """Fonction principale du jeu."""
    # --- CONFIGURATION ---
    # Chemin vers l'image utilisée pour les tuiles du puzzle
    IMAGE_PATH = pathlib.Path("assets") / "c-o-champion-ekko-td-splash.jpg"
    # Dimension de base pour le calcul de la grille. Par exemple, 4x4 si l'image est carrée.
    BASE_TILES = 4
    # Largeur réservée pour le panneau d'information (mouvements, contrôles)
    INFO_PANEL_WIDTH = 250

    # --- CALCUL DYNAMIQUE DE LA TAILLE ---
    try:
        # Tente de charger l'image
        img = pygame.image.load(IMAGE_PATH)
        img_w, img_h = img.get_rect().size
    except pygame.error:
        # En cas d'échec du chargement de l'image
        print(f"INFO : Impossible de charger l'image '{IMAGE_PATH}'. La taille de la fenêtre sera par défaut.")
        img_w, img_h = 400, 300  # Taille par défaut pour éviter une erreur

    # Calcule le ratio Hauteur/Largeur de l'image
    aspect_ratio = img_h / img_w

    # Détermine les dimensions de la grille (GRID_WIDTH x GRID_HEIGHT)
    # L'une des dimensions est fixée à BASE_TILES, l'autre est calculée
    if img_w >= img_h:
        # Image 'Paysage' ou Carrée (Largeur >= Hauteur)
        GRID_WIDTH = BASE_TILES
        GRID_HEIGHT = max(1, round(BASE_TILES * aspect_ratio))
    else:
        # Image 'Portrait' (Hauteur > Largeur)
        GRID_HEIGHT = BASE_TILES
        GRID_WIDTH = max(1, round(BASE_TILES / aspect_ratio))

    GRID_SIZE = (GRID_WIDTH, GRID_HEIGHT)

    # Calcule TILE_SIZE (taille des tuiles en pixels) pour que le puzzle s'adapte
    # à une taille de fenêtre maximale de 1200x900 (moins le panneau d'info).
    TILE_SIZE = min((1200 - INFO_PANEL_WIDTH) // GRID_WIDTH, 900 // GRID_HEIGHT)

    # Calcule les dimensions totales de la zone de puzzle (grille + marges)
    puzzle_width = GRID_WIDTH * (TILE_SIZE + MARGIN) + MARGIN
    puzzle_height = GRID_HEIGHT * (TILE_SIZE + MARGIN) + MARGIN

    # Définit la taille finale de la fenêtre (Puzzle + Panneau d'Info)
    SCREEN_WIDTH = puzzle_width + INFO_PANEL_WIDTH
    SCREEN_HEIGHT = puzzle_height

    pygame.init()
    # Centre la fenêtre au démarrage
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption(f"{GRID_WIDTH}x{GRID_HEIGHT} Puzzle Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Contrôle le framerate

    # Initialise l'objet Puzzle avec les dimensions calculées
    puzzle = Puzzle(GRID_SIZE, TILE_SIZE, screen, IMAGE_PATH)

    # --- BOUCLE PRINCIPALE ---
    running = True
    player_mode = None  # Mode de jeu : None (Menu), 'human', ou 'ai'
    ai_solution_path = []  # Liste des états à suivre pour l'animation de l'IA
    ai_animation_time = 0  # Timestamp pour contrôler la vitesse de l'animation de l'IA
    ai_paused = False  # État de pause de l'animation de l'IA

    while running:
        # --- MENU DE SÉLECTION ---
        if player_mode is None:
            screen.fill(BACKGROUND_COLOR)
            font_title = pygame.font.Font(None, 50)
            font_option = pygame.font.Font(None, 40)

            # Calcule le centre horizontal et vertical pour centrer le menu
            CENTER_X = SCREEN_WIDTH / 2
            CENTER_Y = SCREEN_HEIGHT / 2

            SPACING = 70  # Espacement vertical entre les éléments du menu

            # Titre du jeu (ex: "15-Puzzle avec A*")
            title_text = font_title.render(f"{GRID_WIDTH * GRID_HEIGHT - 1}-Puzzle avec A*", True, TEXT_COLOR)
            # Positionne le titre au-dessus du centre
            title_rect = title_text.get_rect(center=(CENTER_X, CENTER_Y - SPACING))
            screen.blit(title_text, title_rect)

            # Bouton Jouer (Humain)
            human_btn = pygame.Rect(0, 0, 300, 50)
            human_btn.center = (CENTER_X, CENTER_Y)  # Centre le bouton verticalement

            mouse_pos = pygame.mouse.get_pos()
            # Change la couleur si la souris survole le bouton
            btn_color = BUTTON_HOVER_COLOR if human_btn.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, btn_color, human_btn, border_radius=10)
            human_text = font_option.render("Jouer (Humain)", True, TEXT_COLOR)
            screen.blit(human_text, human_text.get_rect(center=human_btn.center))

            # Bouton Résoudre (IA)
            ai_btn = pygame.Rect(0, 0, 300, 50)
            ai_btn.center = (CENTER_X, CENTER_Y + SPACING)  # Positionne le bouton en dessous du centre

            btn_color = BUTTON_HOVER_COLOR if ai_btn.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, btn_color, ai_btn, border_radius=10)
            ai_text = font_option.render("Résoudre (IA)", True, TEXT_COLOR)
            screen.blit(ai_text, ai_text.get_rect(center=ai_btn.center))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if human_btn.collidepoint(event.pos):
                        player_mode = 'human'
                        puzzle.shuffle()  # Commence en mode Humain, mélange le puzzle
                    elif ai_btn.collidepoint(event.pos):
                        player_mode = 'ai'
                        puzzle.shuffle()  # Commence en mode IA, mélange le puzzle
                        solver = AStarSolver(puzzle)

                        print("--- DÉBOGAGE ---")
                        print(f"Configuration à résoudre: {puzzle.state}")
                        # Vérifie si l'état initial est solvable
                        print(f"Est-ce résoluble ? : {puzzle.is_solvable()}")

                        start_time = time.time()
                        solution = solver.solve()  # Exécute l'algorithme A*
                        print(f"Temps de recherche IA: {time.time() - start_time:.4f} secondes.")

                        if solution:
                            print(f"Solution trouvée en {len(solution)} mouvements.")
                            # Le chemin de solution est stocké SANS l'état initial
                            ai_solution_path = solution
                            # Le compteur de mouvements est réinitialisé pour l'animation
                            puzzle.moves = 0
                            ai_animation_time = pygame.time.get_ticks()
                        else:
                            print("ERREUR: L'IA n'a pas trouvé de solution.")
                            player_mode = None  # Retourne au menu en cas d'échec

            pygame.display.flip()  # Met à jour tout l'écran pour le menu
            continue  # Passe directement à la prochaine itération de la boucle

        # --- GESTION DES ÉVÉNEMENTS DU JEU ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Touche ECHAP
                    player_mode = None  # Retour au menu
                    ai_solution_path.clear()
                    ai_paused = False
                # Touche ESPACE pour la pause/reprise de l'animation de l'IA
                if player_mode == 'ai' and event.key == pygame.K_SPACE:
                    ai_paused = not ai_paused
            if event.type == pygame.MOUSEBUTTONDOWN and player_mode == 'human':
                puzzle.handle_click(event.pos)  # Gère le clic de la souris pour les humains

        # --- LOGIQUE DU JEU ---
        # Avancement de l'animation de l'IA
        if player_mode == 'ai' and ai_solution_path and not ai_paused:
            now = pygame.time.get_ticks()
            # Contrôle la vitesse (un mouvement toutes les 200 ms)
            if now - ai_animation_time > 200:
                ai_animation_time = now
                current_state = ai_solution_path.pop(0)  # Prend le prochain état du chemin
                puzzle.state = list(current_state)  # Applique le nouvel état au puzzle
                puzzle.moves += 1  # Incrémente le compteur de mouvements

        # --- DESSIN ---
        screen.fill(BACKGROUND_COLOR)
        puzzle.draw()  # Dessine la grille de tuiles ou l'image complète (si gagné)

        # Afficher le message de pause si l'IA est en pause
        if player_mode == 'ai' and ai_paused:
            font_pause = pygame.font.Font(None, 40)
            pause_text = font_pause.render("PAUSE", True, (255, 200, 0))
            info_panel_x = puzzle_width + 20
            text_rect = pause_text.get_rect(left=info_panel_x, bottom=SCREEN_HEIGHT - 20)
            screen.blit(pause_text, text_rect)

        pygame.display.flip()  # Met à jour tout l'écran pour le jeu

        clock.tick(FPS)  # Limite la boucle à 60 images par seconde

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
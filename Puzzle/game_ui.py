import pygame
import random

# --- Constantes Visuelles ---
BACKGROUND_COLOR = (30, 30, 30)  # Couleur de fond de l'écran
TEXT_COLOR = (240, 240, 240)  # Couleur du texte
TILE_COLOR = (150, 150, 150)  # Couleur de secours pour les tuiles
MARGIN = 5  # Marge (espace) entre les tuiles et autour de la grille


class Puzzle:
    """
    Gère l'état du jeu, l'affichage et les interactions.
    La représentation de l'état est une liste de nombres où l'index
    représente la position sur la grille et la valeur représente la tuile à cette position.
    """

    def __init__(self, grid_size, tile_size, screen, image_path):
        self.gs = grid_size  # Taille de la grille (gw, gh)
        self.gw, self.gh = grid_size  # Largeur (gw) et Hauteur (gh) de la grille
        self.ts = tile_size  # Taille d'une tuile en pixels
        self.screen = screen  # Surface d'affichage Pygame
        # Taille totale en pixels de la zone de puzzle (grille + marges)
        self.puzzle_pixel_size = (self.gw * (self.ts + MARGIN) + MARGIN, self.gh * (self.ts + MARGIN) + MARGIN)
        # Charge l'image complète pour l'affichage de victoire
        self.full_image = self._load_full_image(image_path)

        self.tile_count = self.gw * self.gh  # Nombre total de tuiles
        self.blank_value = self.tile_count - 1  # La valeur représentant la tuile vide (la dernière)

        # L'état initial résolu : liste [0, 1, 2, ..., N-1]
        self.state = list(range(self.tile_count))
        self.solved_state = self.state[:]  # Sauvegarde de l'état résolu

        # Crée et stocke les surfaces Pygame pour chaque tuile découpée
        self.images = self._create_tile_images(image_path)
        self.moves = 0  # Compteur de mouvements
        self.player_mode = None  # Mode de jeu actuel (pour l'affichage contextuel)

    def _load_full_image(self, image_path):
        """Charge et met à l'échelle l'image complète pour correspondre à la taille de la grille de puzzle."""
        try:
            # Charge l'image et l'ajuste à la taille de la grille (y compris les marges)
            pic = pygame.transform.smoothscale(pygame.image.load(image_path), self.puzzle_pixel_size)
            return pic
        except pygame.error:
            print(f"AVERTISSEMENT : Impossible de charger l'image '{image_path}'.")
            # Crée une surface vide (transparente) en cas d'échec
            return pygame.Surface(self.puzzle_pixel_size, pygame.SRCALPHA)

    def _create_tile_images(self, image_path):
        """Découpe l'image source stockée dans self.full_image en tuiles individuelles."""
        images = []
        pic = self.full_image  # Utilise l'image complète déjà chargée

        font = pygame.font.Font(None, int(self.ts * 0.4))

        for i in range(self.tile_count):
            if i == self.blank_value:
                # La tuile vide est une surface transparente
                images.append(pygame.Surface((self.ts, self.ts), pygame.SRCALPHA))
                continue

            # Calcule les coordonnées de la tuile i sur la grande image (incluant la marge)
            x = (i % self.gw) * (self.ts + MARGIN) + MARGIN
            y = (i // self.gw) * (self.ts + MARGIN) + MARGIN

            tile_surface = pygame.Surface((self.ts, self.ts))
            if pic:
                # Copie la portion de l'image (subsurface) sur la surface de la tuile
                tile_surface.blit(pic, (0, 0), (x, y, self.ts, self.ts))
            else:
                # Affichage de secours (couleur unie) si l'image n'a pas pu être chargée
                tile_surface.fill(TILE_COLOR)
                pygame.draw.rect(tile_surface, BACKGROUND_COLOR, tile_surface.get_rect(), 3)

            # Affiche le numéro de la tuile (i+1) pour le débogage/fallback
            text = font.render(str(i + 1), True, TEXT_COLOR)
            text_rect = text.get_rect(center=(self.ts / 2, self.ts / 2))
            tile_surface.blit(text, text_rect)
            images.append(tile_surface)

        return images

    def shuffle(self):
        """Mélange l'état du puzzle jusqu'à ce qu'il soit garanti résoluble."""
        self.moves = 0
        self.state = list(range(self.tile_count))
        random.shuffle(self.state)

        # Répète le mélange tant que l'état n'est pas solvable (selon la règle N-Puzzle)
        while not self.is_solvable():
            random.shuffle(self.state)

    def is_solvable(self):
        """Vérifie si la configuration actuelle est résoluble en comptant les inversions."""
        inversions = 0
        # Compte le nombre de paires (i, j) où i vient avant j mais i > j
        for i in range(self.tile_count):
            if self.state[i] == self.blank_value:  # Ignore la tuile vide
                continue
            for j in range(i + 1, self.tile_count):
                if self.state[j] == self.blank_value:  # Ignore la tuile vide
                    continue
                if self.state[i] > self.state[j]:
                    inversions += 1

        if self.gw % 2 == 1:  # Règle pour Largeur impaire (ex: 3x3)
            # Solvable si le nombre d'inversions est PAIR.
            return inversions % 2 == 0
        else:  # Règle pour Largeur paire (ex: 2x3, 4x4)
            blank_index = self.state.index(self.blank_value)
            blank_row = blank_index // self.gw
            # Rangée de la case vide comptée depuis le BAS (0, 1, 2...)
            blank_row_from_bottom = self.gh - 1 - blank_row

            # Règle corrigée: La somme (Inversions + Rangée depuis le bas) doit être PAIRE.

            if blank_row_from_bottom % 2 == 0:  # Rangée Paire (0, 2, ...)
                # Pour que la somme soit paire, Inversions doit être PAIR.
                return inversions % 2 == 0
            else:  # Rangée Impaire (1, 3, ...)
                # Pour que la somme soit paire, Inversions doit être IMPAIR.
                return inversions % 2 == 1

    def is_win(self):
        """Vérifie si l'état actuel correspond à l'état résolu."""
        return self.state == self.solved_state

    def handle_click(self, mouse_pos):
        """Gère les clics de la souris pour le joueur humain en vérifiant la validité du mouvement."""
        # Détermine la position (x, y) de la tuile cliquée dans la grille
        tile_x = (mouse_pos[0] - MARGIN) // (self.ts + MARGIN)
        tile_y = (mouse_pos[1] - MARGIN) // (self.ts + MARGIN)

        # Vérifie si le clic est à l'intérieur des limites de la grille
        if not (0 <= tile_x < self.gw and 0 <= tile_y < self.gh):
            return

        clicked_idx = tile_y * self.gw + tile_x  # Index plat de la tuile cliquée
        blank_idx = self.state.index(self.blank_value)  # Index plat de la case vide

        b_x, b_y = blank_idx % self.gw, blank_idx // self.gw  # Coordonnées case vide
        c_x, c_y = clicked_idx % self.gw, clicked_idx // self.gw  # Coordonnées tuile cliquée

        # Vérifie l'adjacence: la distance de Manhattan doit être 1
        if (abs(b_x - c_x) + abs(b_y - c_y)) == 1:
            # Effectue l'échange et met à jour l'état
            self.state[blank_idx], self.state[clicked_idx] = self.state[clicked_idx], self.state[blank_idx]
            self.moves += 1  # Incrémente le compteur de mouvements

    def draw(self):
        """Dessine l'état actuel du puzzle et le panneau d'information."""

        if self.is_win():
            # Si gagné, affiche l'image complète à la place de la grille
            self.screen.blit(self.full_image, (MARGIN, MARGIN))
        else:
            # Sinon, dessine les tuiles une par une selon l'état actuel
            for i, tile_value in enumerate(self.state):
                x = (i % self.gw) * (self.ts + MARGIN) + MARGIN
                y = (i // self.gw) * (self.ts + MARGIN) + MARGIN
                # 'tile_value' détermine quelle image de tuile afficher à la position 'i'
                self.screen.blit(self.images[tile_value], (x, y))

        # --- Panneau d'Information ---
        info_x = self.gw * (self.ts + MARGIN) + MARGIN + 20  # Position x du panneau
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        # Affichage du compteur de mouvements
        moves_text = font_medium.render(f"Mouvements : {self.moves}", True, TEXT_COLOR)
        self.screen.blit(moves_text, (info_x, 20))

        if self.is_win():
            # Message de victoire
            win_text = font_medium.render("Gagné !", True, (100, 255, 100))
            self.screen.blit(win_text, (info_x, 70))

        # Affichage des contrôles
        y_offset = 120
        controls_title = font_medium.render("Contrôles :", True, TEXT_COLOR)
        self.screen.blit(controls_title, (info_x, y_offset))

        y_offset += 40
        escape_text = font_small.render("Echap : Retour Menu", True, TEXT_COLOR)
        self.screen.blit(escape_text, (info_x, y_offset))

        # Instructions spécifiques au mode de jeu
        if self.player_mode == 'human':
            y_offset += 30
            mouse_text = font_small.render("Clic : Déplacer une tuile", True, TEXT_COLOR)
            self.screen.blit(mouse_text, (info_x, y_offset))
        elif self.player_mode == 'ai':
            y_offset += 30
            space_text_l1 = font_small.render("Espace : pause / reprendre", True, TEXT_COLOR)
            self.screen.blit(space_text_l1, (info_x, y_offset))
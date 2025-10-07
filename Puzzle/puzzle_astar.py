import heapq


class AStarSolver:
    """
    Classe dédiée à la résolution du puzzle avec l'algorithme A*.
    Elle implémente la recherche A* pour trouver le chemin le plus court (en nombre de mouvements)
    entre l'état initial et l'état résolu du puzzle N-Puzzle.
    """

    def __init__(self, puzzle_instance):
        # Stocke l'instance du puzzle pour accéder à son état et à ses propriétés
        self.puzzle = puzzle_instance
        # Récupère la largeur (gw) et la hauteur (gh) de la grille
        self.gw, self.gh = puzzle_instance.gs

    def _heuristic(self, state):
        """
        Calcule la distance de Manhattan totale (Manhattan Distance) pour un état donné.
        C'est la fonction heuristique h(n) qui estime le coût du nœud actuel à l'objectif.
        """
        distance = 0
        # Parcourt chaque tuile dans l'état actuel (state)
        for i, value in enumerate(state):
            # Ignore la case vide (blank_value) pour le calcul
            if value == self.puzzle.blank_value:
                continue

            # Calcule la position actuelle (x, y) de la tuile i
            current_pos = (i % self.gw, i // self.gw)
            # Calcule la position cible (résolue) de la tuile value
            target_pos = (value % self.gw, value // self.gw)

            # Ajoute la distance de Manhattan: |x_actuel - x_cible| + |y_actuel - y_cible|
            distance += abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])
        return distance

    def _get_successors(self, state):
        """
        Génère tous les états successeurs valides à partir d'un état (tous les mouvements possibles).
        """
        successors = []
        # Trouve l'index (position) de la case vide
        blank_idx = state.index(self.puzzle.blank_value)
        b_x, b_y = blank_idx % self.gw, blank_idx // self.gw  # Coordonnées (x, y) de la case vide

        # Itère sur les quatre mouvements possibles (Haut, Bas, Gauche, Droite)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_x, n_y = b_x + dx, b_y + dy  # Coordonnées du voisin potentiel

            # Vérifie si la nouvelle position est dans les limites de la grille
            if 0 <= n_x < self.gw and 0 <= n_y < self.gh:
                neighbor_idx = n_y * self.gw + n_x  # Calcule l'index plat du voisin

                new_state = list(state)
                # Effectue l'échange (mouvement) de la case vide avec le voisin
                new_state[blank_idx], new_state[neighbor_idx] = new_state[neighbor_idx], new_state[blank_idx]

                # Ajoute l'état résultant sous forme de tuple (pour être hachable dans les dictionnaires)
                successors.append(tuple(new_state))
        return successors

    def solve(self):
        """
        Exécute l'algorithme A* pour trouver le chemin le plus court.
        A* utilise f(n) = g(n) + h(n), où g(n) est le coût réel (nombre de mouvements)
        et h(n) est le coût estimé (heuristique de Manhattan).
        """
        start_node = tuple(self.puzzle.state)
        target_node = tuple(self.puzzle.solved_state)

        # g_score[n] contient le coût réel (nombre de mouvements) du départ à n
        g_score = {start_node: 0}

        # Calcule f_score initial: g(start) + h(start) = 0 + h(start)
        f_score_initial = self._heuristic(start_node)

        # open_set est une min-heap stockant les tuples (f_score, state)
        open_set = [(f_score_initial, start_node)]
        heapq.heapify(open_set)  # Assure que open_set est une pile prioritaire

        # came_from[n] est le nœud qui précède n sur le chemin le plus court trouvé jusqu'à présent
        came_from = {}

        while open_set:
            # Récupère et supprime le nœud avec le plus petit f_score
            _, current = heapq.heappop(open_set)

            if current == target_node:
                # Si le nœud cible est atteint, reconstruit le chemin
                path = []
                temp = current
                while temp in came_from:
                    path.append(temp)  # Ajoute le nœud au chemin
                    temp = came_from[temp]  # Remonte au nœud précédent
                # Renvoie le chemin inversé (du départ à l'arrivée)
                return path[::-1]

            # Explore les voisins
            for neighbor in self._get_successors(current):
                # Calcule le coût réel du départ au voisin via le nœud actuel
                tentative_g_score = g_score[current] + 1

                # Si un chemin plus court est trouvé (ou si c'est la première visite)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Met à jour le g_score et enregistre le chemin
                    g_score[neighbor] = tentative_g_score

                    # Calcule le nouveau f_score
                    f_score = tentative_g_score + self._heuristic(neighbor)

                    # Enregistre le chemin optimal trouvé jusqu'à ce voisin
                    came_from[neighbor] = current

                    # Ajoute ou met à jour le voisin dans la pile de priorité open_set
                    heapq.heappush(open_set, (f_score, neighbor))

        return None  # Retourne None si la pile est vide (pas de solution trouvée)
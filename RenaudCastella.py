"""
----------------------------------------------
TP IA
Renaud Sylvain, Castella Killian
15.11.2017
----------------------------------------------
"""

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN
import sys
import math
from random import shuffle, randint


def init_pygame():
    """Initialise pygame pour l'utilisation de la gui."""
    global city_color
    global line_color
    global city_radius
    global font_color
    global window
    global screen
    global font
    screen_x = 500
    screen_y = 500
    city_color = [10, 10, 200]  # blue
    line_color = [200, 10, 10]  # red
    city_radius = 3
    font_color = [255, 255, 255]  # white
    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)


def draw(positions):
    """Dessine le parcours"""
    city_radius = 3
    screen.fill(0)
    for pos in positions:
        pygame.draw.circle(screen, city_color, (pos.x, pos.y), city_radius)
    text = font.render(f"Nombre: {len(positions)}", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def wait_key():
    """Attente d'une entrée utilisateur avent de fermer la fenêtre."""
    pygame.display.set_caption('Meilleur chemin trouvé !')
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            break


def get_cities_list_from_gui():
    """Construit une liste de villes d'après les points ajoutés par l'utilisateur"""
    cities = []
    collecting = True
    count = 1
    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cities.append(Ville(x, y, f"v{str(count)}"))
                draw(cities)
                count += 1
    return cities


class Ville:
    """Contient un nom et des coordonnées."""

    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return f"[{self.x},{self.y},{self.name}]"

    def __repr__(self):
        return self.__str__()


class Parcours:
    """Contient une liste de ville et une distance de parcours (calculable)."""

    distance = None
    villes = []
    dict_dist = None

    def __init__(self, villes):
        if isinstance(villes, list):
            self.villes = list(villes)

            # Création d'une table de distances entre les villes.
            # Evite de calculer plusieurs fois la même distance.
            if Parcours.dict_dist is None:
                Parcours.dict_dist = {v.name: {u.name: None for u in villes} for v in villes}

    def shuffle(self):
        """Mélange les villes."""
        shuffle(self.villes)
        return self

    def __iter__(self):
        return self.villes.__iter__()

    def __getitem__(self, item):
        return self.villes.__getitem__(item)

    def __setitem__(self, key, value):
        return self.villes.__setitem__(key, value)

    def __delitem__(self, key):
        del self.villes[key]

    def get_points(self):
        """Retourne uniquement les coordonnées des villes."""
        return [(v.x, v.y) for v in self.villes]

    def fitness(self):
        """Calcul de la distance totale du parcours."""
        self.distance = 0
        old_city = None
        for v in self.villes:
            # On regarde d'abord si la distance entre ces deux villes a déjà été calculée.
            # Calcul sinon.
            if old_city is not None:
                if Parcours.dict_dist[old_city.name][v.name] is None:
                    Parcours.dist(old_city, v)
                self.distance += Parcours.dict_dist[old_city.name][v.name]
            old_city = v
        self.distance += Parcours.dist(old_city, self.villes[0])

    @staticmethod
    def dist(a, b):
        """Calcul de la distance entre deux villes. Sauvegarde du résultat dans le dictionnaire."""
        tx = a.x - b.x
        ty = a.y - b.y
        res = math.sqrt(tx * tx + ty * ty)
        # Enregistrement du résultat dans le dictionnaire. Deux entrées car dist(a,b) = dist(b,a).
        Parcours.dict_dist[a.name][b.name] = res
        Parcours.dict_dist[b.name][a.name] = res
        return res


def append(self, ville):
    """Ajoute une ville au parcours."""
    self.villes.append(ville)


def __str__(self):
    str = "{"
    for v in self.villes:
        str += repr(v) + ", "
    return str + "}"


def __repr__(self):
    return self.__str__()


def selection(population):
    """Séléction des meilleurs individus."""
    for individu in population:
        individu.fitness()
    population.sort(key=lambda individu: individu.distance)

    # delete n last elem of list, n = len / 2
    del population[-int(len(population) / 2):]


def crossover(ga, gb):
    """Algorithm: Greedy Subtour Crossover"""
    ga = ga.villes
    gb = gb.villes

    n = len(ga)
    fa = True
    fb = True
    t = ga[randint(0, n - 1)]
    x = ga.index(t)
    y = gb.index(t)

    g = [t]

    while True:
        x = (x - 1) % n
        y = (y + 1) % n
        if fa:
            if ga[x] not in g:
                g.insert(0, ga[x])
            else:
                fa = False
        if fb:
            if gb[y] not in g:
                g.append(gb[y])
            else:
                fb = False
        if not fa or not fb:
            break

    if len(g) < len(ga):
        for v in ga:
            if v not in g:
                g.append(v)
    return g


def croisement(pop):
    """Croisement des parents jusqu'à doubler la taille de la population."""
    n = len(pop)
    while len(pop) < 2 * n:
        x = pop[randint(0, len(pop) - 1)]
        y = pop[randint(0, len(pop) - 1)]
        while y == x:
            y = pop[randint(0, len(pop) - 1)]
        child = crossover(x, y)
        pop.append(Parcours(child))


def mutate1(parcours):
    """Exchange 2 contiguous elements."""
    ind = randint(0, len(parcours.villes) - 1)
    swap = parcours[ind]
    parcours[ind] = parcours[ind - 1]
    parcours[ind - 1] = swap
    parcours.fitness()
    return parcours.villes


def mutate2(parcours):
    """Exchange 2 random elements."""
    i = randint(0, len(parcours.villes) - 1)
    j = i
    while j is i:
        j = randint(0, len(parcours.villes) - 1)
    swap = parcours[i]
    parcours[i] = parcours[j]
    parcours[j] = swap
    parcours.fitness()
    return parcours.villes


def mutation(population):
    """2 chance sur 20 de muter."""
    count = 0
    for p in population:
        rand = randint(0, 20)
        if rand == 0:
            p.villes = mutate1(p)
        elif rand == 1:
            p.villes = mutate2(p)
        count += 1


def two_opt(parcours):
    """Algorithme 2-opt pour l'optimisation."""
    parcours.fitness()
    for i in range(1, len(parcours.villes) - 1):
        for k in range(i + 1, len(parcours.villes)):
            new_parcours = Parcours(two_opt_swap(parcours.villes, i, k))
            new_parcours.fitness()
            if new_parcours.distance < parcours.distance:
                return new_parcours
    return None


def two_opt_swap(route, i, k):
    """Méthode swap de l'algorithme 2-opt."""
    new_route = []
    new_route.extend(route[:i])
    new_route.extend(reversed(route[i:k + 1]))
    new_route.extend(route[k + 1:])
    return new_route


def ga_solve(filename=None, gui=True, maxtime=0, output_dist=False):
    """Donne une solution au problème en utilisant une algo génétique."""
    import time

    # Suppression du dictionnaire des villes si déjà existant.
    Parcours.dict_dist = None

    villes = []
    if gui or filename is None:
        init_pygame()
    if filename is None:
        villes = get_cities_list_from_gui()
    else:
        # Lire le fichier
        with open(filename) as file:
            for line in file:
                name, x, y = line.split()
                villes.append(Ville(int(x), int(y), name))

    start_time = time.time()

    population = []

    # Ajoute 10 individus
    for i in range(10):
        population.append(Parcours(villes).shuffle())

    for p in population:
        p.fitness()
    population.sort(key=lambda individu: individu.distance)

    best = population[0]
    nb_iter = 0
    nb_two_opt = 0
    stagnation = 0

    while True:
        nb_iter += 1

        selection(population)

        mutation(population)

        croisement(population)

        for p in population:
            p.fitness()
        population.sort(key=lambda individu: individu.distance)

        # Conditions d'arrêt sur la stagnation. Si la solution  stagne une fois, on applique le two_opt.
        # Si le le two_opt ne produit pas de meilleur résultats, on arrête.
        if best.distance == population[0].distance:
            stagnation += 1
            if stagnation > 25:
                nb_two_opt += 1
                opt_result = two_opt(best)
                stagnation = 0
                if opt_result is None:
                    # if gui:
                    #     wait_key()
                    if output_dist:
                        print(population[0].distance)
                    return population[0].distance, [v.name for v in population[0].villes]
                else:
                    population.insert(0, opt_result)
                    del population[-1]
                if gui:
                    # dessin de la nouvelle meilleure solution
                    draw_path(population)
        else:
            best = population[0]

        # Conditions d'arrêt sur le temps
        if maxtime != 0 and time.time() - start_time > maxtime:
            # if gui:
            #     wait_key()
            if output_dist:
                print(population[0].distance)
            return population[0].distance, [v.name for v in population[0].villes]


def draw_path(population):
    screen.fill(0)
    pygame.draw.lines(screen, line_color, True, population[0].get_points())
    pygame.display.set_caption('Meilleur chemin trouvé actuellement...')
    pygame.display.flip()


# Tests individuels.
if __name__ == "__main__":
    for _ in range(1):
        ga_solve("data/pb100.txt", False, 90000, True)

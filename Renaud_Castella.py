"""
----------------------------------------------
TP IA
Renaud Sylvain, Castella Killian
15.11.2017
----------------------------------------------
"""

import pygame
from builtins import print
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN
import sys
import math
from random import shuffle, randint


def initPygame():
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
    city_radius = 3
    screen.fill(0)
    for pos in positions:
        pygame.draw.circle(screen, city_color, (pos.x, pos.y), city_radius)
    text = font.render(f"Nombre: {len(positions)}", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def getCitiesListFromGui():
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


class Ville():
    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return f"[{self.x},{self.y},{self.name}]"

    def __repr__(self):
        return self.__str__()


class Parcours():
    distance = None
    villes = []

    def __init__(self, villes):
        if isinstance(villes, list):
            self.villes = list(villes)

    def shuffle(self):
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

    def getPoints(self):
        list = []
        for v in self.villes:
            list.append((v.x, v.y))
        return list

    def fitness(self):
        self.distance = 0
        old_city = None
        for v in self.villes:
            self.distance += Parcours.dist(old_city, v)
            old_city = v

    @staticmethod
    def dist(a, b):
        if a is not None:
            return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
        return 0

    def append(self, ville):
        self.villes.append(ville)

    def __str__(self):
        str = "{"
        for v in self.villes:
            str += repr(v) + ", "
        return str + "}"

    def __repr__(self):
        return self.__str__()


def selection(population):
    for individu in population:
        individu.fitness()
    population.sort(key=lambda individu: individu.distance)
    # delete n last elem of list
    del population[-int(len(population) / 2):]

def mutate1(parcours):
    """exchange 2 contiguous elements"""
    ind = randint(0,len(parcours.villes)-1)
    swap=parcours[ind]
    parcours[ind] = parcours[ind-1]
    parcours[ind-1]=swap

def mutate2(parcours):
    """exchange 2 random elements"""
    ind = randint(0,len(parcours.villes)-1)
    ind2=ind
    while(ind2 is ind):
        ind2=randint(0,len(parcours.villes)-1)
    swap=parcours[ind]
    parcours[ind] = parcours[ind2]
    parcours[ind2]=swap


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
        if fa == True:
            if ga[x] not in g:
                g.insert(0, ga[x])
            else:
                fa = False
        if fb == True:
            if gb[y] not in g:
                g.append(gb[y])
            else:
                fb = False
        if fa == False or fb == False:
            break

    if len(g) < len(ga):
        for v in ga:
            if v not in g:
                g.append(v)
    return g


def croisement(pop):
    n = len(pop)
    while len(pop) < 2 * n:
        x = pop[randint(0, len(pop) - 1)]
        y = pop[randint(0, len(pop) - 1)]
        while y == x:
            y = pop[randint(0, len(pop) - 1)]
        child = crossover(x, y)
        pop.append(Parcours(child))


def mutation(population):
    #test :  on effectue la mutation sur 1 élément sur deux
    count=0
    for p in population:
        if count%2==0:
            mutate1(p)
        else:
            mutate2(p)
        count += 1


def ga_solve(filename=None, gui=True, maxtime=0):
    import time

    villes = []
    if gui:
        initPygame()
    if filename is None:
        villes = getCitiesListFromGui()
        print(len(villes), villes)
    else:
        # lire le fichier
        with open(filename) as file:
            for line in file:
                name, x, y = line.split()
                villes.append(Ville(int(x), int(y), name))
            print(len(villes), villes)

    if gui:
        pass

    start_time = time.time()

    population = []

    # Ajoute 10 individus
    for i in range(10):
        population.append(Parcours(villes).shuffle())

    best = population[0]
    n = 0
    nbIter = 0
    while True:
        nbIter += 1
        croisement(population)
        mutation(population)
        selection(population)

        # Conditions d'arrêt sur le temps
        if time.time() - start_time > maxtime:
            break

        # Conditions d'arrêt sur la stagnation (100x la même solution
        if population[0] == best:
            n += 1
            if n > 100:
                print(nbIter, n)
                break
        else:
            # dessin de la nouvelle meilleure solution
            if gui:
                screen.fill(0)
                pygame.draw.lines(screen, line_color, True, population[0].getPoints())
                print(population[0].getPoints())
                pygame.display.set_caption('Meilleur chemin trouvé actuellement...')
                pygame.display.flip()
            best = population[0]
            n = 0

    pygame.display.set_caption('Meilleur chemin trouvé !')
    print(population[0].distance)

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            break


ga_solve("data/pb050.txt", True, 5)
# ga_solve(maxtime=1)

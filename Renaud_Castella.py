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
from random import shuffle


def initPygame():
    global city_color
    global city_radius
    global font_color
    global window
    global screen
    global font
    screen_x = 500
    screen_y = 500
    city_color = [10, 10, 200]  # blue
    city_radius = 3
    font_color = [255, 255, 255]  # white
    pygame.init()
    pygame.display.set_caption('Add cities')
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
    villes = []

    def __init__(self, villes):
        if isinstance(villes, list):
            self.villes = list(villes)

    def shuffle(self):
        shuffle(self.villes)
        return self

    def __len__(self):
        return len(self.villes)

    def __iter__(self):
        return self.villes.__iter__()

    def append(self, ville):
        self.villes.append(ville)

    def __str__(self):
        str = "{"
        for v in self.villes:
            str += repr(v) + ", "
        return str + "}"

    def __repr__(self):
        return self.__str__()


def ga_solve(filename=None, gui=True, maxtime=0):
    import time

    villes = []
    if filename is None:
        initPygame()
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

    parcours_list = []
    for i in range(10):
        parcours_list.append(Parcours(villes).shuffle())

    print(parcours_list)

    while True:

        # selection()
        # croisement()
        # mutation()

        # Tests
        if time.time() - start_time > maxtime:
            break


ga_solve("data/pb010.txt", False, 1)
# ga_solve(maxtime=1)

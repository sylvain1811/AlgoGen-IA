"""
----------------------------------------------
TP IA
Renaud Sylvain, Castella Killian
15.11.2017
----------------------------------------------
"""

import pygame
import sys


class Probleme():
    villes = []

    def __init__(self, villes):
        if isinstance(villes, list):
            self.villes = villes

    def __len__(self):
        return len(self.villes)

    def __iter__(self):
        return self.villes.__iter__()

    def append(self, ville):
        self.villes.append(ville)


class Solution():
    pass


class Ville():
    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return f"[{self.x},{self.y},{self.name}]"

    def __repr__(self):
        return f"[{self.x},{self.y},{self.name}]"


def ga_solve(filename=None, gui=True, maxtime=0):
    villes = []
    if filename == None:
        # ouvrir la fenetre pour entrer les points manuellement
        pass
    else:
        # lire le fichier
        with open(filename) as file:
            for line in file:
                name, x, y = line.split()
                villes.append(Ville(int(x), int(y), name))
            print(len(villes), villes)

    if gui:
        pass


ga_solve("data/pb010.txt", False)

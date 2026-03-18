import pygame
from Menu import boucle_menu

def afficher_menu_pause(armes_possedees=None, nombre_journees=0):
    return boucle_menu(pause=True, armes_possedees=armes_possedees, nombre_journees=nombre_journees)

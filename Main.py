import pygame
from Main_game import*
from Sounddesign import*
from Menu import *
from menu_pause import*

def main():
    pygame.init()
    running=True
    while running:
        settings=afficher_menu()
        if settings["play"]:
            lancer_jeu(settings)
        else:
            running=False
    pygame.quit()

if __name__ == "__main__":
    main()

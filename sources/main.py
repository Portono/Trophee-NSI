import pygame
from Main_game import*
from Sounddesign import*
from Menu import *
from menu_pause import*
from gameover import*

def main():
    pygame.init()
    running=True
    while running:
        settings=afficher_menu()
        if settings["play"]:
            armes_possedees = lancer_jeu(settings)
            afficher_gameover()
        else:
            running=False
    pygame.quit()

if __name__ == "__main__":
    main()


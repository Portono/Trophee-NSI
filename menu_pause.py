import pygame
from Menu import boucle_menu

def afficher_menu_pause():
    en_pause = True
    while en_pause:
       for event in pygame.event.get():
              if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                            return  # Quitter le menu pause
       if boucle_menu(pause=True):
             return  # Quitter le menu pause

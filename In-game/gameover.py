import pygame
from Menu import*
from Sounddesign import*
pygame.init()
screen=pygame.display.set_mode((width,height))
front=pygame.font.Font("font.ttf",150)

def afficher_gameover():
    tps_debut=pygame.time.get_ticks()
    while pygame.time.get_ticks()-tps_debut<=2000:
        pygame.event.get()
        Sounddeath.play()
        text_surface=front.render("Game Over",True, (255,0,0))
        text_rect=text_surface.get_rect()
        text_rect.center=(width/2,height/2)
        screen.blit(text_surface,text_rect)
        pygame.display.flip()

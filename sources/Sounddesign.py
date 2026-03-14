import pygame

pygame.mixer.init()

Soundhit=pygame.mixer.Sound("data/Hit.mp3")
Sounddeath=pygame.mixer.Sound("data/Death.mp3")
Sounddeath.set_volume(0.35)

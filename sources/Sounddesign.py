import pygame

pygame.mixer.init()

Soundhit=pygame.mixer.Sound("data/Hit.mp3")
Sounddeath=pygame.mixer.Sound("data/Death.mp3")

base_sound_volume=0.5

def set_sfx_volume(volume):
    """Met a jour le volume des effets sonores entre 0.0 et 1.0."""
    global base_sound_volume
    base_sound_volume=max(0,min(1,volume))
    Soundhit.set_volume(base_sound_volume)
    Sounddeath.set_volume(base_sound_volume*0.35)

#Volume par defaut
set_sfx_volume(base_sound_volume)


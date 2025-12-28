import pygame
import random
import math
from Menu_Final import *

pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((Width, Height)) 

#Classes
class Enemy:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.vitesse = 5
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (self.x, self.y)

    def se_deplacer(self, p_x, p_y):
        """Deplace l'ennemi vers le joueur"""
        dx = p_x - self.x
        dy = p_y - self.y
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:   ##Pour éviter la division par zéro
            self.x += (dx / distance) * self.vitesse
            self.y += (dy / distance) * self.vitesse
        
        # Mise à jour de la position réelle
        self.rect.center = (self.x, self.y)

    def dessiner(self, surface, offset_x, offset_y):
        """Dessine l'ennemi en tenant compte du décalage de la caméra"""
        # On dessine l'ennemi à sa position RÉELLE moins le décalage CAMÉRA
        draw_rect = self.rect.copy()    ##Permet d'aficher l'ennemi à la bonne position sans modifier sa position réelle
        draw_rect.x -= offset_x
        draw_rect.y -= offset_y
        pygame.draw.rect(surface, (0, 0, 255), draw_rect)

class Projectile:
    def __init__(self, x_start, y_start, target_x, target_y):
        self.x = x_start
        self.y = y_start
        self.vitesse = 15
        dx = target_x - x_start
        dy = target_y - y_start
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
        else:
            self.dir_x = 0
            self.dir_y = 0
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.center = (self.x, self.y)

    def update(self,surface, offset_x, offset_y):
        #mouvement
        self.x += self.dir_x * self.vitesse
        self.y += self.dir_y * self.vitesse
        self.rect.center = (self.x, self.y)
        #dessin
        draw_rect = self.rect.copy()
        draw_rect.x -= offset_x
        draw_rect.y -= offset_y
        pygame.draw.rect(surface, (0, 255, 0), draw_rect)


def spawn_enemy(p_x, p_y):
    # On fait apparaître les ennemis autour du joueur mais hors écran
    distance_spawn = ((Width//2)**2+(Height//2)**2)**0.5 + 100
    angle = random.uniform(0,2*math.pi)
    spawn_x = p_x + math.cos(angle) * distance_spawn
    spawn_y = p_y + math.sin(angle) * distance_spawn
    return Enemy(spawn_x, spawn_y)

def ennemi_le_plus_proche(x,y, enemies):
    plus_proche=None
    distance_min=float('inf')
    for en in enemies:
        d=(en.x-x)**2+(en.y-y)**2
        if d<distance_min:
            distance_min=d
            plus_proche=en
    return plus_proche
    
x, y = 400, 300 # Position réelle du joueur dans le monde
vitesse_joueur = 10
couleur_joueur = (255, 0, 0)

enemies = []
enemy_spawn_time = 0
delai_spawn = 60 

projectiles = []
dernier_tir = pygame.time.get_ticks()
delai_tir=1000


clock = pygame.time.Clock()

while play == True:
    clock.tick(60)
    temps_actuel = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Dessiner le fond
    screen.fill((255, 255, 255)) # Fond blanc

    #Modifie les coordonnees reelles du joueur
    touches = pygame.key.get_pressed()
    if touches[pygame.K_d]:
        x += vitesse_joueur
    if touches[pygame.K_q] or touches[pygame.K_a]:
        x -= vitesse_joueur
    if touches[pygame.K_s]:
        y += vitesse_joueur
    if touches[pygame.K_z] or touches[pygame.K_w]:
        y -= vitesse_joueur

    #Maintient le joueur au centre de l'ecran en calculant le decalage
    offset_x = x - (Width // 2)
    offset_y = y - (Height // 2)

    #Gestion des spawns d'ennemis
    enemy_spawn_time += 1
    if enemy_spawn_time >= delai_spawn:
        if len(enemies) < 2000:
            enemies.append(spawn_enemy(x, y))
        enemy_spawn_time = 0

    #Gestion des tirs
    if temps_actuel - dernier_tir >= delai_tir:
        cible=ennemi_le_plus_proche(x, y, enemies)
        if cible:
            projectiles.append(Projectile(x, y, cible.x, cible.y))
        dernier_tir = temps_actuel
    for proj in projectiles[:]:
        proj.update(screen, offset_x, offset_y)
        # Vérification des collisions avec les ennemis
        for en in enemies:
            if proj.rect.colliderect(en.rect):
                enemies.remove(en)
                if proj in projectiles:
                    projectiles.remove(proj)
                break
        # Suppression des projectiles hors écran
        if (proj.x < offset_x - 100 or proj.x > offset_x + Width + 100 or
            proj.y < offset_y - 100 or proj.y > offset_y + Height + 100):
            if proj in projectiles:
                projectiles.remove(proj)

    # Dessiner une grille pour voir le mouvement de la caméra
    for i in range(-5000, 5000, 100):
        pygame.draw.line(screen, (240, 240, 240), (i - offset_x, -5000 - offset_y), (i - offset_x, 5000 - offset_y))
        pygame.draw.line(screen, (240, 240, 240), (-5000 - offset_x, i - offset_y), (5000 - offset_x, i - offset_y))

    #Definir le rectangle réel du joueur pour la détection de collision
    player_real_rect = pygame.Rect(0, 0, 50, 50)
    player_real_rect.center = (x, y)

    for en in enemies:
        en.se_deplacer(x, y)
        en.dessiner(screen, offset_x, offset_y)
        
        if player_real_rect.colliderect(en.rect):
            print("GAME OVER")
            play = False 

    # Dessiner le joueur (Fixe au centre de l'écran)
    player_screen_rect = pygame.Rect(0, 0, 50, 50)
    player_screen_rect.center = (Width // 2, Height // 2)
    pygame.draw.rect(screen, couleur_joueur, player_screen_rect)

    pygame.display.flip()

pygame.quit()

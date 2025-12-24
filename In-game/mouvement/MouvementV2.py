import pygame
import random
from Menu_Final import *

pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((Width, Height)) 

# --- CLASSE ENNEMI ---
class Enemy:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.vitesse = 5
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (self.x, self.y)

    def se_deplacer(self, p_x, p_y):
        dx = p_x - self.x
        dy = p_y - self.y
        distance = (dx**2 + dy**2) ** 0.5
        
        if distance != 0:
            self.x += (dx / distance) * self.vitesse
            self.y += (dy / distance) * self.vitesse
        
        # Mise à jour de la position réelle
        self.rect.center = (self.x, self.y)

    def dessiner(self, surface, offset_x, offset_y):
        # On dessine l'ennemi à sa position RÉELLE moins le décalage CAMÉRA
        draw_rect = self.rect.copy()
        draw_rect.x -= offset_x
        draw_rect.y -= offset_y
        pygame.draw.rect(surface, (0, 0, 255), draw_rect)

# --- FONCTION SPAWN ---
def spawn_enemy(p_x, p_y):
    # On fait apparaître les ennemis autour du joueur mais hors écran
    distance_spawn = 1000 
    angle = random.uniform(0, 2 * 3.14159)
    spawn_x = p_x + distance_spawn * (random.choice([-1, 1])) * random.random()
    spawn_y = p_y + distance_spawn * (random.choice([-1, 1])) * random.random()
    return Enemy(spawn_x, spawn_y)

# --- VARIABLES ---
x, y = 400, 300 # Position réelle du joueur dans le monde
vitesse_joueur = 10
color_joueur = (255, 0, 0)

enemies = []
enemy_spawn_time = 0
delai_spawn = 60 

clock = pygame.time.Clock()

# --- BOUCLE PRINCIPALE ---
while play == True:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 1. MOUVEMENT (Modifie les coordonnées réelles)
    touches = pygame.key.get_pressed()
    if touches[pygame.K_d]: x += vitesse_joueur
    if touches[pygame.K_q] or touches[pygame.K_a]: x -= vitesse_joueur
    if touches[pygame.K_s]: y += vitesse_joueur
    if touches[pygame.K_z] or touches[pygame.K_w]: y -= vitesse_joueur

    # 2. CALCUL DE LA CAMÉRA (Offset)
    # On veut que le joueur soit au centre de l'écran
    offset_x = x - (Width // 2)
    offset_y = y - (Height // 2)

    # 3. GESTION ENNEMIS
    enemy_spawn_time += 1
    if enemy_spawn_time >= delai_spawn:
        if len(enemies) < 2000:
            enemies.append(spawn_enemy(x, y))
        enemy_spawn_time = 0

    # 4. RENDU
    screen.fill((255, 255, 255)) # Fond blanc

    # Dessiner une grille pour voir le mouvement de la caméra
    for i in range(-5000, 5000, 100):
        pygame.draw.line(screen, (240, 240, 240), (i - offset_x, -5000 - offset_y), (i - offset_x, 5000 - offset_y))
        pygame.draw.line(screen, (240, 240, 240), (-5000 - offset_x, i - offset_y), (5000 - offset_x, i - offset_y))

    # Gestion des ennemis (Logique + Dessin décalé)
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
    pygame.draw.rect(screen, color_joueur, player_screen_rect)

    pygame.display.flip()

pygame.quit()

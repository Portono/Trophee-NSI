import pygame
import random
from Menu_Final import *

pygame.init()

# Configuration de la fenêtre
# On utilise Width et Height importés de Menu_Final
screen = pygame.display.set_mode((Width, Height)) 

#Classe Ennemi

class Enemy:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.vitesse = 5
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def se_deplacer(self, p_x, p_y):
        # Calcul de la direction vers le joueur
        dx = p_x - self.x
        dy = p_y - self.y
        distance = (dx**2 + dy**2) ** 0.5
        
        if distance != 0:
            self.x += (dx / distance) * self.vitesse
            self.y += (dy / distance) * self.vitesse
        
        # Mise à jour automatique du rectangle de collision
        self.rect.center = (self.x, self.y)

    def dessiner(self, surface):
        # Dessin de l'ennemi (Bleu)
        pygame.draw.rect(surface, (0, 0, 255), self.rect)

#Spawn des ennemis à des positions aléatoires en dehors de l'écran
def spawn_enemy():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        pos = [-50, random.randint(0, Height)]
    elif side == 'right':
        pos = [Width + 50, random.randint(0, Height)]
    elif side == 'top':
        pos = [random.randint(0, Width), -50]
    else: # bottom
        pos = [random.randint(0, Width), Height + 50]
    
    return Enemy(pos[0], pos[1])

#Variable de boucle principale

# Joueur
x, y = 400, 300
vitesse_joueur = 10
color_joueur = (255, 0, 0)

# Ennemis
enemies = []
enemy_spawn_time = 0
delai_spawn = 60 # Apparition toutes les 60 frames (1 seconde)

clock = pygame.time.Clock()
# Boucle principale
while play == True:
    clock.tick(60)
    
    #Quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Mouvement du joueur(WASD ou ZQSD)
    touches = pygame.key.get_pressed()
    if touches[pygame.K_d]: x += vitesse_joueur
    if touches[pygame.K_q] or touches[pygame.K_a]: x -= vitesse_joueur
    if touches[pygame.K_s]: y += vitesse_joueur
    if touches[pygame.K_z] or touches[pygame.K_w]: y -= vitesse_joueur

    #Spawn d'ennemis
    enemy_spawn_time += 1
    if enemy_spawn_time >= delai_spawn:
        if len(enemies) < 2000: ## Limite le nombre d'ennemis à 2000
            enemies.append(spawn_enemy())
        enemy_spawn_time = 0
    #Ecran blanc
    screen.fill((255, 255, 255))
    #Rectangle Joueur
    player_rect = pygame.Rect(x, y, 50, 50)
    #Gestion ennemis
    for en in enemies:
        en.se_deplacer(x, y) # L'ennemi suit le joueur
        en.dessiner(screen)  # L'ennemi se dessine
        # Test de collision
        if player_rect.colliderect(en.rect):
            print("GAME OVER")
            play = False # Arrêter la boucle principale
    #Dessiner le joueur (Rouge)
    pygame.draw.rect(screen, color_joueur, player_rect)
    #Mettre à jour l'affichage
    pygame.display.flip()
pygame.quit()

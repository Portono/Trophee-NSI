import pygame
import random
from Menu_Final import*

pygame.init()   ##initialisation de pygame
screen = pygame.display.set_mode((2560,1440))  ##creation de la fenetre

#Variables du personnage
x=400
y=300
vitesse=10
color=(255,0,0)
#Variables de l'ennemi
enemy_speed=5
enemies=[]  ##list des coordonnes des ennemis
enemy_spawn_time=60  ##temps entre chaque spawn d'ennemi en millisecondes
enemy_color=(0,0,255)

clock=pygame.time.Clock()  ##creation d'une horloge pour gerer les fps

def spawn_enemy():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        return [-50, random.randint(0, Height)]
    elif side == 'right':
        return [Width + 50, random.randint(0, Height)]
    elif side == 'top':
        return [random.randint(0, Width), -50]
    elif side == 'bottom':
        return [random.randint(0, Width), Height + 50]


while play==True:   ##boucle infinie du jeu
    clock.tick(60)   ##limiter a 60 fps
    for event in pygame.event.get():  ##recuperation des evenements
        if event.type == pygame.QUIT:  ##si l'evenement est la fermeture de la fenetre
            pygame.quit()   ##quitter pygame
            exit()   ##quitter le programme
    touches=pygame.key.get_pressed()  ##recuperation des touches appuyees
    if touches[pygame.K_d]:  ##si la touche droite est appuyee
        x+=vitesse   ##deplacer le personnage vers la droite
    if touches[pygame.K_q] or touches[pygame.K_a]:  ##si la touche gauche est appuyee
        x-=vitesse   ##deplacer le personnage vers la gauchedd
    if touches[pygame.K_s]:  ##si la touche bas est appuyee
        y+=vitesse   ##deplacer le personnage vers le bas
    if touches[pygame.K_z] or touches[pygame.K_w]:  ##si la touche haut est appuyee
        y-=vitesse   ##deplacer le personnage vers le haut
    pygame.draw.rect(screen,color,(x,y,50,50))   ##dessiner le personnage
    pygame.display.flip()   ##mettre a jour l'affichage

    #Gestion des ennemis
    enemy_spawn_time += 1
    if enemy_spawn_time >= 240:  ##spawn d'un ennemi toutes les secondes
        enemies.append(spawn_enemy())
        enemy_spawn_time = 0
    screen.fill((255,255,255))   ##remplir l'ecran en blanc
    player_rect=pygame.Rect(x,y,50,50)
    for en in enemies:
        dx= x-en[0]
        dy= y-en[1]
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            en[0]+=(dx/distance)*enemy_speed
            en[1]+=(dy/distance)*enemy_speed
        pygame.draw.rect(screen,enemy_color,(en[0],en[1],40,40))   ##dessiner l'ennemi
        enemy_rect=pygame.Rect(en[0],en[1],40,40)
        if player_rect.colliderect(enemy_rect):
            print("Game Over")
            pygame.quit()

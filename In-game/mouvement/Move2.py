import pygame

pygame.init()   ##initialisation de pygame
screen = pygame.display.set_mode((2560,1440))  ##creation de la fenetre

#Variables du personnage
x=400
y=300
vitesse=10
color=(255,0,0)
#Variable de l'ennemi
enemy_x=800
enemy_y=300
enemy_vitesse=5
enemy_color=(0,0,255)


clock=pygame.time.Clock()  ##creation d'une horloge pour gerer les fps

while True:   ##boucle infinie du jeu
    clock.tick(60)   ##limiter a 60 fps
    for event in pygame.event.get():  ##recuperation des evenements
        if event.type == pygame.QUIT:  ##si l'evenement est la fermeture de la fenetre
            pygame.quit()   ##quitter pygame
            exit()   ##quitter le programme
    touches=pygame.key.get_pressed()  ##recuperation des touches appuyees
    if touches[pygame.K_d]:  ##si la touche droite est appuyee
        x+=vitesse   ##deplacer le personnage vers la droite
    if touches[pygame.K_q]:  ##si la touche gauche est appuyee
        x-=vitesse   ##deplacer le personnage vers la gauche
    if touches[pygame.K_s]:  ##si la touche bas est appuyee
        y+=vitesse   ##deplacer le personnage vers le bas
    if touches[pygame.K_z]:  ##si la touche haut est appuyee
        y-=vitesse   ##deplacer le personnage vers le haut
    screen.fill((255,255,255))   ##remplir l'ecran en noir
    pygame.draw.rect(screen,color,(x,y,50,50))   ##dessiner le personnage
    pygame.draw.rect(screen,enemy_color,(enemy_x,enemy_y,50,50))   ##dessiner l'ennemi
    pygame.display.flip()   ##mettre a jour l'affichage
    Player_rect=pygame.Rect(x,y,50,50)   ##creer un rectangle pour le personnage
    Enemy_rect=pygame.Rect(enemy_x,enemy_y,50,50)   ##creer un rectangle pour l'ennemi
    if Player_rect.colliderect(Enemy_rect):   ##si le personnage touche l'ennemi
        print("Game Over")   ##afficher game over
        pygame.quit()   ##quitter pygame
        exit()   ##quitter le programme
    #Mouvement de l'ennemi
    dx=x-enemy_x
    dy=y-enemy_y
    distance=(dx**2+dy**2)**0.5
    if distance!=0:
        enemy_x+=enemy_vitesse*dx/distance
        enemy_y+=enemy_vitesse*dy/distance

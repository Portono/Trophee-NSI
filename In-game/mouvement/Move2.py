import pygame

pygame.init()   ##initialisation de pygame
screen = pygame.display.set_mode((2560,1440))  ##creation de la fenetre

#Variables du personnage
x=400
y=300
vitesse=10
color=(255,0,0)

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
    pygame.display.flip()   ##mettre a jour l'affichage

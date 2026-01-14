import pygame
import random
import math
from Menu import *

pygame.init()

ennemy_spawn_delay=2000  ##Délai entre chaque spawn d'ennemi en millisecondes TEMPORAIRE

# Configuration de la fenêtre
screen = pygame.display.set_mode((width, height)) 
#Classes
class projectiles_general:
    """Classe principale des projectiles"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=None,couleur=(0,255,0)):  ##AJOUTER PLUS TARD SPRITE AVEC CHEMIN D'ACCES ET COULEUR SERT SEULEMENT SI PAS DE SPRITE
        self.x=x
        self.y=y
        self.vitesse=vitesse
        self.cible=cible_initiale
        self.homing=homing
        self.couleur=couleur

        self.image = None
        if sprite_path:
            self.image = pygame.image.load(sprite_path).convert_alpha()
            self.rect = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, 10, 10)
            self.rect.center = (self.x, self.y)
        #Si cible meurt entre temps, le projectile continue tout droit
        self.calculer_direction(cible_initiale.x, cible_initiale.y)

    def calculer_direction(self, cible_x, cible_y):
        direction_x = cible_x - self.x
        direction_y = cible_y - self.y
        distance= math.hypot(direction_x, direction_y)
        if distance != 0:
            self.dir_x = direction_x / distance
            self.dir_y = direction_y / distance

    def update(self,liste_ennemis):
        if self.homing:
            #Recalcule la direction vers la cible
            if self.cible in liste_ennemis:
                self.calculer_direction(self.cible.x, self.cible.y)
            else:
                if liste_ennemis:
                    self.cible = min(liste_ennemis, key=lambda ennemi: math.hypot(ennemi.x - self.x, ennemi.y - self.y))
        #Mouvement du projectile
        self.x += self.dir_x * self.vitesse
        self.y += self.dir_y * self.vitesse
        self.rect.center = (self.x, self.y)

    def dessiner(self,screen,offset_x,offset_y):
        pos_ecran=(self.rect.x-offset_x,self.rect.y - offset_y)
        if self.image:
            screen.blit(self.image, pos_ecran)
        else:
            pygame.draw.rect(screen,self.couleur,(pos_ecran[0],pos_ecran[1],10,10))

class projectile_laser(projectiles_general):
    """Classe des projectiles laser"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=None, couleur=(255,0,0))  ##Appelle le constructeur de la classe parente avec une couleur rouge
        
class weapon_main:
    """Classe principale des armes"""
    def __init__(self,delai,classe_projectile,homing=False,range_max=1/2*height):
        self.delai=delai  ##Temps entre chaque tir en millisecondes
        self.dernier_tir=0  ##Temps du dernier tir
        self.classe=classe_projectile  ##Classe du projectile tiré
        self.homing=homing  ##Indique si les projectiles sont homing ou non
        self.range=range_max  ##Portée maximale de l'arme
    def tirer(self, temps_actuel):
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.dernier_tir >= self.delai:
            self.dernier_tir = temps_actuel
            return  True
        return False
    

#Variables de jeu
player_x, player_y = 0, 0 # Position réelle du joueur dans le monde
vitesse_joueur = 10
couleur_joueur = (255, 0, 0)
types_ennemis = [ennemi_simple, ennemi_rapide,ennemi_tireur]  ##Liste des types d'ennemis
liste_ennemis = []  ##Liste pour stocker les ennemis
derniers_spawn = {classe: 0 for classe in types_ennemis}  ##Dictionnaire pour stocker le dernier spawn de chaque type d'ennemi
clock = pygame.time.Clock()
liste_projectiles = []  ##Liste pour stocker les projectiles
laser=weapon_main(500, projectile_laser,homing=False,range_max=1/2*height)  ##Crée une arme laser avec un délai de 500ms entre chaque tir et des projectiles homing
type_armes=[laser]   ##Liste des types d'armes
liste_projectiles_ennemis=[]  ##Liste pour stocker les projectiles des ennemis


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
        player_x += vitesse_joueur
    if touches[pygame.K_q] or touches[pygame.K_a]:
        player_x -= vitesse_joueur
    if touches[pygame.K_s]:
        player_y += vitesse_joueur
    if touches[pygame.K_z] or touches[pygame.K_w]:
        player_y -= vitesse_joueur

    #Maintient le joueur au centre de l'ecran en calculant le decalage
    offset_x = player_x - (width // 2)
    offset_y = player_y - (height // 2)

    # Dessiner une grille pour voir le mouvement de la caméra
    for i in range(-5000, 5000, 100):
        pygame.draw.line(screen, (240, 240, 240), (i - offset_x, -5000 - offset_y), (i - offset_x, 5000 - offset_y))
        pygame.draw.line(screen, (240, 240, 240), (-5000 - offset_x, i - offset_y), (5000 - offset_x, i - offset_y))

    # Gérer le spawn des ennemis
    for classe in types_ennemis:
        if temps_actuel - derniers_spawn[classe] >= classe.spawn_delay:
            spawn_x, spawn_y = classe.calculer_pos_spawn(player_x, player_y, width, height)
            nouvel_ennemi = classe(spawn_x, spawn_y)
            liste_ennemis.append(nouvel_ennemi)
            derniers_spawn[classe] = temps_actuel
    # Mettre à jour et dessiner les ennemis
    for ennemi in liste_ennemis:
        ennemi.update(player_x, player_y)
        ennemi.dessiner(screen, offset_x, offset_y)
    # Dessiner le joueur au centre de l'écran (Vraies coordonnees)
    player_real_rect = pygame.Rect(0,0, 50, 50)
    player_real_rect.center = (player_x, player_y)
    #Dessine le joueur
    player_screen_rect = pygame.Rect(width // 2, height // 2, 50, 50)
    player_screen_rect.center = (width // 2, height // 2)
    pygame.draw.rect(screen, couleur_joueur, player_screen_rect)
    #Gerer le tir du joueur
    if liste_ennemis:
        cible_proche= min(liste_ennemis, key=lambda ennemi: math.hypot(ennemi.x - player_x, ennemi.y - player_y))
        for armes in type_armes:
            if armes.tirer(temps_actuel) and math.hypot(cible_proche.x - player_x, cible_proche.y - player_y)<=armes.range:
                nouveau_projectile = armes.classe(player_x, player_y, 15, cible_proche, homing=armes.homing)
                liste_projectiles.append(nouveau_projectile)

    #Dessiner les projectiles du joueur
    for proj in liste_projectiles[:]:
        proj.update(liste_ennemis)
        proj.dessiner(screen, offset_x, offset_y)

    #Gerer les tirs des ennemis
    for proj in liste_projectiles_ennemis[:]:
        proj.update([])
        proj.dessiner(screen, offset_x, offset_y)

        if proj.rect.colliderect(player_real_rect):
            liste_projectiles_ennemis.remove(proj)
        elif math.hypot(proj.x - player_x, proj.y - player_y) > height:
            liste_projectiles_ennemis.remove(proj)
            #Gerer les degats au joueur ici
    pygame.display.flip()

pygame.quit()

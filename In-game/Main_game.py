import pygame
import random
import math
from Menu import *

pygame.init()

ennemy_spawn_delay=2000  ##Délai entre chaque spawn d'ennemi en millisecondes TEMPORAIRE

# Configuration de la fenêtre
screen = pygame.display.set_mode((width, height))
#Classes

class ennemi_main:
    """Classe principale des ennemis"""
    def __init__(self,x,y,vitesse,hp,arme=None): ##AJOUTER PLUS TARD PARAMETRES COMME VIE, SPRITE AVEC CHEMIN D'ACCES, ETC
        self.x=x    ##Coordonnees reelles de l'ennemi
        self.y=y    ##Coordonnees reelles de l'ennemi
        self.vitesse=vitesse    ##Vitesse de deplacement de l'ennemi
        self.hp=hp  ##Points de vie de l'ennemi
        self.arme=arme  ##Arme de l'ennemi
        self.rect = pygame.Rect(self.x, self.y, 50, 50) ##Rectangle de collision de l'ennemi
        self.rect.center = (self.x, self.y) ##Centre le rectangle de collision sur les coordonnees reelles de l'ennemi

    def dessiner(self,screen,offset_x,offset_y):    ##Dessine l'ennemi a l'ecran en fonction du decalage de la camera
        pygame.draw.rect(screen,(0,0,255),(self.rect.x - offset_x,self.rect.y - offset_y,50,50))  ##Dessine un rectangle bleu representant l'ennemi(LE BLEU EST TEMPORAIRE), on utilise le self.rect.x pour avoir les coordonnees du centre de l'ennemi sinon, les coordonnees sont egal au coin en haut a gauche du rectangle

    def update(self, player_x, player_y):   ##Met a jour la position de l'ennemi pour qu'il suive le joueur
        # Calculer la direction vers le joueur
        direction_x = player_x - self.x ##Difference de x
        direction_y = player_y - self.y ##Difference de y
        distance = math.hypot(direction_x, direction_y) ##Pythagore
        #Armes ennemies
        if self.arme:
            distance_arret = self.arme.range*0.8  ##Distance a laquelle l'ennemi s'arrete de suivre le joueur pour tirer dans ce cas, 80% de la portée de l'arme
        else:
            distance_arret = 0  ##Si l'ennemi n'a pas d'arme, il ne s'arrete jamais
        if distance > distance_arret and distance != 0:
            self.x += (direction_x / distance) * self.vitesse
            self.y += (direction_y / distance) * self.vitesse

        self.rect.center = (self.x, self.y)

        if self.arme and distance <= self.arme.range:   
            if self.arme.tirer(temps_actuel):
                cible=type('Cible',(),{'x':player_x,'y':player_y})()  ##Crée un objet temporaire pour représenter la cible du projectile (pris d'internet car si je recodais une fonction joueur, il aurait fallu que je change tout le code)
                nouveau_projectile = self.arme.classe(self.x, self.y, 10, cible, homing=self.arme.homing)
                liste_projectiles_ennemis.append(nouveau_projectile)

    @staticmethod   ##Sert a attribuer une fonction a une classe sans avoir besoin d'instancier un objet
    def calculer_pos_spawn(player_x, player_y,width,height):    ##Calcule une position de spawn aleatoire autour du joueur
        distance=math.hypot(width,height)/2 ##Pythagore mais plus simple
        angle=random.uniform(0,2*math.pi)   ##Angle aléatoire en radians
        return (player_x + distance*math.cos(angle), player_y + distance*math.sin(angle))   ##Calcule les coordonnees de spawn en fonction de l'angle et de la distance
    

class ennemi_simple(ennemi_main):
    """Classe des ennemis simples"""
    spawn_delay=ennemy_spawn_delay
    def __init__(self,x,y):
        super().__init__(x,y,2,2)  ##Appelle le constructeur de la classe parente avec une vitesse de 2


class ennemi_rapide(ennemi_main):
    """Classe des ennemis rapides"""
    spawn_delay=ennemy_spawn_delay//2
    def __init__(self,x,y,):
        super().__init__(x,y,4,3)  ##Appelle le constructeur de la classe parente avec une vitesse de 4

class ennemi_tireur(ennemi_main):
    """Classe des ennemis tireurs"""
    spawn_delay=ennemy_spawn_delay*2
    def __init__(self,x,y):
        arme_ennemi=weapon_main(1000, projectile_ennemi,homing=False,range_max=1/3*height)  ##Crée une arme pour l'ennemi avec un délai de 1000ms entre chaque tir et des projectiles non homing
        super().__init__(x,y,1,1,arme=arme_ennemi)  ##Appelle le constructeur de la classe parente avec une vitesse de 1 et une arme

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

class projectile_ennemi(projectiles_general):
    """Classe des projectiles ennemis"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=None, couleur=(0,0,0))  ##Appelle le constructeur de la classe parente avec une couleur noire

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
pv_joueur=10  ##Points de vie du joueur

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

        for ennemi in liste_ennemis:
            if proj.rect.colliderect(ennemi.rect):
                if proj in liste_projectiles:
                    liste_projectiles.remove(proj)
                ennemi.hp -= 1
                if ennemi.hp <= 0:
                    liste_ennemis.remove(ennemi)
                break
            elif math.hypot(proj.x - player_x, proj.y - player_y) > height:
                if proj in liste_projectiles:
                    liste_projectiles.remove(proj)

    #Gerer les tirs des ennemis
    for proj in liste_projectiles_ennemis[:]:
        proj.update([])
        proj.dessiner(screen, offset_x, offset_y)

        if proj.rect.colliderect(player_real_rect):
            liste_projectiles_ennemis.remove(proj)
            pv_joueur -= 1
            if pv_joueur <= 0:
                play = False  ##Le joueur meurt
        elif math.hypot(proj.x - player_x, proj.y - player_y) > height:
            if proj in liste_projectiles_ennemis:
                liste_projectiles_ennemis.remove(proj)

    #Gerer collisions ennemis-joueur
    for ennemi in liste_ennemis[:]:
        if ennemi.rect.colliderect(player_real_rect):
            liste_ennemis.remove(ennemi)
            pv_joueur -= 1
            if pv_joueur <= 0:
                play = False  ##Le joueur meurt
    pygame.display.flip()

pygame.quit()

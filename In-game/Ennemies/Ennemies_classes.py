import pygame
import math
import random
from Main_game import*

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
        
class projectile_ennemi(projectiles_general):
    """Classe des projectiles ennemis"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=None, couleur=(0,0,0))  ##Appelle le constructeur de la classe parente avec une couleur noire

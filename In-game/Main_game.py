import pygame
import random
import math
from Menu import *
from Sounddesign import*
from menu_pause import*
from random_module import*

pygame.init()
echelle_difficulte=0
vitesse_joueur = 0  ##Vitesse de deplacement du joueur (définie dans lancer_jeu)
image_marcel=None
image_marcel_liste=[]
image_philippe=None
image_philippe_liste=[]
upgrades_joueur={}  ##défini dans lancer_jeu
laser_sprite=None
roquette_sprite=None
sprite_explosion_roquette=None
enemi_spawn_delay=2000
offset_x,offset_y=0,0  ##Décalage de la caméra par rapport au centre du monde, utilisé pour dessiner les éléments à l'écran
liste_ennemis=[]    ##Liste pour stocker les ennemis, définie dans lancer_jeu
# Couleurs (importées de Menu)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# position de la base (centre du monde) utilisée pour la flèche
base_x, base_y = 0, 0

def fleche_vers_destination(player_x, player_y, destination_x, destination_y):
    if destination_x>offset_x+width or destination_x<offset_x or destination_y>offset_y+height or destination_y<offset_y:
        angle = math.atan2(destination_y - player_y, destination_x - player_x)
        arrow_length = width // 30
        arrow_size=width//100
        arrow_x = width // 2 + math.cos(angle) * arrow_length
        arrow_y = height // 2 + math.sin(angle) * arrow_length
        pygame.draw.polygon(screen, red, [
                                        (arrow_x, arrow_y),
                                        (arrow_x - arrow_size * math.cos(angle - math.pi / 6),
                                        arrow_y - arrow_size * math.sin(angle - math.pi / 6)),
                                        (arrow_x - arrow_size * math.cos(angle + math.pi / 6),
                                        arrow_y - arrow_size * math.sin(angle + math.pi / 6))])
    return

#Classes
class ennemi_main:
    """Classe principale des ennemis"""
    def __init__(self,x,y,vitesse=1,hp=1,arme=None,xp=0,sprite=None,vitesse_animation=0.15,taille_hitbox=[50,50], degat=10): ##AJOUTER PLUS TARD PARAMETRES COMME VIE, SPRITE AVEC CHEMIN D'ACCES, ETC
        self.x=x	##Coordonnees reelles de l'ennemi
        self.y=y	##Coordonnees reelles de l'ennemi
        self.vitesse=vitesse+echelle_difficulte/10    ##Vitesse de deplacement de l'ennemi
        self.hp=hp+echelle_difficulte  ##Points de vie de l'ennemi
        self.arme=arme 	##Arme de l'ennemi
        self.xp=xp	##xp de l'ennemi
        self.hitbox=taille_hitbox
        self.degat=degat+echelle_difficulte

        self.sprite_list=sprite if isinstance(sprite,list) else ([sprite] if sprite else [])
        self.animation_index=0
        self.vitesse_animation=vitesse_animation+echelle_difficulte*0.01  ##Vitesse d'animation qui augmente avec la difficulté

        self.rect=pygame.Rect(self.x,self.y,self.hitbox[0],self.hitbox[1])
        self.rect.center=(self.x,self.y)

    def dessiner(self,screen,offset_x,offset_y):    ##Dessine l'ennemi a l'ecran en fonction du decalage de la camera
        pos_ecran=(self.rect.x-offset_x,self.rect.y-offset_y)
        ##pygame.draw.rect(screen,(0,0,255),pygame.Rect(self.rect.x-offset_x,self.rect.y-offset_y,self.hitbox[0],self.hitbox[1]))

        if self.sprite_list:
            if len(self.sprite_list)>1:
                self.animation_index+=self.vitesse_animation
                if self.animation_index>=len(self.sprite_list):
                    self.animation_index=0
            image_a_afficher=self.sprite_list[int(self.animation_index)]
            screen.blit(image_a_afficher,pos_ecran)
        else:
            pygame.draw.rect(screen,(0,255,255),(pos_ecran[0],pos_ecran[1],50,50))
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
            if self.arme.tirer():
                cible=type('Cible',(),{'x':player_x,'y':player_y})()  ##Crée un objet temporaire pour représenter la cible du projectile (pris d'internet car si je recodais une fonction joueur, il aurait fallu que je change tout le code)
                nouveau_projectile = self.arme.classe(self.x, self.y, self.arme.vitesse, cible, homing=self.arme.homing,range=self.arme.range_balle,degat=self.arme.degat,aoe=self.arme.aoe,aoe_rayon=self.arme.aoe_rayon,degat_AOE=self.arme.degat_AOE)  ##Crée un nouveau projectile en utilisant la classe de l'arme de l'ennemi
                liste_projectiles_ennemis.append(nouveau_projectile)
    def prendre_degats(self, degats_infliges):
        self.hp -= degats_infliges
        if self.hp <= 0:
            if self in liste_ennemis:
                liste_ennemis.remove(self)
        return False
    
    @staticmethod   ##Sert a attribuer une fonction a une classe sans avoir besoin d'instancier un objet
    def calculer_pos_spawn(player_x, player_y,width,height):    ##Calcule une position de spawn aleatoire autour du joueur
        distance=math.hypot(width,height)/2 ##Pythagore mais plus simple
        angle=random.uniform(0,2*math.pi)   ##Angle aléatoire en radians
        return (player_x + distance*math.cos(angle), player_y + distance*math.sin(angle))   ##Calcule les coordonnees de spawn en fonction de l'angle et de la distance
    

class ennemi_simple(ennemi_main):
    """Classe des ennemis simples"""
    spawn_delay=enemi_spawn_delay
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/600,hp=3,xp=2,degat=10)  ##Appelle le constructeur de la classe parente avec une vitesse de 2


class Marcel(ennemi_main):
    """Classe des ennemis rapides"""
    spawn_delay=enemi_spawn_delay*1.5
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/300,hp=2,xp=2,sprite=image_marcel_liste,taille_hitbox=[image_marcel_liste[0].get_width(),image_marcel_liste[0].get_height()],degat=5)  ##Appelle le constructeur de la classe parente avec une vitesse de 4

class ennemi_tireur(ennemi_main):
    """Classe des ennemis tireurs"""
    spawn_delay=enemi_spawn_delay*3
    def __init__(self,x,y):
        arme_ennemi=weapon_main(1000-echelle_difficulte, projectile_ennemi,homing=False,portee_detection=1/3*height,vitesse=width/400+echelle_difficulte)  ##Crée une arme pour l'ennemi avec un délai de 1000ms entre chaque tir et des projectiles non homing
        super().__init__(x,y,vitesse=width/600,hp=1,arme=arme_ennemi,xp=1,degat=7)  ##Appelle le constructeur de la classe parente avec une vitesse de 1 et une arme

class Philippe(ennemi_main):
    """Classe des ennemis lourds"""
    spawn_delay=enemi_spawn_delay*2
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/1200,hp=5,xp=3,sprite=image_philippe_liste,taille_hitbox=[image_philippe_liste[0].get_width(),image_philippe_liste[0].get_height()],degat=20)
            
class projectiles_general:
    """Classe principale des projectiles"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=None,couleur=(0,255,0),degat=1,range=10,aoe=False,aoe_rayon=None,degat_AOE=0,duree_AOE=0,duree=None):
        self.x=x
        self.y=y
        self.start_x=x
        self.start_y=y
        self.vitesse=vitesse
        self.cible=cible_initiale
        self.homing=homing
        self.couleur=couleur
        self.degat=degat
        self.degat_AOE=degat_AOE
        self.range=range
        self.image = sprite_path
        self.aoe=aoe
        self.duree=duree
        self.duree_AOE=duree_AOE
        self.temps_creation=pygame.time.get_ticks()
        self.aoe_rayon=aoe_rayon if aoe_rayon is not None else width/10
        if sprite_path!=None:
            self.rect = self.image.get_rect(center=(self.x, self.y))
        if sprite_path==None:
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
            radians=math.atan2(-direction_y, direction_x)
            self.angle=math.degrees(radians)
    def update(self,liste_ennemis,player_pos=None):
        if self.homing:
            #Recalcule la direction vers la cible
            if player_pos:
                self.calculer_direction(player_pos[0],player_pos[1])
            elif self.cible in liste_ennemis:
                self.calculer_direction(self.cible.x, self.cible.y)
            else:
                if liste_ennemis:
                    self.cible = min(liste_ennemis, key=lambda ennemi: (ennemi.x - self.x)**2 + (ennemi.y - self.y)**2)
        if self.duree is not None:
            if pygame.time.get_ticks() - self.temps_creation >= self.duree:
                return True  ##Indique que le projectile doit être supprimé

        #Mouvement du projectile
        self.x += self.dir_x * self.vitesse
        self.y += self.dir_y * self.vitesse
        self.rect.center = (self.x, self.y)
    def est_trop_loin(self):
        return math.hypot(self.x-self.start_x, self.y-self.start_y) > self.range
    def dessiner(self,screen,offset_x,offset_y):
        pos_ecran_x=self.rect.x-offset_x
        pos_ecran_y=self.rect.y - offset_y
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect= rotated_image.get_rect(center=(pos_ecran_x, pos_ecran_y))
            screen.blit(rotated_image, new_rect)
        else:
            pygame.draw.rect(screen,self.couleur,(pos_ecran_x,pos_ecran_y,10,10))

class projectile_laser(projectiles_general):
    """Classe des projectiles laser"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite=None,degat=1,range=10,duree_AOE=0,aoe=False,aoe_rayon=None,degat_AOE=0):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite, couleur=(255,0,0),degat=degat+upgrades_joueur["degats"],range=range,duree_AOE=duree_AOE,aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE)  ##Appelle le constructeur de la classe parente avec une couleur rouge

class projectile_roquette(projectiles_general):
    """Classe des projectiles roquettes"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=True,sprite=None,degat=3,range=10,aoe=True,aoe_rayon=None,degat_AOE=1,duree_AOE=333):
        if aoe_rayon is None:
            aoe_rayon=width/10
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite, couleur=(255,165,0),degat=degat+upgrades_joueur["degats"],range=range,aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE,duree_AOE=duree_AOE)  ##Appelle le constructeur de la classe parente avec une couleur orange

class projectile_mine(projectiles_general):
    """Classe des projectiles roquettes"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite=None,degat=3,range=10,aoe=True,aoe_rayon=None,degat_AOE=1,duree_AOE=333,duree=5000):
        if aoe_rayon is None:
            aoe_rayon=width/10
        super().__init__(x,y,0,cible_initiale,homing=homing, sprite_path=sprite, couleur=(255,165,0),degat=degat+upgrades_joueur["degats"],range=range,aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE,duree_AOE=duree_AOE,duree=duree)  ##Appelle le constructeur de la classe parente avec une couleur orange

    def update(self, liste_ennemis, player_pos=None):
        maintenant = pygame.time.get_ticks()
        # La mine renvoie True UNIQUEMENT si le temps est écoulé
        if maintenant - self.temps_creation >= self.duree:
            return True 
        return False



class projectile_ennemi(projectiles_general):
    """Classe des projectiles ennemis"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=None,degat=7,range=10,aoe=False,aoe_rayon=None,degat_AOE=0,duree_AOE=0):
        super().__init__(x,y,vitesse+echelle_difficulte/10,cible_initiale,homing=homing, sprite_path=sprite_path, couleur=(0,0,0),degat=degat+echelle_difficulte,range=range,aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE,duree_AOE=duree_AOE)  ##Appelle le constructeur de la classe parente avec une couleur noire

class weapon_main:
    """Classe principale des armes"""
    def __init__(self,delai,classe_projectile,homing=False,portee_detection=None,vitesse=10,aoe=False,aoe_rayon=None,degat=1,degat_AOE=1,duree_AOE=333,duree=None):
        if portee_detection is None:
            portee_detection=height/2
        if aoe_rayon is None:
            aoe_rayon=width/10
        self.delai=delai  ##Temps entre chaque tir en millisecondes
        self.dernier_tir=0  ##Temps du dernier tir
        self.classe=classe_projectile  ##Classe du projectile tiré
        self.homing=homing  ##Indique si les projectiles sont homing ou non
        self.range=portee_detection  ##Portée maximale de l'arme
        self.vitesse=vitesse  ##Vitesse des projectiles tirés
        self.range_balle=portee_detection*2  ##Portée maximale des projectiles tirés
        self.aoe=aoe
        self.degat=degat
        self.degat_AOE=degat_AOE
        self.aoe_rayon=aoe_rayon
        self.duree_AOE=duree_AOE
        self.duree=duree
    def tirer(self):
        if pygame.time.get_ticks() - self.dernier_tir >= self.delai:
            self.dernier_tir = pygame.time.get_ticks()
            return  True
        return False
    def compenser_pause(self,duree_pause):
        self.dernier_tir += duree_pause  ##Décale le temps du dernier tir pour compenser la pause
        
class Explosion:
    def __init__(self,x,y,sprite_list,vitesse_animation=0.1):
        self.x=x
        self.y=y
        self.sprite_list=sprite_list
        self.animation_index=0
        self.vitesse_animation=vitesse_animation
        self.terminee=False
        
    def update(self):
        self.animation_index+=self.vitesse_animation
        if self.animation_index>=len(self.sprite_list):
            self.terminee=True
            
    def dessiner(self,screen,offset_x,offset_y):
        if not self.terminee:
             image=self.sprite_list[int(self.animation_index)]
             rect=image.get_rect(center=(self.x-offset_x,self.y-offset_y))
             screen.blit(image,rect)

class AOE:
    def __init__(self,x,y,rayon,degat_par_tick,duree_ms,interval_tick_ms=100,sprite=None):
        self.x=x
        self.y=y
        self.rayon=rayon
        self.degat=degat_par_tick+upgrades_joueur["degats_aoe"]

        self.duree=duree_ms+upgrades_joueur["duree_aoe"]*100  ##Durée totale de l'AOE en millisecondes
        self.interval_tick=interval_tick_ms
        self.sprite=sprite

        self.temps_creation=pygame.time.get_ticks()
        self.dernier_tick=self.temps_creation
        self.dernier_tick=pygame.time.get_ticks()-self.interval_tick  ##Permet de faire en sorte que les dégâts soient appliqués immédiatement à la création de l'AOE
        self.terminee=False

        if self.sprite:
            taille=int(self.rayon*2)
            self.sprite=pygame.transform.scale(self.sprite,(taille,taille))
            self.rect=self.sprite.get_rect(center=(self.x,self.y))

    def update(self,liste_ennemis):
        maintenant=pygame.time.get_ticks()

        #verifie si la duree de l'aoe est terminee
        if maintenant - self.temps_creation >= self.duree:
            self.terminee=True
            return
        
        elif maintenant - self.dernier_tick >= self.interval_tick:

            for ennemi in liste_ennemis:
                if math.hypot(self.x-ennemi.x,self.y-ennemi.y)<=self.rayon:
                    ennemi.hp-=self.degat

            self.dernier_tick=maintenant

    def dessiner(self,screen,offset_x,offset_y):
        if self.terminee:
            return
        if self.sprite:
            pos_ecran=(self.x-offset_x-self.rayon,self.y-offset_y-self.rayon)
            screen.blit(self.sprite,pos_ecran)
        else:
            pygame.draw.circle(screen,(255,165,0),(int(self.x-offset_x),int(self.y-offset_y)),self.rayon,2)

def lancer_jeu(settings):
    global width, height, screen, pv_joueur, liste_projectiles_ennemis, image_marcel, image_marcel_liste,echelle_difficulte,laser_sprite,roquette_sprite,upgrades_joueur, sprite_explosion_roquette,image_philippe,image_philippe_liste,offset_x,offset_y,enemi_spawn_delay,liste_ennemis
    for sprite,classe in [('projectile_laser.png',laser_sprite),('projectile_roquette.png',roquette_sprite)]:
        img=pygame.image.load(sprite).convert_alpha()
        img=pygame.transform.scale(img,(width/25,int(img.get_height()/img.get_width()*width/25)))
        if classe==laser_sprite:
            laser_sprite=img
        else:
            roquette_sprite=img
    #Sprite explosion Roquette
    sprite_explosion_roquette=[]
    for sprite in ["Explosion1.png","Explosion2.png"]:
        img=pygame.image.load(sprite).convert_alpha()
        img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
        sprite_explosion_roquette.append(img)
    image_marcel_liste.clear()
    image_philippe_liste.clear()
    echelle_difficulte=0
    enemi_spawn_delay=2000-echelle_difficulte
    # Mettre à jour les spawn delays des classes en fonction de la difficulté
    ennemi_simple.spawn_delay=enemi_spawn_delay
    Marcel.spawn_delay=enemi_spawn_delay*1.5
    ennemi_tireur.spawn_delay=enemi_spawn_delay*3
    Philippe.spawn_delay=enemi_spawn_delay*2
    upgrades_joueur=dico_upgrades
    width = settings["width"]
    height = settings["height"]
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN if settings["fullscreen"] else 0)
    en_jeu=True
    #Variables de jeu
    player_x, player_y = 0, 0 # Position réelle du joueur dans le monde
    vitesse_joueur = width/300  ##Vitesse de deplacement du joueur
    couleur_joueur = (255, 0, 0)
    types_ennemis = [ennemi_simple, Marcel,ennemi_tireur,Philippe]  ##Liste des types d'ennemis
    liste_ennemis = []  ##Liste pour stocker les ennemis
    derniers_spawn = {classe: 0 for classe in types_ennemis}  ##Dictionnaire pour stocker le dernier spawn de chaque type d'ennemi
    clock = pygame.time.Clock()
    liste_projectiles = []  ##Liste pour stocker les projectiles
    laser=weapon_main(500, projectile_laser,homing=False,portee_detection=height/5,vitesse=width/200)  ##Crée une arme laser avec un délai de 500ms entre chaque tir et des projectiles homing
    roquette=weapon_main(10000, projectile_roquette,homing=True,portee_detection=width/5,vitesse=width/300,aoe=True,aoe_rayon=width/10,duree_AOE=333)  ##Crée une arme roquette avec un délai de 1500ms entre chaque tir et des projectiles homing
    mine=weapon_main(5000, projectile_mine,homing=False,portee_detection=math.inf,vitesse=0,aoe=True,aoe_rayon=width/10,duree_AOE=5000,duree=10000,degat_AOE=1)  ##Crée une arme mine avec un délai de 15000ms entre chaque tir et des projectiles non homing
    type_armes=[laser,roquette,mine]   ##Liste des types d'armes
    liste_projectiles_ennemis=[]  ##Liste pour stocker les projectiles des ennemis
    liste_explosions=[]
    pv_joueur=100  ##Points de vie du joueur
    pv_max_joueur=100
    pygame.mixer.music.stop()
    xp=0
    xp_for_level=10
    niveau=0
    astro=pygame.image.load("Astro.png").convert_alpha()
    astro=pygame.transform.scale(astro,(width/20,int(astro.get_height()/astro.get_width()*width/20)))
    font=pygame.font.Font(None,int(width/25))
    pv_heal_cooldown=0
    duree_journee=0
    nombre_journees=0
    dernier_soin=pygame.time.get_ticks()
    maintenant=0
    liste_aoe=[]
    #Importation des sprites de Marcel
    for i in range(1,7):
        image_marcel=pygame.image.load(f"Marcel({i}).png").convert_alpha()
        image_marcel=pygame.transform.scale(image_marcel,(width/25,int(image_marcel.get_height()/image_marcel.get_width()*width/25)))
        image_marcel_liste.append(image_marcel)
    #Importation des sprites de Philippe
    for i in range(1,7):
        image_philippe=pygame.image.load(f"Philippe({i}).png").convert_alpha()
        image_philippe=pygame.transform.scale(image_philippe,(width/13,int(image_philippe.get_height()/image_philippe.get_width()*width/13)))
        image_philippe_liste.append(image_philippe)
    while en_jeu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    temps_debut_pause=pygame.time.get_ticks()
                    afficher_menu_pause()
                    duree_pause=pygame.time.get_ticks()-temps_debut_pause

                    for classe in derniers_spawn:
                        derniers_spawn[classe] += duree_pause  ##Décale les temps de spawn des ennemis pour compenser la pause
                    for armes in type_armes:
                        armes.compenser_pause(duree_pause)  ##Décale les temps de tir des armes pour compenser la pause
                    for ennemi in liste_ennemis:
                        if ennemi.arme:
                            ennemi.arme.compenser_pause(duree_pause)  ##Décale les temps de tir des armes des ennemis pour compenser la pause
                            
        player_real_rect = pygame.Rect(0,0,astro.get_width()/1.4,astro.get_height())
        player_real_rect.center = (player_x, player_y)
        #Mouvement et logique du joueur
        if True:
            #Mouvement du joueur
            touches = pygame.key.get_pressed()
            if touches[pygame.K_d]:
                player_x += vitesse_joueur
            if touches[pygame.K_q] or touches[pygame.K_a]:
                player_x -= vitesse_joueur
            if touches[pygame.K_s]:
                player_y += vitesse_joueur
            if touches[pygame.K_z] or touches[pygame.K_w]:
                player_y -= vitesse_joueur
            if touches[pygame.K_e] and math.hypot(abs(player_x),abs(player_y))<width/4 and niveau>=1:
                temps_debut_pause=pygame.time.get_ticks()
                for _ in range(niveau):
                    upgrades_joueur=level_up(screen,width,height)
                    niveau-=1
                liste_ennemis.clear()
                liste_projectiles_ennemis.clear()
                liste_projectiles.clear()
                liste_aoe.clear()
                nombre_journees+=1
                duree_journee=0
                # Mettre à jour HP max et scale le HP actuel proportionnellement
                ancien_pv_max=pv_max_joueur
                pv_max_joueur=100+(upgrades_joueur["pv"])*10
                if ancien_pv_max > 0:
                    pv_joueur = int(pv_joueur * (pv_max_joueur / ancien_pv_max))
                vitesse_joueur=width/300+(upgrades_joueur["vitesse"])*width/900
                laser=weapon_main(500/(1+upgrades_joueur["cadence_de_tir"]/10), projectile_laser,homing=False,portee_detection=width/10+upgrades_joueur["portee"]*10,vitesse=width/200+upgrades_joueur["vitesse_balles"]/10,degat=1+upgrades_joueur["degats"])  ##Crée une arme laser avec un délai de 500ms entre chaque tir et des projectiles homing
                roquette=weapon_main(10000/(1+upgrades_joueur["cadence_de_tir"]/10), projectile_roquette,homing=True,portee_detection=width/5+upgrades_joueur["portee"]*10,vitesse=width/300+upgrades_joueur["vitesse_balles"]/10,aoe=True,aoe_rayon=width/20+5*upgrades_joueur["deflagrations"],degat=3+upgrades_joueur["degats"],degat_AOE=1+upgrades_joueur["degats_aoe"],duree_AOE=333)  ##Crée une arme roquette avec un délai de 1500ms entre chaque tir et des projectiles homing
                type_armes=[laser,roquette]   ##Liste des types d'armes
                #Explosion
                sprite_explosion_roquette=[]
                for sprite in ["Explosion1.png","Explosion2.png"]:
                    img=pygame.image.load(sprite).convert_alpha()
                    img=pygame.transform.scale(img,(width/10+10*upgrades_joueur["deflagrations"],int(img.get_height()/img.get_width()*(width/10+10*upgrades_joueur["deflagrations"]))))
                    sprite_explosion_roquette.append(img)
                for sprite,classe in [('projectile_laser.png',laser_sprite),('projectile_roquette.png',roquette_sprite)]:
                    img=pygame.image.load(sprite).convert_alpha()
                    img=pygame.transform.scale(img,(width/25+5*upgrades_joueur["taille_projectiles"],int(img.get_height()/img.get_width()*(width/25+5*upgrades_joueur["taille_projectiles"]))))
                    if classe==laser_sprite:
                        laser_sprite=img
                    else:
                        roquette_sprite=img
                duree_pause=pygame.time.get_ticks()-temps_debut_pause
                for classe in derniers_spawn:
                    derniers_spawn[classe]+=duree_pause
                for armes in type_armes:
                        armes.compenser_pause(duree_pause)  ##Décale les temps de tir des armes pour compenser la pause
                for ennemi in liste_ennemis:
                    if ennemi.arme:
                        ennemi.arme.compenser_pause(duree_pause)  ##Décale les temps de tir des armes des ennemis pour compenser la pause
            #Fond blanc
            screen.fill((255, 255, 255))

            # Gérer le spawn des ennemis
            for classe in types_ennemis:
                if pygame.time.get_ticks() - derniers_spawn[classe] >= classe.spawn_delay:
                    spawn_x, spawn_y = classe.calculer_pos_spawn(player_x, player_y, width, height)
                    nouvel_ennemi = classe(spawn_x, spawn_y)
                    liste_ennemis.append(nouvel_ennemi)
                    derniers_spawn[classe] = pygame.time.get_ticks()
            # Mettre à jour les ennemis
            for ennemi in liste_ennemis:
                ennemi.update(player_x, player_y)
                # Mettre à jour la vitesse d'animation en fonction de la difficulté
                if ennemi.sprite_list:
                    ennemi.vitesse_animation=0.15+echelle_difficulte*0.01
                
            #Mettre à jour les explosions
            for explosion in liste_explosions[:]:
                explosion.update()
                if explosion.terminee:
                    liste_explosions.remove(explosion)
                    
            # Gérer les tirs du joueur
            if liste_ennemis or mine in type_armes: # On autorise le tir si ennemis OU si on a des mines
                for armes in type_armes:
                    # Condition spéciale pour la mine : on la pose toujours sous nos pieds
                    if armes.classe == projectile_mine:
                        if armes.tirer():
                            # On crée une cible factice sur le joueur pour la mine
                            cible_ici = type('Cible', (), {'x': player_x, 'y': player_y})()
                            nouveau_p = projectile_mine(
                                player_x, player_y, 0, cible_ici,
                                degat=armes.degat,
                                range=armes.range_balle,
                                aoe=armes.aoe,
                                aoe_rayon=armes.aoe_rayon,
                                degat_AOE=armes.degat_AOE,
                                duree_AOE=armes.duree_AOE,
                                sprite=None,
                                duree=armes.duree
                            )
                            liste_projectiles.append(nouveau_p)
                    
                    # Tir normal pour les autres armes (Laser, Roquette)
                    elif liste_ennemis:
                        cible_proche = min(liste_ennemis, key=lambda ennemi: (ennemi.x - player_x)**2 + (ennemi.y - player_y)**2)
                        if armes.tirer() and math.hypot(cible_proche.x - player_x, cible_proche.y - player_y) <= armes.range_balle:
                            nouveau_p = armes.classe(
                                player_x, player_y, armes.vitesse, cible_proche, 
                                homing=armes.homing, range=armes.range_balle,
                                sprite=laser_sprite if armes==laser else roquette_sprite,
                                degat=armes.degat, aoe=armes.aoe, aoe_rayon=armes.aoe_rayon,
                                degat_AOE=armes.degat_AOE, duree_AOE=armes.duree_AOE
                            )
                            liste_projectiles.append(nouveau_p)
                        
            for proj in liste_projectiles[:]:

                temps_ecoule = proj.update(liste_ennemis)

                # 1. Détection collision
                hit_ennemi = None
                for ennemi in liste_ennemis:
                    if proj.rect.colliderect(ennemi.rect):
                        hit_ennemi = ennemi
                        break

                # 2. APPLIQUER DEGATS DIRECTS → METTRE ICI
                if hit_ennemi:
                    hit_ennemi.prendre_degats(proj.degat)

                # 3. SUPPRESSION ET AOE
                if hit_ennemi or proj.est_trop_loin() or temps_ecoule:

                    if proj.aoe:
                        aoe_zone = AOE(
                            proj.x,
                            proj.y,
                            proj.aoe_rayon,
                            proj.degat_AOE,
                            proj.duree_AOE
                        )
                        liste_aoe.append(aoe_zone)

                    liste_projectiles.remove(proj)

            # Mettre à jour les projectiles des ennemis
            for proj in liste_projectiles_ennemis[:]:
                proj.update([], player_pos=(player_x, player_y))
                if proj.rect.colliderect(player_real_rect):
                    liste_projectiles_ennemis.remove(proj)
                    pv_joueur -= proj.degat
                    Soundhit.play()
                elif proj.est_trop_loin():
                    if proj.aoe:  # <-- add this
                        explosion = Explosion(proj.x, proj.y, sprite_explosion_roquette)
                        liste_explosions.append(explosion)
                        aoe_zone = AOE(proj.x, proj.y, proj.aoe_rayon, proj.degat_AOE, proj.duree_AOE, interval_tick_ms=300)
                        liste_aoe.append(aoe_zone)
                    if proj in liste_projectiles_ennemis:
                        liste_projectiles_ennemis.remove(proj)
            
            for ennemi in liste_ennemis[:]:
                if ennemi.rect.colliderect(player_real_rect):
                    pv_joueur -= ennemi.degat
                    liste_ennemis.remove(ennemi)

            #Gerer les AOE
            for aoe in liste_aoe[:]:
                aoe.update(liste_ennemis)
                aoe.dessiner(screen,offset_x,offset_y)
                if aoe.terminee:
                    liste_aoe.remove(aoe)

        
        #Maintient le joueur au centre de l'ecran en calculant le decalage
        offset_x = player_x - (width // 2)
        offset_y = player_y - (height // 2)

        # Dessiner une grille pour voir le mouvement de la caméra
        for i in range(-5000, 5000, 100):
            pygame.draw.line(screen, (240, 240, 240), (i - offset_x, -5000 - offset_y), (i - offset_x, 5000 - offset_y))
            pygame.draw.line(screen, (240, 240, 240), (-5000 - offset_x, i - offset_y), (5000 - offset_x, i - offset_y))

        #Dessiner les ennemis
        for ennemi in liste_ennemis:
            ennemi.dessiner(screen, offset_x, offset_y)
            
        #Dessine le joueur
        astro_rect=astro.get_rect()
        astro_rect.center=(width/2,height/2)
        screen.blit(astro,astro_rect)

        #Dessiner les projectiles du joueur
        for proj in liste_projectiles[:]:
            proj.dessiner(screen, offset_x, offset_y)

        #Dessiner les tirs des ennemis
        for proj in liste_projectiles_ennemis[:]:
            proj.dessiner(screen, offset_x, offset_y)
            
        #Dessiner les explosions
        for explosion in liste_explosions[:]:
            explosion.dessiner(screen,offset_x,offset_y)
            
        #Dessiner la barre de vie
        for rect,color in [("max_health_bar_rect",red),("health_bar_rect",green)]:
            rect=pygame.Rect(width/2,height/2,width/8 if rect=="max_health_bar_rect" else pv_joueur/pv_max_joueur*width/8,height/100)
            rect.topleft=(width/150,height/150)
            pygame.draw.rect(screen,color,rect)
            
        #Dessiner la barre d'exp
        for rect,color in [("xp_for_level_rect",black),("current_xp",blue)]:
            rect=pygame.Rect(width/2,height/2,width/8 if rect=="xp_for_level_rect" else xp/xp_for_level*width/8,height/100)
            rect.topleft=(width/150,height/60)
            pygame.draw.rect(screen,color,rect)
            
        #Gestion de l'exp   
        if xp>=xp_for_level:
            xp-=xp_for_level
            xp_for_level=int(xp_for_level*1.2)
            niveau+=1

        if pv_joueur<=0:
            en_jeu=False
            
        maintenant=pygame.time.get_ticks()
        if upgrades_joueur["regen_pv"]>=1:
            if maintenant-dernier_soin>=1000:
                if pv_joueur+upgrades_joueur["regen_pv"]>=pv_max_joueur and pv_joueur!=pv_max_joueur:
                    pv_joueur=pv_max_joueur
                else:
                    pv_joueur+=upgrades_joueur["regen_pv"]
                dernier_soin=maintenant

        duree_journee+=1
        echelle_difficulte=nombre_journees*5+duree_journee//1200

        # Mettre à jour les spawn delays quand la difficulté change
        enemi_spawn_delay=2000-echelle_difficulte
        ennemi_simple.spawn_delay=enemi_spawn_delay
        Marcel.spawn_delay=enemi_spawn_delay*1.5
        ennemi_tireur.spawn_delay=enemi_spawn_delay*3
        Philippe.spawn_delay=enemi_spawn_delay*2

        rect_centre=pygame.Rect(0,0,150,150)
        rect_centre.center=(-offset_x,-offset_y)
        pygame.draw.rect(screen,(0,26,158),rect_centre)
        
        texte_niveau=font.render(f"Niveaux:{niveau}",True,(0,0,0))
        texte_niveau_rect=texte_niveau.get_rect(topleft=(width/150,height/20))
        screen.blit(texte_niveau,texte_niveau_rect)

        fleche_vers_destination(player_x,player_y,0,0)
        pygame.display.flip()





import pygame
import random
import math
from Menu import *
from Sounddesign import*
from menu_pause import*
from random_module import*

pygame.init()
echelle_difficulte=0
ennemy_spawn_delay=2000-echelle_difficulte  ##Délai entre chaque spawn d'ennemi en millisecondes TEMPORAIRE
vitesse_joueur = width/300  ##Vitesse de deplacement du joueur
image_marcel=None
image_marcel_liste=[]
image_philippe=None
image_philippe_liste=[]

#Classes
def retour_menu():
    en_jeu=False
class ennemi_main:
    """Classe principale des ennemis"""
    def __init__(self,x,y,vitesse=1,hp=1,arme=None,xp=0,sprite=None,vitesse_animation=0.15,taille_hitbox=[50,50]): ##AJOUTER PLUS TARD PARAMETRES COMME VIE, SPRITE AVEC CHEMIN D'ACCES, ETC
        self.x=x    ##Coordonnees reelles de l'ennemi
        self.y=y    ##Coordonnees reelles de l'ennemi
        self.vitesse=vitesse+echelle_difficulte    ##Vitesse de deplacement de l'ennemi
        self.hp=hp+echelle_difficulte  ##Points de vie de l'ennemi
        self.arme=arme  ##Arme de l'ennemi
        self.xp=xp	##xp de l'ennemi
        self.hitbox=taille_hitbox

        self.sprite_list=sprite if isinstance(sprite,list) else ([sprite] if sprite else [])
        self.animation_index=0
        self.vitesse_animation=0.15

        self.rect=pygame.Rect(self.x,self.y,self.hitbox[0],self.hitbox[1])
        self.rect.center=(self.x,self.y)

    def dessiner(self,screen,offset_x,offset_y):    ##Dessine l'ennemi a l'ecran en fonction du decalage de la camera
        pos_ecran=(self.rect.x-offset_x,self.rect.y-offset_y)
        pygame.draw.rect(screen,(0,0,255),pygame.Rect(self.rect.x-offset_x,self.rect.y-offset_y,self.hitbox[0],self.hitbox[1]))

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
                nouveau_projectile = self.arme.classe(self.x, self.y, self.arme.vitesse, cible, homing=self.arme.homing,range=self.arme.range_balle)
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
        super().__init__(x,y,vitesse=width/600,hp=3,xp=2)  ##Appelle le constructeur de la classe parente avec une vitesse de 2


class Marcel(ennemi_main):
    """Classe des ennemis rapides"""
    spawn_delay=ennemy_spawn_delay*1.5
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/300,hp=2,xp=2,sprite=image_marcel_liste,taille_hitbox=[image_marcel_liste[0].get_width(),image_marcel_liste[0].get_height()])  ##Appelle le constructeur de la classe parente avec une vitesse de 4

class ennemi_tireur(ennemi_main):
    """Classe des ennemis tireurs"""
    spawn_delay=ennemy_spawn_delay*3
    def __init__(self,x,y):
        arme_ennemi=weapon_main(1000, projectile_ennemi,homing=False,portee_detection=1/3*height,vitesse=width/400)  ##Crée une arme pour l'ennemi avec un délai de 1000ms entre chaque tir et des projectiles non homing
        super().__init__(x,y,vitesse=width/600,hp=1,arme=arme_ennemi,xp=1)  ##Appelle le constructeur de la classe parente avec une vitesse de 1 et une arme

class Philippe(ennemi_main):
    """Classe des ennemis lourds"""
    spawn_delay=ennemy_spawn_delay*2
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/1200,hp=5,xp=3,sprite=image_philippe_liste,taille_hitbox=[image_philippe_liste[0].get_width(),image_philippe_liste[0].get_height()])

class projectiles_general:
    """Classe principale des projectiles"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=None,couleur=(0,255,0),degat=1,range=10,aoe=False,aoe_rayon=width/10):  ##AJOUTER PLUS TARD SPRITE AVEC CHEMIN D'ACCES ET COULEUR SERT SEULEMENT SI PAS DE SPRITE
        self.x=x
        self.y=y
        self.start_x=x
        self.start_y=y
        self.vitesse=vitesse
        self.cible=cible_initiale
        self.homing=homing
        self.couleur=couleur
        self.degat=degat
        self.range=range
        self.image = sprite_path
        self.aoe=aoe
        self.aoe_rayon=aoe_rayon
        if sprite_path:
            image_originale = pygame.image.load(sprite_path).convert_alpha()
            self.image = pygame.transform.scale(image_originale, (90, 35))
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
                    self.cible = min(liste_ennemis, key=lambda ennemi: math.hypot(ennemi.x - self.x, ennemi.y - self.y))
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
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path='projectile1.png',degat=1,range=10):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite_path, couleur=(255,0,0),degat=degat,range=range)  ##Appelle le constructeur de la classe parente avec une couleur rouge

class projectile_roquette(projectiles_general):
    """Classe des projectiles roquettes"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=True,sprite_path='projectile2.png',degat=3,range=10,aoe=True,aoe_rayon=width/10):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite_path, couleur=(255,165,0),degat=degat,range=range,aoe=aoe,aoe_rayon=aoe_rayon)  ##Appelle le constructeur de la classe parente avec une couleur orange

class projectile_ennemi(projectiles_general):
    """Classe des projectiles ennemis"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=True,sprite_path=None,degat=1,range=10):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite_path, couleur=(0,0,0),degat=degat,range=range)  ##Appelle le constructeur de la classe parente avec une couleur noire

class weapon_main:
    """Classe principale des armes"""
    def __init__(self,delai,classe_projectile,homing=False,portee_detection=1/2*height,vitesse=10,aoe=False,aoe_rayon=width/10):
        self.delai=delai  ##Temps entre chaque tir en millisecondes
        self.dernier_tir=0  ##Temps du dernier tir
        self.classe=classe_projectile  ##Classe du projectile tiré
        self.homing=homing  ##Indique si les projectiles sont homing ou non
        self.range=portee_detection  ##Portée maximale de l'arme
        self.vitesse=vitesse  ##Vitesse des projectiles tirés
        self.range_balle=portee_detection*2  ##Portée maximale des projectiles tirés
        self.aoe=aoe
    def tirer(self):
        if pygame.time.get_ticks() - self.dernier_tir >= self.delai:
            self.dernier_tir = pygame.time.get_ticks()
            return  True
        return False
    def compenser_pause(self,duree_pause):
        self.dernier_tir += duree_pause  ##Décale le temps du dernier tir pour compenser la pause
    
def lancer_jeu(settings):
    global width, height, screen, pv_joueur, liste_projectiles_ennemis, image_marcel, image_marcel_liste
    upgrades_joueur=dico_upgrades
    en_pause=False
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
    roquette=weapon_main(10000, projectile_roquette,homing=True,portee_detection=width/5,vitesse=width/300,aoe=True,aoe_rayon=width/10)  ##Crée une arme roquette avec un délai de 1500ms entre chaque tir et des projectiles homing
    type_armes=[laser,roquette]   ##Liste des types d'armes
    liste_projectiles_ennemis=[]  ##Liste pour stocker les projectiles des ennemis
    pv_joueur=10  ##Points de vie du joueur
    pv_max_joueur=10
    pygame.mixer.music.stop()
    xp=0
    xp_for_level=10
    niveau=0
    astro=pygame.image.load("Astro.png").convert_alpha()
    astro=pygame.transform.scale(astro,(width/20,int(astro.get_height()/astro.get_width()*width/20)))
    font=pygame.font.Font(None,150)
    #Importation des sprites de Marcel
    for i in range(1,7):
        image_marcel=pygame.image.load(f"Marcel({i}).png").convert_alpha()
        image_marcel=pygame.transform.scale(image_marcel,(width/20,int(image_marcel.get_height()/image_marcel.get_width()*width/20)))
        image_marcel_liste.append(image_marcel)
    #Importation des sprites de Philippe
    for i in range(1,7):
        image_philippe=pygame.image.load(f"Philippe({i}).png").convert_alpha()
        image_philippe=pygame.transform.scale(image_philippe,(width/20,int(image_philippe.get_height()/image_philippe.get_width()*width/20)))
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
        #Si en jeu
        if not en_pause:
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
            if touches[pygame.K_e]:
                temps_debut_pause=pygame.time.get_ticks()
                upgrades_joueur=level_up(screen,width,height)
                pv_max_joueur=10+(upgrades_joueur["hp"])
                pv_joueur=pv_joueur+1 if pv_joueur+1<=pv_max_joueur else pv_joueur
                duree_pause=pygame.time.get_ticks()-temps_debut_pause
                for classe in derniers_spawn:
                    derniers_spawn[classe]+=duree_pause
                for armes in type_armes:
                        armes.compenser_pause(duree_pause)  ##Décale les temps de tir des armes pour compenser la pause
                for ennemi in liste_ennemis:
                    if ennemi.arme:
                        ennemi.arme.compenser_pause(duree_pause)  ##Décale les temps de tir des armes des ennemis pour compenser la pause
                
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
            # Gérer les tirs du joueur
            if liste_ennemis:
                cible_proche= min(liste_ennemis, key=lambda ennemi: math.hypot(ennemi.x - player_x, ennemi.y - player_y))
                for armes in type_armes:
                    if armes.tirer() and math.hypot(cible_proche.x - player_x, cible_proche.y - player_y)<=armes.range_balle:
                        nouveau_projectile = armes.classe(player_x, player_y, armes.vitesse, cible_proche, homing=armes.homing,range=armes.range_balle)
                        liste_projectiles.append(nouveau_projectile)
            # Mettre à jour les projectiles du joueur
            for proj in liste_projectiles[:]:
                proj.update(liste_ennemis)
                hit_ennemi=None

                for ennemi in liste_ennemis:
                    if proj.rect.colliderect(ennemi.rect):
                        hit_ennemi=ennemi
                        break

                if hit_ennemi or proj.est_trop_loin():
                    if proj.aoe:
                        for e in liste_ennemis:
                            if math.hypot(proj.x-e.x,proj.y-e.y)<=proj.aoe_rayon:
                                    e.hp-=proj.degat
                    elif hit_ennemi:
                        hit_ennemi.hp-=proj.degat
                    if proj in liste_projectiles:
                        liste_projectiles.remove(proj)
            for e in liste_ennemis[:]:
                if e.hp<0:
                    xp+=e.xp
                    liste_ennemis.remove(e)

            # Mettre à jour les projectiles des ennemis
            for proj in liste_projectiles_ennemis[:]:
                proj.update([],player_pos=(player_x,player_y))
                if proj.rect.colliderect(player_real_rect):
                    liste_projectiles_ennemis.remove(proj)
                    pv_joueur -= proj.degat+echelle_difficulte
                    Soundhit.play()
                elif proj.est_trop_loin():
                    if proj in liste_projectiles_ennemis:
                        liste_projectiles_ennemis.remove(proj)
            #Gerer collisions ennemis-joueur
            for ennemi in liste_ennemis[:]:
                if ennemi.rect.colliderect(player_real_rect):
                    liste_ennemis.remove(ennemi)
                    pv_joueur -= 1+echelle_difficulte
                    Soundhit.play()
            if pv_joueur <= 0:
                en_jeu = False  ##Le joueur a perdu
            

        # Dessiner le fond
        screen.fill((255, 255, 255)) # Fond blanc
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

        #Gerer les tirs des ennemis
        for proj in liste_projectiles_ennemis[:]:
            proj.dessiner(screen, offset_x, offset_y)

        #Dessiner la barre de vie
        for rect,color in [("max_health_bar_rect",red),("health_bar_rect",green)]:
            rect=pygame.Rect(width/2,height/2,width/8 if rect=="max_health_bar_rect" else pv_joueur/pv_max_joueur*width/8,height/100)
            rect.topleft=(width/150,height/150)
            pygame.draw.rect(screen,color,rect)
        #dDessiner la barre d'exp
        for rect,color in [("xp_for_level_rect",black),("current_xp",blue)]:
            rect=pygame.Rect(width/2,height/2,width/8 if rect=="xp_for_level" else xp/xp_for_level*width/8,height/100)
            rect.topleft=(width/150,height/60)
            pygame.draw.rect(screen,color,rect)
            texte_hp=font.render(f"hp:{pv_joueur}/{pv_max_joueur}",True,green)
            texte_hp_rect=texte_hp.get_rect(center=(width/2,height/4))
            screen.blit(texte_hp,texte_hp_rect)
             
        if xp>=xp_for_level:
            xp-=xp_for_level
            xp_for_level=int(xp_for_level*1.5)
            niveau+=1
        
        
        
        centre=pygame.Rect(0,0,width/4,height/4)
        centre.center=(0-offset_x,0-offset_y)
        texte_base=font.render("Base", True,orange)
        texte_base_rect=texte_base.get_rect(center=centre.center)
        pygame.draw.rect(screen,black,centre)
        screen.blit(texte_base,texte_base_rect)


        pygame.display.flip()

pygame.quit()



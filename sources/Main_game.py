import pygame
import random
import math
import json
import io
import base64
from Menu import *
from Sounddesign import*
from menu_pause import*
from random_module import*
from paths import data_path

pygame.init()
echelle_difficulte=0
vitesse_joueur = 0  ##Vitesse de deplacement du joueur (définie dans lancer_jeu)
image_marcel=None
image_marcel_liste=[]
image_philippe=None
image_philippe_liste=[]
laser_sprite=None
roquette_sprite=None
projectile_leure_sprite=None
sprite_explosion_roquette=None
enemi_spawn_delay=2000
offset_x,offset_y=0,0  ##Décalage de la caméra par rapport au centre du monde, utilisé pour dessiner les éléments à l'écran
liste_ennemis=[]    ##Liste pour stocker les ennemis, définie dans lancer_jeu
liste_projectiles=[]    ##Liste pour stocker les projectiles, définie dans lancer_jeu
projectile_tourelle_sprite=None
attack_delay_ennemi=1000
image_leure_liste=[]
image_majo_liste=[]
sprites_poison_mine=[]
image_terminateur_liste=[]
sprite_feu_roquette=None
sprite_feu_leure=None
projectile_mine_sprite=None
aura_sprites=[]
sprite_feu_mine=None
sprite_explosion_mine=None
sprite_explosion_leure=[]
projectile_terminateur=[]
shrapnel_sprite=[]

# Couleurs (importées de Menu)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

GAME_MUSIC_EVENT=pygame.USEREVENT+1
GAME_MUSIC_TRACKS=[data_path("1-3.mp3"),data_path("2-3.mp3"), data_path("3-3.mp3")]
def ajouter_xp(g):
    global xp
    xp+=g

def jouer_musique_jeu_aleatoire(settings):
        morceau=random.choice(GAME_MUSIC_TRACKS)
        pygame.mixer.music.load(morceau)
        pygame.mixer.music.set_volume(settings.get("sound_volume",50)/100)
        pygame.mixer.music.play()

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


class ennemi_main:
    """Classe principale des ennemis"""
    def __init__(self,x,y,vitesse=1,hp=1,arme=None,xp=0,sprite=None,vitesse_animation=0.15,taille_hitbox=[50,50], degat=10): 
        self.x=x	##Coordonnees reelles de l'ennemi
        self.y=y	##Coordonnees reelles de l'ennemi
        self.vitesse_base=vitesse+echelle_difficulte/10
        self.vitesse=self.vitesse_base   ##Vitesse de deplacement de l'ennemi
        self.hp=hp+echelle_difficulte/2  ##Points de vie de l'ennemi
        self.arme=arme 	##Arme de l'ennemi
        self.xp=xp+dico_upgrades_stats["gain_xp"]	##xp de l'ennemi
        self.hitbox=taille_hitbox
        self.degat=degat+echelle_difficulte
        self.dernier_coup=0

        self.slow_fin=0
        self.facteur_slow=1

        self.est_empoisonne=False
        self.degat_poison=0
        self.interval_poison_ms=1000
        self.prochain_tick_poison=0
        self.sprites_poison=[]
        self.vitesse_animation_poison=0.1
        self.animation_index_poison=0

        self.sprite_list=sprite if isinstance(sprite,list) else ([sprite] if sprite else [])
        self.animation_index=0
        self.vitesse_animation=vitesse_animation  ##Vitesse d'animation qui augmente avec la difficulté

        self.rect=pygame.Rect(self.x,self.y,self.hitbox[0],self.hitbox[1])
        self.rect.center=(self.x,self.y)

    def dessiner(self,screen,offset_x,offset_y):    ##Dessine l'ennemi a l'ecran en fonction du decalage de la camera
        pos_ecran=(self.rect.x-offset_x,self.rect.y-offset_y)

        #pygame.draw.rect(screen,(0,0,255),pygame.Rect(self.rect.x-offset_x,self.rect.y-offset_y,self.hitbox[0],self.hitbox[1]))        #NE PAS SUPPRIMER, C'EST LA HITBOX DE L'ENNEMI, UTILE POUR LE DEBUG

        if not self.sprite_list:
            pygame.draw.rect(screen,(0,255,255),(pos_ecran[0],pos_ecran[1],50,50))
            return
        if not (-(width*0.1)<=pos_ecran[0]<=width+(width*0.1) and -(height*0.1)<=pos_ecran[1]<=height+(height*0.1)):
            return
        if len(self.sprite_list) > 1:
            self.animation_index += self.vitesse_animation

        index = int(self.animation_index) % len(self.sprite_list)
        image = self.sprite_list[index]

        screen.blit(image,pos_ecran)

        if self.est_empoisonne and self.sprites_poison:
            self.animation_index_poison += self.vitesse_animation_poison
            index_poison = int(self.animation_index_poison) % len(self.sprites_poison)
            sprite_poison = self.sprites_poison[index_poison]
            largeur_poison = int(self.rect.width * 1.8)
            hauteur_poison = max(1, int(self.rect.height * 1.2))
            sprite_poison_scale = pygame.transform.scale(sprite_poison, (largeur_poison, hauteur_poison))
            rect_poison = sprite_poison_scale.get_rect(center=(self.rect.centerx-offset_x, self.rect.centery-offset_y))
            screen.blit(sprite_poison_scale, rect_poison)


    def update(self, cible_x, cible_y):
        direction_x = cible_x - self.x
        direction_y = cible_y - self.y
        distance = math.hypot(direction_x, direction_y)
        maintenant=pygame.time.get_ticks()

        if maintenant>self.slow_fin:
            self.vitesse=self.vitesse_base
        else:
            self.vitesse=self.vitesse_base*self.facteur_slow
        
        if self.est_empoisonne and maintenant>=self.prochain_tick_poison:
            mort_poison=self.prendre_degats(self.degat_poison)
            if mort_poison:
                ajouter_xp(self.xp)
                return
            self.prochain_tick_poison=maintenant+self.interval_poison_ms


        # Ça évite de "dépasser" le centre et de changer de cible par erreur
        if distance < 5: 
            self.rect.center = (self.x, self.y)
            return # On arrête l'update ici pour cet ennemi

        if self.arme:
            distance_arret = self.arme.range * 0.8
        else:
            distance_arret = 10 # Même sans arme, on s'arrête à 10px pour ne pas "clignoter"

        if distance > distance_arret:
            self.x += (direction_x / distance) * self.vitesse
            self.y += (direction_y / distance) * self.vitesse

        self.rect.center = (self.x, self.y)

        if self.arme and distance <= self.arme.range:   
            if self.arme.tirer():
                cible=type('Cible',(),{'x':cible_x,'y':cible_y})()  ##Crée un objet temporaire pour représenter la cible du projectile (pris d'internet car si je recodais une fonction joueur, il aurait fallu que je change tout le code)
                if isinstance(self, Terminateur) and isinstance(self.arme.sprite, list):
                    sprite_choisi = random.choice(self.arme.sprite)
                else:
                    sprite_choisi = self.arme.sprite
                nouveau_projectile = self.arme.classe(self.x,
                                                      self.y,
                                                      self.arme.vitesse,
                                                      cible,
                                                      homing=self.arme.homing,
                                                      range=self.arme.range_balle,
                                                      degat=self.arme.degat,
                                                      aoe=self.arme.aoe,
                                                      aoe_rayon=self.arme.aoe_rayon,
                                                      degat_AOE=self.arme.degat_AOE,
                                                      sprite_path=sprite_choisi,
                                                      duree_AOE=self.arme.duree_AOE,
                                                      sprite_feu=self.arme.sprite_feu,
                                                      sprite_explosion=self.arme.sprite_explosion,
                                                      proprietaire=self)  ##Crée un nouveau projectile en utilisant la classe de l'arme de l'ennemi
                liste_projectiles_ennemis.append(nouveau_projectile)
    def prendre_degats(self, degats_infliges):
        self.hp -= degats_infliges
        if self.hp <= 0:
            if self in liste_ennemis:
                liste_ennemis.remove(self)
            return True
        return False
    
    def appliquer_slow(self,facteur,duree_ms):
        self.facteur_slow=facteur
        self.slow_fin=pygame.time.get_ticks()+duree_ms
    
    def appliquer_poison(self, degat_par_tick, interval_ms=1000, sprites_poison=None):
        self.est_empoisonne=True
        self.degat_poison=max(self.degat_poison,degat_par_tick)
        self.interval_poison_ms=interval_ms
        self.prochain_tick_poison=pygame.time.get_ticks()
        if sprites_poison:
            self.sprites_poison=sprites_poison


    @staticmethod   ##Sert a attribuer une fonction a une classe sans avoir besoin d'instancier un objet
    def calculer_pos_spawn(player_x, player_y,width,height):    ##Calcule une position de spawn aleatoire autour du joueur
        distance=math.hypot(width,height)/2 ##Pythagore mais plus simple
        angle=random.uniform(0,2*math.pi)   ##Angle aléatoire en radians
        return (player_x + distance*math.cos(angle), player_y + distance*math.sin(angle))   ##Calcule les coordonnees de spawn en fonction de l'angle et de la distance
    

class Majo(ennemi_main):
    """Classe des ennemis simples"""
    spawn_delay=enemi_spawn_delay
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/600,hp=3,xp=2,degat=10,sprite=image_majo_liste,taille_hitbox=[image_majo_liste[0].get_width(),image_majo_liste[0].get_height()],vitesse_animation=0.04)  # pyright: ignore[reportArgumentType] ##Appelle le constructeur de la classe parente avec une vitesse de 2


class Marcel(ennemi_main):
    """Classe des ennemis rapides"""
    spawn_delay=enemi_spawn_delay*1.5
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/300,hp=2,xp=2,sprite=image_marcel_liste,taille_hitbox=[image_marcel_liste[0].get_width(),image_marcel_liste[0].get_height()],degat=5)  ##Appelle le constructeur de la classe parente avec une vitesse de 4

class Terminateur(ennemi_main):
    """Classe des ennemis tireurs"""
    spawn_delay=enemi_spawn_delay*3
    def __init__(self,x,y):
        arme_ennemi=weapon_main(max(100,1000-echelle_difficulte/10), projectile_ennemi,homing=False,portee_detection=1/3*height+echelle_difficulte/10,vitesse=width/400+echelle_difficulte/10,sprite=projectile_terminateur)  ##Crée une arme pour l'ennemi avec un délai de 1000ms entre chaque tir et des projectiles non homing
        super().__init__(x,y,vitesse=width/600,hp=1,arme=arme_ennemi,xp=1,degat=7,sprite=image_terminateur_liste,taille_hitbox=[image_terminateur_liste[0].get_width(),image_terminateur_liste[0].get_height()],vitesse_animation=0.04)  ##Appelle le constructeur de la classe parente avec une vitesse de 1 et une arme

class Leure(ennemi_main):
    """Classe des ennemis lanceur de bombes"""
    spawn_delay=enemi_spawn_delay*3
    def __init__(self,x,y):
        arme_leure=weapon_main(max(200,2000-echelle_difficulte/10),projectile_leure,homing=False,portee_detection=1/3*height+echelle_difficulte/10,vitesse=width/400+echelle_difficulte/10,sprite=projectile_leure_sprite,aoe=True,sprite_feu=sprite_feu_leure,duree_AOE=2000+echelle_difficulte*100,degat=20+echelle_difficulte,degat_AOE=5+echelle_difficulte,interval_tick_ms=500,sprite_explosion=sprite_explosion_leure)
        super().__init__(x,y,vitesse=width/600,hp=2,arme=arme_leure,xp=3,degat=5,sprite=image_leure_liste,taille_hitbox=[image_leure_liste[0].get_width(),image_leure_liste[0].get_height()],vitesse_animation=0.05)

class Philippe(ennemi_main):
    """Classe des ennemis lourds"""
    spawn_delay=enemi_spawn_delay*2
    def __init__(self,x,y):
        super().__init__(x,y,vitesse=width/1200,hp=5,xp=3,sprite=image_philippe_liste,taille_hitbox=[image_philippe_liste[0].get_width(),image_philippe_liste[0].get_height()],degat=20)
            
class projectiles_general:
    """Classe principale des projectiles"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=None,couleur=(0,255,0),degat=1,range=10,aoe=False,aoe_rayon=None,degat_AOE=0,duree_AOE=0,duree=None,interval_tick_ms=500,sprite_feu=None,sprite_explosion=None,vitesse_animation=0,proprietaire=None):
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
        self.interval_tick_ms=interval_tick_ms
        self.angle=0
        self.sprite_explosion=sprite_explosion
        self.vitesse_animation=vitesse_animation
        self.animation_index=0
        self.ennemis_touches=[]
        self.proprietaire=proprietaire
        if sprite_feu!=None:
            self.sprite_feu=sprite_feu
        else:
            self.sprite_feu=sprite_feu
        self.aoe_rayon=aoe_rayon if aoe_rayon is not None else width/10
        if sprite_path!=None:
            if isinstance(self.image,list):
                self.rect=self.image[0].get_rect(center=(self.x,self.y))
            else:
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
        return False
    
    def est_trop_loin(self):
        return math.hypot(self.x-self.start_x, self.y-self.start_y) > self.range
    def dessiner(self,screen,offset_x,offset_y):
        pos_ecran_x=self.rect.x-offset_x
        pos_ecran_y=self.rect.y - offset_y
        if isinstance(self.image,list):
            self.animation_index += self.vitesse_animation
            if self.animation_index >= len(self.image):
                self.animation_index = 0

            image = self.image[int(self.animation_index)]

            rotated_image = pygame.transform.rotate(image, self.angle)
            new_rect = rotated_image.get_rect(center=(pos_ecran_x, pos_ecran_y))
            screen.blit(rotated_image, new_rect)
        elif self.image and not isinstance(self.image,list):
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            new_rect= rotated_image.get_rect(center=(pos_ecran_x, pos_ecran_y))
            screen.blit(rotated_image, new_rect)
        else:
            pygame.draw.rect(screen,self.couleur,(pos_ecran_x,pos_ecran_y,10,10))

class projectile_laser(projectiles_general):
    """Classe des projectiles laser"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite=laser_sprite,degat=1,range=10,duree_AOE=0,aoe=False,aoe_rayon=None,degat_AOE=0,sprite_feu=None,sprite_explosion=None):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite, couleur=(255,0,0),degat=degat+dico_upgrades_laser["degat"],range=range+dico_upgrades_laser["portee"],duree_AOE=duree_AOE,aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE,sprite_feu=sprite_feu,sprite_explosion=sprite_explosion)  ##Appelle le constructeur de la classe parente avec une couleur rouge

    def chain_lightning(self, ennemi_initial, liste_ennemis,liste_arcs):
        global arc_electrique_sprite
        if not dico_upgrades_uniques["laser"]["laser_electrique"]:
            return

        max_chaines = 5
        distance_arc = width/5+dico_upgrades_laser["portee"]*40

        touches = [ennemi_initial]
        source = ennemi_initial

        for _ in range(max_chaines - 1):

            cible = None
            distance_min = float("inf")

            for ennemi in liste_ennemis:
                if ennemi in touches:
                    continue

                dist = math.hypot(ennemi.x - source.x, ennemi.y - source.y)

                if dist <= distance_arc and dist < distance_min:
                    distance_min = dist
                    cible = ennemi

            if cible is None:
                break

            liste_arcs.append(arc_electrique(source.x,source.y,cible.x,cible.y,arc_electrique_sprite))

            mort = cible.prendre_degats(self.degat)

            if dico_upgrades_uniques["laser"]["laser_ralentissant"]:
                cible.appliquer_slow(0.2,2500)

            if mort:
                ajouter_xp(cible.xp)

            touches.append(cible)
            source = cible

class projectile_roquette(projectiles_general):
    """Classe des projectiles roquettes"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=True,sprite=roquette_sprite,degat=3,range=10,aoe=True,aoe_rayon=width/10,degat_AOE=1,duree_AOE=333,interval_tick_ms=500,sprite_feu=sprite_feu_roquette,sprite_explosion=sprite_explosion_roquette):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite, couleur=(255,165,0),degat=degat+dico_upgrades_roquette["degat"],range=range+dico_upgrades_roquette["portee"],aoe=aoe,aoe_rayon=aoe_rayon+dico_upgrades_roquette["rayon_aoe"]*10,degat_AOE=degat_AOE+dico_upgrades_roquette["degat"],duree_AOE=duree_AOE+5000 if dico_upgrades_uniques["roquette"]["roquette_enflammee"] else duree_AOE,sprite_feu=sprite_feu,sprite_explosion=sprite_explosion)  ##Appelle le constructeur de la classe parente avec une couleur orange
        self.interval_tick_ms=interval_tick_ms
        self.ricochet_actif=dico_upgrades_uniques["roquette"]["roquette_ricochet"]
        self.nb_contacts_ricochet=0
        self.nb_contacts_ricochet_max=3

    def creer_shrapnels(self, cible_impact):
        if not dico_upgrades_uniques["roquette"]["roquette_shrapnel"]:
            return []

        projectiles_shrapnels=[]
        for decalage in (-30, 0, 30):
            fragment = shrapnel(
                self.x,
                self.y,
                width/90,
                cible_impact,
                angle_tir=self.angle+decalage,
                sprite=shrapnel_sprite
            )
            decalage_spawn = max(12, width/80)
            fragment.x += fragment.dir_x * decalage_spawn
            fragment.y += fragment.dir_y * decalage_spawn
            fragment.start_x, fragment.start_y = fragment.x, fragment.y
            fragment.rect.center = (fragment.x, fragment.y)
            projectiles_shrapnels.append(fragment)
        return projectiles_shrapnels

    def preparer_ricochet(self,liste_ennemis):
        cibles_possibles=[ennemi for ennemi in liste_ennemis if ennemi not in self.ennemis_touches]
        if not cibles_possibles:
            return False
        self.cible=min(cibles_possibles,key=lambda ennemi:(ennemi.x-self.x)**2+(ennemi.y-self.y)**2)
        self.calculer_direction(self.cible.x,self.cible.y)
        self.start_x,self.start_y=self.x,self.y
        return True




class projectile_mine(projectiles_general):
    """Classe des projectiles roquettes"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite=projectile_mine_sprite,degat=2,range=math.inf,aoe=True,aoe_rayon=width/10,degat_AOE=1,duree_AOE=333,duree=5000,interval_tick_ms=500,sprite_feu=sprite_feu_mine,sprite_explosion=sprite_explosion_mine,vitesse_animation=0.1):
        super().__init__(x,y,0,cible_initiale,homing=homing, sprite_path=sprite, couleur=(255,165,0),degat=degat+dico_upgrades_mine["degat"],range=range,aoe=aoe,aoe_rayon=aoe_rayon+dico_upgrades_mine["rayon_aoe"]*10,degat_AOE=degat_AOE+dico_upgrades_mine["degat"],duree_AOE=duree_AOE+dico_upgrades_mine["duree_aoe"]*10,duree=duree+dico_upgrades_mine["duree_vie"]*100,sprite_feu=sprite_feu,sprite_explosion=sprite_explosion,vitesse_animation=vitesse_animation)  ##Appelle le constructeur de la classe parente avec une couleur orange
        self.interval_tick_ms=interval_tick_ms
        if dico_upgrades_uniques["mine"]["mine_empoisonnee"]:
            self.sprite_feu=sprites_poison_mine
        self.double_vie_active=dico_upgrades_uniques["mine"]["mine_double_vie"]
        self.charges_restantes=2 if self.double_vie_active else 1
        self.en_recharge=False
        self.delai_reactivation_ms=1000
        self.temps_reactivation=0

    def est_active(self):
        return not self.en_recharge

    def declencher_apres_explosion(self):
        self.charges_restantes -= 1
        if self.double_vie_active and self.charges_restantes>0:
            self.en_recharge=True
            self.temps_reactivation=pygame.time.get_ticks()+self.delai_reactivation_ms
            return True
        return False

    def update(self, liste_ennemis, player_pos=None):
        maintenant = pygame.time.get_ticks()
        if self.en_recharge and maintenant>=self.temps_reactivation:
            self.en_recharge=False

        # La mine renvoie True UNIQUEMENT si le temps est écoulé
        if maintenant - self.temps_creation >= self.duree:
            return True 
        return False

    def dessiner(self,screen,offset_x,offset_y):
        if isinstance(self.image,list) and self.image:
            if self.en_recharge and len(self.image)>0:
                image=self.image[0]
            else:
                frame_debut=1 if len(self.image)>1 else 0
                nb_frames=max(1,len(self.image)-frame_debut)
                self.animation_index += self.vitesse_animation
                index=frame_debut + (int(self.animation_index) % nb_frames)
                image=self.image[index]

            rect_image=image.get_rect(center=(self.rect.centerx-offset_x,self.rect.centery-offset_y))
            screen.blit(image,rect_image)
        else:
            super().dessiner(screen,offset_x,offset_y)


    
class shrapnel(projectiles_general):
    """Projectile secondaire déclenché par l'upgrade roquette_shrapnel"""
    def __init__(self,x,y,vitesse,cible_initiale,angle_tir,sprite=None,degat=1,range=None):
        if range is None:
            range = width/3
        super().__init__(x,y,vitesse,cible_initiale,homing=False,sprite_path=sprite,couleur=(255,200,100),degat=degat+dico_upgrades_roquette["degat"],range=range+dico_upgrades_roquette["portee"],aoe=False)
        self.dir_x=math.cos(math.radians(angle_tir))
        self.dir_y=-math.sin(math.radians(angle_tir))
        self.angle=angle_tir



class projectile_tourelle(projectiles_general):
    """Classe des projectiles de tourelle, qui sont plus faibles que les projectiles normaux pour ne pas rendre la tourelle trop puissante"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite=projectile_tourelle_sprite,degat=0.5,range=10,aoe=False,aoe_rayon=None,degat_AOE=0,duree_AOE=0):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite, couleur=(0,255,255),degat=degat+dico_upgrades_tourelle["degat"]/2,range=range+dico_upgrades_tourelle["portee"],aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE,duree_AOE=duree_AOE)  ##Appelle le constructeur de la classe parente avec une couleur cyan

class projectile_ennemi(projectiles_general):
    """Classe des projectiles ennemis"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=projectile_terminateur,degat=7,range=10,aoe=False,aoe_rayon=None,degat_AOE=0,duree_AOE=0,sprite_feu=None,sprite_explosion=None,proprietaire=None):
        super().__init__(x,y,vitesse,cible_initiale,homing=homing, sprite_path=sprite_path, couleur=(0,0,0),degat=degat+echelle_difficulte,range=range+echelle_difficulte*10,aoe=aoe,aoe_rayon=aoe_rayon,degat_AOE=degat_AOE,duree_AOE=duree_AOE,sprite_feu=sprite_feu,sprite_explosion=sprite_explosion,proprietaire=proprietaire)  ##Appelle le constructeur de la classe parente avec une couleur noire

class projectile_leure(projectiles_general):
    """Classe des projectiles de Leure"""
    def __init__(self,x,y,vitesse,cible_initiale,homing=False,sprite_path=projectile_leure_sprite,degat=20,range=10,aoe=True,aoe_rayon=width/20,degat_AOE=5,duree_AOE=2000,sprite_feu=sprite_feu_leure,interval_tick_ms=500,sprite_explosion=sprite_explosion_leure,vitesse_animation=0.1,proprietaire=None):
        super().__init__(
                x,
                y,
                vitesse,
                cible_initiale,
                homing=homing,
                sprite_path=sprite_path,
                couleur=(255,60,5),
                degat=degat+echelle_difficulte,
                range=range+echelle_difficulte*10,
                aoe=aoe,
                aoe_rayon=aoe_rayon+echelle_difficulte*5,
                degat_AOE=degat_AOE+echelle_difficulte,
                duree_AOE=duree_AOE+echelle_difficulte*100,
                interval_tick_ms=interval_tick_ms,
                sprite_feu=sprite_feu,
                sprite_explosion=sprite_explosion,
                vitesse_animation=vitesse_animation,
                proprietaire=proprietaire
                        )
class weapon_main:
    """Classe principale des armes"""
    def __init__(self,delai,classe_projectile,homing=False,portee_detection=None,vitesse=10,aoe=False,aoe_rayon=None,degat=1,degat_AOE=1,duree_AOE=333,duree=None,interval_tick_ms=500,sprite=None,sprite_feu=None,sprite_explosion=None):
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
        self.interval_tick_ms=interval_tick_ms
        self.sprite=sprite
        self.sprite_feu=sprite_feu
        self.sprite_explosion=sprite_explosion
    def tirer(self):
        if pygame.time.get_ticks() - self.dernier_tir >= self.delai:
            self.dernier_tir = pygame.time.get_ticks()
            return  True
        return False
    def compenser_pause(self,duree_pause):
        self.dernier_tir += duree_pause  ##Décale le temps du dernier tir pour compenser la pause
        
class Explosion:
    def __init__(self,x,y,sprite_list,rayon,vitesse_animation=0.1,):
        self.x=x
        self.y=y
        self.rayon=rayon
        self.sprite_list=[]
        self.animation_index=0
        self.vitesse_animation=vitesse_animation
        self.terminee=False

        if sprite_list:
            taille=int(self.rayon*2)
            for img in sprite_list:
                img_scale=pygame.transform.scale(img,(taille,taille))
                self.sprite_list.append(img_scale)        
    def update(self):
        if not self.sprite_list:
            return
        self.animation_index+=self.vitesse_animation
        if self.animation_index>=len(self.sprite_list):
            self.terminee=True
            
    def dessiner(self, screen, offset_x, offset_y):

        pos_ecran = (self.x-offset_x, self.y-offset_y)

        if not self.sprite_list:
            pygame.draw.rect(screen,(0,255,255),(pos_ecran[0],pos_ecran[1],50,50))
            return


        index = min(int(self.animation_index), len(self.sprite_list)-1)
        image = self.sprite_list[index]

        rect = image.get_rect(center=pos_ecran)
        screen.blit(image,rect)

class AOE:
    def __init__(self,x,y,rayon,degat_par_tick,duree_ms,interval_tick_ms=500,sprite_feu=None,cible="joueur",proprietaire=None,empoisonne=False):
        self.x=x
        self.y=y
        self.rayon=rayon
        self.degat=degat_par_tick
        self.cible=cible
        self.duree=duree_ms  ##Durée totale de l'AOE en millisecondes
        self.interval_tick=interval_tick_ms
        self.sprite=sprite_feu
        self.proprietaire=proprietaire
        self.empoisonne=empoisonne
        self.index_animation=0
        self.vitesse_animation=0.15


        self.temps_creation=pygame.time.get_ticks()
        self.dernier_tick=self.temps_creation
        self.dernier_tick=pygame.time.get_ticks()-self.interval_tick  ##Permet de faire en sorte que les dégâts soient appliqués immédiatement à la création de l'AOE
        self.terminee=False

        if self.sprite and not isinstance(self.sprite,list):
            taille=int(self.rayon*2)
            self.sprite=pygame.transform.scale(self.sprite,(taille,taille))
            self.rect=self.sprite.get_rect(center=(self.x,self.y))

    def update(self, liste_ennemis, player_rect=None, xp_callback=None, aura_active=None, aura_affaiblissante=False, player_x=None, player_y=None): 
        maintenant = pygame.time.get_ticks()
        
        if maintenant - self.temps_creation >= self.duree:
            self.terminee = True
            return
        
        if maintenant - self.dernier_tick >= self.interval_tick:
            # SI LA CIBLE EST LE JOUEUR
            if self.cible == "joueur" and player_rect is not None:
                # On calcule la distance entre le centre de l'AOE et le centre du joueur
                if math.hypot(self.x - player_rect.centerx, self.y - player_rect.centery) <= self.rayon and not random.randint(1,11)<=dico_upgrades_stats["esquive"]:
                    global pv_joueur
                    reduction=1
                    if aura_affaiblissante and aura_active and aura_active.ennemi_dans_aura(self.proprietaire,player_x,player_y):
                        reduction=0.5
                    pv_joueur-=self.degat*reduction
                    Soundhit.play()
            
            # SI LA CIBLE EST UN ENNEMI
            else:
                for ennemi in liste_ennemis[:]:
                    if math.hypot(self.x - ennemi.x, self.y - ennemi.y) <= self.rayon:
                        mort = ennemi.prendre_degats(self.degat)

                        if self.empoisonne:
                            ennemi.appliquer_poison(self.degat,self.interval_tick,self.sprite if isinstance(self.sprite,list) else None)

                        if mort and xp_callback:
                            xp_callback(ennemi.xp)

            self.dernier_tick = maintenant

    def dessiner(self, screen, offset_x, offset_y):
        if self.terminee:
            return
        
        if self.sprite:
            if isinstance(self.sprite,list):
                self.index_animation += self.vitesse_animation
                index = int(self.index_animation) % len(self.sprite)
                frame = self.sprite[index]
                frame_scale=pygame.transform.scale(frame,(int(self.rayon*2),int(self.rayon*2)))
                pos_ecran = (self.x - offset_x - self.rayon, self.y - offset_y - self.rayon)
                screen.blit(frame_scale, pos_ecran)
            else:
                pos_ecran = (self.x - offset_x - self.rayon, self.y - offset_y - self.rayon)
                screen.blit(self.sprite, pos_ecran)

        else:
            # Créer une surface temporaire pour de l'alpha (transparence) si tu veux
            # Ou simplement dessiner un cercle plein (enlever le "2" à la fin)
            centre = (int(self.x - offset_x), int(self.y - offset_y))
            # Remplacer 2 par 0 pour un cercle plein
            pygame.draw.circle(screen, (255, 165, 0), centre, int(self.rayon), 2)

class aura:

    def __init__(self, rayon, degat, sprite, interval_tick_ms=500, vitesse_animation=0.1):

        self.rayon = rayon
        self.degat = degat

        # sprites originaux
        self.sprites_originaux = sprite
        self.sprites_scales = []

        self.frame_index = 0
        self.vitesse_animation = vitesse_animation

        self.interval_tick_ms = interval_tick_ms
        self.temps_dernier_tick = pygame.time.get_ticks()

        self.ancien_rayon = -1


    def update(self, player_x, player_y, liste_ennemis, xp_callback=None):

        # upgrades
        self.rayon = width/4 + dico_upgrades_aura["portee"] * (width/40)
        self.degat = 1 + dico_upgrades_aura["degat"]

        self.interval_tick_ms = max(100,500 - dico_upgrades_aura["cadence_de_tir"] * 50)

        maintenant = pygame.time.get_ticks()

        if maintenant - self.temps_dernier_tick >= self.interval_tick_ms:

            self.temps_dernier_tick = maintenant

            for ennemi in liste_ennemis:

                dist = math.hypot(
                    ennemi.x - player_x,
                    ennemi.y - player_y
                )

                if dist <= self.rayon:

                    mort = ennemi.prendre_degats(self.degat)
                    global pv_joueur
                    pv_joueur=min(pv_max_joueur,pv_joueur+dico_upgrades_stats["vol_de_vie"]*self.degat)
                    if mort and xp_callback:
                        xp_callback(ennemi.xp)
    
    def ennemi_dans_aura(self,ennemi,player_x,player_y):
        if ennemi is None:
            return False
        return math.hypot(ennemi.x - player_x, ennemi.y - player_y) <= self.rayon


    def dessiner(self, screen, player_x, player_y, offset_x, offset_y):

        if self.rayon != self.ancien_rayon:

            diametre = int(self.rayon * 2)

            self.sprites_scales = [
                pygame.transform.scale(sprite, (diametre, diametre))
                for sprite in self.sprites_originaux
            ]

            self.ancien_rayon = self.rayon

        # animation
        self.frame_index += self.vitesse_animation

        if self.frame_index >= len(self.sprites_scales):
            self.frame_index = 0

        sprite = self.sprites_scales[int(self.frame_index)]

        screen.blit(
            sprite,
            (
                player_x - self.rayon - offset_x,
                player_y - self.rayon - offset_y
            )
        )

class tourelle:
    def __init__(self, x, y, sprite_batiment=None, sprite_balle=None, delai_spawn=10000,vitesse_animation=0.1):
        self.x = x
        self.y = y
        self.sprite = sprite_batiment
        self.nom = "Tourelle"
        self.hp = 50+dico_upgrades_tourelle["hp"]
        self.max_hp = 50+dico_upgrades_tourelle["hp"]
        self.delai_spawn=delai_spawn
        self.dernier_spawn=pygame.time.get_ticks()

        self.animation_index=0
        self.vitesse_animation=vitesse_animation

        if sprite_batiment!=None:
            self.colliderect=self.sprite[0].get_rect(center=(self.x,self.y))
        else:
            self.colliderect=pygame.rect.Rect(self.x-25, self.y-25, 50, 50)
        
        self.arme = weapon_main(
            delai=max(100,1000-dico_upgrades_tourelle["cadence_de_tir"]*10), 
            classe_projectile=projectile_tourelle, 
            vitesse=width/100, 
            degat=0.5+dico_upgrades_tourelle["degat"]/2,
            sprite=sprite_balle
        )

    def update(self, liste_ennemis, liste_projectiles):
        self.arme.delai = max(100, 1000 - dico_upgrades_tourelle["cadence_de_tir"]*45)
        self.arme.vitesse = width/100
        self.arme.degat = 0.5 + dico_upgrades_tourelle["degat"]/2
        self.max_hp = 50+dico_upgrades_tourelle["hp"]
        self.delai_spawn=max(200,10000-dico_upgrades_tourelle["cadence_de_tir"]*45)
        if self.arme.tirer():
            if liste_ennemis:
                cible = min(liste_ennemis, key=lambda e: (e.x - self.x)**2 + (e.y - self.y)**2)
                
                nouveau_p = self.arme.classe(
                    self.x, 
                    self.y, 
                    self.arme.vitesse, 
                    cible, 
                    homing=self.arme.homing,
                    range=self.arme.range_balle,
                    degat=self.arme.degat,
                    aoe=self.arme.aoe,
                    aoe_rayon=self.arme.aoe_rayon,
                    degat_AOE=self.arme.degat_AOE,
                    sprite=self.arme.sprite
                )
                liste_projectiles.append(nouveau_p)

    def dessiner(self, screen, offset_x, offset_y):
        pos_ecran = (self.x - offset_x, self.y - offset_y)

        if self.sprite:
            if len(self.sprite) > 1:
                self.animation_index += self.vitesse_animation
                if self.animation_index >= len(self.sprite):
                    self.animation_index = 0

            image = self.sprite[int(self.animation_index)]
            rect = image.get_rect(center=pos_ecran)
            screen.blit(image, rect)

        else:
            pygame.draw.rect(screen, (0,255,255), (pos_ecran[0]-25, pos_ecran[1]-25, 50, 50))
    
    def compenser_pause(self,duree_pause):
        self.dernier_spawn+=duree_pause
    
class arc_electrique:
    def __init__(self,x1,y1,x2,y2,sprite_list,duree=150,vitesse_animation=0.5):

        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

        self.sprites=sprite_list
        self.index=0
        self.vitesse_animation=vitesse_animation

        self.temps_creation=pygame.time.get_ticks()
        self.duree=duree
        self.terminee=False

        dx=x2-x1
        dy=y2-y1
        self.angle=-math.degrees(math.atan2(dy,dx))
        self.distance=math.hypot(dx,dy)

    def update(self):
        if pygame.time.get_ticks()-self.temps_creation>=self.duree:
            self.terminee=True
            return
        self.index+=self.vitesse_animation
        if self.index>=len(self.sprites):
            self.index=0
    def dessiner(self,screen,offset_x,offset_y):
        sprite=self.sprites[int(self.index)]

        sprite=pygame.transform.scale(sprite,(int(self.distance),sprite.get_height()))
        sprite=pygame.transform.rotate(sprite,self.angle)

        rect=sprite.get_rect(center=((self.x1+self.x2)/2-offset_x,(self.y1+self.y2)/2-offset_y))

        screen.blit(sprite,rect)

def lancer_jeu(settings):
    global width, height, screen, pv_joueur, liste_projectiles_ennemis, image_marcel, image_marcel_liste,echelle_difficulte,laser_sprite,roquette_sprite, sprite_explosion_roquette,image_philippe,image_philippe_liste,offset_x,offset_y,enemi_spawn_delay,liste_ennemis,player_y,player_x,pv_max_joueur,laser,roquette,mine,aura_active,type_armes,liste_armes,mines_actuelles,projectile_leure_sprite,liste_projectiles_ennemis,tourelle,sprite_feu_roquette,sprite_feu_leure,projectile_mine_sprite,image_leure_liste,xp,xp_for_level,sprite_explosion_leure,sprite_explosion_mine,sprite_explosion_roquette,image_majo_liste,image_terminateur_liste,aura_sprites,arc_electrique_sprite,liste_arcs,projectile_terminateur,shrapnel_sprite,sprites_poison_mine
    if settings is None:
        settings={"width":width,"height":height,"fullscreen":fullscreen,"sound_volume":50,"play":True}


    player_x,player_y=0,0
    #reset_upgrades()

    #Chargement de la map
    with open(data_path("Map_Jeu.json"),"r") as f:
        map_data=json.load(f)
    
    zoom = width/512
    MAP_COLS = 149
    MAP_ROWS = 100

    mur_collision=[]
    textures = {}
    TILE_SIZE = map_data.get("tileSize", 16)

    # Largeur totale de la map en pixels avec le zoom
    map_width_px = MAP_COLS * TILE_SIZE * zoom
    map_height_px = MAP_ROWS * TILE_SIZE * zoom

    # On calcule l'espace vide à diviser en deux pour centrer
    marge_centrage_x = (width - map_width_px) // 2-width/2-TILE_SIZE*zoom*2.5
    marge_centrage_y = (height - map_height_px) // 2-height/2-TILE_SIZE*zoom*3.5


    # Position de la base au centre de la grille (coordonnées Monde)
    # On divise par 2 pour tomber sur la tuile centrale
    base_x = (MAP_COLS * TILE_SIZE) // 2
    base_y = (MAP_ROWS * TILE_SIZE) // 2


    # Initialisation de l'offset pour que la caméra soit centrée sur le joueur/base
    # (Position Monde * Zoom) - (Moitié de l'écran)
    offset_x = (player_x * zoom) - (width // 2)
    offset_y = (player_y * zoom) - (height // 2)

    for sheet_id, sheet_info in map_data["spriteSheets"].items():
        img_data = base64.b64decode(sheet_info["base64"].split(",")[1])
        img_file = io.BytesIO(img_data)
        full_surface = pygame.image.load(img_file).convert_alpha()
        
        sheet_w, sheet_h = full_surface.get_size()
        cols = sheet_w // TILE_SIZE
        rows = sheet_h // TILE_SIZE
        
        for i in range(cols * rows):
            px = (i % cols) * TILE_SIZE
            py = (i // cols) * TILE_SIZE
            rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
            
            if full_surface.get_rect().contains(rect):
                textures[f"{sheet_id}_{i}"] = full_surface.subsurface(rect)
    for layers in map_data["layers"]:
        if layers.get("collider")==True:
            for tile in layers["tiles"]:
                x=tile["x"]*zoom+marge_centrage_x
                y=tile["y"]*zoom+marge_centrage_y
                rect_mur=pygame.Rect(x,y,TILE_SIZE*zoom,TILE_SIZE*zoom)
                mur_collision.append(rect_mur)
    #Chargement des sprites

    ##Chargement des sprites des projectiles

    ###Laser
    img=pygame.image.load(data_path('projectile_laser.png')).convert_alpha()
    img=pygame.transform.scale(img,(width/25,int(img.get_height()/img.get_width()*width/25)))
    laser_sprite=img

    ###Roquette
    img=pygame.image.load(data_path('projectile_roquette.png')).convert_alpha()
    img=pygame.transform.scale(img,(width/25,int(img.get_height()/img.get_width()*width/25)))
    roquette_sprite=img

    ###Shrapnel
    shrapnel_sprite=[]
    for i in range(1,4):
        img=pygame.image.load(data_path(f'Shrapnel({i}).png')).convert_alpha()
        img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
        shrapnel_sprite.append(img)

    ###Tourelle
    img=pygame.image.load(data_path('projectile_tourelle.png')).convert_alpha()
    img=pygame.transform.scale(img,(width/25,int(img.get_height()/img.get_width()*width/25)))
    projectile_tourelle_sprite=img

    ###Mine
    projectile_mine_sprite=[]
    img=pygame.image.load(data_path('Landmine_desactive.png')).convert_alpha()
    img=pygame.transform.scale(img,(width/25,int(img.get_height()/img.get_width()*width/25)))
    projectile_mine_sprite.append(img)
    for i in range(1,3):
        img=pygame.image.load(data_path(f'Landmine({i}).png')).convert_alpha()
        img=pygame.transform.scale(img,(width/25,int(img.get_height()/img.get_width()*width/25)))
        projectile_mine_sprite.append(img)

    ###Leure
    projectile_leure_sprite=[]
    for i in range(1,3):
        img=pygame.image.load(data_path(f'enemy_bomb({i}).png')).convert_alpha()
        img=pygame.transform.scale(img,(width/35,int(img.get_height()/img.get_width()*width/35)))
        projectile_leure_sprite.append(img)

    ##Terminateur
    projectile_terminateur=[]
    for i in range(1,10):
        img=pygame.image.load(data_path(f"E_Shoot({i}).png")).convert_alpha()
        img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
        projectile_terminateur.append(img)

    ##Chargement des sprites des AOE

    ###Aura
    aura_sprites=[]
    for i in range(1,8):
        img=pygame.image.load(data_path(f"Aura({i}).png")).convert_alpha()##on scale pas car la classe le fait
        aura_sprites.append(img)

    ###Sprite feu roquette
    img=pygame.image.load(data_path("Fire.png")).convert_alpha()
    img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
    sprite_feu_roquette=img

    ###Sprite feu mine
    img=pygame.image.load(data_path("Fire.png")).convert_alpha()
    img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
    sprite_feu_mine=img

    ###Sprite poison mine
    sprites_poison_mine=[]
    for i in range(1,3):
        img=pygame.image.load(data_path(f"Poison({i}).png")).convert_alpha()
        sprites_poison_mine.append(img)

    ###Sprite feu Leure
    img=pygame.image.load(data_path("Fire.png")).convert_alpha()
    img=pygame.transform.scale(img,(width/20,int(img.get_height()/img.get_width()*width/20)))
    sprite_feu_leure=img

    ##Chargement des sprites des explosions

    ###Sprite de l'explosion de la roquette
    sprite_explosion_roquette=[]
    for i in range(1,3):
        img=pygame.image.load(data_path(f"Explosion{i}.png")).convert_alpha()
        img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
        sprite_explosion_roquette.append(img)    

    ###Sprite de l'explosion de la mine
    sprite_explosion_mine=[]
    for i in range(1,3):
        img=pygame.image.load(data_path(f"Explosion{i}.png")).convert_alpha()
        img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
        sprite_explosion_mine.append(img) 
    
    ###Sprite de l'explosion des projectiles de Leure
    sprite_explosion_leure=[]
    for i in range(1,3):
        img=pygame.image.load(data_path(f"Explosion{i}.png")).convert_alpha()
        img=pygame.transform.scale(img,(width/10,int(img.get_height()/img.get_width()*width/10)))
        sprite_explosion_leure.append(img) 

    ##Chargement des sprites des ennemis

    ###Sprite de Marcel(rapide)
    image_marcel_liste=[]
    for i in range(1,7):
        image_marcel=pygame.image.load(data_path(f"Marcel({i}).png")).convert_alpha()
        image_marcel=pygame.transform.scale(image_marcel,(width/25,int(image_marcel.get_height()/image_marcel.get_width()*width/25)))
        image_marcel_liste.append(image_marcel)
    
    ###Sprite de Philippe(tank)
    image_philippe_liste=[]
    for i in range(1,7):
        image_philippe=pygame.image.load(data_path(f"Philippe({i}).png")).convert_alpha()
        image_philippe=pygame.transform.scale(image_philippe,(width/13,int(image_philippe.get_height()/image_philippe.get_width()*width/13)))
        image_philippe_liste.append(image_philippe)

    ###Sprite de Leure(bombardier)
    image_leure_liste=[]
    for i in range(1,7):
        image_leure=pygame.image.load(data_path(f"Leure({i}).png")).convert_alpha()
        image_leure=pygame.transform.scale(image_leure,(width/20,int(image_leure.get_height()/image_leure.get_width()*width/20)))
        image_leure_liste.append(image_leure)

    ###Sprite de Majo(ennemie normal)
    image_majo_liste=[]
    for i in range(1,3):
        image_majo=pygame.image.load(data_path(f"Majo({i}).png")).convert_alpha()
        image_majo=pygame.transform.scale(image_majo,(width/20,int(image_majo.get_height()/image_majo.get_width()*width/20)))
        image_majo_liste.append(image_majo)

    ###Sprite de Terminateur(ennemie tireur)
    image_terminateur_liste=[]
    for i in range(1,8):
        image_terminateur=pygame.image.load(data_path(f"Terminateur({i}).png")).convert_alpha()
        image_terminateur=pygame.transform.scale(image_terminateur,(width/20,int(image_terminateur.get_height()/image_terminateur.get_width()*width/20)))
        image_terminateur_liste.append(image_terminateur)

    ##Chargement des autres trucs

    ###Chargement de la tourelle
    tourelle_sprites=[]
    for i in range(1,5):
        img=pygame.image.load(data_path(f'Turret({i}).png')).convert_alpha()
        img=pygame.transform.scale(img,(width/20,width/20))
        tourelle_sprites.append(img)
    
    ###Chargement de la font
    font=pygame.font.Font(None,int(width/25))

    ###Chargement de Astro(joueur)
    astro_front_sprites=[]
    for i in range(1,7):
        astro_front=pygame.image.load(data_path(f"AstroFront({i}).png")).convert_alpha()
        astro_front=pygame.transform.scale(astro_front,(width/20,int(astro_front.get_height()/astro_front.get_width()*width/20)))
        astro_front_sprites.append(astro_front)
    astro_back_sprites=[]
    for i in range(1,8):
        astro_back=pygame.image.load(data_path(f"AstroBack({i}).png")).convert_alpha()
        astro_back=pygame.transform.scale(astro_back,(width/20,int(astro_back.get_height()/astro_back.get_width()*width/20)))
        astro_back_sprites.append(astro_back)


    ##Chargement de l'arc electrique
    arc_electrique_sprite=[]
    for i in range(1,4):
        img=pygame.image.load(data_path(f"ArcE({i}).png")).convert_alpha() ## on resize pas car la fonction le fait
        arc_electrique_sprite.append(img)

    echelle_difficulte=0
    enemi_spawn_delay=4000-echelle_difficulte
    # Mettre à jour les spawn delays des classes en fonction de la difficulté
    Majo.spawn_delay=enemi_spawn_delay
    Marcel.spawn_delay=enemi_spawn_delay*1.5
    Terminateur.spawn_delay=enemi_spawn_delay*3
    Philippe.spawn_delay=enemi_spawn_delay*2
    Leure.spawn_delay=enemi_spawn_delay*3
    width = settings["width"]
    height = settings["height"]
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN if settings["fullscreen"] else 0)
    en_jeu=True
    #Variables de jeu
    player_x, player_y = 0, 0 # Position réelle du joueur dans le monde
    astro_animation_index=0
    astro_animation_vitesse=0.1
    astro_sprite_actuel=astro_front_sprites[0]
    direction="bas"

    vitesse_joueur = width/300+dico_upgrades_stats["vitesse"]*20  ##Vitesse de deplacement du joueur
    couleur_joueur = (255, 0, 0)
    types_ennemis = [Majo, Marcel,Terminateur,Philippe,Leure]  ##Liste des types d'ennemis
    liste_ennemis = []  ##Liste pour stocker les ennemis
    derniers_spawn = {classe: 0 for classe in types_ennemis}  ##Dictionnaire pour stocker le dernier spawn de chaque type d'ennemi
    clock = pygame.time.Clock()
    liste_projectiles = []  ##Liste pour stocker les projectiles
    laser=weapon_main(max(100, 500 - dico_upgrades_laser["cadence_de_tir"]*50), projectile_laser, homing=False, portee_detection=height/5 + dico_upgrades_laser["portee"]*(height/20), vitesse=width/200, interval_tick_ms=500, sprite=laser_sprite)
    laser.nom="Laser"
    roquette=weapon_main(max(500, 10000 - dico_upgrades_roquette["cadence_de_tir"]*500), projectile_roquette,homing=True,portee_detection=width/5,vitesse=width/300,aoe=True,aoe_rayon=width/10,duree_AOE=333,interval_tick_ms=500,sprite=roquette_sprite,degat=3,degat_AOE=1,sprite_feu=sprite_feu_roquette,sprite_explosion=sprite_explosion_roquette)  ##Crée une arme roquette avec un délai de 1500ms entre chaque tir et des projectiles homing
    roquette.nom="Roquette"
    mine=weapon_main(max(500, 5000 - dico_upgrades_mine["cadence_de_tir"]*500), projectile_mine,homing=False,portee_detection=math.inf,vitesse=0,aoe=True,aoe_rayon=width/20,duree_AOE=2500,duree=10000,degat_AOE=1,interval_tick_ms=500,degat=2,sprite=projectile_mine_sprite,sprite_feu=sprite_feu_mine,sprite_explosion=sprite_explosion_mine)  ##Crée une arme mine avec un délai de 1500ms entre chaque tir et des projectiles non homing
    mine.nom="Mine"
    aura_active=aura(width/4,1,sprite=aura_sprites,interval_tick_ms=500,vitesse_animation=0.1)  ##Crée une aura qui inflige des dégâts aux ennemis à proximité toutes les 500ms
    aura_active.nom="Aura Active"
    tourelle_active=tourelle(0,0,sprite_batiment=tourelle_sprites,sprite_balle=projectile_tourelle_sprite,vitesse_animation=0.1)  ##Crée une tourelle qui tire des projectiles de tourelle
    type_armes=["stats",laser,mine]   ##Liste des types d'armes
    liste_armes=[laser,roquette,mine,aura_active,tourelle_active]   ##Liste des armes du joueur, utilisée pour le level up
    armes_possedees=["stats"]+(["laser"] if laser in type_armes else [])+(["roquette"] if roquette in type_armes else [])+(["mine"] if mine in type_armes else [])+(["aura"] if aura_active in type_armes else [])+(["tourelle"] if tourelle_active in type_armes else [])
    liste_projectiles_ennemis=[]  ##Liste pour stocker les projectiles des ennemis
    liste_explosions=[]
    mines_actuelles=[]  ##Liste pour stocker les mines posées par le joueur
    liste_tourelles=[]  ##Liste pour stocker les tourelles posées par le joueur
    armes_dict = {
    "laser": laser,
    "roquette": roquette,
    "mine": mine,
    "aura": aura_active,
    "tourelle": tourelle_active
    }
    pv_joueur=100  ##Points de vie du joueur
    pv_max_joueur=100
    pygame.mixer.music.stop()
    set_sfx_volume(settings.get("sound_volume",50)/100)
    pygame.mixer.music.set_endevent(GAME_MUSIC_EVENT)
    jouer_musique_jeu_aleatoire(settings)
    xp=0
    xp_for_level=10
    niveau=0
    pv_heal_cooldown=0
    duree_journee=0
    nombre_journees=0
    dernier_soin=pygame.time.get_ticks()
    maintenant=0
    liste_aoe=[]
    liste_fragmentations_mine=[]
    liste_arcs=[]
    taille_base = int(TILE_SIZE * zoom)
    # On ajoute 1 pixel pour l'overlapping
    taille_overlap = taille_base + 1 
    textures_zoom = {}
    for key, surf in textures.items():
        # On scale avec le pixel supplémentaire
        textures_zoom[key] = pygame.transform.scale(surf, (taille_overlap, taille_overlap))
    
    def programmer_fragmentations_mine(x,y,projectile_source):
        if not dico_upgrades_uniques["mine"]["mine_fragmentation"]:
            return
        moment_declenchement=pygame.time.get_ticks()+500
        rayon_fragment=max(1,projectile_source.aoe_rayon/2)
        rayon_disposition=projectile_source.aoe_rayon
        for i in range(8):
            angle=(2*math.pi*i)/8
            fx=x+math.cos(angle)*rayon_disposition
            fy=y+math.sin(angle)*rayon_disposition
            liste_fragmentations_mine.append({
                "x":fx,
                "y":fy,
                "rayon":rayon_fragment,
                "degat":projectile_source.degat_AOE,
                "duree":projectile_source.duree_AOE,
                "interval":projectile_source.interval_tick_ms,
                "sprite_feu":projectile_source.sprite_feu,
                "sprite_explosion":projectile_source.sprite_explosion,
                "empoisonne":dico_upgrades_uniques["mine"]["mine_empoisonnee"],
                "declenchement":moment_declenchement,
            })


    while en_jeu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type==GAME_MUSIC_EVENT:
                jouer_musique_jeu_aleatoire(settings)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    temps_debut_pause=pygame.time.get_ticks()
                    pygame.mixer.music.stop()
                    settings=afficher_menu_pause()
                    set_sfx_volume(settings.get("sound_volume",50)/100)
                    pygame.mixer.music.set_endevent(GAME_MUSIC_EVENT)
                    jouer_musique_jeu_aleatoire(settings)
                    duree_pause=pygame.time.get_ticks()-temps_debut_pause

                    for classe in derniers_spawn:
                        derniers_spawn[classe] += duree_pause  ##Décale les temps de spawn des ennemis pour compenser la pause
                    for armes in [a for a in type_armes if hasattr(a, 'compenser_pause')]:  ##Vérifie que l'arme a une méthode compenser_pause avant de l'appeler
                        armes.compenser_pause(duree_pause)  ##Décale les temps de tir des armes pour compenser la pause
                    for tourelles in liste_tourelles:
                        tourelles.compenser_pause(duree_pause)
                    for ennemi in liste_ennemis:
                        if ennemi.arme:
                            ennemi.arme.compenser_pause(duree_pause)  ##Décale les temps de tir des armes des ennemis pour compenser la pause
                            
        player_real_rect = pygame.Rect(0,0,astro_front_sprites[0].get_width()/1.4,astro_front_sprites[0].get_height())
        player_real_rect.center = (player_x, player_y)
        #Mouvement et logique du joueur
        if True:
            #Mouvement du joueur
            touches = pygame.key.get_pressed()
            if touches[pygame.K_d]:
                player_x += vitesse_joueur
                astro_animation_index += astro_animation_vitesse
                astro_sprite_actuel = astro_front_sprites[int(astro_animation_index) % len(astro_front_sprites)] if direction=="bas" else astro_back_sprites[int(astro_animation_index) % len(astro_back_sprites)]
            if touches[pygame.K_q] or touches[pygame.K_a]:
                player_x -= vitesse_joueur
                astro_animation_index += astro_animation_vitesse
                astro_sprite_actuel = astro_front_sprites[int(astro_animation_index) % len(astro_front_sprites)] if direction=="bas" else astro_back_sprites[int(astro_animation_index) % len(astro_back_sprites)]
            if touches[pygame.K_s]:
                player_y += vitesse_joueur
                direction="bas"
                astro_animation_index += astro_animation_vitesse
                astro_sprite_actuel = astro_front_sprites[int(astro_animation_index) % len(astro_front_sprites)]
            if touches[pygame.K_z] or touches[pygame.K_w]:
                player_y -= vitesse_joueur
                direction="haut"
                astro_animation_index += astro_animation_vitesse
                astro_sprite_actuel = astro_back_sprites[int(astro_animation_index) % len(astro_back_sprites)]
            if touches[pygame.K_e] and niveau>=1:
                temps_debut_pause = pygame.time.get_ticks()

                if nombre_journees >= 5:
                    arme_nom, stat = afficher_upgrades(screen,width,height,3,armes_possedees,font,nouvelle_arme=True)
                    type_armes.append(armes_dict[arme_nom])
                    
                for _ in range(niveau):
                    afficher_upgrades(screen,width,height,3,armes_possedees,font)
                    niveau -= 1
                pv_max_joueur=100+dico_upgrades_stats["pv"]*10
                pv_joueur=100+dico_upgrades_stats["pv"]*10
                vitesse_joueur=width/300+dico_upgrades_stats["vitesse"]*5
                armes_possedees=["stats"]+(["laser"] if laser in type_armes else [])+(["roquette"] if roquette in type_armes else [])+(["mine"] if mine in type_armes else [])+(["aura"] if aura_active in type_armes else [])+(["tourelle"] if tourelle_active in type_armes else [])
                duree_pause=pygame.time.get_ticks()-temps_debut_pause
                for armes in type_armes:
                    if hasattr(armes,"compenser_pause"):
                        armes.compenser_pause(duree_pause)
                for classe in derniers_spawn:
                        derniers_spawn[classe] += duree_pause  ##Décale les temps de spawn des ennemis pour compenser la pause
                for ennemi in liste_ennemis:
                        if ennemi.arme:
                            ennemi.arme.compenser_pause(duree_pause)  ##Décale les temps de tir des armes des ennemis pour compenser la pause

                #enleve tous les ennemis et les balles et tous les autres trucs
                liste_aoe.clear()
                liste_ennemis.clear()
                liste_projectiles.clear()
                liste_projectiles_ennemis.clear()
                mines_actuelles.clear()
                liste_tourelles.clear()
                nombre_journees+=1
                duree_journee=0

            #Maintient le joueur au centre de l'ecran en calculant le decalage
            offset_x = player_x - (width // 2)
            offset_y = player_y - (height // 2)

            #Map??
            screen.fill(white)


            for layer in map_data["layers"]:
                for tile in layer["tiles"]:
                    texture_key = f"{tile['spriteSheetId']}_{tile.get('id', 0)}"
                    
                    if texture_key in textures_zoom:
                        # On ajoute marge_centrage pour décaler tout le dessin vers le milieu
                        draw_x = int(tile["x"] * zoom - offset_x + marge_centrage_x)
                        draw_y = int(tile["y"] * zoom - offset_y + marge_centrage_y)
                        
                        if -taille_overlap <= draw_x <= width and -taille_overlap <= draw_y <= height:
                            screen.blit(textures_zoom[texture_key], (draw_x, draw_y))
            #g du le decale la pour fix un bug
            for tourelles in liste_tourelles:
                tourelles.update(liste_ennemis,liste_projectiles)
                tourelles.dessiner(screen,offset_x,offset_y)

            # Gérer le spawn des ennemis
            for classe in types_ennemis:
                if pygame.time.get_ticks() - derniers_spawn[classe] >= classe.spawn_delay:
                    spawn_x, spawn_y = classe.calculer_pos_spawn(player_x, player_y, width, height)
                    nouvel_ennemi = classe(spawn_x, spawn_y)
                    liste_ennemis.append(nouvel_ennemi)
                    derniers_spawn[classe] = pygame.time.get_ticks()

            #Targetting des ennemis pour savoir si c le joueur ou la tourelle
            for ennemi in liste_ennemis[:]:
                target_x, target_y = player_x, player_y

                if liste_tourelles and dico_upgrades_uniques["tourelle"]["tourelle_leurre"]:
                    # Toujours cibler la tourelle la plus proche
                    t_proche = min(liste_tourelles, key=lambda t: math.hypot(ennemi.x - t.x, ennemi.y - t.y))
                    target_x, target_y = t_proche.x, t_proche.y
                elif liste_tourelles:
                    # si pas l'upgrade cibler le plus proche entre tourelle et joueur
                    dist_joueur = math.hypot(ennemi.x - player_x, ennemi.y - player_y)
                    min_dist = dist_joueur
                    for t in liste_tourelles:
                        dist_t = math.hypot(ennemi.x - t.x, ennemi.y - t.y)
                        if dist_t < min_dist:
                            min_dist = dist_t
                            target_x, target_y = t.x, t.y

                ennemi.update(target_x, target_y)
                
                
            #Mettre à jour les explosions
            for explosion in liste_explosions[:]:
                explosion.update()
                if explosion.terminee:
                    liste_explosions.remove(explosion)
                    
            # Gérer les tirs du joueur
            if liste_ennemis or mine in type_armes: # On autorise le tir si ennemis OU si on a des mines
                for armes in [a for a in type_armes if isinstance(a, weapon_main)]:  ##On vérifie que c'est bien une arme avant de proposer de tirer, pour éviter les erreurs avec l'aura
                    # Condition spéciale pour la mine : on la pose toujours sous nos pieds
                    if armes.classe == projectile_mine:
                        if armes.tirer():
                            mines_actuelles=[p for p in liste_projectiles if isinstance(p, projectile_mine)]
                            if len(mines_actuelles) >= 10+dico_upgrades_mine["duree_vie"]:  # Limite à 10
                                for p in liste_projectiles:
                                    if isinstance(p, projectile_mine):
                                        liste_projectiles.remove(p)
                                        break
                            # On crée une cible factice sur le joueur
                            cible_ici = type('Cible', (), {'x': player_x, 'y': player_y})()
                            sprite_aoe_mine = sprites_poison_mine if dico_upgrades_uniques["mine"]["mine_empoisonnee"] else armes.sprite_feu
                            nouveau_p = projectile_mine(
                                player_x, player_y, 0, cible_ici,
                                degat=armes.degat,
                                range=armes.range_balle,
                                aoe=armes.aoe,
                                aoe_rayon=armes.aoe_rayon,
                                degat_AOE=armes.degat_AOE,
                                duree_AOE=armes.duree_AOE,
                                sprite=projectile_mine_sprite,
                                duree=armes.duree,
                                interval_tick_ms=armes.interval_tick_ms,
                                sprite_feu=sprite_aoe_mine,
                                sprite_explosion=armes.sprite_explosion
                            )
                            liste_projectiles.append(nouveau_p)
                    
                    # Tir normal pour les autres armes (Laser, Roquette)
                    elif liste_ennemis:
                        cible_proche = min(liste_ennemis, key=lambda ennemi: (ennemi.x - player_x)**2 + (ennemi.y - player_y)**2)
                        if armes.tirer() and math.hypot(cible_proche.x - player_x, cible_proche.y - player_y) <= armes.range_balle:
                            nouveau_p = armes.classe(
                                player_x, player_y, armes.vitesse, cible_proche, 
                                homing=armes.homing, range=armes.range_balle,
                                sprite=armes.sprite,
                                degat=armes.degat, aoe=armes.aoe, aoe_rayon=armes.aoe_rayon,
                                degat_AOE=armes.degat_AOE, duree_AOE=armes.duree_AOE,sprite_feu=armes.sprite_feu,sprite_explosion=armes.sprite_explosion
                            )
                            liste_projectiles.append(nouveau_p)
                        
            for proj in liste_projectiles[:]:
                temps_ecoule = proj.update(liste_ennemis)
                explosion_deja_creee = False
                continuer_ricochet = False
                roquette_ricochet_active = isinstance(proj, projectile_roquette) and proj.ricochet_actif


                # 1. Détection collision
                hit_ennemi = None
                for ennemi in liste_ennemis:
                    if isinstance(proj, projectile_mine) and not proj.est_active():
                        continue
                    if not proj.rect.colliderect(ennemi.rect):
                        continue

                    if (isinstance(proj, projectile_laser)
                        and dico_upgrades_uniques["laser"]["laser_perforant"]
                        and ennemi in proj.ennemis_touches
                    ):
                        continue

                    if roquette_ricochet_active and ennemi in proj.ennemis_touches:
                        continue


                    hit_ennemi = ennemi
                    break

                # 2. APPLIQUER DEGATS ET RECUPERER XP
                if hit_ennemi:
                    # On capture si l'ennemi est mort (nécessite le 'return True' dans prendre_degats)
                    pv_joueur=min(pv_max_joueur,pv_joueur+dico_upgrades_stats["vol_de_vie"]*proj.degat)

                    if isinstance(proj,projectile_laser):
                        proj.chain_lightning(hit_ennemi,liste_ennemis,liste_arcs)
                    mort = hit_ennemi.prendre_degats(proj.degat)

                    if isinstance(proj,projectile_laser) and dico_upgrades_uniques["laser"]["laser_ralentissant"]:
                        hit_ennemi.appliquer_slow(0.2,2500)

                    if isinstance(proj,projectile_laser) and dico_upgrades_uniques["laser"]["laser_perforant"]:
                        proj.ennemis_touches.append(hit_ennemi)

                    if roquette_ricochet_active:
                        proj.ennemis_touches.append(hit_ennemi)
                        proj.nb_contacts_ricochet += 1
                        if proj.aoe:
                            aoe_zone = AOE(
                                proj.x,
                                proj.y,
                                proj.aoe_rayon,
                                proj.degat_AOE,
                                proj.duree_AOE,
                                interval_tick_ms=proj.interval_tick_ms,
                                cible="ennemi",
                                sprite_feu=proj.sprite_feu
                            )
                            liste_aoe.append(aoe_zone)
                            liste_explosions.append(Explosion(proj.x, proj.y, proj.sprite_explosion,proj.aoe_rayon))
                            explosion_deja_creee = True

                        if (proj.nb_contacts_ricochet < proj.nb_contacts_ricochet_max
                            and proj.preparer_ricochet(liste_ennemis)):
                            continuer_ricochet = True

                    if isinstance(proj,projectile_roquette) and dico_upgrades_uniques["roquette"]["roquette_shrapnel"]:
                        nouveaux_shrapnels = proj.creer_shrapnels(hit_ennemi)
                        liste_projectiles.extend(nouveaux_shrapnels)

                    if mort:
                        xp += hit_ennemi.xp #J'avais oublie ca ;-;
                trop_loin = proj.est_trop_loin()

                # On ajoute une vérification pour éviter de supprimer deux fois (si hit + trop loin)
                if hit_ennemi or trop_loin or temps_ecoule:
                    doit_creer_explosion = proj.aoe and not explosion_deja_creee and (hit_ennemi or (not roquette_ricochet_active and (trop_loin or temps_ecoule)))
                    if doit_creer_explosion:
                        # Création de l'AOE
                        aoe_zone = AOE(
                            proj.x,
                            proj.y,
                            proj.aoe_rayon,
                            proj.degat_AOE,
                            proj.duree_AOE,
                            interval_tick_ms=proj.interval_tick_ms,
                            cible="ennemi",
                            sprite_feu=proj.sprite_feu,
                            empoisonne=isinstance(proj, projectile_mine) and dico_upgrades_uniques["mine"]["mine_empoisonnee"]

                        )
                        liste_aoe.append(aoe_zone)
                        
                        liste_explosions.append(Explosion(proj.x, proj.y, proj.sprite_explosion,proj.aoe_rayon))
                        if isinstance(proj,projectile_mine):
                            programmer_fragmentations_mine(proj.x, proj.y, proj)

                    # On vérifie si le projectile est toujours dans la liste avant de remove
                    if proj in liste_projectiles:
                        if continuer_ricochet:
                            continue
                        if isinstance(proj, projectile_mine) and hit_ennemi:
                            if proj.declencher_apres_explosion():
                                continue
                            liste_projectiles.remove(proj)
                            continue
                        if proj.est_trop_loin() or temps_ecoule:
                            liste_projectiles.remove(proj)
                        elif hit_ennemi and not (
                            isinstance(proj, projectile_laser)
                            and dico_upgrades_uniques["laser"]["laser_perforant"]):
                            liste_projectiles.remove(proj)

                            

            #Mettre a jour l'aura
            if aura_active in type_armes:
                aura_active.update(player_x, player_y, liste_ennemis, xp_callback=ajouter_xp)
                aura_active.dessiner(screen, player_x, player_y, offset_x, offset_y)

            aura_affaiblissante_active = (
                aura_active in type_armes
                and dico_upgrades_uniques["aura"].get("aura_affaiblissante", False)
            )

            # Mettre à jour les projectiles des ennemis
            for proj in liste_projectiles_ennemis[:]:
                proj.update([], player_pos=(player_x, player_y))

                impact = False  # indique si le projectile touche quelque chose

                # Collision avec les tourelles
                for t in liste_tourelles[:]:
                    if proj.rect.colliderect(t.colliderect):
                        reduction=0.5 if aura_affaiblissante_active and aura_active.ennemi_dans_aura(proj.proprietaire, player_x, player_y) else 1
                        t.hp-=proj.degat*reduction
                        impact = True
                        if t.hp<=0 and t in liste_tourelles:
                            liste_tourelles.remove(t)
                            if dico_upgrades_uniques["tourelle"]["tourelle_explosive"]:
                                liste_aoe.append(AOE(t.x, t.y, width/5, 10+dico_upgrades_tourelle["degat"], 500, cible="ennemi"))
                        break

                # Collision avec le joueur
                if not impact and proj.rect.colliderect(player_real_rect):
                    if not random.randint(1,11)<=dico_upgrades_stats["esquive"]:    ##Pour l'esquive
                        reduction=0.5 if aura_affaiblissante_active and aura_active.ennemi_dans_aura(proj.proprietaire, player_x, player_y) else 1
                        pv_joueur -= proj.degat*reduction
                        Soundhit.play()
                        impact = True

                # Projectile trop loin
                if not impact and proj.est_trop_loin():
                    impact = True

                # Si le projectile a eu un impact, créer explosion / AOE et le retirer
                if impact:
                    if proj.aoe:
                        explosion = Explosion(proj.x, proj.y, proj.sprite_explosion,proj.aoe_rayon)
                        liste_explosions.append(explosion)
                        aoe_zone = AOE(
                            proj.x, proj.y, proj.aoe_rayon, proj.degat_AOE, proj.duree_AOE,
                            interval_tick_ms=proj.interval_tick_ms, cible="joueur", sprite_feu=proj.sprite_feu, proprietaire=proj.proprietaire
                        )
                        liste_aoe.append(aoe_zone)

                    if proj in liste_projectiles_ennemis:
                        liste_projectiles_ennemis.remove(proj)

            # Mettre à jour les collisions ennemis avec le joueur
            for ennemi in liste_ennemis[:]:
                if ennemi.rect.colliderect(player_real_rect):
                    if not random.randint(1,11)<=dico_upgrades_stats["esquive"]:
                        reduction=0.5 if aura_affaiblissante_active and aura_active.ennemi_dans_aura(proj.proprietaire, player_x, player_y) else 1
                        pv_joueur -= ennemi.degat*reduction
                        Soundhit.play()
                    liste_ennemis.remove(ennemi)

                #pour les tourelles
                for t in liste_tourelles[:]:
                    if ennemi.rect.colliderect(t.colliderect):
                        if maintenant-ennemi.dernier_coup>=attack_delay_ennemi:
                            reduction=0.5 if aura_affaiblissante_active and aura_active.ennemi_dans_aura(proj.proprietaire, player_x, player_y) else 1
                            t.hp-=ennemi.degat*reduction
                            if t.hp<=0 and t in liste_tourelles:
                                liste_tourelles.remove(t)
                                if dico_upgrades_uniques["tourelle"]["tourelle_explosive"]:
                                    liste_aoe.append(AOE(t.x, t.y, width/5,10+dico_upgrades_tourelle["degat"], 500, cible="ennemi"))
                            ennemi.dernier_coup=maintenant

        maintenant_fragmentations=pygame.time.get_ticks()
        for fragmentation in liste_fragmentations_mine[:]:
            if maintenant_fragmentations<fragmentation["declenchement"]:
                continue
            liste_explosions.append(Explosion(fragmentation["x"],fragmentation["y"],fragmentation["sprite_explosion"],fragmentation["rayon"]))
            liste_aoe.append(AOE(
                fragmentation["x"],
                fragmentation["y"],
                fragmentation["rayon"],
                fragmentation["degat"],
                fragmentation["duree"],
                interval_tick_ms=fragmentation["interval"],
                cible="ennemi",
                sprite_feu=fragmentation["sprite_feu"],
                empoisonne=fragmentation.get("empoisonne", False)

            ))
            liste_fragmentations_mine.remove(fragmentation)

        ##Gerer le spawn des tourelles
        maintenant=pygame.time.get_ticks()
        if tourelle_active in type_armes:
            if maintenant-tourelle_active.dernier_spawn>=tourelle_active.delai_spawn:
                if len(liste_tourelles)>=10+dico_upgrades_tourelle["cadence_de_tir"]:
                    liste_tourelles.pop(0)
                nouvelle_t=tourelle(
                    player_x,
                    player_y,
                    sprite_batiment=tourelle_sprites,
                    sprite_balle=projectile_tourelle_sprite,
                    vitesse_animation=0.1
                )
                liste_tourelles.append(nouvelle_t)
                tourelle_active.dernier_spawn=maintenant


        # Gerer les AOE
        for aoe in liste_aoe[:]:
            if aoe.cible == "ennemi":
                aoe.update(liste_ennemis)
            else:
                aoe.update([],player_rect=player_real_rect,aura_active=aura_active,aura_affaiblissante=aura_affaiblissante_active,player_x=player_x,player_y=player_y) 

            aoe.dessiner(screen, offset_x, offset_y)

            if aoe.terminee:
                liste_aoe.remove(aoe)

        #Dessiner les ennemis
        for ennemi in liste_ennemis:
            ennemi.dessiner(screen, offset_x, offset_y)
            
        #Dessine le joueur
        astro_rect=astro_front_sprites[0].get_rect()
        astro_rect.center=(width/2,height/2)
        screen.blit(astro_sprite_actuel,astro_rect)

        #Dessiner les projectiles du joueur
        for proj in liste_projectiles[:]:
            proj.dessiner(screen, offset_x, offset_y)

        #Dessiner les tirs des ennemis
        for proj in liste_projectiles_ennemis[:]:
            proj.dessiner(screen, offset_x, offset_y)
            
        #Dessiner les explosions
        for explosion in liste_explosions[:]:
            explosion.dessiner(screen,offset_x,offset_y)
        
        #gerer les arcs
        for arc in liste_arcs[:]:
            arc.update()
            if arc.terminee:
                liste_arcs.remove(arc)
            if arc in liste_arcs:
                arc.dessiner(screen,offset_x,offset_y)
        
        #Gerer la regen_pv
        maintenant=pygame.time.get_ticks()
        if maintenant-dernier_soin>=1000:
            pv_joueur=min(pv_max_joueur,pv_joueur+dico_upgrades_stats["regen_pv"])
            dernier_soin=maintenant
            
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
        

        # Mettre à jour les délais de tir
        laser.delai = max(100, 500 - dico_upgrades_laser["cadence_de_tir"] * 50)
        laser.range = height/5 + dico_upgrades_laser["portee"] * (height/20)
        laser.range_balle = laser.range * 2
        roquette.delai = max(500, 10000 - dico_upgrades_roquette["cadence_de_tir"] * 500)
        roquette.range = width/5 + dico_upgrades_roquette["portee"] * (width/20)  
        roquette.range_balle = roquette.range * 2                                   
        mine.delai = max(500, 5000 - dico_upgrades_mine["cadence_de_tir"] * 500)

        duree_journee+=1
        echelle_difficulte=nombre_journees*2+duree_journee//1200

        # Mettre à jour les spawn delays quand la difficulté change
        enemi_spawn_delay=max(4000-echelle_difficulte,500)  # On limite le spawn delay minimum à 500ms pour éviter que ce soit injouable ou que ca aille dans le negatif
        Majo.spawn_delay=enemi_spawn_delay
        Marcel.spawn_delay=enemi_spawn_delay*1.5
        Terminateur.spawn_delay=enemi_spawn_delay*3
        Philippe.spawn_delay=enemi_spawn_delay*2
        
        texte_niveau=font.render(f"Niveaux disponibles:{niveau}",True,(0,0,0))
        texte_niveau_rect=texte_niveau.get_rect(topleft=(width/150,height/20))
        screen.blit(texte_niveau,texte_niveau_rect)

        texte_journee=font.render(f"Journee:{nombre_journees}",True,(0,0,0))
        texte_journee_rect=texte_niveau.get_rect(center=(width/2,height/40))
        screen.blit(texte_journee,texte_journee_rect)

        fleche_vers_destination(player_x,player_y,0,0)
        pygame.display.flip()




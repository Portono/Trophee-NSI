import pygame
import random
import math

pygame.init()

dico_upgrades={"chance":1,
               "xp_gain":0,
               "hp":0,
               "vitesse":0,
               "vitesse_balles":0,
               "fire_rate":0,
               "degats":0,
               "portee":0,
               "regen_hp":0,
               "lifesteal":0,
               "taille_projectiles":0,
               "multishot":0,
               "bigger_aoe":0,
               "dodge":0,
               "deflect":0,
               "piercing":0,
               "arc_degats":0,
               "tirs_ralentissants":0,
               "aoe_joueur":0,
               "resistance":0,
               "summon_allies":0,
               "distance_damage":0,
               }

dico_rarete_upgrades={"chance":"commun",
                      "hp":"commun",
                      "vitesse":"commun",
                      "vitesse_balles":"commun",
                      "degats":"commun",
                      "portee":"commun",
                      "fire_rate":"commun",
                      "xp_gain":"rare",
                      "regen_hp":"rare",
                      "taille_projectiles":"rare",
                      "aoe_joueur":"rare",
                      "resistance":"rare",
                      "bigger_aoe":"rare",
                      "lifesteal":"epique",
                      "deflect":"epique",
                      "piercing":"epique",
                      "arc_degats":"epique",
                      "tirs_ralentissants":"epique",
                      "distance_damage":"epique",
                      "dodge":"epique",
                      "multishot":"legendaire",
                      "summon_allies":"legendaire"
                      }

dico_poids_upgrade={"chance":0,
                    "xp_gain":0,
                    "hp":0,
                    "vitesse":0,
                    "vitesse_balles":0,
                    "fire_rate":0,
                    "degats":0,
                    "portee":0,
                    "regen_hp":0,
                    "lifesteal":0,
                    "taille_projectiles":0,
                    "multishot":0,
                    "bigger_aoe":0,
                    "dodge":0,
                    "deflect":0,
                    "piercing":0,
                    "arc_degats":0,
                    "tirs_ralentissants":0,
                    "aoe_joueur":0,
                    "resistance":0,
                    "summon_allies":0,
                    "distance_damage":0,
                    }

def get_coef_rarete(upgrade):
    table_rarete={"commun":9,"rare":6,"epique":3,"legendaire":1}
    return table_rarete.get(dico_rarete_upgrades[upgrade],1)

def random_upgrade():
    total_points=sum(v for k,v in dico_upgrades.items() if k!="chance")
    multipl_rarete=dico_upgrades["chance"]
    for upgrade in dico_upgrades:
        if upgrade=="chance":
            dico_poids_upgrade[upgrade]=1
            continue
        r=get_coef_rarete(upgrade)
        if total_points>0:
            ratio=dico_upgrades[upgrade]/total_points
            malus=(ratio/multipl_rarete)
            poids=r*(1-malus)
        else:
            poids=r
        dico_poids_upgrade[upgrade]=max(0,poids)
    return dico_poids_upgrade

def choisir_upgrades():
    random_upgrade()
    options=[]
    poids_temp=dico_poids_upgrade.copy()
    for _ in range(3):
        noms=list(poids_temp.keys())
        poids=list(poids_temp.values())
        if sum(poids)==0:
            break   ##au cas ou tous les poids serait a 0, on sait jamais
        choix=random.choices(noms,weights=poids,k=1)[0] ##renvoie une selection au hasard de facon aleatoire en prenant compte le poids
        options.append(choix)
        poids_temp[choix]=0
    return options

def level_up(screen,width,height):
    upgrading=True
    options=choisir_upgrades()
    while upgrading:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((255,255,255))
        option1_rect=pygame.Rect(0,0,width/6,height/1.5)
        option2_rect=option1_rect.copy()
        option3_rect=option1_rect.copy()
        option1_rect.center=((width-3*(width/6))/4+(width/12),height/2)
        option2_rect.center=(2*(width-3*(width/6))/4+3*(width/12),height/2)
        option3_rect.center=(3*(width-3*(width/6))/4+5*(width/12),height/2)
        pygame.draw.rect(screen,(0,0,0),option1_rect)
        pygame.draw.rect(screen,(255,0,0),option2_rect)
        pygame.draw.rect(screen,(0,255,0),option3_rect)
        pygame.display.flip()

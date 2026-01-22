import pygame
import random
import math

dico_upgrades={"chance":0,
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
    if dico_rarete_upgrades[upgrade]=="commun":
        return 9
    if dico_rarete_upgrades[upgrade]=="rare":
        return 6
    if dico_rarete_upgrades[upgrade]=="epique":
        return 3
    if dico_rarete_upgrades[upgrade]=="legendaire":
        return 1

def random_upgrade():
    sum_upgrades=0
    for upgrades in dico_upgrades:
        sum_upgrades+=dico_upgrades[upgrades]
        poids_upgrade_dico[upgrades]=get_coef_rarete(upgrades)*(1-(dico_upgrades[upgrades]/(sum_upgrades*
        
        
    

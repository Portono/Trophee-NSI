import pygame
import random
import math

pygame.init()

#-------------------Upgrades stats classiques-------------------------------------
dico_upgrades_stats={
                "chance":1,         
                "gain_xp":0,        
                "pv":0,             
                "vitesse":0,                        
                "regen_pv":0,           
                "vol_de_vie":0,  
                "esquive":0,
                "renvoi":0,
                }

#------------------Upgrades armes uniques----------------------------------------
dico_upgrades_uniques={
                "laser":{"laser_electrique":False,
                         "laser_ralentissant":False,
                         "laser_perforant":False
                         },
                "roquette":{"roquette_shrapnel":False,
                            "roquette_enflammee":False,
                            "roquette_ricochet":False
                            },
                "mine":{"mine_empoisonnee":False,
                        "mine_fragmentation":False,
                        "mine_double_vie":False
                        },
                "aura":{"aura_trainee":False,
                        "aura_scaling":False,
                        "aura_pulse":False
                        },
                "tourelle":{"tourelle_explosive":False,
                            "tourelle_aoe_defensive":False,
                            "tourelle_leurre":False
                            },
                "airstrike":{"airstrike_stun":False,
                             "airstrike_":False,
                             "airstrike_":False
                            }
                }
#------------------Upgrades stats laser------------------------------------------
dico_upgrades_laser={
                "cadence_de_tir":0,
                "degat":0,
                "taille_projectile":0,
                "vitesse_balles":0,
                "portee":0,
                }  
#------------------Upgrades stats roquette------------------------------------------   
dico_upgrades_roquette={
                "cadence_de_tir":0,
                "degat":0,
                "taille_projectile":0,
                "vitesse_balles":0,
                "portee":0,
                }
#------------------Upgrades stats mine------------------------------------------
dico_upgrades_mine={
                "cadence_de_tir":0,
                "degat":0,
                "taille_projectile":0,
                "portee":0
                }
#------------------Upgrades stats aura------------------------------------------
dico_upgrades_aura={
                "cadence_de_tir":0,
                "degat":0,
                "portee":0
                }
#------------------Upgrades stats tourelle------------------------------------------
dico_upgrades_tourelle={
                "cadence_de_tir":0,
                "degat":0,
                "hp":0,
                "vitesse_balles":0,
                "portee":0
                }
#------------------Upgrades stats tourelle------------------------------------------
dico_upgrades_airstrike={
                "cadence_de_tir":0,
                "degat":0,
                }


liste_dicos=[dico_upgrades_stats,dico_upgrades_laser,dico_upgrades_roquette,dico_upgrades_mine,dico_upgrades_aura,dico_upgrades_tourelle]
master_dico = {
    "stats": dico_upgrades_stats,
    "laser": dico_upgrades_laser,
    "roquette": dico_upgrades_roquette,
    "mine": dico_upgrades_mine,
    "aura": dico_upgrades_aura,
    "tourelle": dico_upgrades_tourelle
}

def random_upgrade(nb_upgrades=3, armes_possedees=["stats", "laser","roquette"]):
    liste_upgrades = []
    type_upgrade = random.randint(0, 10)

    if type_upgrade == 0:   ##pour les upgrades uniques
        options_uniques = []
        for arme in armes_possedees:
            if arme in dico_upgrades_uniques:
                for upgrade, deja_pris in dico_upgrades_uniques[arme].items():
                    if not deja_pris:
                        options_uniques.append((arme, upgrade))
        
        if options_uniques:
            # On pioche le nombre demandé sans doublons
            nb_a_piger = min(nb_upgrades, len(options_uniques))
            liste_upgrades = random.sample(options_uniques, nb_a_piger)
            return liste_upgrades # On sort direct avec les uniques 
        
    #liste de toutes les stats dispo
    options_stats = []
    for arme in armes_possedees:
        if arme in master_dico:
            for upgrade_nom in master_dico[arme].keys():
                options_stats.append((arme, upgrade_nom))
    
    nb_a_piger = min(nb_upgrades, len(options_stats))
    liste_upgrades = random.sample(options_stats, nb_a_piger)   ##sample c mieux, ca evite les doubles

    return liste_upgrades

def afficher_upgrades(screen, width, height, nb_upgrades, armes_possedees, font):
    liste_upgrades = random_upgrade(nb_upgrades=nb_upgrades, armes_possedees=armes_possedees)
    
    nb_u = len(liste_upgrades)
    # On divise la largeur totale par le nombre d'upgrades
    r_width = width / nb_u 
    r_height = height / 1.1 # Presque toute la hauteur

    while True:
        screen.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Pour détecter le clic, on regarde juste quel index i est touché
                index_clique = int(event.pos[0] // r_width)
                if 0 <= index_clique < nb_u:
                    return liste_upgrades[index_clique]

        # Dessin des colonnes/cartes
        for i in range(nb_u):

            # On laisse juste 5 pixels de marge entre eux pour le style ;) c "style"
            rect = pygame.Rect(i * r_width + 5, (height - r_height) / 2, r_width - 10, r_height)
            
            pygame.draw.rect(screen, (0, 200, 0), rect) # Vert un peu plus sombre
            pygame.draw.rect(screen, (255, 255, 255), rect, 2) # Bordure

            # Affichage du texte centré dans chaque colonne
            nom_arme, nom_stat = liste_upgrades[i]
            
            # Texte 1 : L'arme
            txt_arme = font.render(str(nom_arme).upper(), True, (255, 255, 255))
            # Texte 2 : La stat
            txt_stat = font.render(str(nom_stat), True, (200, 255, 200))
            
            # Centrage automatique dans le rectangle i
            centro_x = i * r_width + (r_width / 2)
            screen.blit(txt_arme, txt_arme.get_rect(center=(centro_x, height // 2 - 30)))
            screen.blit(txt_stat, txt_stat.get_rect(center=(centro_x, height // 2 + 30)))

        pygame.display.flip()



#for _ in range(100):
    #print(random_upgrade()) ##debug

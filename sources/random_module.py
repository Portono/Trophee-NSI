import pygame
import random
import math

pygame.init()

#-------------------Upgrades stats classiques-------------------------------------
dico_upgrades_stats={         
                "gain_xp":0,        
                "pv":0,             
                "vitesse":0,                        
                "regen_pv":0,           
                "vol_de_vie":0,  
                "esquive":0
                }

#------------------Upgrades armes uniques----------------------------------------
dico_upgrades_uniques={
                "laser":{"laser_electrique":False,                  ##Fait
                         "laser_ralentissant":False,                ##Fait
                         "laser_perforant":False                    ##Fait
                         },
                "roquette":{"roquette_shrapnel":False,              ##Fait
                            "roquette_enflammee":False,             ##Fait
                            "roquette_ricochet":False               ##Fait
                            },
                "mine":{"mine_empoisonnee":False,                   ##Fait
                        "mine_fragmentation":False,                 ##Fait
                        "mine_double_vie":False                     ##Fait
                        },
                "aura":{"aura_surpopulation":False,                 ##Fait
                        "aura_affaiblissante":False,                ##Fait
                        "aura_rage":False                           ##Fait
                        },
                "tourelle":{"tourelle_explosive":False,             ##Fait
                            "tourelle_aoe_defensive":False,         ##Fait
                            "tourelle_leurre":False                 ##Fait
                            },
                }
#------------------Upgrades stats laser------------------------------------------
dico_upgrades_laser={
                "cadence_de_tir":0,
                "degat":0,
                "portee":0,
                }  
#------------------Upgrades stats roquette------------------------------------------   
dico_upgrades_roquette={
                "cadence_de_tir":0,
                "degat":0,
                "portee":0,
                "rayon_aoe":0,
                }
#------------------Upgrades stats mine------------------------------------------
dico_upgrades_mine={
                "cadence_de_tir":0,
                "degat":0,
                "rayon_aoe":0,
                "duree_aoe":0,
                "duree_vie":0
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
                "portee":0
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

MAX_STAT_UPGRADE = {
    "stats": {"esquive": 10},
    "laser": {"cadence_de_tir": 8},
    "roquette": {"cadence_de_tir": 19},
    "mine": {"cadence_de_tir": 9},
    "aura": {"cadence_de_tir": 8},
    "tourelle": {"cadence_de_tir": 20},
}

def random_upgrade(nb_upgrades=3, armes_possedees=["stats", "laser"]):
    liste_upgrades = []
    type_upgrade = random.randint(0, 10)

    if type_upgrade ==0:   ##pour les upgrades uniques
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
                if arme in MAX_STAT_UPGRADE and upgrade_nom in MAX_STAT_UPGRADE[arme]:
                    if master_dico[arme][upgrade_nom] >= MAX_STAT_UPGRADE[arme][upgrade_nom]:
                        continue
                options_stats.append((arme, upgrade_nom))
    
    nb_a_piger = min(nb_upgrades, len(options_stats))
    liste_upgrades = random.sample(options_stats, nb_a_piger)   ##sample c mieux, ca evite les doubles

    return liste_upgrades

def afficher_upgrades(screen, width, height, nb_upgrades, armes_possedees, font, nouvelle_arme=False):
    if nouvelle_arme:
        # toutes les armes possibles
        toutes_armes = ["laser","roquette","mine","aura","tourelle"]

        # armes non possédées
        armes_disponibles = [arme for arme in toutes_armes if arme not in armes_possedees]

        # on en propose 3
        nb_a_piger = min(3, len(armes_disponibles))
        armes_choix = random.sample(armes_disponibles, nb_a_piger)

        # format compatible avec ton UI
        liste_upgrades = [(arme, "nouvelle arme") for arme in armes_choix]

    else:
        liste_upgrades = random_upgrade(nb_upgrades=nb_upgrades, armes_possedees=armes_possedees)

    nb_u = len(liste_upgrades)

    # Marges relatives à la taille de l'écran
    marge_ecran = width * 0.05  # 5% de la largeur de l'écran
    marge_entre = width * 0.02   # 2% de la largeur de l'écran

    # Taille des boutons
    r_width = (width - 2*marge_ecran - (nb_u-1)*marge_entre) / nb_u
    r_height = height * 0.6  # 60% de la hauteur de l'écran

    while True:
        screen.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Calcul de l'index du bouton cliqué
                index_clique = int((event.pos[0] - marge_ecran) // (r_width + marge_entre))
                
                if 0 <= index_clique < nb_u:
                    arme_choisie, stat_choisie = liste_upgrades[index_clique]
                    
                    #C'est une nouvelle arme (on l'ajoute à la liste du joueur)
                    if stat_choisie == "nouvelle arme":
                        armes_possedees.append(arme_choisie)
                    
                    #C'est une upgrade unique (True/False)
                    elif arme_choisie in dico_upgrades_uniques:
                         dico_upgrades_uniques[arme_choisie][stat_choisie] = True
                    
                    #C'est une upgrade de stat classique
                    elif arme_choisie in master_dico:
                        master_dico[arme_choisie][stat_choisie] += 1
                    
                    return liste_upgrades[index_clique]
                    

        souris_x, souris_y = pygame.mouse.get_pos()

        # Dessin des boutons
        for i in range(nb_u):
            x = marge_ecran + i * (r_width + marge_entre)
            y = (height - r_height) / 2
            rect = pygame.Rect(x, y, r_width, r_height)

            # Effet au survol
            scale = 1.05 if rect.collidepoint(souris_x, souris_y) else 1.0  # grossissement 5% pour quand tu le survole comme ca ca fait "style"
            largeur_scaled = rect.width * scale
            hauteur_scaled = rect.height * scale
            x_scaled = rect.centerx - largeur_scaled / 2
            y_scaled = rect.centery - hauteur_scaled / 2
            rect_scaled = pygame.Rect(x_scaled, y_scaled, largeur_scaled, hauteur_scaled)

            # Couleur au hover
            arme, stat = liste_upgrades[i]

            est_unique = (arme in dico_upgrades_uniques and stat in dico_upgrades_uniques[arme])

            if est_unique:
                couleur = (255, 255, 0) if scale > 1 else (255, 0, 0)  # jaune hover, rouge normal
            else:
                couleur = (0, 255, 0) if scale > 1 else (0, 200, 0)

            # Rectangle avec coins arrondis
            pygame.draw.rect(screen, couleur, rect_scaled, border_radius=int(width*0.015))
            pygame.draw.rect(screen, (255, 255, 255), rect_scaled, 3, border_radius=int(width*0.015))

            # Texte centré
            nom_arme, nom_stat = liste_upgrades[i]
            txt_arme = font.render(str(nom_arme).upper(), True, (255, 255, 255))
            txt_stat = font.render(str(nom_stat), True, (200, 255, 200))
            centro_x = rect_scaled.centerx
            screen.blit(txt_arme, txt_arme.get_rect(center=(centro_x, rect_scaled.y + rect_scaled.height/3)))
            screen.blit(txt_stat, txt_stat.get_rect(center=(centro_x, rect_scaled.y + 2*rect_scaled.height/3)))

        pygame.display.flip()




def reset_upgrades():

    for k in dico_upgrades_stats:
        dico_upgrades_stats[k] = 0

    for d in [
        dico_upgrades_laser,
        dico_upgrades_roquette,
        dico_upgrades_mine,
        dico_upgrades_aura,
        dico_upgrades_tourelle
    ]:
        for k in d:
            d[k] = 0

    for arme in dico_upgrades_uniques:
        for k in dico_upgrades_uniques[arme]:
            dico_upgrades_uniques[arme][k] = False



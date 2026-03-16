import json
import os
from random_module import *
from Main_game import *

dico_all = {
    "dico_upgrades_stats":dico_upgrades_stats,
    "dico_upgrades_uniques":dico_upgrades_uniques,
    "dico_upgrades_laser":dico_upgrades_laser,
    "dico_upgrades_roquette":dico_upgrades_roquette,
    "dico_upgrades_mine":dico_upgrades_mine,
    "dico_upgrades_aura":dico_upgrades_aura,
    "dico_upgrades_tourelle":dico_upgrades_tourelle,
    "armes_possedees":armes_possedees
    }


def sauvegarder_jeu():
    with open("save.json", "w") as fichier:
        json.dump(dico_all, fichier, indent=4)
    print("Jeu sauvegardé !")


def charger_jeu():
    global pv_joueur, xp, niveau
    global player_x, player_y
    global nombre_journees, duree_journee
    global type_armes

    if os.path.exists("save.json"):
        with open("save.json", "r") as fichier:
            data = json.load(fichier)

        pv_joueur = data.get("pv_joueur", 100)
        xp = data.get("xp", 0)
        niveau = data.get("niveau", 1)

        # Assure-toi que width et height sont définis globalement quelque part avant cet appel
        player_x = data.get("player_x", width // 2)
        player_y = data.get("player_y", height // 2)

        nombre_journees = data.get("nombre_journees", 0)
        duree_journee = data.get("duree_journee", 0)

        type_armes = data.get("armes", [])

        print("Sauvegarde chargée !")
    else:
        print("Aucune sauvegarde trouvée.")



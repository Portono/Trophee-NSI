import json
import os
from paths import data_path
from random_module import*


SAVE_FILE = "save.json"


def sauvegarder_jeu(dico_upgrades_stats,dico_upgrades_uniques,dico_upgrades_laser,dico_upgrades_roquette,dico_upgrades_mine,dico_upgrades_aura,dico_upgrades_tourelle,armes_possedees):

    with open(data_path(SAVE_FILE), "w") as fichier:
        for dico,settings in [("dico_upgrades_stats:",dico_upgrades_stats),("dico_upgrades_uniques:",dico_upgrades_uniques),("dico_upgrades_laser:",dico_upgrades_laser),("dico_upgrades_roquette:",dico_upgrades_roquette),("dico_upgrades_mine:",dico_upgrades_mine),("dico_upgrades_aura:",dico_upgrades_aura),("dico_upgrades_tourelle:",dico_upgrades_tourelle),armes_possedees]:
            json.dump((dico+settings), fichier, indent=4)
    
    fichier.close()
    print("Jeu sauvegardé !")


def charger_jeu():

    try:
        with open(data_path(SAVE_FILE), "r") as fichier:
            data = json.load(fichier)

        Main_game.pv_joueur = data.get("pv_joueur", 100)
        Main_game.xp = data.get("xp", 0)


        Main_game.nombre_journees = data.get("nombre_journees", 0)

        Main_game.armes_possedees = data.get("armes", [])

        Main_game.dico_upgrades_stats = data.get("dico_upgrades_stats", {})
        Main_game.dico_upgrades_uniques = data.get("dico_upgrades_uniques", {})
        Main_game.dico_upgrades_laser = data.get("dico_upgrades_laser", {})
        Main_game.dico_upgrades_roquette = data.get("dico_upgrades_roquette", {})
        Main_game.dico_upgrades_mine = data.get("dico_upgrades_mine", {})
        Main_game.dico_upgrades_aura = data.get("dico_upgrades_aura", {})
        Main_game.dico_upgrades_tourelle = data.get("dico_upgrades_tourelle", {})

        print("Sauvegarde chargée !")
        fichier.close()

    except:
        print("Aucune sauvegarde trouvée.")
    

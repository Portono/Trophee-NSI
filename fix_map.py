import json

# Remplace par le nom exact de ton fichier
filename = 'Map_Jeu.json' 

def fixer_map(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # On parcourt tous les calques (layers)
        for layer in data.get("layers", []):
            # On cible uniquement "Map" et "Walls"
            if layer["name"] in ["Map", "Walls"]:
                tiles = layer.get("tiles", [])
                
                if not tiles:
                    continue

                # 1. On trouve le décalage (offset) pour que le mini soit 0
                min_x = min(t["x"] for t in tiles)
                min_y = min(t["y"] for t in tiles)
                
                print(f"Correction du calque '{layer['name']}':")
                print(f"  - Ancien départ: ({min_x}, {min_y}) -> Nouveau départ: (0, 0)")

                # 2. On applique la correction à chaque tile du calque
                for tile in tiles:
                    tile["x"] -= min_x
                    tile["y"] -= min_y
                    tile["id"] = "0" # On force l'ID à 0 comme à l'origine

        # Sauvegarde du résultat
        output_name = 'Main_game_FIXED.json'
        with open(output_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"\nSuccès ! Fichier corrigé enregistré sous : {output_name}")

    except Exception as e:
        print(f"Erreur : {e}")

# Lancer le script
fixer_map(filename)

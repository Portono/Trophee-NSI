import pygame
import random
import math

def obtenir_upgrade(stat_chance, inventaire_joueur):
    upgrades=["hp","vitesse","portee","vitesse balles","taille balles","regen","degat","cadence","multishot"]

    poids_calcule=[]

    for i,nom in enumerate(upgrades):
        position_courbe=(i+1)/len(upgrades)
        poids_base=position_courbe**(4.0/stat_chance)

        multiplicateur=max(0,1.0-(inventaire_joueur.get(nom,0)*0.01))

        poids_final=poids_base*multiplicateur
        poids_calcule.append(poids_final)
    if sum(poids_calcule)<=0:
        poids_calcule=[]
        for i in range(len(upgrades)):
            position_courbe=(i+1)/len(upgrades)
            poids_calcule.append(position_courbe**(4.0/stat_chance))
            
    selection=random.choices(upgrades,weights=poids_calcule,k=1)[0]

    return selection

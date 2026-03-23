import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from paths import data_path
from save_load import *

pygame.init()

#Dimensions de la fenetre
#acquisition de la resolution de l'ecran
monitor_info=pygame.display.Info()
monitor_width=monitor_info.current_w   #=valeur de test (temporaire)
monitor_height=monitor_info.current_h  #=valeur de test (temporaire)
width=monitor_width
height=monitor_height

#Variables de gestion du mode plein ecran
fullscreen_change=False  #True si bouton Fulscreen appuye Temporaire, doit etre False au debut mais peut varier selon les parametres sauvegardes
fullscreen=True    #Etat de plein ecran, doit etre True au debut mais peut varier selon les parametres sauvegardes
resolution_change=True  #True si resolution changee doit etre True au debut pour tout initialiser mais peut varier selon les parametres sauvegardes
user_width_input="Largeur"  #Variable pour stocker l'input utilisateur pour la largeur
width_input_toggle=False  #Variable pour activer/desactiver l'input de la largeur
user_height_input="Hauteur"  #Variable pour stocker l'input utilisateur pour la hauteur
height_input_toggle=False  #Variable pour activer/desactiver l'input de la hauteur

#predefinission des couleurs utiles
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
orange=(255,165,0)
gray=(128,128,128)

#Predeffinission de la police et de la couleur des boutons
menu_font=pygame.font.Font(data_path("font.ttf"), int(height*0.05)) ##Definition de la police et de la taille du texte des boutons
button_color=black
hover_color=gray
text_color=orange
height_button_text="Hauteur"
width_button_text="Largeur"
#definition des dimensions des boutons
button_width=int(width*0.25)
button_height=int(height*0.1)

#Definition des boutons
play_button_rect=pygame.Rect(0,0,button_width,button_height)
settings_button_rect=pygame.Rect(0,0,button_width,button_height)
quit_button_rect=pygame.Rect(0,0,button_width,button_height)
fullscreen_button_rect=pygame.Rect(0, 0, button_width, button_height)
goback_button_rect=pygame.Rect(0, 0, button_width, button_height)
input_width_rect=pygame.Rect(0, 0, button_width, button_height)
input_height_rect=pygame.Rect(0, 0, button_width, button_height)
astropedia_button_rect=pygame.Rect(0,0,button_width,button_height)
astropedia_back_button_rect=pygame.Rect(0,0,button_width,button_height)
charger_button_rect=pygame.Rect(0,0,button_width,button_height)
#Definition de texte des boutons
height_button_text="Hauteur"
width_button_text="Largeur"
#Ajout du logo + redissionnement adaptatif a la resolution choisie
logo_import=pygame.image.load(data_path("logo_champ_de_mars.png"))
logo_import_width=logo_import.get_width()
logo_import_height=logo_import.get_height()
logo=pygame.transform.scale(logo_import,(width,int(logo_import_height/logo_import_width*width)))

#astrowantsyou
AstroWantsYou=pygame.image.load(data_path("AstroWantsYou.png"))
AstroWantsYou=pygame.transform.scale(AstroWantsYou,(int(AstroWantsYou.get_width()/AstroWantsYou.get_height()*height),height))
#fond
background_import=[]
backgrounds_flou_import=[]
for i in range(1,7):
    img = pygame.image.load(data_path(f"Wallpaper({i}).png"))
    background_import.append(img)

backgrounds_flou_import=[]
for i in range(1,7):
    img = pygame.image.load(data_path(f"Wallpaper_flou({i}).png"))
    backgrounds_flou_import.append(img)

backgrounds=[]
backgrounds_flou=[]

for img in background_import:
    normal = pygame.transform.smoothscale(img,(width,height))
    backgrounds.append(normal)

for img in backgrounds_flou_import:
    blur = pygame.transform.smoothscale(img,(width,height))
    backgrounds_flou.append(blur)

#Astropedia
astropedia_images=[]
for i in range(1, 6):
    img = pygame.image.load(data_path(f"Astropedia({i}).png"))
    img = pygame.transform.smoothscale(img, (width, height))
    astropedia_images.append(img)
astropedia_index = 0

#Game Icon
game_icon=pygame.image.load(data_path("ChampDeMarsLogo.png"))
image_index=0
image_delay=200
dernier_frame=pygame.time.get_ticks()

#on définit les variables pour les changement de scène du menu
menu_main="main"
menu_settings="settings"
menu_astropedia="astropedia"
current_menu=menu_main
play=False  ##Variable pour lancer le jeu
sound_volume=50
sound_slider=None

def refresh_ui():
    """
    Cette fonction sert a rafraichir l'interface utilisateur en repositionnant les boutons et le logo en recalculant leurs positions et leurs tailles car leur position n'est calcule seulement lors de leur creation
    """
    global play_button_rect, settings_button_rect, quit_button_rect, logo, menu_font, fullscreen_button_rect, goback_button_rect, input_width_rect,input_height_rect,screen,astropedia_back_button_rect,sound_slider,sound_volume,astropedia_button_rect,charger_button_rect,astropedia_images
    monitor_info=pygame.display.Info()
    monitor_width=monitor_info.current_w
    monitor_height=monitor_info.current_h
    if fullscreen==True:
        screen=pygame.display.set_mode((width,height), pygame.FULLSCREEN)
    elif fullscreen==False:
        screen=pygame.display.set_mode((width,height))
    #Repositionnement du logo
    logo=pygame.transform.smoothscale(logo_import,(width,int(logo_import_height/logo_import_width*width)))
    #Repositionnement des boutons
    button_width=int(width*0.25)
    button_height=int(height*0.1)
    ##Bouton Play
    play_button_rect=pygame.Rect(0,0,button_width,button_height)
    play_button_rect.center=(width//2, height//3.8)
    ##Bouton Settings
    settings_button_rect=pygame.Rect(0,0,button_width,button_height)
    settings_button_rect.center=(width//2, height*2//3.8)
    ##Bouton Quit
    quit_button_rect=pygame.Rect(0,0,button_width,button_height)
    quit_button_rect.center=(width//2, height*3//3.8)
    ##Bouton Settings-Fullscreen
    fullscreen_button_rect=pygame.Rect(0, 0, button_width/1.25, button_height/1.25)
    fullscreen_button_rect.center = (width // 2, height*2 // 3.8)
    ##Bouton Settings-Go Back
    goback_button_rect=pygame.Rect(0, 0, button_width, button_height)
    goback_button_rect.center = (width//2, height*3//3.8)
    ##Bouton Settings-Input Width
    input_width_rect=pygame.Rect(0, 0, button_width/1.5, button_height/1.5)
    input_width_rect.center = (width // 3, height // 3)   
    ##Bouton Settings-Input Height
    input_height_rect=pygame.Rect(0, 0, button_width/1.5, button_height/1.5)
    input_height_rect.center = (width // 1.5, height // 3)
    ##Bouton Astropedia
    astropedia_button_rect=pygame.Rect(0,0,button_width,button_height)
    astropedia_button_rect.bottomleft=(0,height)
    ##Bouton retour astropedia
    astropedia_back_button_rect=pygame.Rect(0,0,button_width,button_height)
    astropedia_back_button_rect.bottomright=(width/2+button_width/2,height)
    ##Taille de la police
    menu_font=pygame.font.Font(data_path("font.ttf"), int(height*0.05))
    ##Slider de son
    sound_slider=Slider(screen,int(width*0.85),int(height*0.25),int(width*0.02),int(height*0.45),min=0,max=100,step=1,initial=sound_volume,vertical=True,colour=hover_color,valueColour=orange)
    ##Taille de AstroWantsYou
    AstroWantsYou=pygame.image.load(data_path("AstroWantsYou.png"))
    AstroWantsYou=pygame.transform.smoothscale(AstroWantsYou,(int(AstroWantsYou.get_width()/AstroWantsYou.get_height()*height),height))
    ##Bouton Charger
    charger_button_rect=pygame.Rect(0,0,button_width,button_height)
    charger_button_rect.center=(width//2, height*1.5//3.8)
    ##Astropedia
    astropedia_images=[]
    for i in range(1, 6):
        img = pygame.image.load(data_path(f"Astropedia({i}).png"))
        img = pygame.transform.smoothscale(img, (width, height))
        astropedia_images.append(img)
    ##Taille de background
    background_import=[]
    backgrounds_flou_import=[]
    for i in range(1,7):
        img = pygame.image.load(data_path(f"Wallpaper({i}).png"))
        background_import.append(img)

    backgrounds_flou_import=[]
    for i in range(1,7):
        img = pygame.image.load(data_path(f"Wallpaper_flou({i}).png"))
        backgrounds_flou_import.append(img)

    backgrounds=[]
    backgrounds_flou=[]

    for img in background_import:
        normal = pygame.transform.smoothscale(img,(width,height))
        backgrounds.append(normal)

    for img in backgrounds_flou_import:
        blur = pygame.transform.smoothscale(img,(width,height))
        backgrounds_flou.append(blur)

def afficher_menu(armes_possedees=None):
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption('Champ de Mars')
    refresh_ui()
    return boucle_menu(armes_possedees=armes_possedees)

def boucle_menu(pause=False, armes_possedees=None, nombre_journees=0):
    global current_menu, play, fullscreen, fullscreen_change, resolution_change, width, height, user_width_input, width_input_toggle, user_height_input, height_input_toggle,screen,width_button_text,height_button_text,dernier_frame,image_delay,image_index,sound_slider,sound_volume,astropedia_index
    play=False
    pygame.mixer.music.load(data_path("Mainmenu.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(sound_volume/100)
    #Recuperation de la position de la souris
    #Raffraichissement du logo sur l'ecran
    while not play:
        maintenant=pygame.time.get_ticks()


        if maintenant-dernier_frame>image_delay:
            image_index=(image_index+1)%len(backgrounds)
            dernier_frame=maintenant

        mouse_pos=pygame.mouse.get_pos()
        events=pygame.event.get()
        #Quitter le jeu
        for event in events:    ##Recuperation des evenements
            if event.type == pygame.QUIT:   ##Si on clique sur la croix
                pygame.quit()       ##Quitte pygame
                exit()      ##Quitte le programme
            if event.type == pygame.MOUSEBUTTONDOWN:   ##Si un bouton de la souris est appuye 
                #   Main Menu   #
                if current_menu==menu_main: ##Si on est dans le menu principal
                    width_input_toggle,height_input_toggle=False,False
                    if play_button_rect.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        screen.fill(black)
                        screen.blit(AstroWantsYou, AstroWantsYou.get_rect(center=(width//2,height//2)))
                        pygame.display.flip()
                        return {"width": width, "height": height, "fullscreen": fullscreen, "play": True,"sound_volume":sound_volume,"charger":False}
                    if not pause and charger_button_rect.collidepoint(mouse_pos):
                        if save_existe():
                            pygame.mixer.music.stop()
                            screen.fill(black)
                            screen.blit(AstroWantsYou, AstroWantsYou.get_rect(center=(width//2,height//2)))
                            pygame.display.flip()
                            return {"width": width, "height": height, "fullscreen": fullscreen, "play": True, "sound_volume": sound_volume,"charger":True}
                        # sinon on ne fait rien (ou on affiche un message)
                    if settings_button_rect.collidepoint(mouse_pos):   ##Si le bouton Settings est appuye
                        current_menu=menu_settings
                    if quit_button_rect.collidepoint(mouse_pos):
                        if pause and armes_possedees is not None:
                            sauvegarder_jeu(armes_possedees, nombre_journees)
                        pygame.quit()       ##Quitte pygame
                        exit()      ##Quitte le programme
                    if astropedia_button_rect.collidepoint(mouse_pos):
                        current_menu=menu_astropedia
                #   Settings Menu   #
                elif current_menu==menu_settings: ##Si on est dans le menu des parametres
                    
                    if fullscreen_button_rect.collidepoint(mouse_pos):   ##Si le bouton Fullscreen est appuye
                        fullscreen_change=True
                        fullscreen=not fullscreen
                    if goback_button_rect.collidepoint(mouse_pos):   ##Si le bouton Go Back est appuye
                        current_menu=menu_main ##on retourne au menu principal
                    if input_width_rect.collidepoint(mouse_pos):   ##Si le bouton de la largeur est appuye
                        width_input_toggle=True
                        width_button_text="Largeur"
                        user_width_input=""
                    if input_height_rect.collidepoint(mouse_pos):   ##Si le bouton de la hauteur est appuye
                        height_input_toggle=True
                        height_button_text="Hauteur"
                        user_height_input=""
                elif current_menu==menu_astropedia:
                    if astropedia_back_button_rect.collidepoint(mouse_pos):
                        current_menu=menu_main
            ##Changement de la resolution via l'input utilisateur
            if event.type==pygame.KEYDOWN and current_menu==menu_settings and width_input_toggle==True:   ##Si une touche est appuye dans le menu des parametres
                if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:   ##Si la touche entree est appuyee
                    try:
                        width=int(user_width_input)   ##Conversion de l'input utilisateur en entier
                        resolution_change=True
                        width_input_toggle=False
                        user_width_input=width_button_text  ##Reset de l'input utilisateur
                    except ValueError:
                        pass
                elif event.key==pygame.K_BACKSPACE:   ##Si la touche retour est appuyee
                    user_width_input=user_width_input[:-1]   ##Supprime le dernier caractere de l'input utilisateur
                else:
                    user_width_input+=event.unicode   ##Ajoute le caractere appuye a l'input utilisateur

            if event.type == pygame.KEYDOWN and current_menu==menu_settings and height_input_toggle==True:   ##Si une touche est appuye dans le menu des parametres
                if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:   ##Si la touche entree est appuyee
                    try:
                        height=int(user_height_input)   ##Conversion de l'input utilisateur en entier
                        resolution_change=True
                        height_input_toggle=False
                        user_height_input=height_button_text  ##Reset de l'input utilisateure
                    except ValueError:
                        pass
                elif event.key==pygame.K_BACKSPACE:   ##Si la touche retour est appuyee
                    user_height_input=user_height_input[:-1]   ##Supprime le dernier caractere de l'input utilisateur
                else:
                    user_height_input+=event.unicode   ##Ajoute le caractere appuye a l'input utilisateur
            if event.type == pygame.KEYDOWN and current_menu==menu_astropedia:
                if event.key == pygame.K_RIGHT:
                    astropedia_index = (astropedia_index + 1) % len(astropedia_images)
                elif event.key == pygame.K_LEFT:
                    astropedia_index = (astropedia_index - 1) % len(astropedia_images)

        #dessine les boutons et le texte
        if current_menu==menu_main: ##les boutons dans le menu principal
            screen.blit(backgrounds[image_index],(0,0))
            screen.blit(logo,(0,0))     ##Affichage du logo en haut de l'ecran
            user_width_input=width_button_text
            user_height_input=height_button_text
            if pause:
                boutons = [(play_button_rect, "Reprendre"), (settings_button_rect, "Parametres"), (quit_button_rect, "Quitter"),(astropedia_button_rect, "Astropedia")]
            else:
                boutons = [(play_button_rect, "Nouvelle partie"), (charger_button_rect, "Charger"), (settings_button_rect, "Parametres"), (quit_button_rect, "Quitter"), (astropedia_button_rect, "Astropedia")]

            for rect, texte in boutons:
                if rect == charger_button_rect and not save_existe():
                    couleur = (50, 50, 50)  # gris foncé = désactivé
                elif rect.collidepoint(mouse_pos):
                    couleur = hover_color
                else:
                    couleur = black
                pygame.draw.rect(screen, couleur, rect, border_radius=100)
                texte_surface=menu_font.render(texte,True,orange)    ##Creation du texte
                texte_rect=texte_surface.get_rect(center=rect.center)   ##Centrage du texte
                screen.blit(texte_surface, texte_rect)  ##Affichage du texte
                if save_existe():
                    score = charger_score()
                    texte_score = menu_font.render(f"Journees : {score}", True, orange)
                    texte_score_rect = texte_score.get_rect(center=(width//2+button_width, height*1.5//3.8))
                    screen.blit(texte_score, texte_score_rect)
        if current_menu==menu_settings: #les boutons dans le menu des parametres
            #Texte de la resolution actuelle
            screen.blit(backgrounds_flou[image_index],(0,0))
            resolution_texte=menu_font.render(f"Resolution: {width}x{height}",True,orange) if pause==False else menu_font.render("Il est recommande de changer la resolution dans le menu principal",True,red)  ##Creation du texte de la resolution
            resolution_texte_rect=resolution_texte.get_rect(center=(width//2, height//5))   ##Centrage du texte de la resolution
            screen.blit(resolution_texte, resolution_texte_rect)  ##Affichage du texte
            for rect,texte in [(fullscreen_button_rect,"Plein ecran"),(goback_button_rect,"Retour"),(input_width_rect,user_width_input),(input_height_rect,user_height_input)]:
                if rect.collidepoint(mouse_pos):    ##Si la souris est au dessus du bouton
                    button_color=hover_color    ##Change la couleur du bouton
                else:
                    button_color=black
                pygame.draw.rect(screen,button_color, rect,border_radius=100)   ##Dessin du bouton
                texte_surface=menu_font.render(texte,True,orange)    ##Creation du texte
                texte_rect=texte_surface.get_rect(center=rect.center)   ##Centrage du texte
                screen.blit(texte_surface, texte_rect)  ##Affichage du texte

            pygame_widgets.update(events)
            sound_volume=int(sound_slider.getValue())
            pygame.mixer.music.set_volume(sound_volume/100)
            sound_text=menu_font.render(f"Volume : {sound_volume}",True,orange)
            sound_text_rect=sound_text.get_rect(center=(int(width*0.86), int(height*0.18)))
            screen.blit(sound_text,sound_text_rect)

        if current_menu == menu_astropedia:
            # Affiche uniquement l'image
            screen.blit(astropedia_images[astropedia_index], (0, 0))

            # Bouton retour
            button_color = hover_color if astropedia_back_button_rect.collidepoint(mouse_pos) else black
            pygame.draw.rect(screen, button_color, astropedia_back_button_rect, border_radius=100)

            retour_surface = menu_font.render("Retour", True, orange)
            retour_rect = retour_surface.get_rect(center=astropedia_back_button_rect.center)
            screen.blit(retour_surface, retour_rect)
            

        #Toggle du fullscreen
        if fullscreen_change==True or resolution_change==True:
            fullscreen_change=False
            resolution_change=False
            refresh_ui()
        pygame.display.flip()
    return {"width": width, "height": height, "fullscreen": fullscreen, "play": play,"sound_volume":sound_volume}









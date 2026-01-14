import pygame

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
menu_font=pygame.font.Font("font.ttf", int(height*0.05)) ##Definition de la police et de la taille du texte des boutons
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
#Definition de texte des boutons
height_button_text="Hauteur"
width_button_text="Largeur"
#Creation de la fenetre
screen=pygame.display.set_mode((width,height), pygame.FULLSCREEN)   ##Definition de la fenetre avec la resolution
pygame.display.set_caption("Champ de Mars") ##Titre de la fenetre

#Ajout du logo + redissionnement adaptatif a la resolution choisie
logo_import=pygame.image.load("logo_champ_de_mars.png")
logo_import_width=logo_import.get_width()
logo_import_height=logo_import.get_height()
logo=pygame.transform.smoothscale(logo_import,(width,int(logo_import_height/logo_import_width*width)))
screen.fill(white)

#on définit les variables pour les changement de scène du menu
menu_main="main"
menu_settings="settings"
current_menu=menu_main
play=False  ##Variable pour lancer le jeu

pygame.mixer.music.load("Mainmenu.mp3")
pygame.mixer.music.play()

def refresh_ui():
    """
    Cette fonction sert a rafraichir l'interface utilisateur en repositionnant les boutons et le logo en recalculant leurs positions et leurs tailles car leur position n'est calcule seulement lors de leur creation
    """
    global play_button_rect, settings_button_rect, quit_button_rect, logo, menu_font, fullscreen_button_rect, goback_button_rect, input_width_rect,input_height_rect
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
    ##Taille de la police
    menu_font=pygame.font.Font("font.ttf", int(height*0.05))

while play!=True:   ##Boucle principale du menu
    #Recuperation de la position de la souris
    mouse_pos=pygame.mouse.get_pos()
    #Raffraichissement du logo sur l'ecran
    screen.fill(white)  ##Fond blanc
    screen.blit(logo,(0,0))     ##Affichage du logo en haut de l'ecran

    #Quitter le jeu
    for event in pygame.event.get():    ##Recuperation des evenements
        if event.type == pygame.QUIT:   ##Si on clique sur la croix
            pygame.quit()       ##Quitte pygame
            exit()      ##Quitte le programme
        if event.type == pygame.MOUSEBUTTONDOWN:   ##Si un bouton de la souris est appuye 
            #   Main Menu   #
            if current_menu==menu_main: ##Si on est dans le menu principal
                width_input_toggle,height_input_toggle=False,False
                if play_button_rect.collidepoint(mouse_pos):   ##Si le bouton Play est appuye
                    play=True
                if settings_button_rect.collidepoint(mouse_pos):   ##Si le bouton Settings est appuye
                    current_menu=menu_settings
                if quit_button_rect.collidepoint(mouse_pos):   ##Si le bouton Quit est appuye
                    pygame.quit()       ##Quitte pygame
                    exit()      ##Quitte le programme
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

        ##Changement de la resolution via l'input utilisateur
        if event.type==pygame.KEYDOWN and current_menu==menu_settings and width_input_toggle==True:   ##Si une touche est appuye dans le menu des parametres
            if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:   ##Si la touche entree est appuyee
                try:
                    width=int(user_width_input)   ##Conversion de l'input utilisateur en entier
                    resolution_change=True
                    width_input_toggle=False
                    user_width_input=width_button_text  ##Reset de l'input utilisateur
                except ValueError:
                    print("Invalid width input")   ##Message d'erreur pour input invalide
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
                    user_height_input=height_button_text  ##Reset de l'input utilisateur
                except ValueError:
                    print("Invalid height input")   ##Message d'erreur pour input invalide
            elif event.key==pygame.K_BACKSPACE:   ##Si la touche retour est appuyee
                user_height_input=user_height_input[:-1]   ##Supprime le dernier caractere de l'input utilisateur
            else:
                user_height_input+=event.unicode   ##Ajoute le caractere appuye a l'input utilisateur

    #dessine les boutons et le texte
    if current_menu==menu_main: ##les boutons dans le menu principal
        user_width_input=width_button_text
        user_height_input=height_button_text
        for rect,texte in [(play_button_rect,"Play"),(settings_button_rect,"Parametres"),(quit_button_rect,"Quitter")]:
            if rect.collidepoint(mouse_pos):    ##Si la souris est au dessus du bouton
                button_color=hover_color    ##Change la couleur du bouton
            else:
                button_color=black
            pygame.draw.rect(screen,button_color, rect, border_radius=30)   ##Dessin du bouton
            texte_surface=menu_font.render(texte,True,orange)    ##Creation du texte
            texte_rect=texte_surface.get_rect(center=rect.center)   ##Centrage du texte
            screen.blit(texte_surface, texte_rect)  ##Affichage du texte
    if current_menu==menu_settings: #les boutons dans le menu des parametres
        #Texte de la resolution actuelle
        resolution_texte=menu_font.render(f"Resolution: {width}x{height}",True,black)  ##Creation du texte de la resolution
        resolution_texte_rect=resolution_texte.get_rect(center=(width//2, height//5))   ##Centrage du texte de la resolution
        screen.blit(resolution_texte, resolution_texte_rect)  ##Affichage du texte
        for rect,texte in [(fullscreen_button_rect,"Plein ecran"),(goback_button_rect,"Retour"),(input_width_rect,user_width_input),(input_height_rect,user_height_input)]:
            if rect.collidepoint(mouse_pos):    ##Si la souris est au dessus du bouton
                button_color=hover_color    ##Change la couleur du bouton
            else:
                button_color=black
            pygame.draw.rect(screen,button_color, rect,border_radius=30)   ##Dessin du bouton
            texte_surface=menu_font.render(texte,True,orange)    ##Creation du texte
            texte_rect=texte_surface.get_rect(center=rect.center)   ##Centrage du texte
            screen.blit(texte_surface, texte_rect)  ##Affichage du texte

    #Toggle du fullscreen
    if fullscreen_change==True or resolution_change==True:
        fullscreen_change=False
        resolution_change=False
        refresh_ui()
    pygame.display.flip()


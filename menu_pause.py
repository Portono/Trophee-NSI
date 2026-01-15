while running: 
       if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                        pause = not pause

        if pause and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

        if resume_rect.collidepoint(mouse_pos):
               pause = False  # on reprend le jeu

        if settings_rect.collidepoint(mouse_pos):
               print("Paramètres cliqué !")  #Vous pourrez codez un menu paramètre, ou juste copié-collé celui qu'on a déjà
        if quit_rect.collidepoint(mouse_pos):
               pygame.quit()
               sys.exit()

  
    screen.fill((0, 0, 0))

       if pause:
              resume_rect = pygame.rect(100, 200, 200, 80)       #j'ai mis des valeurs aléatoires pour le positionnement
              settings_rect = pygame.rect(500, 150, 220, 120)    #idem
              quit_rect = pygame.rect(100, 300, 200, 80)         #idem

        #là j'ai codé leurs format
              pygame.draw.rect(screen, (50, 150, 50), resume_rect)
              pygame.draw.rect(screen, (150, 150, 50), settings_rect)
              pygame.draw.rect(screen, (150, 50, 50), quit_rect)

      #ça c'est chat gpt jusqu'à la fin
              screen.blit(font.render("Reprendre", True, (255,255,255)), (110, 210))
              screen.blit(font.render("Paramètres", True, (255,255,255)), (505, 180))
              screen.blit(font.render("Quitter", True, (255,255,255)), (125, 310))

    else:
        # Ton code de jeu ici (déplacements, logique, etc.)
        screen.fill((30, 30, 30))
        game_text = font.render("Jeu en cours... (appuie P)", True, (255,255,255))
        screen.blit(game_text, (150, 50))

    pygame.display.flip()

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)
LIGHT_BLUE = (100, 150, 255)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Home Screen")

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Font
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = button_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def main():
    # Create buttons
    play_button = Button(250, 250, 300, 80, "Play", LIGHT_BLUE, (150, 200, 255))
    settings_button = Button(250, 370, 300, 80, "Settings", LIGHT_BLUE, (150, 200, 255))
    quit_button = Button(250, 490, 300, 80, "Quit", LIGHT_BLUE, (150, 200, 255))
    
    buttons = [play_button, settings_button, quit_button]
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_pos):
                    print("Play button clicked!")
                elif settings_button.is_clicked(mouse_pos):
                    print("Settings button clicked!")
                elif quit_button.is_clicked(mouse_pos):
                    running = False
        
        # Update button hover states
        for button in buttons:
            button.update(mouse_pos)
        
        # Draw
        screen.fill(WHITE)
        
        # Draw background gradient effect (simple version)
        pygame.draw.rect(screen, BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        
        # Draw title
        title_text = title_font.render("Welcome", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = small_font.render("to My Game", True, BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

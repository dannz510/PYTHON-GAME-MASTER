import pygame
from ....utils import QuitGame
import random

# A simple class for background stars
class BackgroundStar:
    def __init__(self, screen_width, screen_height):
        self.x = random.randrange(0, screen_width)
        self.y = random.randrange(0, screen_height)
        self.speed = random.randint(1, 3) # Varying speed for depth
        self.size = random.randint(1, 2) # Varying size
        self.color = (random.randint(150, 255), random.randint(150, 255), 255) # Bluish-white stars

    def update(self, screen_height):
        self.y += self.speed
        if self.y > screen_height:
            self.y = 0 # Loop back to top
            self.x = random.randrange(0, pygame.display.get_surface().get_width()) # New random X

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)


def showText(screen, text, color, font, x, y):
    """
    Renders text with a subtle glow effect (by drawing multiple offset layers).
    """
    # Offset values for "glow" effect
    offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1)] # Simple 4-way offset
    glow_color = (min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50)) # Slightly brighter
    dark_color = (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50)) # Slightly darker

    # Draw "shadow" or outline for glow
    for ox, oy in offsets:
        text_surface_glow = font.render(text, True, glow_color)
        screen.blit(text_surface_glow, (x + ox, y + oy))

    # Draw main text
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def showLife(screen, num_life, color):
    """
    Draws a futuristic life indicator using glowing bars.
    """
    life_bar_width = 25
    life_bar_height = 8
    spacing = 10
    start_x = screen.get_width() - (num_life * (life_bar_width + spacing)) - 10 # Align to right
    start_y = 60 # Below scores

    for i in range(num_life):
        x = start_x + i * (life_bar_width + spacing)
        y = start_y
        
        # Base bar
        pygame.draw.rect(screen, (color[0]//2, color[1]//2, color[2]//2), (x, y, life_bar_width, life_bar_height), 0, 3) # Darker base
        # Glowing inner bar
        pygame.draw.rect(screen, color, (x, y, life_bar_width, life_bar_height), 0, 3) # Main glow
        # Subtle flicker effect for glow
        if pygame.time.get_ticks() % 200 < 100:
            pygame.draw.rect(screen, (min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50)), (x, y, life_bar_width, life_bar_height), 0, 3) # Brighter flicker


def endInterface(screen, background_color, is_win, cfg, resource_loader, stars):
    """
    Displays the end-game interface with a futuristic message and background stars.
    """
    clock = pygame.time.Clock()
    font = resource_loader.fonts['default30'] # Larger font for end message

    if is_win:
        text = 'VICTORY PROTOCOL INITIATED'
        text_color = (0, 255, 255) # Cyan for victory
    else:
        text = 'MISSION FAILED'
        text_color = (255, 50, 50) # Red for failure

    # Prepare text surfaces for glow effect
    text_surface_main = font.render(text, True, text_color)
    offsets = [(2, 2), (-2, -2), (2, -2), (-2, 2), (0, 2), (0, -2), (2, 0), (-2, 0)]
    glow_color = (min(255, text_color[0]+80), min(255, text_color[1]+80), min(255, text_color[2]+80))

    text_rect = text_surface_main.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if (event.type == pygame.KEYDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                return

        # Draw background stars
        screen.fill(background_color)
        for star in stars:
            star.update(cfg.SCREENSIZE[1]) # Update stars even on end screen
            star.draw(screen)

        # Draw glowing text
        for ox, oy in offsets:
            glow_surface = font.render(text, True, glow_color)
            screen.blit(glow_surface, (text_rect.x + ox, text_rect.y + oy))
        screen.blit(text_surface_main, text_rect)

        # Prompt to continue
        prompt_text = "PRESS ANY KEY OR MOUSE BUTTON TO CONTINUE..."
        prompt_font = resource_loader.fonts['default18']
        prompt_color = (150, 150, 255) # Faded blue
        prompt_surface = prompt_font.render(prompt_text, True, prompt_color)
        prompt_rect = prompt_surface.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 50))
        screen.blit(prompt_surface, prompt_rect)


        clock.tick(cfg.FPS)
        pygame.display.update()


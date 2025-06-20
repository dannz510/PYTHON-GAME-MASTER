import pygame
from ....utils import QuitGame


'''游戏结束界面'''
def EndInterface(screen, cfg, resource_loader, final_score):
    font_color = (255, 255, 255)
    font_big = resource_loader.fonts['default60']
    font_small = resource_loader.fonts['default30']
    
    # Create a translucent overlay
    surface = pygame.Surface(cfg.SCREENSIZE, pygame.SRCALPHA) # Use SRCALPHA for transparency
    surface.fill((0, 0, 0, 180)) # Black with 180 alpha (more opaque)

    # Game Over text
    text_gameover = font_big.render('Game Over!', True, font_color)
    text_gameover_rect = text_gameover.get_rect(center=(cfg.SCREENSIZE[0]/2, cfg.SCREENSIZE[1]/2 - 100))
    surface.blit(text_gameover, text_gameover_rect)

    # Final Score text
    text_score = resource_loader.fonts['score_font'].render(f'Final Score: {final_score}', True, (255, 255, 0)) # Yellow score
    text_score_rect = text_score.get_rect(center=(cfg.SCREENSIZE[0]/2, cfg.SCREENSIZE[1]/2 - 30))
    surface.blit(text_score, text_score_rect)

    # Button dimensions
    button_width, button_height = 150, 60 # Larger buttons
    button_spacing = 40 # Space between buttons
    
    # Calculate button positions
    total_buttons_width = (button_width * 2) + button_spacing
    start_x = (cfg.SCREENSIZE[0] - total_buttons_width) / 2
    button_start_y = cfg.SCREENSIZE[1] / 2 + 50

    # Restart Button
    restart_button_rect = pygame.Rect(start_x, button_start_y, button_width, button_height)
    pygame.draw.rect(surface, (50, 150, 50), restart_button_rect, border_radius=10) # Green, rounded corners
    text_restart = font_small.render('Restart', True, font_color)
    text_restart_rect = text_restart.get_rect(center=restart_button_rect.center)
    surface.blit(text_restart, text_restart_rect)

    # Quit Button
    quit_button_rect = pygame.Rect(start_x + button_width + button_spacing, button_start_y, button_width, button_height)
    pygame.draw.rect(surface, (150, 50, 50), quit_button_rect, border_radius=10) # Red, rounded corners
    text_quit = font_small.render('Quit', True, font_color)
    text_quit_rect = text_quit.get_rect(center=quit_button_rect.center)
    surface.blit(text_quit, text_quit_rect)

    while True:
        screen.blit(surface, (0, 0)) # Blit the transparent surface onto the screen
        
        # Add a subtle animation/pulsing to buttons (optional, for more flair)
        mouse_pos = pygame.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (80, 180, 80), restart_button_rect, border_radius=10)
            screen.blit(text_restart, text_restart_rect)
        if quit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (180, 80, 80), quit_button_rect, border_radius=10)
            screen.blit(text_quit, text_quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button
                if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return False
                if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        pygame.display.update()
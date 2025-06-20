# -*- coding: utf-8 -*-
import pygame
from ....utils import QuitGame


'''
Function: Button
Description: Draws a button on the screen with enhanced styling.
Parameters:
    screen: Pygame display surface.
    position: Tuple (left, top) for the button's top-left corner.
    text: String, the text to display on the button.
    cfg: Configuration object containing game settings.
    resource_loader: Object to load game resources (fonts, images).
Returns:
    pygame.Rect: The rectangle object for the button, used for collision detection.
'''
def Button(screen, position, text, cfg, resource_loader):
    bwidth = 310
    bheight = 65
    left, top = position

    # Define button colors
    base_color = (100, 100, 100) # Dark grey
    highlight_color = (150, 150, 150) # Lighter grey for top/left shadow
    shadow_color = (50, 50, 50) # Darker grey for bottom/right shadow
    hover_color = (120, 120, 120) # Slightly lighter grey for hover effect
    text_color = (255, 255, 255) # White text

    button_rect = pygame.Rect(left, top, bwidth, bheight)

    # Check for hover
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        current_bg_color = hover_color
    else:
        current_bg_color = base_color

    # Draw the main button rectangle
    pygame.draw.rect(screen, current_bg_color, button_rect)

    # Draw 3D-like borders
    # Top border
    pygame.draw.line(screen, highlight_color, (left, top), (left + bwidth, top), 5)
    # Left border
    pygame.draw.line(screen, highlight_color, (left, top), (left, top + bheight), 5)
    # Bottom border
    pygame.draw.line(screen, shadow_color, (left, top + bheight), (left + bwidth, top + bheight), 5)
    # Right border
    pygame.draw.line(screen, shadow_color, (left + bwidth, top + bheight), (left + bwidth, top), 5)

    # Render text
    font = resource_loader.fonts['default_l'] # Assuming 'default_l' is a larger font
    text_render = font.render(text, True, text_color)
    text_rect = text_render.get_rect(center=button_rect.center) # Center the text on the button
    screen.blit(text_render, text_rect)

    return button_rect


'''
Function: StartInterface
Description: Displays the game start screen with options for single player and two-player modes.
Parameters:
    screen: Pygame display surface.
    cfg: Configuration object containing game settings.
    resource_loader: Object to load game resources (fonts, images).
Returns:
    int: Returns 1 for single player, 2 for two-player mode.
'''
def StartInterface(screen, cfg, resource_loader):
    clock = pygame.time.Clock()
    bg = resource_loader.images['bg_big'] # Load background image
    bg_rect = bg.get_rect()

    title_font = resource_loader.fonts['default_xl'] # Assuming 'default_xl' is an extra large font
    title_text = title_font.render(cfg.TITLE, True, (255, 255, 0)) # Yellow title
    title_rect = title_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 4))

    while True:
        screen.blit(bg, bg_rect) # Draw background
        screen.blit(title_text, title_rect) # Draw title

        # Center buttons
        button_width = 310
        button_height = 65
        button_spacing = 30 # Space between buttons

        # Calculate positions for centered buttons
        total_buttons_height = (button_height * 2) + button_spacing
        start_y = (cfg.SCREENSIZE[1] - total_buttons_height) // 2
        button_1_pos = ((cfg.SCREENSIZE[0] - button_width) // 2, start_y)
        button_2_pos = ((cfg.SCREENSIZE[0] - button_width) // 2, start_y + button_height + button_spacing)


        button_1 = Button(screen, button_1_pos, 'Single Player', cfg, resource_loader)
        button_2 = Button(screen, button_2_pos, 'Two Players', cfg, resource_loader)

        # Pygame event loop for this interface.
        # Note: If running Pygame in a separate thread from a PyQt application,
        # input events (like mouse clicks) might not be reliably received here
        # due to event loop conflicts. This is a common architectural challenge.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Start Screen: Mouse click detected at: {pygame.mouse.get_pos()}") # Debugging line
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    print("Start Screen: Single Player button clicked!") # Debugging line
                    return 1
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    print("Start Screen: Two Players button clicked!") # Debugging line
                    return 2
        
        pygame.display.update()
        clock.tick(cfg.FPS)


'''
Function: EndInterface
Description: Displays the game end screen with options to restart or quit.
Parameters:
    screen: Pygame display surface.
    cfg: Configuration object containing game settings.
    resource_loader: Object to load game resources (fonts, images).
    score_1: Integer, Player 1's final score.
    score_2: Integer, Player 2's final score (optional, set to None for single player).
Returns:
    bool: True to restart, False to quit.
'''
def EndInterface(screen, cfg, resource_loader, score_1, score_2=None):
    clock = pygame.time.Clock()
    bg = resource_loader.images['bg_big'] # Load background image
    bg_rect = bg.get_rect()

    end_font_large = resource_loader.fonts['default_xl']
    end_font_medium = resource_loader.fonts['default_l']

    # Determine winning message or final scores
    if score_2 is not None: # Two-player mode
        if score_1 > score_2:
            win_message = "Player 1 Wins!"
        elif score_2 > score_1:
            win_message = "Player 2 Wins!"
        else:
            win_message = "It's a Tie!"
        score_text_p1 = f"Player 1 Score: {score_1}"
        score_text_p2 = f"Player 2 Score: {score_2}"
        
        score_render_p1 = end_font_medium.render(score_text_p1, True, (0, 0, 255)) # Blue
        score_rect_p1 = score_render_p1.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 80))
        
        score_render_p2 = end_font_medium.render(score_text_p2, True, (255, 0, 0)) # Red
        score_rect_p2 = score_render_p2.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 40))

        message_render = end_font_large.render(win_message, True, (255, 255, 0)) # Yellow
        message_rect = message_render.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 150))

    else: # Single-player mode
        message_render = end_font_large.render("Game Over!", True, (255, 0, 0)) # Red
        message_rect = message_render.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 150))
        
        score_text = f"Your Final Score: {score_1}"
        score_render = end_font_medium.render(score_text, True, (255, 255, 255)) # White
        score_rect = score_render.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 80))


    while True:
        screen.blit(bg, bg_rect) # Draw background

        screen.blit(message_render, message_rect)
        if score_2 is not None:
            screen.blit(score_render_p1, score_rect_p1)
            screen.blit(score_render_p2, score_rect_p2)
        else:
            screen.blit(score_render, score_rect)

        # Center buttons
        button_width = 310
        button_height = 65
        button_spacing = 30

        total_buttons_height = (button_height * 2) + button_spacing
        start_y = (cfg.SCREENSIZE[1] - total_buttons_height) // 2 + 100 # Adjust position lower
        button_1_pos = ((cfg.SCREENSIZE[0] - button_width) // 2, start_y)
        button_2_pos = ((cfg.SCREENSIZE[0] - button_width) // 2, start_y + button_height + button_spacing)

        button_1 = Button(screen, button_1_pos, 'Restart Game', cfg, resource_loader)
        button_2 = Button(screen, button_2_pos, 'Quit Game', cfg, resource_loader)

        # Pygame event loop for this interface.
        # Note: If running Pygame in a separate thread from a PyQt application,
        # input events (like mouse clicks) might not be reliably received here
        # due to event loop conflicts. This is a common architectural challenge.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"End Screen: Mouse click detected at: {pygame.mouse.get_pos()}") # Debugging line
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    print("End Screen: Restart Game button clicked!") # Debugging line
                    return True # Restart
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    print("End Screen: Quit Game button clicked!") # Debugging line
                    return False # Quit
        
        pygame.display.update()
        clock.tick(cfg.FPS)

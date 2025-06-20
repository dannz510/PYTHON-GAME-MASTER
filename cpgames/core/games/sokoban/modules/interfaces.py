# interfaces.py
import pygame
from ....utils import QuitGame


'''Custom Button function with 3D effect'''
def Button(screen, position, text, cfg, resource_loader, button_color=(100, 100, 100), text_color=(255, 255, 255), hover_color=(130, 130, 130), active_color=(70, 70, 70), shadow_color=(50, 50, 50), highlight_color=(150, 150, 150)):
    bwidth = 300
    bheight = 70
    left, top = position
    
    # Create the button rectangle
    button_rect = pygame.Rect(left, top, bwidth, bheight)

    # Check for mouse interaction
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    current_button_color = button_color
    if button_rect.collidepoint(mouse_pos):
        current_button_color = hover_color
        if clicked:
            current_button_color = active_color

    # Draw the main button surface
    pygame.draw.rect(screen, current_button_color, button_rect, border_radius=10)

    # Add 3D effect (shadow and highlight)
    # Shadow
    pygame.draw.line(screen, shadow_color, (left + 5, top + bheight - 5), (left + bwidth - 5, top + bheight - 5), 5)
    pygame.draw.line(screen, shadow_color, (left + bwidth - 5, top + 5), (left + bwidth - 5, top + bheight - 5), 5)
    
    # Highlight
    pygame.draw.line(screen, highlight_color, (left + 5, top + 5), (left + bwidth - 5, top + 5), 5)
    pygame.draw.line(screen, highlight_color, (left + 5, top + 5), (left + 5, top + bheight - 5), 5)

    # Render text
    font = resource_loader.fonts['default_50']
    text_surface = font.render(text, True, text_color) # Anti-aliasing True
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect


'''Start Interface'''
def startInterface(screen, cfg, resource_loader):
    # Load background image if available, else use solid color
    background_image = resource_loader.images.get('background_menu')
    if background_image:
        background_image = pygame.transform.scale(background_image, cfg.SCREENSIZE)
    
    clock = pygame.time.Clock()
    
    # Title
    title_font = resource_loader.fonts['title']
    title_text_surface = title_font.render(cfg.TITLE, True, (255, 215, 0)) # Gold-like color for title
    title_text_rect = title_text_surface.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 4))

    while True:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(cfg.BACKGROUNDCOLOR)

        screen.blit(title_text_surface, title_text_rect)

        button_1 = Button(screen, (cfg.SCREENSIZE[0] // 2 - 150, cfg.SCREENSIZE[1] // 2), 'Start Game', cfg, resource_loader, text_color=(255, 0, 0))
        button_2 = Button(screen, (cfg.SCREENSIZE[0] // 2 - 150, cfg.SCREENSIZE[1] // 2 + 100), 'Exit Game', cfg, resource_loader, text_color=(255, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    QuitGame()
        
        pygame.display.update()
        clock.tick(cfg.FPS)


'''End Interface'''
def endInterface(screen, cfg, resource_loader):
    # Load background image if available, else use solid color
    background_image = resource_loader.images.get('background_menu')
    if background_image:
        background_image = pygame.transform.scale(background_image, cfg.SCREENSIZE)

    clock = pygame.time.Clock()
    text = 'Congratulations on your cleverness!'
    font = resource_loader.fonts['default_30']
    text_render = font.render(text, True, (255, 255, 255)) # Anti-aliasing True
    text_rect = text_render.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 50))

    sub_text = 'Press any key to exit...'
    sub_font = resource_loader.fonts['default_15']
    sub_text_render = sub_font.render(sub_text, True, (200, 200, 200))
    sub_text_rect = sub_text_render.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 50))


    while True:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(cfg.BACKGROUNDCOLOR)

        screen.blit(text_render, text_rect)
        screen.blit(sub_text_render, sub_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.KEYDOWN: # Exit on any key press
                QuitGame()
        
        pygame.display.update()
        clock.tick(cfg.FPS)


'''Level Switch Interface'''
def switchInterface(screen, cfg, resource_loader):
    # Load background image if available, else use solid color
    background_image = resource_loader.images.get('background_menu')
    if background_image:
        background_image = pygame.transform.scale(background_image, cfg.SCREENSIZE)

    clock = pygame.time.Clock()
    
    # Message for next level
    next_level_msg = 'Level Completed!'
    font = resource_loader.fonts['default_50']
    msg_render = font.render(next_level_msg, True, (0, 255, 0)) # Green color for success message
    msg_rect = msg_render.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 3))

    while True:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(cfg.BACKGROUNDCOLOR)

        screen.blit(msg_render, msg_rect)

        button_1 = Button(screen, (cfg.SCREENSIZE[0] // 2 - 150, cfg.SCREENSIZE[1] // 2), 'Next Level', cfg, resource_loader, text_color=(0, 0, 255))
        button_2 = Button(screen, (cfg.SCREENSIZE[0] // 2 - 150, cfg.SCREENSIZE[1] // 2 + 100), 'Exit Game', cfg, resource_loader, text_color=(255, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    QuitGame()
        
        pygame.display.update()
        clock.tick(cfg.FPS)
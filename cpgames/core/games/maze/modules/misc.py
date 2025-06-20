import pygame
from ....utils import QuitGame


'''在屏幕指定位置显示文字'''
def showText(screen, font, text, color, position):
    text_render = font.render(text, True, color)
    rect = text_render.get_rect()
    rect.left, rect.top = position
    screen.blit(text_render, rect)
    return rect.right


'''按钮'''
def Button(screen, position, text, font, 
           button_colors=((100, 200, 255), (0, 100, 200)), # Brighter to darker blue gradient
           border_color=(25, 25, 75), # Dark border
           text_color=(255, 255, 255), 
           bwidth=200, bheight=50):
    left, top = position

    # Create a surface for the button with alpha for gradient and effects
    button_surface = pygame.Surface((bwidth, bheight), pygame.SRCALPHA)
    
    # Draw gradient background (smoother transition)
    for i in range(bheight):
        ratio = i / bheight
        # Interpolate colors for a smooth gradient
        r = int(button_colors[0][0] * (1 - ratio) + button_colors[1][0] * ratio)
        g = int(button_colors[0][1] * (1 - ratio) + button_colors[1][1] * ratio)
        b = int(button_colors[0][2] * (1 - ratio) + button_colors[1][2] * ratio)
        pygame.draw.line(button_surface, (r, g, b, 255), (0, i), (bwidth, i)) # Full opacity

    # Add a subtle highlight for top/left edges (3D effect)
    pygame.draw.line(button_surface, (255, 255, 255, 80), (1, 1), (bwidth - 2, 1), 2)
    pygame.draw.line(button_surface, (255, 255, 255, 80), (1, 1), (1, bheight - 2), 2)

    # Add a subtle shadow for bottom/right edges (3D effect)
    pygame.draw.line(button_surface, (0, 0, 0, 80), (1, bheight - 2), (bwidth - 2, bheight - 2), 2)
    pygame.draw.line(button_surface, (0, 0, 0, 80), (bwidth - 2, 1), (bwidth - 2, bheight - 2), 2)

    # Draw rounded border
    pygame.draw.rect(button_surface, border_color, button_surface.get_rect(), 3, border_radius=8)
    
    screen.blit(button_surface, (left, top))

    # Render text with a pronounced shadow for 3D effect
    shadow_offset = 3
    shadow_color = (0, 0, 0, 100) # Semi-transparent black for shadow
    
    text_render_shadow = font.render(text, 1, shadow_color) 
    text_rect_shadow = text_render_shadow.get_rect(centerx=left + bwidth / 2 + shadow_offset, centery=top + bheight / 2 + shadow_offset)
    screen.blit(text_render_shadow, text_rect_shadow)

    text_render = font.render(text, 1, text_color)
    text_rect = text_render.get_rect(centerx=left + bwidth / 2, centery=top + bheight / 2)
    return screen.blit(text_render, text_rect)


'''游戏开始/关卡切换/游戏结束界面'''
def Interface(screen, cfg, mode='game_start'):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    
    # Define vibrant color schemes for interfaces
    background_color = (200, 220, 240) # A soothing light blue for backgrounds
    title_color = (30, 40, 100) # Deep blue for titles
    
    if mode == 'game_start':
        clock = pygame.time.Clock()
        while True:
            screen.fill(background_color)
            # Draw a larger, more prominent title
            title_font = pygame.font.SysFont('Consolas', 60, bold=True)
            showText(screen, title_font, cfg.TITLE, title_color, ((cfg.SCREENSIZE[0]-title_font.size(cfg.TITLE)[0])//2, cfg.SCREENSIZE[1]//6)) # Centered title
            
            button_1 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3 + 50), 'START', font)
            button_2 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2 + 50), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        QuitGame()
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_switch':
        clock = pygame.time.Clock()
        while True:
            screen.fill(background_color)
            title_font = pygame.font.SysFont('Consolas', 50, bold=True)
            showText(screen, title_font, 'LEVEL COMPLETE!', title_color, ((cfg.SCREENSIZE[0]-title_font.size('LEVEL COMPLETE!')[0])//2, cfg.SCREENSIZE[1]//6))
            button_1 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3 + 50), 'NEXT', font)
            button_2 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2 + 50), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        QuitGame()
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_end':
        clock = pygame.time.Clock()
        while True:
            screen.fill(background_color)
            title_font = pygame.font.SysFont('Consolas', 50, bold=True)
            showText(screen, title_font, 'GAME OVER!', title_color, ((cfg.SCREENSIZE[0]-title_font.size('GAME OVER!')[0])//2, cfg.SCREENSIZE[1]//6))
            button_1 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3 + 50), 'RESTART', font)
            button_2 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2 + 50), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        QuitGame()
            pygame.display.update()
            clock.tick(cfg.FPS)
    else:
        raise ValueError('Interface.mode unsupport %s...' % mode)

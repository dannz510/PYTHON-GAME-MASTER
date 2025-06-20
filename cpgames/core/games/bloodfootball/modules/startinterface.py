
import pygame
from ....utils import QuitGame


def StartInterface(screen, resource_loader, cfg):
    clock = pygame.time.Clock()
    font, flag, count = resource_loader.fonts['default30'], True, 0
    font_render = font.render('Press any key to start the game', False, cfg.RED)
    while True:
        count += 1
        if count > 20: count, flag = 0, not flag
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                return True
        screen.blit(resource_loader.images['background_start'], (0, 0))
        if flag: screen.blit(font_render, ((cfg.SCREENSIZE[0] - font.size('Press any key to start the game')[0]) // 2, cfg.SCREENSIZE[1] - 200))
        clock.tick(cfg.FPS)
        pygame.display.update()
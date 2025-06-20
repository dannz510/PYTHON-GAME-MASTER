# cpgames/core/games/catchcoins/modules/endinterface.py

import pygame
from ....utils import QuitGame
from ..constants import WHITE, DARK_BLUE, RED, GREEN, LIGHT_BLUE # Import colors from constants.py

'''游戏结束画面'''
def ShowEndGameInterface(screen, cfg, score, highest_score, resource_loader, render_text_func):
    # Display scaled background image on end screen for consistency
    scaled_background = pygame.transform.scale(resource_loader.images['background'], cfg.SCREENSIZE)

    # 显示的文本信息设置
    font_big = resource_loader.fonts['default_l']
    font_small = resource_loader.fonts['default_s']

    text_title = render_text_func(font_big, f"TIME IS UP!", RED, DARK_BLUE, 3)
    text_title_rect = text_title.get_rect()
    text_title_rect.centerx = screen.get_rect().centerx
    text_title_rect.centery = screen.get_rect().centery - 100

    text_score = render_text_func(font_small, f"Score: {score}, Highest Score: {highest_score}", WHITE, DARK_BLUE, 2)
    text_score_rect = text_score.get_rect()
    text_score_rect.centerx = screen.get_rect().centerx
    text_score_rect.centery = screen.get_rect().centery - 10

    text_tip = render_text_func(font_small, f"Press Q to quit or R to restart", LIGHT_BLUE, DARK_BLUE, 2)
    text_tip_rect = text_tip.get_rect()
    text_tip_rect.centerx = screen.get_rect().centerx
    text_tip_rect.centery = screen.get_rect().centery + 60

    text_tip_count = 0
    text_tip_freq = 30
    text_tip_show_flag = True

    clock = pygame.time.Clock()
    while True:
        screen.blit(scaled_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_r:
                    return True

        screen.blit(text_title, text_title_rect)
        screen.blit(text_score, text_score_rect)
        if text_tip_show_flag:
            screen.blit(text_tip, text_tip_rect)

        text_tip_count += 1
        if text_tip_count % text_tip_freq == 0:
            text_tip_count = 0
            text_tip_show_flag = not text_tip_show_flag

        pygame.display.flip()
        clock.tick(cfg.FPS)
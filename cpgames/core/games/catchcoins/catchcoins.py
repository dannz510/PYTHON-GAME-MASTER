# cpgames/core/games/catchcoins/catchcoins.py

import os
import pygame
import random
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Hero, Food, ShowEndGameInterface
from .constants import WHITE, BLACK, RED, GREEN, BLUE, LIGHT_BLUE, DARK_BLUE # Import colors from constants.py

'''配置类'''
class Config():
    # rootdir, TITLE, FPS, SCREENSIZE, etc. remain the same
    # ... (rest of your Config class) ...
    # No need for color definitions here anymore
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 标题
    TITLE = 'Catch the Coins - Dannz'
    # FPS
    FPS = 60 # Increased FPS for smoother animation
    # 屏幕大小
    SCREENSIZE = (800, 600)
    # 背景颜色 (This will be less relevant if using background image that fits)
    BACKGROUND_COLOR = (0, 160, 233)
    # 最高分记录的路径
    HIGHEST_SCORE_RECORD_FILEPATH = os.path.join(rootdir, 'highest.rec')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'gold': os.path.join(rootdir, 'resources/images/gold.png'),
        'apple': os.path.join(rootdir, 'resources/images/apple.png'),
        'background': os.path.join(rootdir, 'resources/images/background.jpg'),
        'hero': [],
    }
    for i in range(1, 11):
        IMAGE_PATHS_DICT['hero'].append(os.path.join(rootdir, 'resources/images/%d.png' % i))
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
     # 游戏声音路径
    SOUND_PATHS_DICT = {
        'get': os.path.join(rootdir, 'resources/audios/get.wav'),
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'default_s': {'name': os.path.join(rootdir.replace('catchcoins', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 40},
        'default_l': {'name': os.path.join(rootdir.replace('catchcoins', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 60},
    }

'''Helper function to render text with an outline (New)'''
def render_text_with_outline(font, text, text_color, outline_color, outline_thickness=2):
    text_surface = font.render(text, True, text_color)
    outline_surface = pygame.Surface(text_surface.get_size()).convert_alpha()
    outline_surface.fill((0,0,0,0)) # Transparent

    # Render outline by blitting shifted text
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0: # Avoid re-rendering original text
                outline_text = font.render(text, True, outline_color)
                outline_surface.blit(outline_text, (dx + outline_thickness, dy + outline_thickness))

    # Blit the original text on top
    final_surface = pygame.Surface((text_surface.get_width() + 2 * outline_thickness,
                                    text_surface.get_height() + 2 * outline_thickness)).convert_alpha()
    final_surface.fill((0,0,0,0))
    final_surface.blit(outline_surface, (0, 0))
    final_surface.blit(text_surface, (outline_thickness, outline_thickness))
    return final_surface


'''接金币小游戏'''
class CatchCoinsGame(PygameBaseGame):
    game_type = 'catchcoins'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(CatchCoinsGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        flag = True
        while flag:
            # Initialization remains the same
            screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
            game_images, game_sounds = resource_loader.images, resource_loader.sounds

            # Scale background image to fit screen (FIX for background.jpg)
            scaled_background = pygame.transform.scale(game_images['background'], cfg.SCREENSIZE)

            resource_loader.playbgm()
            font = resource_loader.fonts['default_s']
            hero = Hero(game_images['hero'], position=(375, 520))
            food_sprites_group = pygame.sprite.Group()
            generate_food_freq = random.randint(10, 20)
            generate_food_count = 0
            score = 0
            highest_score = 0 if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH) else int(open(cfg.HIGHEST_SCORE_RECORD_FILEPATH).read())
            clock = pygame.time.Clock()
            start_time = pygame.time.get_ticks()
            game_duration_ms = 90 * 1000

            while True:
                screen.blit(scaled_background, (0, 0))

                elapsed_time_ms = pygame.time.get_ticks() - start_time
                remaining_time_ms = max(0, game_duration_ms - elapsed_time_ms)
                minutes = remaining_time_ms // 60000
                seconds = (remaining_time_ms // 1000) % 60
                countdown_text_str = f'Time: {minutes:02d}:{seconds:02d}'
                countdown_text_surface = render_text_with_outline(font, countdown_text_str, WHITE, DARK_BLUE, 2)
                countdown_rect = countdown_text_surface.get_rect()
                countdown_rect.topright = [cfg.SCREENSIZE[0] - 20, 10]
                screen.blit(countdown_text_surface, countdown_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        QuitGame()
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                    hero.move(cfg.SCREENSIZE, 'left')
                if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                    hero.move(cfg.SCREENSIZE, 'right')

                generate_food_count += 1
                if generate_food_count > generate_food_freq:
                    generate_food_freq = random.randint(10, 20)
                    generate_food_count = 0
                    food_type = random.choice(['gold'] * 8 + ['apple'] * 2 + ['bomb'])
                    food = Food(game_images, food_type, cfg.SCREENSIZE)
                    food_sprites_group.add(food)

                for food in food_sprites_group:
                    if food.update(): food_sprites_group.remove(food)

                for food in food_sprites_group:
                    if pygame.sprite.collide_mask(food, hero):
                        game_sounds['get'].play()
                        food_sprites_group.remove(food)
                        score += food.score
                        if score > highest_score: highest_score = score
                        # New rule: If score drops below 0, game ends (optional, for challenge)
                        # if score < 0:
                        #    pygame.time.set_timer(pygame.USEREVENT, 1) # Trigger end game immediately

                hero.draw(screen)
                food_sprites_group.draw(screen)

                score_text_str = f'Score: {score} | High Score: {highest_score}'
                score_text_surface = render_text_with_outline(font, score_text_str, WHITE, DARK_BLUE, 2)
                score_rect = score_text_surface.get_rect()
                score_rect.topleft = [20, 10]
                screen.blit(score_text_surface, score_rect)

                if remaining_time_ms <= 0:
                    break

                pygame.display.flip()
                clock.tick(cfg.FPS)

            fp = open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, 'w')
            fp.write(str(highest_score))
            fp.close()
            flag = ShowEndGameInterface(screen, cfg, score, highest_score, resource_loader, render_text_with_outline)
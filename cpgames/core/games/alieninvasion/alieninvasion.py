import os
import random
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
# Importing updated modules
from .modules import (
    AircraftSprite, UFOSprite, EnemySprite, MyBulletSprite, EnemyBulletSprite,
    showLife, showText, endInterface, BackgroundStar
)


# Updated Configuration for a futuristic theme
class Config():
    rootdir = os.path.split(os.path.abspath(__file__))[0]

    # Futuristic Color Palette (Cyan, Magenta, Electric Blue, Orange)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    # Backgrounds/Dark elements
    DARK_SPACE = (10, 10, 20)
    DEEP_SPACE = (5, 5, 15)
    # Player/Positive elements
    PLAYER_NEON = (0, 255, 255) # Cyan
    PLAYER_BULLET_NEON = (0, 200, 255) # Lighter Cyan
    # Enemy/Threat elements
    ENEMY_NEON_SMALL = (255, 100, 200) # Pinkish-purple
    ENEMY_NEON_MEDIUM = (255, 150, 50) # Orange
    ENEMY_NEON_LARGE = (255, 50, 50) # Red
    ENEMY_BULLET_NEON = (255, 50, 150) # Magenta
    UFO_NEON = (150, 0, 255) # Purple
    EXPLOSION_CORE = (255, 255, 100) # Yellowish
    EXPLOSION_OUTER = (255, 100, 0) # Orange
    SHIELD_COLOR = (50, 150, 255, 128) # Semi-transparent blue for shield

    FPS = 60
    BGM_PATH = os.path.join(rootdir, 'resources/bgm.mp3') # Ensure this path is correct
    HIGHEST_SCORE_SAVE_PATH = os.path.join(rootdir, 'score')
    SCREENSIZE = (800, 600)
    TITLE = 'Cosmic Incursion: 2077 - Dannz'

    # Using system fonts for broader compatibility, with a futuristic vibe
    FONT_PATHS_DICT = {
        'default18': {'name': 'consolas', 'size': 18, 'system_font': True},
        'default30': {'name': 'consolas', 'size': 30, 'system_font': True},
        'neon_font': {'name': 'couriernew', 'size': 24, 'system_font': True}, # A new font for scores
    }

    # Game difficulty progression (Waves)
    WAVE_ENEMIES_INCREASE = 5 # How many more enemies per wave
    WAVE_SPEED_INCREASE = 0.5 # How much enemy speed increases
    WAVE_SHOT_RATE_DECREASE = 5 # How much enemy shot interval decreases
    INITIAL_ENEMY_MOVE_INTERVAL = 24
    INITIAL_ENEMY_SHOT_INTERVAL = 100
    UFO_SPAWN_INTERVAL = 5000 # UFO spawns every 5000 frames (roughly 83 seconds)


'''Cosmic Incursion Minigame'''
class AlienInvasionGame(PygameBaseGame):
    game_type = 'alieninvasion'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(AlienInvasionGame, self).__init__(config=self.cfg, **kwargs)
        # Initialize stars for background
        self.stars = [BackgroundStar(self.cfg.SCREENSIZE[0], self.cfg.SCREENSIZE[1]) for _ in range(100)]

    '''Run the game'''
    def run(self):
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        resource_loader.playbgm() # Play background music

        while True:
            is_win = self.GamingInterface(screen, cfg, resource_loader)
            # Pass the background stars to endInterface as well
            endInterface(screen, cfg.DARK_SPACE, is_win, cfg, resource_loader, self.stars)

    '''Start the game'''
    def GamingInterface(self, screen, cfg, resource_loader):
        clock = pygame.time.Clock()
        font_score = resource_loader.fonts['neon_font'] # Use neon font for scores
        font_info = resource_loader.fonts['default18'] # Use default font for other info

        # Load highest score
        if not os.path.isfile(cfg.HIGHEST_SCORE_SAVE_PATH):
            with open(cfg.HIGHEST_SCORE_SAVE_PATH, 'w') as f:
                f.write('0')
        with open(cfg.HIGHEST_SCORE_SAVE_PATH, 'r') as f:
            highest_score = int(f.read().strip())

        # Game state variables
        current_wave = 1
        enemies_group, boomed_enemies_group, en_bullets_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
        myaircraft = AircraftSprite(color=cfg.PLAYER_NEON, bullet_color=cfg.PLAYER_BULLET_NEON)
        my_bullets_group = pygame.sprite.Group()
        ufo = UFOSprite(color=cfg.UFO_NEON)

        # Enemy spawning logic
        def spawn_enemies(wave):
            nonlocal enemies_group
            enemies_group.empty() # Clear existing enemies
            num_enemies = min(55 + (wave - 1) * cfg.WAVE_ENEMIES_INCREASE, 100) # Cap max enemies
            for i in range(num_enemies):
                # Distribute enemy types more evenly or based on wave
                if i < num_enemies * 0.2: # 20% small
                    enemy = EnemySprite('small', i, cfg.ENEMY_NEON_SMALL, cfg.ENEMY_BULLET_NEON)
                elif i < num_enemies * 0.6: # 40% medium
                    enemy = EnemySprite('medium', i, cfg.ENEMY_NEON_MEDIUM, cfg.ENEMY_BULLET_NEON)
                else: # 40% large
                    enemy = EnemySprite('large', i, cfg.ENEMY_NEON_LARGE, cfg.ENEMY_BULLET_NEON)
                enemy.rect.x = 85 + (i % 11) * 50
                enemy.rect.y = 120 + (i // 11) * 45
                enemies_group.add(enemy)

        spawn_enemies(current_wave)

        # Enemy movement and shooting logic
        enemy_move_count = 0
        enemy_move_interval = cfg.INITIAL_ENEMY_MOVE_INTERVAL
        enemy_move_flag = False
        enemy_change_direction_count = 0
        enemy_change_direction_interval = 60
        enemy_need_down = False
        enemy_move_right = True
        enemy_need_move_row = 6
        enemy_max_row = 5
        enemy_shot_interval = cfg.INITIAL_ENEMY_SHOT_INTERVAL
        enemy_shot_count = 0
        enemy_shot_flag = False
        ufo_spawn_count = 0

        running = True
        is_win = False

        # Main game loop
        while running:
            # Update background stars
            screen.fill(cfg.DARK_SPACE)
            for star in self.stars:
                star.update(cfg.SCREENSIZE[1])
                star.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        QuitGame()
                    if event.key == pygame.K_SPACE: # Charge shot on spacebar
                        my_bullet = myaircraft.shot(charge=True)
                        if my_bullet:
                            my_bullets_group.add(my_bullet)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click for normal shot
                        my_bullet = myaircraft.shot()
                        if my_bullet:
                            my_bullets_group.add(my_bullet)

            # Collision detection (Player Bullets vs. Enemies/UFO)
            for enemy in enemies_group:
                hit_bullets = pygame.sprite.spritecollide(enemy, my_bullets_group, False, None)
                for bullet in hit_bullets:
                    if bullet.is_charged: # Charged shot deals more damage
                        enemy.health -= 2
                    else:
                        enemy.health -= 1
                    my_bullets_group.remove(bullet)
                    del bullet
                    if enemy.health <= 0:
                        boomed_enemies_group.add(enemy)
                        enemies_group.remove(enemy)
                        myaircraft.score += enemy.reward

            if not ufo.is_dead:
                hit_ufo_bullets = pygame.sprite.spritecollide(ufo, my_bullets_group, False, None)
                for bullet in hit_ufo_bullets:
                    if bullet.is_charged:
                        ufo.health -= 2
                    else:
                        ufo.health -= 1
                    my_bullets_group.remove(bullet)
                    del bullet
                    if ufo.health <= 0:
                        ufo.is_dead = True
                        myaircraft.score += ufo.reward

            # UFO logic
            ufo_spawn_count += 1
            if ufo_spawn_count >= cfg.UFO_SPAWN_INTERVAL and ufo.is_dead:
                ufo.reset() # Reset UFO after it's dead
                ufo_spawn_count = 0 # Reset spawn counter

            # Enemy shooting
            enemy_shot_count += 1
            if enemy_shot_count > enemy_shot_interval:
                enemy_shot_flag = True
                if enemies_group: # Ensure there are enemies to shoot
                    enemies_survive_list = [enemy.number for enemy in enemies_group]
                    shot_number = random.choice(enemies_survive_list)
                enemy_shot_count = 0

            # Enemy movement
            enemy_move_count += 1
            if enemy_move_count > enemy_move_interval:
                enemy_move_count = 0
                enemy_move_flag = True
                enemy_need_move_row -= 1
                if enemy_need_move_row == 0:
                    enemy_need_move_row = enemy_max_row
                enemy_change_direction_count += 1
                if enemy_change_direction_count > enemy_change_direction_interval:
                    enemy_change_direction_count = 1
                    enemy_move_right = not enemy_move_right
                    enemy_need_down = True

                    # Difficulty increase for enemies per wave
                    enemy_move_interval = max(10, enemy_move_interval - cfg.WAVE_SPEED_INCREASE)
                    enemy_shot_interval = max(30, enemy_shot_interval - cfg.WAVE_SHOT_RATE_DECREASE)

            # Update and draw enemies
            for enemy in enemies_group:
                if enemy_shot_flag:
                    if enemy.number == shot_number:
                        en_bullet = enemy.shot()
                        en_bullets_group.add(en_bullet)
                if enemy_move_flag:
                    if enemy.number in range((enemy_need_move_row - 1) * 11, enemy_need_move_row * 11):
                        if enemy_move_right:
                            enemy.update('right', cfg.SCREENSIZE[1])
                        else:
                            enemy.update('left', cfg.SCREENSIZE[1])
                else:
                    enemy.update(None, cfg.SCREENSIZE[1])
                if enemy_need_down:
                    if enemy.update('down', cfg.SCREENSIZE[1]):
                        running = False # Game over if enemy reaches bottom
                        is_win = False
                    enemy.change_count -= 1 # Ensure animation continues
                enemy.draw(screen)

            enemy_move_flag = False
            enemy_need_down = False
            enemy_shot_flag = False

            # Enemy explosion effects
            for boomed_enemy in boomed_enemies_group:
                if boomed_enemy.boom(screen, cfg.EXPLOSION_OUTER, cfg.EXPLOSION_CORE): # Pass colors
                    boomed_enemies_group.remove(boomed_enemy)
                    del boomed_enemy

            # Collision detection (Enemy Bullets vs. Player Ship)
            if not myaircraft.is_shielded: # Only take damage if not shielded
                if pygame.sprite.spritecollide(myaircraft, en_bullets_group, True, None):
                    myaircraft.one_dead = True
                    myaircraft.is_shielded = True # Activate temporary shield
                    myaircraft.shield_timer_start = pygame.time.get_ticks() # Start shield timer

            # Player ship updates
            if myaircraft.one_dead:
                if myaircraft.boom(screen, cfg.EXPLOSION_OUTER, cfg.EXPLOSION_CORE): # Pass colors
                    myaircraft.resetBoom()
                    myaircraft.num_life -= 1
                    if myaircraft.num_life < 1:
                        running = False
                        is_win = False
            else:
                myaircraft.update(cfg.SCREENSIZE[0])
                myaircraft.draw(screen)
                if myaircraft.is_shielded: # Draw shield if active
                    myaircraft.draw_shield(screen, cfg.SHIELD_COLOR)

            # UFO updates
            if not ufo.has_boomed and ufo.is_dead:
                if ufo.boom(screen, cfg.EXPLOSION_OUTER, cfg.EXPLOSION_CORE): # Pass colors
                    ufo.has_boomed = True
            else:
                ufo.update(cfg.SCREENSIZE[0])
                ufo.draw(screen)

            # Player bullet updates
            for bullet in my_bullets_group:
                if bullet.update():
                    my_bullets_group.remove(bullet)
                    del bullet
                else:
                    bullet.draw(screen)

            # Enemy bullet updates
            for bullet in en_bullets_group:
                if bullet.update(cfg.SCREENSIZE[1]):
                    en_bullets_group.remove(bullet)
                    del bullet
                else:
                    bullet.draw(screen)

            # Score and life updates
            if myaircraft.score > highest_score:
                highest_score = myaircraft.score
            if (myaircraft.score % 2000 == 0) and (myaircraft.score > 0) and (myaircraft.score != myaircraft.old_score):
                myaircraft.old_score = myaircraft.score
                myaircraft.num_life = min(myaircraft.num_life + 1, myaircraft.max_num_life)

            # Wave progression
            if len(enemies_group) < 1:
                current_wave += 1
                spawn_enemies(current_wave)
                myaircraft.num_life = min(myaircraft.num_life + 1, myaircraft.max_num_life) # Reward life for clearing wave
                # Optionally reset/adjust UFO for new wave, or make it appear more often
                ufo.reset()
                ufo_spawn_count = 0 # Reset UFO spawn for new wave

            # Display text
            showText(screen, 'SCORE: ', cfg.PLAYER_NEON, font_info, 200, 8)
            showText(screen, str(myaircraft.score), cfg.PLAYER_NEON, font_score, 200, 28)

            showText(screen, 'ENEMIES: ', cfg.ENEMY_NEON_LARGE, font_info, 370, 8)
            showText(screen, str(len(enemies_group)), cfg.ENEMY_NEON_LARGE, font_score, 370, 28)

            showText(screen, 'HIGHEST: ', cfg.WHITE, font_info, 540, 8)
            showText(screen, str(highest_score), cfg.WHITE, font_score, 540, 28)

            showText(screen, f'WAVE: {current_wave}', cfg.UFO_NEON, font_info, 8, 48) # Display current wave
            # Changed cfg.RED to cfg.ENEMY_NEON_LARGE
            showText(screen, 'FPS: ' + str(int(clock.get_fps())), cfg.ENEMY_NEON_LARGE, font_info, 8, 8) 

            showLife(screen, myaircraft.num_life, cfg.PLAYER_NEON) # Pass player neon color

            pygame.display.update()
            clock.tick(cfg.FPS)

        with open(cfg.HIGHEST_SCORE_SAVE_PATH, 'w') as f:
            f.write(str(highest_score))
        return is_win

import os
import pygame
import random
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Bullet, Ship, Asteroid, StartInterface, EndInterface

'''
Class: Config
Description: Holds all configuration settings for the game.
'''
class Config():
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    FPS = 60
    SCREENSIZE = (956, 560)
    TITLE = 'Asteroid Attack!' # More engaging title

    # Paths to sound files
    SOUND_PATHS_DICT = {
        'boom': os.path.join(rootdir, 'resources/audios/boom.wav'),
        'shot': os.path.join(rootdir, 'resources/audios/shot.ogg'),
        # 'hit': os.path.join(rootdir, 'resources/audios/hit.wav') # Removed: This file was causing FileNotFoundError
    }
    BGM_PATH = os.path.join(rootdir, 'resources/audios/Cool Space Music.mp3')

    # Paths to image files
    IMAGE_PATHS_DICT = {
        'asteroid': os.path.join(rootdir, 'resources/images/asteroid.png'),
        'bg_big': os.path.join(rootdir, 'resources/images/bg_big.png'), # Used for interfaces
        'bullet': os.path.join(rootdir, 'resources/images/bullet.png'),
        'seamless_space': os.path.join(rootdir, 'resources/images/seamless_space.png'), # For scrolling background
        'ship': os.path.join(rootdir, 'resources/images/ship.png'),
        'ship_exploded': os.path.join(rootdir, 'resources/images/ship_exploded.png'),
    }

    # Font settings
    FONT_PATHS_DICT = {
        'default_s': {'name': pygame.font.get_default_font(), 'size': 18},
        'default_m': {'name': pygame.font.get_default_font(), 'size': 24},
        'default_l': {'name': pygame.font.get_default_font(), 'size': 36}, # For buttons/scores
        'default_xl': {'name': pygame.font.get_default_font(), 'size': 48}, # For titles
    }


'''
Class: AircraftWarGame
Description: Main game class inheriting from PygameBaseGame.
Handles game initialization, main loop, and game states.
'''
class AircraftWarGame(PygameBaseGame):
    def __init__(self, **kwargs):
        # Instantiate Config here and pass the instance to the superclass.
        # This ensures 'self.cfg' is explicitly an instance of Config.
        config_instance = Config()
        super(AircraftWarGame, self).__init__(config_instance, **kwargs)
        
        # Fallback: if PygameBaseGame.__init__ somehow doesn't set self.cfg,
        # ensure it's set by the child class after the super call.
        if not hasattr(self, 'cfg') or self.cfg is None:
            self.cfg = config_instance
        
        self.game_type = None # 1 for single player, 2 for two players
        self.background_y = 0 # For scrolling background
        self.bg_scroll_speed = 1 # Speed of background scrolling

    '''
    Method: start
    Description: Displays the start interface and sets the game type.
    '''
    def start(self):
        # self.cfg should now be guaranteed to exist here
        self.game_type = StartInterface(self.screen, self.cfg, self.resource_loader)

    '''
    Method: end
    Description: Displays the end interface and handles game restart/quit.
    Parameters:
        score_1: Player 1's score.
        score_2: Player 2's score (optional).
    Returns:
        bool: True if the game should restart, False otherwise.
    '''
    def end(self, score_1, score_2=None):
        # self.cfg should now be guaranteed to exist here
        return EndInterface(self.screen, self.cfg, self.resource_loader, score_1, score_2)

    '''
    Method: run
    Description: The main game loop.
    '''
    def run(self):
        # Initialize game state for a fresh run
        pygame.mixer.music.stop() # Stop any previous music
        # Load sounds
        shot_sound = self.resource_loader.sounds['shot']
        explosion_sound = self.resource_loader.sounds['boom']
        pygame.mixer.music.load(self.cfg.BGM_PATH)
        pygame.mixer.music.play(-1, 0.0)

        # Game entities
        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        asteroid_group = pygame.sprite.Group()

        # Create players based on game type
        player1 = Ship(1, self.cfg, self.resource_loader)
        player_group.add(player1)
        if self.game_type == 2:
            player2 = Ship(2, self.cfg, self.resource_loader)
            player_group.add(player2)
        else:
            player2 = None # Ensure player2 is None in single-player mode

        score_1 = 0
        score_2 = 0

        # Game timers and counters
        asteroid_spawn_timer = 0
        asteroid_spawn_rate = 60 # Frames between asteroid spawns (initially)
        MAX_ASTEROID_SPAWN_RATE = 20 # Minimum spawn rate (faster)

        # Game loop
        clock = pygame.time.Clock()
        running = True
        while running:
            # --Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    # Player 1 controls (Arrow keys, Space)
                    if event.key == pygame.K_SPACE and player1.can_shoot():
                        bullet = Bullet(1, player1.rect.midtop, self.cfg, self.resource_loader)
                        bullet_group.add(bullet)
                        player1.reset_cooldown()
                        shot_sound.play()
                    # Player 2 controls (W, A, S, D, LSHIFT)
                    if self.game_type == 2 and player2 and event.key == pygame.K_LSHIFT and player2.can_shoot():
                        bullet = Bullet(2, player2.rect.midtop, self.cfg, self.resource_loader)
                        bullet_group.add(bullet)
                        player2.reset_cooldown()
                        shot_sound.play()

            # --Continuous key presses for movement
            keys = pygame.key.get_pressed()
            # Player 1
            if keys[pygame.K_LEFT]:
                player1.move('left')
            if keys[pygame.K_RIGHT]:
                player1.move('right')
            if keys[pygame.K_UP]:
                player1.move('up')
            if keys[pygame.K_DOWN]:
                player1.move('down')
            
            # Player 2
            if self.game_type == 2 and player2:
                if keys[pygame.K_a]:
                    player2.move('left')
                if keys[pygame.K_d]:
                    player2.move('right')
                if keys[pygame.K_w]:
                    player2.move('up')
                if keys[pygame.K_s]:
                    player2.move('down')
            
            # --Update game elements
            # Update cooldowns and invincibility
            for player in player_group:
                player.update_cooldown()
                player.update_invincibility()

            # Spawn asteroids
            asteroid_spawn_timer += 1
            if asteroid_spawn_timer >= asteroid_spawn_rate:
                asteroid_group.add(Asteroid(self.cfg, self.resource_loader))
                asteroid_spawn_timer = 0
                # Gradually increase difficulty by decreasing spawn rate
                asteroid_spawn_rate = max(MAX_ASTEROID_SPAWN_RATE, asteroid_spawn_rate - 1)


            # --Collision Detection
            # Bullet-Asteroid collisions
            for bullet in bullet_group:
                hit_asteroids = pygame.sprite.spritecollide(bullet, asteroid_group, True) # True means asteroid is removed
                if hit_asteroids:
                    bullet_group.remove(bullet)
                    if bullet.player_idx == 1:
                        score_1 += len(hit_asteroids) * 10 # Score per asteroid
                    else:
                        score_2 += len(hit_asteroids) * 10
                    explosion_sound.play() # Play sound for asteroid explosion

            # Player-Asteroid collisions
            for player in player_group:
                if not player.is_invincible: # Only check collision if not invincible
                    collided_asteroids = pygame.sprite.spritecollide(player, asteroid_group, True)
                    if collided_asteroids:
                        if player.take_hit(): # Player takes damage
                            explosion_sound.play() # Play explosion for player hit
                            player.explode_step = 1 # Start explosion animation
                        else: # Player was invincible, just remove asteroid
                            pass # Asteroid still removed by spritecollide(..., True)

            # Remove off-screen bullets and asteroids
            for bullet in bullet_group:
                if bullet.position[1] < -bullet.rect.height:
                    bullet_group.remove(bullet)
            for asteroid in asteroid_group:
                if asteroid.position[1] > self.cfg.SCREENSIZE[1]:
                    asteroid_group.remove(asteroid)

            # --Draw everything
            # Scrolling background
            self.background_y = (self.background_y + self.bg_scroll_speed) % self.cfg.SCREENSIZE[1]
            # Draw two background images to create a continuous loop
            self.screen.blit(self.resource_loader.images['seamless_space'], (0, self.background_y - self.cfg.SCREENSIZE[1]))
            self.screen.blit(self.resource_loader.images['seamless_space'], (0, self.background_y))


            # Draw bullets
            for bullet in bullet_group:
                bullet.move()
                bullet.draw(self.screen)
            
            # Draw asteroids
            for asteroid in asteroid_group:
                asteroid.move()
                asteroid.rotate()
                asteroid.draw(self.screen)
            
            # Draw players and handle explosions/lives
            active_players = []
            for player in player_group:
                if player.lives > 0 or player.explode_step > 0: # Still alive or animating explosion
                    active_players.append(player)
                
                if player.explode_step > 0: # If exploding
                    if player.explode(self.screen): # Explosion animation finished
                        if player.lives <= 0: # If no lives left, remove player
                            pass # Player will be removed from active_players if lives <= 0
                        else: # If lives left, player becomes invincible and continues
                            player.explode_step = 0 # Reset explode animation
                else: # Not exploding, draw normally
                    player.draw(self.screen)
            
            # Check for game over condition
            # The game ends if player1 has 0 lives and, in 2-player mode, player2 also has 0 lives.
            game_over = False
            if player1.lives <= 0:
                if self.game_type == 2:
                    if player2 is None or player2.lives <= 0: # Ensure player2 exists before checking lives
                        game_over = True
                else: # Single player
                    game_over = True

            if game_over:
                running = False # Exit the main game loop

            # --Display score and lives
            font_score = self.resource_loader.fonts['default_m']
            
            score_1_text = f'Player 1 Score: {score_1}'
            lives_1_text = f'Lives: {player1.lives}'
            text_1_score = font_score.render(score_1_text, True, (0, 0, 255))
            text_1_lives = font_score.render(lives_1_text, True, (0, 0, 255))
            self.screen.blit(text_1_score, (10, 10))
            self.screen.blit(text_1_lives, (10, 40))

            if self.game_type == 2 and player2:
                score_2_text = f'Player 2 Score: {score_2}'
                lives_2_text = f'Lives: {player2.lives}'
                text_2_score = font_score.render(score_2_text, True, (255, 0, 0))
                text_2_lives = font_score.render(lives_2_text, True, (255, 0, 0))
                self.screen.blit(text_2_score, (self.cfg.SCREENSIZE[0] - text_2_score.get_width() - 10, 10))
                self.screen.blit(text_2_lives, (self.cfg.SCREENSIZE[0] - text_2_lives.get_width() - 10, 40))

            pygame.display.update()
            clock.tick(self.cfg.FPS)

        # After the main game loop ends (game_over is True)
        pygame.mixer.music.stop() # Stop background music when game ends

        print("Calling EndInterface now...") # Diagnostic print
        restart = self.end(score_1, score_2 if self.game_type == 2 else None) #
        
        if restart: # If EndInterface returned True (Restart Game button clicked)
            print("Restarting game...")
            self.run()  # Recursively call run to restart the game
        else: # If EndInterface returned False (Quit Game button clicked)
            print("Quitting game...")
            QuitGame() # Call the utility function to quit Pygame and exit


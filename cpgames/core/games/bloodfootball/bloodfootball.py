
import os
import random
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import StartInterface, Player, Ball



class Config():
    
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 50
    
    SCREENSIZE = (769, 563)
    SCREENSIZE_GAMING = (1200, 800)
    
    TITLE = 'Hot Blood Football - Dannz'
    
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    LIGHTGREEN = (0, 100, 0)
    
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.flac')
    
    IMAGE_PATHS_DICT = {
        'players': [
            os.path.join(rootdir, 'resources/images/player1.png'),
            os.path.join(rootdir, 'resources/images/player2.png'),
            os.path.join(rootdir, 'resources/images/player3.png'),
            os.path.join(rootdir, 'resources/images/player4.png'),
        ],
        'balls': [
            os.path.join(rootdir, 'resources/images/ball1.png'),
            os.path.join(rootdir, 'resources/images/ball2.png'),
            os.path.join(rootdir, 'resources/images/ball3.png'),
        ],
        'doors': [
            os.path.join(rootdir, 'resources/images/door1.bmp'),
            os.path.join(rootdir, 'resources/images/door2.bmp'),
        ],
        'background_start': os.path.join(rootdir, 'resources/images/background_start.jpg'),
    }
    
    FONT_PATHS_DICT = {
        'default20': {'name': os.path.join(rootdir.replace('bloodfootball', 'base'), 'resources/fonts/simkai.ttf'), 'size': 20},
        'default30': {'name': os.path.join(rootdir.replace('bloodfootball', 'base'), 'resources/fonts/simkai.ttf'), 'size': 30},
        'default50': {'name': os.path.join(rootdir.replace('bloodfootball', 'base'), 'resources/fonts/simkai.ttf'), 'size': 50},
    }



class BloodFootballGame(PygameBaseGame):
    game_type = 'bloodfootball'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(BloodFootballGame, self).__init__(config=self.cfg, **kwargs)
    
    def run(self):
        
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        resource_loader.playbgm()
        
        StartInterface(screen, resource_loader, cfg)
        
        screen = pygame.display.set_mode(cfg.SCREENSIZE_GAMING)
        score_group1, score_group2 = 0, 0
        font = resource_loader.fonts['default30']
        while True:
            win_group = self.playonegame(screen, resource_loader, cfg, font.render(f'{score_group1}   {score_group2}', False, cfg.WHITE))
            assert win_group in [1, 2]
            if win_group == 1: score_group1 += 1
            else: score_group2 += 1
    
    def playonegame(self, screen, resource_loader, cfg, score_board):
        
        players_group1, players_group2 = pygame.sprite.Group(), pygame.sprite.Group()
        
        position = random.randint(250, 500), random.randint(350-25, 450-25)
        player_controlled = Player(resource_loader.images['players'][0], position, (1, 0), False, 'common', 1)
        players_group1.add(player_controlled)
        position = random.randint(250, 500), random.randint(50-25, 350-25)
        players_group1.add(Player(resource_loader.images['players'][1], position, (1, 0), True, 'upperhalf', 1))
        position = random.randint(250, 500), random.randint(450-25, 750-25)
        players_group1.add(Player(resource_loader.images['players'][1], position, (1, 0), True, 'bottomhalf', 1))
        position = (85, 390)
        players_group1.add(Player(resource_loader.images['players'][1], position, (0, 1), True, 'goalkeeper', 1))
        
        position = random.randint(700, 950), random.randint(350-25, 450-25)
        players_group2.add(Player(resource_loader.images['players'][2], position, (-1, 0), True, 'common', 2))
        position = random.randint(700, 950), random.randint(50-25, 350-25)
        players_group2.add(Player(resource_loader.images['players'][3], position, (-1, 0), True, 'upperhalf', 2))
        position = random.randint(700, 950), random.randint(450-25, 750-25)
        players_group2.add(Player(resource_loader.images['players'][3], position, (-1, 0), True, 'bottomhalf', 2))
        position = (1070, 390)
        players_group2.add(Player(resource_loader.images['players'][3], position, (0, 1), True, 'goalkeeper', 2))
        
        ball = Ball(resource_loader.images['balls'], (600, 400))
        
        clock = pygame.time.Clock()
        while True:
            
            screen.fill(cfg.LIGHTGREEN)
            pygame.draw.circle(screen, cfg.WHITE, (600, 400), 80, 5)
            pygame.draw.rect(screen, cfg.WHITE, (10, 10, 600, 790), 5)
            pygame.draw.rect(screen, cfg.WHITE, (600, 10, 590, 790), 5)
            pygame.draw.rect(screen, cfg.WHITE, (10, 150, 300, 500), 5)
            pygame.draw.rect(screen, cfg.WHITE, (890, 150, 300, 500), 5)
            screen.blit(resource_loader.images['doors'][0].convert(), (8, 305))
            screen.blit(resource_loader.images['doors'][1].convert(), (1121, 305))
            screen.blit(score_board, (565, 15))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    QuitGame()
            pressed_keys = pygame.key.get_pressed()
            direction = [0, 0]
            if pressed_keys[pygame.K_w]: direction[1] -= 1
            if pressed_keys[pygame.K_d]: direction[0] += 1
            if pressed_keys[pygame.K_s]: direction[1] += 1
            if pressed_keys[pygame.K_a]: direction[0] -= 1
            if direction != [0, 0]: player_controlled.setdirection(direction)
            if pressed_keys[pygame.K_SPACE] and player_controlled == ball.taken_by_player: 
                ball.kick(player_controlled.direction)
            
            for item in players_group1:
                if pygame.sprite.collide_mask(item, ball) and ball.taken_by_player != item: 
                    ball.is_moving = True
                    ball.taken_by_player = item
            for item in players_group2:
                if pygame.sprite.collide_mask(item, ball) and ball.taken_by_player != item: 
                    ball.is_moving = True
                    ball.taken_by_player = item
            for item in players_group1:
                item.update(cfg.SCREENSIZE_GAMING, ball)
            for item in players_group2:
                item.update(cfg.SCREENSIZE_GAMING, ball)
            
            ball.update(cfg.SCREENSIZE_GAMING)
            
            ball.draw(screen)
            players_group1.draw(screen)
            players_group2.draw(screen)
            clock.tick(cfg.FPS)
            pygame.display.update()
            
            if ball.rect.bottom > 305 and ball.rect.top < 505:
                if ball.rect.right > 1121: return 1
                elif ball.rect.left < 75: return 2
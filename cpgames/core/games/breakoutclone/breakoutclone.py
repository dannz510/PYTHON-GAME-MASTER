
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Paddle, Ball, Brick, loadLevel


class Config():

    rootdir = os.path.split(os.path.abspath(__file__))[0]

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PINK = (212, 149, 174) 
    PURPLE = (168, 152, 191)
    YELLOW = (245, 237, 162)
    BLUE  = (51, 170, 230)
    AQUA = (182, 225, 225)

    BRICKWIDTH = 10
    BRICKHEIGHT = 10
    PADDLEWIDTH = 60
    PADDLEHEIGHT = 12
    BALLRADIUS = 8

    SCREENSIZE = (640, 480)
    SCREENWIDTH = 640
    SCREENHEIGHT = 480

    TITLE = 'Brick Breaker Game - Dannz'
    # FPS
    FPS = 30
    FPS_GAMING = 50

    FONT_PATHS_DICT = {
        'default20': {'name': os.path.join(rootdir.replace('breakoutclone', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 20},
        'default30': {'name': os.path.join(rootdir.replace('breakoutclone', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 30},
    }

    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    
    SOUND_PATHS_DICT = {
        'hit': os.path.join(rootdir, 'resources/audios/hit.wav'),
    }
   
    LEVELROOTDIR = os.path.join(rootdir, 'resources/levels')
    LEVELPATHS = []
    for i in range(len(os.listdir(LEVELROOTDIR))):
        LEVELPATHS.append(os.path.join(LEVELROOTDIR, '%s.level' % str(i+1)))


class BreakoutcloneGame(PygameBaseGame):
    game_type = 'breakoutclone'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(BreakoutcloneGame, self).__init__(config=self.cfg, **kwargs)
        self.font_small = self.resource_loader.fonts['default20']
        self.font_big = self.resource_loader.fonts['default30']
  
    def run(self):
     
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        
        resource_loader.playbgm()
      
        while True:
            self.__startInterface()
            for idx, levelpath in enumerate(self.cfg.LEVELPATHS):
                state = self.__runLevel(levelpath)
                if idx == len(self.cfg.LEVELPATHS)-1:
                    break
                if state == 'win':
                    self.__nextLevel()
                else:
                    break
            if state == 'fail':
                self.__endInterface(False)
            else:
                self.__endInterface(True)
  
    def __runLevel(self, levelpath):
        score = 0
        num_lives = 2
  
        state = 'running'
        paddle = Paddle((self.cfg.SCREENWIDTH-self.cfg.PADDLEWIDTH)/2, self.cfg.SCREENHEIGHT-self.cfg.PADDLEHEIGHT-10, self.cfg.PADDLEWIDTH, self.cfg.PADDLEHEIGHT, self.cfg.SCREENWIDTH, self.cfg.SCREENHEIGHT)
        ball = Ball(paddle.rect.centerx-self.cfg.BALLRADIUS, paddle.rect.top-self.cfg.BALLRADIUS*2, self.cfg.BALLRADIUS, self.cfg.SCREENWIDTH, self.cfg.SCREENHEIGHT)
        brick_sprites = pygame.sprite.Group()
        brick_positions = loadLevel(levelpath)
        for bp in brick_positions:
            brick_sprites.add(Brick(bp[0]*self.cfg.BRICKWIDTH, bp[1]*self.cfg.BRICKHEIGHT, self.cfg.BRICKWIDTH, self.cfg.BRICKHEIGHT))
        clock = pygame.time.Clock()
        while True:
            if state != 'running':
                return state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                paddle.move('left')
            elif keys_pressed[pygame.K_RIGHT]:
                paddle.move('right')
            self.screen.fill(self.cfg.AQUA)
            is_alive = ball.move()
            
            if not is_alive:
                ball.reset()
                paddle.reset()
                num_lives -= 1
                if num_lives == 0:
                    state = 'fail'
           
            num_bricks = pygame.sprite.spritecollide(ball, brick_sprites, True)
            score += len(num_bricks)
       
            if pygame.sprite.collide_rect(ball, paddle):
                ball.change()
          
            if len(brick_sprites) == 0:
                state = 'win'
            
            paddle.draw(self.screen, self.cfg.PURPLE)
            ball.draw(self.screen, self.cfg.WHITE)
            for brick in brick_sprites:
                brick.draw(self.screen, self.cfg.YELLOW)
            text_render = self.font_small.render('SCORE: %s, LIVES: %s' % (score, num_lives), False, self.cfg.BLUE)
            self.screen.blit(text_render, (10, 10))
            pygame.display.flip()
            clock.tick(self.cfg.FPS_GAMING)
  
    def __nextLevel(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
            self.screen.fill(self.cfg.AQUA)
            text = 'Press <Enter> to enter the next level'
            text_render = self.font_big.render(text, False, self.cfg.BLUE)
            self.screen.blit(text_render, ((self.cfg.SCREENWIDTH-text_render.get_rect().width)//2, (self.cfg.SCREENHEIGHT-text_render.get_rect().height)//3))
            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    def __startInterface(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
            self.screen.fill(self.cfg.AQUA)
            text1 = 'Press <Enter> to start the game'
            text2 = 'Press <Esc> to quit the game'
            text_render1 = self.font_big.render(text1, False, self.cfg.BLUE)
            text_render2 = self.font_big.render(text2, False, self.cfg.BLUE)
            self.screen.blit(text_render1, ((self.cfg.SCREENWIDTH-text_render1.get_rect().width)//2, (self.cfg.SCREENHEIGHT-text_render1.get_rect().height)//4))
            self.screen.blit(text_render2, ((self.cfg.SCREENWIDTH-text_render2.get_rect().width)//2, (self.cfg.SCREENHEIGHT-text_render2.get_rect().height)//2))
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
   
    def __endInterface(self, is_win):
        if is_win:
            text1 = 'Congratulations! You win!'
        else:
            text1 = 'Game Over! You fail!'
        text2 = 'Press <R> to restart the game'
        text3 = 'Press <Esc> to quit the game.'
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return
            self.screen.fill(self.cfg.AQUA)
            text_render1 = self.font_big.render(text1, False, self.cfg.BLUE)
            text_render2 = self.font_big.render(text2, False, self.cfg.BLUE)
            text_render3 = self.font_big.render(text3, False, self.cfg.BLUE)
            self.screen.blit(text_render1, ((self.cfg.SCREENWIDTH-text_render1.get_rect().width)//2, (self.cfg.SCREENHEIGHT-text_render1.get_rect().height)//4))
            self.screen.blit(text_render2, ((self.cfg.SCREENWIDTH-text_render2.get_rect().width)//2, (self.cfg.SCREENHEIGHT-text_render2.get_rect().height)//2))
            self.screen.blit(text_render3, ((self.cfg.SCREENWIDTH-text_render3.get_rect().width)//2, (self.cfg.SCREENHEIGHT-text_render2.get_rect().height)//1.5))
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
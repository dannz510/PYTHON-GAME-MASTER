import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import showText, Button, Interface, Block, RandomMaze, Hero


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 20
    # 屏幕大小
    SCREENSIZE = (800, 625)
    # 标题
    TITLE = 'MAZE ADVENTURE' # Updated title
    # 块大小
    BLOCKSIZE = 15
    MAZESIZE = (35, 50) # num_rows * num_cols
    BORDERSIZE = (25, 50) # 25 * 2 + 50 * 15 = 800, 50 * 2 + 35 * 15 = 625
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'hero': os.path.join(rootdir, 'resources/images/hero.png'),
    }


'''走迷宫小游戏'''
class MazeGame(PygameBaseGame):
    game_type = 'maze'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MazeGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # Initialization
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        
        # Font for game info text
        game_info_font = pygame.font.SysFont('Consolas', 18, bold=True)
        game_info_color = (0, 0, 100) # Dark blue for game info text

        # Play background music
        resource_loader.playbgm()
        # Start interface
        Interface(screen, cfg, 'game_start')
        # Record level count
        num_levels = 0
        # Record best score
        best_scores = 'None'
        # Level loop
        while True:
            num_levels += 1
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode(cfg.SCREENSIZE)
            
            # --Randomly generate level map
            maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --Generate hero
            hero_now = Hero(resource_loader.images['hero'], [0, 0], cfg.BLOCKSIZE, cfg.BORDERSIZE)
            
            # Mark the starting block as visited by the hero to show the path immediately
            maze_now.blocks_list[hero_now.coordinate[1]][hero_now.coordinate[0]].is_path_visited = True
            
            # --Count steps
            num_steps = 0
            # --Main loop within the level
            while True:
                dt = clock.tick(cfg.FPS)
                screen.fill((200, 210, 220)) # Slightly darker background for main game
                is_move = False
                
                # ----Control hero
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        QuitGame()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            is_move = hero_now.move('up', maze_now)
                        elif event.key == pygame.K_DOWN:
                            is_move = hero_now.move('down', maze_now)
                        elif event.key == pygame.K_LEFT:
                            is_move = hero_now.move('left', maze_now)
                        elif event.key == pygame.K_RIGHT:
                            is_move = hero_now.move('right', maze_now)
                        
                        if is_move:
                            # Mark the new block as visited by the hero after it moves
                            maze_now.blocks_list[hero_now.coordinate[1]][hero_now.coordinate[0]].is_path_visited = True

                num_steps += int(is_move) # Update steps *after* potential move
                
                # Draw maze first, then hero on top
                maze_now.draw(screen)
                hero_now.draw(screen) # Draw hero after maze so it's on top and updates position

                # ----Display information
                showText(screen, game_info_font, 'LEVEL: %d' % num_levels, game_info_color, (10, 10))
                showText(screen, game_info_font, 'BEST SCORE: %s' % best_scores, game_info_color, (210, 10))
                showText(screen, game_info_font, 'STEPS: %s' % num_steps, game_info_color, (410, 10))
                
                # Add clearer instructions at the bottom
                showText(screen, game_info_font, 'Navigate with arrow keys!', (80, 80, 80), (10, 600))
                
                # ----Check if game is won
                if (hero_now.coordinate[0] == cfg.MAZESIZE[1] - 1) and (hero_now.coordinate[1] == cfg.MAZESIZE[0] - 1):
                    break
                pygame.display.update()
            
            # --Update best score
            if best_scores == 'None':
                best_scores = num_steps
            else:
                if best_scores > num_steps:
                    best_scores = num_steps
            # --Level transition
            Interface(screen, cfg, mode='game_switch')

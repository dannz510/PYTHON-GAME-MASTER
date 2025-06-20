import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import drawGameGrid, showScore, EndInterface, Apple, Snake, ParticleEffect


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 5
    # 屏幕大小
    SCREENSIZE = (800, 500)
    # 标题
    TITLE = 'Snake Game - Dannz'
    # 一些常量
    BLOCK_SIZE = 20
    BLACK = (0, 0, 0)
    # New Grid Color
    GRID_COLOR = (40, 40, 40) # A subtle dark grey for the grid lines
    GAME_MATRIX_SIZE = (int(SCREENSIZE[0]/BLOCK_SIZE), int(SCREENSIZE[1]/BLOCK_SIZE))

    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # Sound Effects
    EAT_SOUND_PATH = os.path.join(rootdir, 'resources/audios/eat.wav')
    GAMEOVER_SOUND_PATH = os.path.join(rootdir, 'resources/audios/gameover.wav')
    # NEW: SOUND_PATHS_DICT for PygameResourceLoader
    SOUND_PATHS_DICT = {
        'eat': EAT_SOUND_PATH,
        'gameover': GAMEOVER_SOUND_PATH,
    }

    # 字体路径
    FONT_PATHS_DICT = {
        # Ensure this path is correct relative to your overall project structure
        'score_font': {'name': os.path.join(rootdir.replace('greedysnake', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 50}, # Larger score font
        'default30': {'name': os.path.join(rootdir.replace('greedysnake', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 30},
        'default60': {'name': os.path.join(rootdir.replace('greedysnake', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 60},
    }

    # Snake Skins (Updated for procedural drawing)
    # Each 'head' and 'tail' list should contain 4 colors for inner/outer/highlight/shadow or eye parts.
    SNAKE_SKINS = {
        'default': {
            'head': [(0, 150, 255), (0, 200, 255), (0, 80, 255), (0, 255, 255)], # Outer, Inner, Eye Main, Eye Pupil
            'tail': [(0, 100, 0), (0, 150, 0), (0, 170, 0), (0, 70, 0)] # Outer, Inner, Highlight, Shadow
        },
        'red': {
            'head': [(255, 0, 0), (255, 50, 50), (150, 0, 0), (255, 255, 255)],
            'tail': [(180, 0, 0), (220, 0, 0), (250, 50, 50), (120, 0, 0)]
        },
        'green': {
            'head': [(0, 200, 0), (50, 255, 50), (0, 100, 0), (255, 255, 255)],
            'tail': [(0, 150, 0), (0, 190, 0), (50, 220, 50), (0, 100, 0)]
        },
        'purple': {
            'head': [(150, 0, 200), (200, 50, 255), (80, 0, 100), (255, 255, 255)],
            'tail': [(100, 0, 150), (140, 0, 190), (180, 50, 220), (70, 0, 100)]
        },
        # Add more skin options with 4 colors for head and 4 for tail
    }
    DEFAULT_SKIN = 'default' # Set the default skin

    # Background Colors for procedural drawing (New)
    BACKGROUND_COLOR_START = (20, 30, 60)   # Dark blue/purple
    BACKGROUND_COLOR_END = (60, 80, 120)    # Lighter blue/purple

    # Icon path for the game window (New - since seticons was removed from GreedySnakeGame's __init__)
    ICON_PATH = os.path.join(rootdir, 'resources/images/icon.png')


'''贪吃蛇小游戏'''
class GreedySnakeGame(PygameBaseGame):
    game_type = 'greedysnake'
    def __init__(self, **kwargs):
        self.cfg = Config
        # Pass the config object to the parent class's __init__.
        # PygameBaseGame should handle setting title, icon, and loading resources based on this config.
        super(GreedySnakeGame, self).__init__(config=self.cfg, **kwargs) 
        
        # Removed explicit self.settitle, self.seticons, and self.loadresources calls here.
        # These operations are expected to be handled by PygameBaseGame's __init__ using the 'config' passed.
        # Ensure PygameBaseGame's __init__ uses cfg.TITLE, cfg.ICON_PATH, cfg.BGM_PATH, etc.
        # If PygameBaseGame doesn't automatically load resources from config, 
        # you might need to adjust PygameBaseGame's __init__ or add a `resource_loader` attribute
        # and call its `loadresources` method directly, e.g., self.resource_loader.loadresources(...)
        # if self.resource_loader is initialized in PygameBaseGame. For now, assume it's handled.


    '''运行游戏'''
    def run(self):
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 游戏主循环
        while True:
            if not self.GamingInterface(screen, resource_loader, cfg):
                break

    '''Draws a linear gradient background (New)'''
    def draw_procedural_background(self, screen, cfg):
        start_color = cfg.BACKGROUND_COLOR_START
        end_color = cfg.BACKGROUND_COLOR_END
        width, height = cfg.SCREENSIZE

        # Draw a linear gradient from top to bottom
        for y in range(height):
            # Interpolate colors based on y position
            r = int(start_color[0] + (end_color[0] - start_color[0]) * y / height)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * y / height)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * y / height)
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    '''游戏运行界面'''
    def GamingInterface(self, screen, resource_loader, cfg):
        # 播放背景音乐
        resource_loader.playbgm()

        # 游戏主循环
        snake = Snake(cfg, skin=cfg.DEFAULT_SKIN) # Pass the selected skin
        apple = Apple(cfg, snake.coords)
        score = 0
        clock = pygame.time.Clock()

        # Particle effects group
        all_particles = pygame.sprite.Group()

        while True:
            self.draw_procedural_background(screen, cfg) # Draw procedural background

            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.K_ESCAPE: # Added ESCAPE to quit
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]: # Added WASD
                        key_map = {
                            pygame.K_UP: 'up', pygame.K_w: 'up',
                            pygame.K_DOWN: 'down', pygame.K_s: 'down',
                            pygame.K_LEFT: 'left', pygame.K_a: 'left',
                            pygame.K_RIGHT: 'right', pygame.K_d: 'right'
                        }
                        snake.setDirection(key_map[event.key])

            # --更新贪吃蛇和食物
            if snake.update(apple):
                resource_loader.playsound('eat') # Play eat sound
                # Create particle effect when apple is eaten
                apple_center_grid = apple.get_center_grid_coords() # Get grid coordinates from Apple object
                for _ in range(20): # Generate 20 particles
                    all_particles.add(ParticleEffect(apple_center_grid, cfg.BLOCK_SIZE, apple.color)) # Use Apple's color
                apple = Apple(cfg, snake.coords)
                score += 1
                cfg.FPS = min(15, cfg.FPS + 0.5) # Increase speed dynamically, max 15 FPS
            
            # Update and draw particles
            all_particles.update()
            all_particles.draw(screen) # Particles are drawn as sprites

            # --判断游戏是否结束
            if snake.isgameover: 
                resource_loader.playsound('gameover') # Play game over sound
                break

            # --显示游戏里必要的元素
            drawGameGrid(cfg, screen) # Draw grid over background/particles
            snake.draw(screen)
            apple.draw(screen)
            showScore(cfg, score, screen, resource_loader)
            
            pygame.display.flip()
            clock.tick(cfg.FPS)
        
        # Game over interface
        return EndInterface(screen, cfg, resource_loader, score) # Pass score to EndInterface
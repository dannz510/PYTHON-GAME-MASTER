# minesweeper.py

import os
import time
import pygame
# Corrected import for QuitGame: go up two levels from current directory
from ...utils import QuitGame 
# Assuming PygameBaseGame is available in the parent directory of 'minesweeper'
from ..base import PygameBaseGame
from .modules import Mine, TextBoard, MinesweeperMap, EmojiButton


'''Configuration Class'''
class Config():
    # Root directory for resources
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    
    # Define modern color palette
    # Background color for the game window - a very light, almost white grey
    BACKGROUND_COLOR = (235, 235, 235) 
    # Red for text (e.g., mine count, time) - a slightly deeper red for contrast
    RED = (220, 30, 30)
    
    # Colors for 3D effects on buttons/cells - softer, more harmonious grays
    LIGHT_GREY = (245, 245, 245) # Top/left highlight for raised buttons - almost white
    DARK_GREY = (170, 170, 170)  # Bottom/right shadow for raised buttons - a medium grey
    PRESSED_DARK = (190, 190, 190) # Top/left shadow for pressed/sunken buttons - slightly darker than BACKGROUND_COLOR
    PRESSED_LIGHT = (250, 250, 250) # Bottom/right highlight for pressed/sunken buttons - almost pure white for subtle highlight
    BORDER_COLOR = (120, 120, 120) # Outer border for main game area - a stronger, defined grey

    # Frames per second
    FPS = 60
    # Grid cell size in pixels
    GRIDSIZE = 24 
    # Number of mines
    NUM_MINES = 40 
    # Game matrix dimensions (width, height)
    GAME_MATRIX_SIZE = (16, 16) 
    # Border size around the game area
    BORDERSIZE = 10 
    # Screen dimensions based on grid and border sizes
    SCREENSIZE = (GAME_MATRIX_SIZE[0] * GRIDSIZE + BORDERSIZE * 2, 
                  (GAME_MATRIX_SIZE[1] + 2) * GRIDSIZE + BORDERSIZE)
    # Window title
    TITLE = 'Minesweeper Reimagined'
    # Background music path (ensure this path is correct relative to your project)
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # Font paths dictionary
    FONT_PATHS_DICT = {
        'default': {'name': os.path.join(rootdir, 'resources/fonts/font.ttf'), 'size': 40},
    }
    # Game image paths (assuming these exist in your resources folder)
    IMAGE_PATHS_DICT = {
        '0': os.path.join(rootdir, 'resources/images/0.bmp'),
        '1': os.path.join(rootdir, 'resources/images/1.bmp'),
        '2': os.path.join(rootdir, 'resources/images/2.bmp'),
        '3': os.path.join(rootdir, 'resources/images/3.bmp'),
        '4': os.path.join(rootdir, 'resources/images/4.bmp'),
        '5': os.path.join(rootdir, 'resources/images/5.bmp'),
        '6': os.path.join(rootdir, 'resources/images/6.bmp'),
        '7': os.path.join(rootdir, 'resources/images/7.bmp'),
        '8': os.path.join(rootdir, 'resources/images/8.bmp'),
        'ask': os.path.join(rootdir, 'resources/images/ask.bmp'),
        'blank': os.path.join(rootdir, 'resources/images/blank.bmp'),
        'blood': os.path.join(rootdir, 'resources/images/blood.bmp'),
        'error': os.path.join(rootdir, 'resources/images/error.bmp'),
        'face_fail': os.path.join(rootdir, 'resources/images/face_fail.png'),
        'face_normal': os.path.join(rootdir, 'resources/images/face_normal.png'),
        'face_success': os.path.join(rootdir, 'resources/images/face_success.png'),
        'flag': os.path.join(rootdir, 'resources/images/flag.bmp'),
        'mine': os.path.join(rootdir, 'resources/images/mine.bmp')
    }


'''Minesweeper Game Class'''
class MineSweeperGame(PygameBaseGame):
    game_type = 'minesweeper'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MineSweeperGame, self).__init__(config=self.cfg, **kwargs)
    
    '''Run the game loop'''
    def run(self):
        # Initialize screen, resource loader, and config
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        
        # Load and scale all images
        images = resource_loader.images
        for key, image in images.items():
            # Special scaling for emoji faces to maintain aspect ratio and fit
            if key in ['face_fail', 'face_normal', 'face_success']:
                images[key] = pygame.transform.smoothscale(image, (int(cfg.GRIDSIZE*1.5), int(cfg.GRIDSIZE*1.5)))
            else:
                # Convert for faster blitting and smoothscale for general images
                image = image.convert_alpha() # Use convert_alpha for images with transparency
                images[key] = pygame.transform.smoothscale(image, (cfg.GRIDSIZE, cfg.GRIDSIZE))
        
        # Load font
        font = resource_loader.fonts['default']
        
        # Play background music
        resource_loader.playbgm()
        
        # Instantiate game map
        minesweeper_map = MinesweeperMap(cfg, images)
        
        # Calculate position for the emoji button (centered in the top bar)
        emoji_button_size = (int(cfg.GRIDSIZE * 1.5), int(cfg.GRIDSIZE * 1.5))
        position = (cfg.SCREENSIZE[0] - emoji_button_size[0]) // 2, (cfg.GRIDSIZE * 2 - emoji_button_size[1]) // 2
        emoji_button = EmojiButton(images, position=position, size=emoji_button_size)
        
        # Initialize remaining mines display
        fontsize_mines = font.size(str(cfg.NUM_MINES))
        remaining_mine_board = TextBoard(str(cfg.NUM_MINES), font, 
                                        (cfg.BORDERSIZE + 10, (cfg.GRIDSIZE * 2 - fontsize_mines[1]) // 2 - 2), cfg.RED)
        
        # Initialize time display
        fontsize_time = font.size('000')
        time_board = TextBoard('000', font, 
                               (cfg.SCREENSIZE[0] - cfg.BORDERSIZE - fontsize_time[0] - 10, (cfg.GRIDSIZE * 2 - fontsize_time[1]) // 2 - 2), cfg.RED)
        time_board.is_start = False
        
        # Game main loop
        clock = pygame.time.Clock()
        while True:
            screen.fill(cfg.BACKGROUND_COLOR)
            
            # Draw the main game area border
            pygame.draw.rect(screen, cfg.BORDER_COLOR, 
                             (cfg.BORDERSIZE - 2, cfg.GRIDSIZE * 2 - 2, 
                              cfg.GAME_MATRIX_SIZE[0] * cfg.GRIDSIZE + 4, 
                              cfg.GAME_MATRIX_SIZE[1] * cfg.GRIDSIZE + 4), 2)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    mouse_pressed = pygame.mouse.get_pressed()
                    minesweeper_map.update(mouse_pressed=mouse_pressed, mouse_pos=mouse_pos, type_='down')
                elif event.type == pygame.MOUSEBUTTONUP:
                    minesweeper_map.update(type_='up')
                    # Reset game if emoji button is clicked
                    if emoji_button.rect.collidepoint(pygame.mouse.get_pos()):
                        minesweeper_map = MinesweeperMap(cfg, images)
                        time_board.update('000')
                        time_board.is_start = False
                        remaining_mine_board.update(str(cfg.NUM_MINES))
                        emoji_button.setstatus(status_code=0)
            
            # Update time display
            if minesweeper_map.gaming:
                if not time_board.is_start:
                    start_time = time.time()
                    time_board.is_start = True
                time_board.update(str(int(time.time() - start_time)).zfill(3))
            
            # Update remaining mines display
            remianing_mines = max(cfg.NUM_MINES - minesweeper_map.flags, 0)
            remaining_mine_board.update(str(remianing_mines).zfill(2))
            
            # Update emoji button status based on game state
            if minesweeper_map.status_code == 1: # Game over (loss)
                emoji_button.setstatus(status_code=1)
            # Check for win condition
            if minesweeper_map.openeds + minesweeper_map.flags == cfg.GAME_MATRIX_SIZE[0] * cfg.GAME_MATRIX_SIZE[1] and minesweeper_map.status_code != 1:
                minesweeper_map.status_code = 2 # Set to win status
                emoji_button.setstatus(status_code=2)
            
            # Draw game elements
            minesweeper_map.draw(screen)
            emoji_button.draw(screen)
            remaining_mine_board.draw(screen)
            time_board.draw(screen)
            
            # Update the entire screen
            pygame.display.update()
            # Control frame rate
            clock.tick(cfg.FPS)

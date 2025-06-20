# sokoban.py
import os
import pygame
from itertools import chain
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import pusherSprite, elementSprite, startInterface, endInterface, switchInterface


'''Config class'''
class Config():
    # Root directory
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    FPS_GAMING = 100
    # Screen size
    SCREENSIZE = (800, 600)  # Increased screen size for better aesthetics
    # Title
    TITLE = 'The Crate Escape'
    # Block size
    BLOCKSIZE = 60 # Adjusted block size
    # Background color - A darker, more modern grey
    BACKGROUNDCOLOR = (30, 30, 30)
    # Levels directory
    LEVELDIR = os.path.join(rootdir, 'resources/levels')
    # Background music path
    BGM_PATH = os.path.join(rootdir, 'resources/audios/EineLiebe.mp3') # Consider a more upbeat/puzzle-like BGM
    # Font paths
    FONT_PATHS_DICT = {
        'default_15': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 15},
        'default_30': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 36}, # Slightly larger
        'default_50': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 60}, # Slightly larger
        'title': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 80}, # New font size for titles
    }
    # Game image paths - Placeholder, ideally these would be higher resolution and more stylized
    IMAGE_PATHS_DICT = {
        'box': os.path.join(rootdir, 'resources/images/box_modern.png'), # Assuming new images
        'player': os.path.join(rootdir, 'resources/images/player_modern.png'), # Assuming new images
        'target': os.path.join(rootdir, 'resources/images/target_modern.png'), # Assuming new images
        'wall': os.path.join(rootdir, 'resources/images/wall_modern.png'), # Assuming new images
        'background_game': os.path.join(rootdir, 'resources/images/game_bg.png'), # New background for the game map
        'background_menu': os.path.join(rootdir, 'resources/images/menu_bg.png'), # New background for menus
    }


'''GameMap class'''
class GameMap():
    def __init__(self, num_cols, num_rows, cfg, resource_loader):
        self.cfg = cfg
        self.resource_loader = resource_loader
        self.walls = []
        self.boxes = []
        self.targets = []
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.game_background = resource_loader.images.get('background_game')
        if self.game_background:
            self.game_background = pygame.transform.scale(self.game_background, (num_cols * cfg.BLOCKSIZE, num_rows * cfg.BLOCKSIZE))

    '''Add game element'''
    def addElement(self, elem_type, col, row):
        if elem_type == 'wall':
            self.walls.append(elementSprite('wall', col, row, self.cfg, self.resource_loader))
        elif elem_type == 'box':
            self.boxes.append(elementSprite('box', col, row, self.cfg, self.resource_loader))
        elif elem_type == 'target':
            self.targets.append(elementSprite('target', col, row, self.cfg, self.resource_loader))

    '''Draw game map'''
    def draw(self, screen):
        if self.game_background:
            screen.blit(self.game_background, (0, 0))
        else:
            screen.fill(self.cfg.BACKGROUNDCOLOR) # Fallback if no background image

        for elem in self.elemsIter():
            elem.draw(screen)

    '''Game element iterator'''
    def elemsIter(self):
        # Draw targets first so boxes can cover them
        for elem in chain(self.targets, self.walls, self.boxes):
            yield elem

    '''Check if level is completed'''
    def levelCompleted(self):
        for box in self.boxes:
            is_match = False
            for target in self.targets:
                if box.col == target.col and box.row == target.row:
                    is_match = True
                    break
            if not is_match:
                return False
        return True

    '''Check if position is valid'''
    def isValidPos(self, col, row):
        if 0 <= col < self.num_cols and 0 <= row < self.num_rows:
            block_size = self.cfg.BLOCKSIZE
            # Create temporary rect for collision detection
            temp_rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)

            # Check for collisions with walls
            for wall in self.walls:
                if temp_rect.colliderect(wall.rect):
                    return False
            # Check for collisions with boxes (except for the one being pushed, handled separately)
            for box in self.boxes:
                if temp_rect.colliderect(box.rect):
                    return False
            return True
        else:
            return False

    '''Get box at a given position'''
    def getBox(self, col, row):
        for box in self.boxes:
            if box.col == col and box.row == row:
                return box
        return None


'''GameInterface class'''
class GameInterface():
    def __init__(self, screen, cfg, resource_loader):
        self.cfg = cfg
        self.resource_loader = resource_loader
        self.screen = screen
        self.levels_path = cfg.LEVELDIR
        self.initGame()

    '''Load level map'''
    def loadLevel(self, game_level):
        with open(os.path.join(self.levels_path, game_level), 'r') as f:
            lines = f.readlines()
        # Game map dimensions
        self.game_map = GameMap(max([len(line) for line in lines]) - 1, len(lines), self.cfg, self.resource_loader)
        # Game surface
        height = self.cfg.BLOCKSIZE * self.game_map.num_rows
        width = self.cfg.BLOCKSIZE * self.game_map.num_cols
        self.game_surface = pygame.Surface((width, height))
        self.game_surface.fill(self.cfg.BACKGROUNDCOLOR) # This will be covered by game_map.draw's background or elements
        self.game_surface_blank = self.game_surface.copy()

        for row, elems in enumerate(lines):
            for col, elem in enumerate(elems.strip()): # .strip() to remove newline characters
                if elem == 'p':
                    self.player = pusherSprite(col, row, self.cfg, self.resource_loader)
                elif elem == '*':
                    self.game_map.addElement('wall', col, row)
                elif elem == '#':
                    self.game_map.addElement('box', col, row)
                elif elem == 'o':
                    self.game_map.addElement('target', col, row)

    '''Game initialization'''
    def initGame(self):
        self.scroll_x = 0
        self.scroll_y = 0

    '''Draw game interface'''
    def draw(self, *elems):
        self.scroll()
        self.game_surface.blit(self.game_surface_blank, dest=(0, 0)) # Clear the game surface

        self.game_map.draw(self.game_surface) # Draw the map elements (including its background)
        self.player.draw(self.game_surface) # Draw the player

        # Draw other specified elements (if any, though player and map cover most)
        for elem in elems:
            if elem != self.player and elem != self.game_map:
                elem.draw(self.game_surface)

        self.screen.blit(self.game_surface, dest=(self.scroll_x, self.scroll_y))

    '''Scroll game interface based on player position'''
    def scroll(self):
        player_screen_x = self.player.rect.x + self.scroll_x
        player_screen_y = self.player.rect.y + self.scroll_y

        # Define a "dead zone" in the center of the screen
        dead_zone_width = self.cfg.SCREENSIZE[0] * 0.4
        dead_zone_height = self.cfg.SCREENSIZE[1] * 0.4
        dead_zone_left = (self.cfg.SCREENSIZE[0] - dead_zone_width) / 2
        dead_zone_right = dead_zone_left + dead_zone_width
        dead_zone_top = (self.cfg.SCREENSIZE[1] - dead_zone_height) / 2
        dead_zone_bottom = dead_zone_top + dead_zone_height

        # Calculate map boundaries in screen coordinates
        map_width_on_screen = self.game_map.num_cols * self.cfg.BLOCKSIZE
        map_height_on_screen = self.game_map.num_rows * self.cfg.BLOCKSIZE

        # Horizontal scrolling
        if player_screen_x < dead_zone_left:
            self.scroll_x += int(abs(player_screen_x - dead_zone_left) * 0.1) # Smooth scroll
        elif player_screen_x + self.player.rect.width > dead_zone_right:
            self.scroll_x -= int(abs((player_screen_x + self.player.rect.width) - dead_zone_right) * 0.1) # Smooth scroll

        # Vertical scrolling
        if player_screen_y < dead_zone_top:
            self.scroll_y += int(abs(player_screen_y - dead_zone_top) * 0.1) # Smooth scroll
        elif player_screen_y + self.player.rect.height > dead_zone_bottom:
            self.scroll_y -= int(abs((player_screen_y + self.player.rect.height) - dead_zone_bottom) * 0.1) # Smooth scroll

        # Clamp scroll to ensure the map edges don't go beyond screen
        self.scroll_x = max(min(self.scroll_x, 0), self.cfg.SCREENSIZE[0] - map_width_on_screen)
        self.scroll_y = max(min(self.scroll_y, 0), self.cfg.SCREENSIZE[1] - map_height_on_screen)


'''SokobanGame class'''
class SokobanGame(PygameBaseGame):
    game_type = 'sokoban'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(SokobanGame, self).__init__(config=self.cfg, **kwargs)

    '''Run game'''
    def run(self):
        # Initialization
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # Play background music
        resource_loader.playbgm()
        # Game start interface
        startInterface(screen, cfg, resource_loader)
        # Game levels
        for level_name in sorted(os.listdir(cfg.LEVELDIR)):
            self.runlevel(screen, level_name)
            switchInterface(screen, cfg, resource_loader)
        # Game end interface
        endInterface(screen, cfg, resource_loader)

    '''Main loop for a single level'''
    def runlevel(self, screen, game_level):
        clock = pygame.time.Clock()
        game_interface = GameInterface(screen, self.cfg, self.resource_loader)
        game_interface.loadLevel(game_level)
        text = 'Press R to restart | Level: ' + game_level.split('.')[0] # Display current level
        font = self.resource_loader.fonts['default_15']
        
        while True:
            screen.fill(self.cfg.BACKGROUNDCOLOR) # Clear screen for general UI elements

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    player_moved = False
                    if event.key == pygame.K_LEFT:
                        next_player_pos = game_interface.player.move('left', is_test=True)
                        if game_interface.game_map.isValidPos(*next_player_pos):
                            game_interface.player.move('left')
                            player_moved = True
                        else:
                            box = game_interface.game_map.getBox(*next_player_pos)
                            if box:
                                next_box_pos = box.move('left', is_test=True)
                                if game_interface.game_map.isValidPos(*next_box_pos):
                                    game_interface.player.move('left')
                                    box.move('left')
                                    player_moved = True
                    elif event.key == pygame.K_RIGHT:
                        next_player_pos = game_interface.player.move('right', is_test=True)
                        if game_interface.game_map.isValidPos(*next_player_pos):
                            game_interface.player.move('right')
                            player_moved = True
                        else:
                            box = game_interface.game_map.getBox(*next_player_pos)
                            if box:
                                next_box_pos = box.move('right', is_test=True)
                                if game_interface.game_map.isValidPos(*next_box_pos):
                                    game_interface.player.move('right')
                                    box.move('right')
                                    player_moved = True
                    elif event.key == pygame.K_DOWN:
                        next_player_pos = game_interface.player.move('down', is_test=True)
                        if game_interface.game_map.isValidPos(*next_player_pos):
                            game_interface.player.move('down')
                            player_moved = True
                        else:
                            box = game_interface.game_map.getBox(*next_player_pos)
                            if box:
                                next_box_pos = box.move('down', is_test=True)
                                if game_interface.game_map.isValidPos(*next_box_pos):
                                    game_interface.player.move('down')
                                    box.move('down')
                                    player_moved = True
                    elif event.key == pygame.K_UP:
                        next_player_pos = game_interface.player.move('up', is_test=True)
                        if game_interface.game_map.isValidPos(*next_player_pos):
                            game_interface.player.move('up')
                            player_moved = True
                        else:
                            box = game_interface.game_map.getBox(*next_player_pos)
                            if box:
                                next_box_pos = box.move('up', is_test=True)
                                if game_interface.game_map.isValidPos(*next_box_pos):
                                    game_interface.player.move('up')
                                    box.move('up')
                                    player_moved = True
                    elif event.key == pygame.K_r:
                        game_interface.initGame()
                        game_interface.loadLevel(game_level)
                    
                    # Add a slight delay after player moves for smoother animation (if not already handled by clock.tick)
                    # if player_moved:
                    #     pygame.time.wait(50) # Small delay to see movement more clearly

            game_interface.draw(game_interface.player, game_interface.game_map) # Pass player and map for drawing

            if game_interface.game_map.levelCompleted():
                return

            text_render = font.render(text, 1, (255, 255, 255))
            screen.blit(text_render, (10, 10)) # Position the text at top-left corner

            pygame.display.flip()
            clock.tick(self.cfg.FPS_GAMING)
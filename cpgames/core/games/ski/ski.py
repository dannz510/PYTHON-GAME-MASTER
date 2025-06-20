import os
import sys 
import pygame
import random
import re

# Changed relative imports to absolute imports from the dzgames package root
from ...utils import QuitGame
from ..base import PygameBaseGame

# Initialize Pygame globally at the very beginning of the script
# This ensures pygame.display.Info() can be called safely in Config
pygame.init()


'''Configuration Class'''
class Config():
    # Base directory for the current skii.py file.
    # This resolves to: C:\Users\Anh Duc\Documents\GitHub\dzgames\dzgames\core\games\ski
    current_ski_game_dir = os.path.split(os.path.abspath(__file__))[0]
    
    # Base directory for the 'base' game resources.
    # From current_ski_game_dir (dzgames/core/games/ski), go up one level ('..') to reach 'dzgames/core/games',
    # then navigate into 'base'.
    base_game_resources_dir = os.path.join(os.path.dirname(current_ski_game_dir), 'base', 'resources')

    FPS = 40
    # Initial Screen size - Will be dynamic based on display info and resizable
    # Use pygame.display.Info() to get current screen resolution for initial setup
    DISPLAY_INFO = pygame.display.Info()
    # Start with a windowed size that's 80% of screen height, maintaining aspect ratio
    INITIAL_SCREEN_HEIGHT = int(DISPLAY_INFO.current_h * 0.8)
    INITIAL_SCREEN_WIDTH = int(DISPLAY_INFO.current_w * 0.8) 
    
    # Cap initial width/height to avoid issues on very small screens, min 800x600
    SCREENSIZE = (max(800, INITIAL_SCREEN_WIDTH), max(600, INITIAL_SCREEN_HEIGHT))

    # Title
    TITLE = 'Ski Game - Dannz'
    # Game image paths: now correctly relative to the ski game's directory
    IMAGE_PATHS_DICT = {
        'background': os.path.join(current_ski_game_dir, 'resources', 'images', 'background.png'),
        'env_map': os.path.join(current_ski_game_dir, 'resources', 'images', 'env_map.png'),
        'skiers_map': os.path.join(current_ski_game_dir, 'resources', 'images', 'skiers_map.png'),
    }
    # Path to skiers.txt for sprite data - Assuming it's in resources/images relative to skii.py
    SKIER_DATA_PATH = os.path.join(current_ski_game_dir, 'resources', 'images', 'skiers.txt') 

    # Background music path: relative to skii.py's directory
    BGM_PATH = os.path.join(current_ski_game_dir, 'resources', 'audios', 'bgm.mp3')
    
    # Font paths: use the base_game_resources_dir
    FONT_PATHS_DICT = {
        'large': {'name': os.path.join(base_game_resources_dir, 'fonts', 'simkai.ttf'), 'size': SCREENSIZE[0] // 5},
        'medium': {'name': os.path.join(base_game_resources_dir, 'fonts', 'simkai.ttf'), 'size': SCREENSIZE[0] // 30},
        'small': {'name': os.path.join(base_game_resources_dir, 'fonts', 'simkai.ttf'), 'size': SCREENSIZE[0] // 20},
        'button': {'name': os.path.join(base_game_resources_dir, 'fonts', 'simkai.ttf'), 'size': SCREENSIZE[0] // 45},
        'default': {'name': os.path.join(base_game_resources_dir, 'fonts', 'simkai.ttf'), 'size': 30},
    }



    # Data for subsurfacing from env_map.png (from game.txt)
    ENV_MAP_SPRITES = {
        'heart': {'x': 0, 'y': 1, 'w': 25, 'h': 22}, 
        'heart_loss': {'x': 0, 'y': 25, 'w': 23, 'h': 22},
        'power': {'x': 25, 'y': 0, 'w': 22, 'h': 25},
        'power_loss': {'x': 25, 'y': 25, 'w': 21, 'h': 22},
        'defense': {'x': 49, 'y': 1, 'w': 21, 'h': 22},
        'defense_loss': {'x': 48, 'y': 30, 'w': 24, 'h': 12},
        'coin_count': {'x': 74, 'y': 2, 'w': 20, 'h': 20},
        'snowflake1': {'x': 105, 'y': 32, 'w': 9, 'h': 11},
        'snowflake2': {'x': 139, 'y': 28, 'w': 25, 'h': 28},
        'snowflake3': {'x': 200, 'y': 33, 'w': 26, 'h': 18},
        'snowflake4': {'x': 249, 'y': 35, 'w': 32, 'h': 23},
        'snowflake5': {'x': 310, 'y': 25, 'w': 33, 'h': 31},
        'snowflake6': {'x': 361, 'y': 36, 'w': 17, 'h': 15},
        'slippery_warning': {'x': 395, 'y': 0, 'w': 43, 'h': 60}, 
        'jumping_slide_area': {'x': 458, 'y': 0, 'w': 45, 'h': 59},
        'wind_flag': {'x': 532, 'y': 1, 'w': 31, 'h': 54},
        'red_panel': {'x': 582, 'y': 0, 'w': 48, 'h': 65},
        'camping_fire': {'x': 640, 'y': 23, 'w': 65, 'h': 36},
        'snowboard1': {'x': 713, 'y': 7, 'w': 47, 'h': 48},
        'snowboard2': {'x': 777, 'y': 2, 'w': 43, 'h': 53},
        'bin': {'x': 834, 'y': 13, 'w': 60, 'h': 43},
        'tree_trunk': {'x': 896, 'y': 29, 'w': 59, 'h': 28},
        'slide_to_jump_1': {'x': 959, 'y': 0, 'w': 66, 'h': 56}, 
        'energy1': {'x': 1039, 'y': 7, 'w': 39, 'h': 55},
        'heart1': {'x': 1096, 'y': 12, 'w': 48, 'h': 52},
        'skier1_bot': {
            'images': [
                {'x': 1104, 'y': 73, 'w': 38, 'h': 47}, # forward
                {'x': 1163, 'y': 2, 'w': 41, 'h': 61},  # left_turning
                {'x': 1224, 'y': 2, 'w': 45, 'h': 62},  # right_turning
            ],
            'fall': {'x': 1282, 'y': 7, 'w': 59, 'h': 57}
        },
        'rabbit_animated': [
            {'x': 1359, 'y': 76, 'w': 37, 'h': 52}, # rabit_jump1
            {'x': 1355, 'y': 147, 'w': 37, 'h': 43}, # rabit_jump2
            {'x': 1350, 'y': 222, 'w': 28, 'h': 30}, # rabit_stand
            {'x': 578, 'y': 418, 'w': 24, 'h': 28},  # rabit_object
        ],
        'squirrel_animated': [
            {'x': 1437, 'y': 14, 'w': 30, 'h': 46},  # squirrel_jump1
            {'x': 1429, 'y': 77, 'w': 32, 'h': 49},  # squirrel_jump2
            {'x': 1410, 'y': 146, 'w': 32, 'h': 43}, # squirrel_jump3
            {'x': 1411, 'y': 230, 'w': 24, 'h': 22}, # squirrel_stand
            {'x': 610, 'y': 423, 'w': 30, 'h': 21},  # squirrel_object
        ],
        'wolf_animated': [
            {'x': 1489, 'y': 34, 'w': 28, 'h': 26},  # wolf_in_snow
            {'x': 1489, 'y': 85, 'w': 29, 'h': 42},  # wolf__head_out_snow1
            {'x': 1489, 'y': 159, 'w': 31, 'h': 28}, # wolf__head_out_snow_close_eyes
            {'x': 1488, 'y': 223, 'w': 29, 'h': 27}, # wolf__head_out_snow_open_eyes
        ],
        'dog_animated': [
            {'x': 1044, 'y': 285, 'w': 26, 'h': 24},  # dog
            {'x': 1039, 'y': 327, 'w': 37, 'h': 48},  # dog_sound1
            {'x': 1040, 'y': 390, 'w': 36, 'h': 50},  # dog_sound2
            {'x': 1035, 'y': 455, 'w': 42, 'h': 48},  # dog_sound3
        ],
        'polar_bear': {'x': 1537, 'y': 201, 'w': 62, 'h': 53},

        'monster_animated_states': {
            'in_snow': [
                {'x': 1089, 'y': 320, 'w': 63, 'h': 61},
                {'x': 1087, 'y': 386, 'w': 67, 'h': 60},
                {'x': 1088, 'y': 448, 'w': 67, 'h': 68},
            ],
            'chase': [
                {'x': 1182, 'y': 280, 'w': 78, 'h': 102},
                {'x': 1307, 'y': 282, 'w': 77, 'h': 100},
                {'x': 1433, 'y': 281, 'w': 75, 'h': 99},
                {'x': 1562, 'y': 280, 'w': 77, 'h': 101},
                {'x': 1698, 'y': 284, 'w': 65, 'h': 93},
                {'x': 1814, 'y': 281, 'w': 90, 'h': 101},
            ],
            'catch': [
                {'x': 1180, 'y': 393, 'w': 72, 'h': 113},
                {'x': 1307, 'y': 396, 'w': 72, 'h': 111},
                {'x': 1438, 'y': 390, 'w': 68, 'h': 117},
                {'x': 1561, 'y': 395, 'w': 78, 'h': 112},
                {'x': 1691, 'y': 415, 'w': 76, 'h': 91},
                {'x': 1818, 'y': 409, 'w': 79, 'h': 109},
            ]
        },
        'edgecoin_animated': [
            {'x': 978, 'y': 331, 'w': 29, 'h': 51},
            {'x': 979, 'y': 396, 'w': 26, 'h': 53},
            {'x': 976, 'y': 459, 'w': 32, 'h': 56},
        ],
        'snow1_land1': {'x': 1539, 'y': 3, 'w': 60, 'h': 54},
        'snow2_land1': {'x': 1602, 'y': 6, 'w': 63, 'h': 54},
        'snow3_land1': {'x': 1665, 'y': 6, 'w': 56, 'h': 52},
        'grass1_land1': {'x': 1729, 'y': 0, 'w': 63, 'h': 62}, 
        'grass2_land1': {'x': 1794, 'y': 1, 'w': 62, 'h': 57},
        'grass3_land1': {'x': 1857, 'y': 2, 'w': 60, 'h': 60},

        'snowman1': {'x': 6, 'y': 64, 'w': 51, 'h': 65},
        'snowman2': {'x': 67, 'y': 72, 'w': 55, 'h': 46},
        'firewood1': {'x': 131, 'y': 92, 'w': 59, 'h': 36},
        'firewood2': {'x': 193, 'y': 97, 'w': 63, 'h': 25},
        'bush1': {'x': 257, 'y': 71, 'w': 63, 'h': 50},
        'bush2': {'x': 325, 'y': 88, 'w': 49, 'h': 35},
        'tree1': {'x': 393, 'y': 64, 'w': 45, 'h': 57},
        'tree2': {'x': 463, 'y': 73, 'w': 33, 'h': 46},
        'tree3': {'x': 521, 'y': 74, 'w': 47, 'h': 46},
        'tree4': {'x': 587, 'y': 66, 'w': 43, 'h': 54},
        'tree5': {'x': 645, 'y': 64, 'w': 53, 'h': 57},
        'smalltree1': {'x': 773, 'y': 77, 'w': 54, 'h': 41},
        'smalltree2': {'x': 837, 'y': 75, 'w': 53, 'h': 46},
        'smalltree3': {'x': 898, 'y': 77, 'w': 58, 'h': 45},
        'slide_to_jump_2': {'x': 960, 'y': 65, 'w': 64, 'h': 55},
        'energy2': {'x': 1039, 'y': 71, 'w': 43, 'h': 58},
        'heart2': {'x': 1096, 'y': 70, 'w': 48, 'h': 52},
        'skier2_bot': {
            'images': [
                {'x': 1107, 'y': 118, 'w': 30, 'h': 41}, # forward
                {'x': 1161, 'y': 64, 'w': 41, 'h': 63},  # left_turning
                {'x': 1229, 'y': 65, 'w': 41, 'h': 63},  # right_turning
            ],
            'fall': {'x': 1282, 'y': 65, 'w': 58, 'h': 63}
        },
        'snow1_land2': {'x': 1542, 'y': 70, 'w': 58, 'h': 51},
        'snow2_land2': {'x': 1601, 'y': 71, 'w': 61, 'h': 52},
        'snow3_land2': {'x': 1665, 'y': 69, 'w': 58, 'h': 53},
        'grass1_land2': {'x': 1727, 'y': 69, 'w': 67, 'h': 56},
        'grass2_land2': {'x': 1794, 'y': 70, 'w': 63, 'h': 54},
        'grass3_land2': {'x': 1857, 'y': 70, 'w': 63, 'h': 54},

        'ice_lake1': {'x': 0, 'y': 129, 'w': 128, 'h': 129},
        'ice_lake2': {'x': 129, 'y': 130, 'w': 127, 'h': 127},
        'ice_lake3': {'x': 256, 'y': 130, 'w': 130, 'h': 132},
        'rock1': {'x': 388, 'y': 131, 'w': 182, 'h': 124},
        'house': {'x': 575, 'y': 130, 'w': 189, 'h': 124},
        'rock2': {'x': 765, 'y': 131, 'w': 191, 'h': 120},
        'slide_to_jump_3': {'x': 960, 'y': 131, 'w': 64, 'h': 55},
        'energy3': {'x': 1039, 'y': 131, 'w': 41, 'h': 62},
        'heart3': {'x': 1097, 'y': 139, 'w': 46, 'h': 51},
        'skier3_bot': {
            'images': [
                {'x': 1104, 'y': 213, 'w': 39, 'h': 53}, # forward
                {'x': 1157, 'y': 130, 'w': 54, 'h': 62},  # left_turning
                {'x': 1222, 'y': 65, 'w': 41, 'h': 63},  # right_turning (using skier2's right, since skier3_bot_right is missing a y)
            ],
            'fall': {'x': 1284, 'y': 140, 'w': 54, 'h': 52}
        },
        'snow1_land3': {'x': 1542, 'y': 133, 'w': 58, 'h': 51},
        'snow2_land3': {'x': 1601, 'y': 133, 'w': 61, 'h': 52},
        'snow3_land3': {'x': 1665, 'y': 133, 'w': 58, 'h': 53}, 
        'grass1_land3': {'x': 1727, 'y': 133, 'w': 67, 'h': 56},
        'grass2_land3': {'x': 1794, 'y': 133, 'w': 63, 'h': 56},
        'grass3_land3': {'x': 1857, 'y': 133, 'w': 63, 'h': 54},
        
        'slide_to_jump_4': {'x': 960, 'y': 193, 'w': 64, 'h': 55},
        'energy4': {'x': 1039, 'y': 199, 'w': 40, 'h': 57},
        'heart4': {'x': 1096, 'y': 204, 'w': 50, 'h': 51},
        'skier4_bot': {
            'images': [
                {'x': 1105, 'y': 285, 'w': 54, 'h': 67}, # forward
                {'x': 1156, 'y': 193, 'w': 58, 'h': 62},  # left_turning
                {'x': 1221, 'y': 193, 'w': 53, 'h': 62},  # right_turning
            ],
            'fall': {'x': 1286, 'y': 202, 'w': 52, 'h': 52}
        },
        'fall_skier': {'x': 1600, 'y': 201, 'w': 60, 'h': 50},
        'boy_on_buoy': {'x': 1668, 'y': 201, 'w': 58, 'h': 52},
        'girl_on_sleigh': {'x': 1733, 'y': 194, 'w': 52, 'h': 63},
        'white_flag_station': {'x': 1806, 'y': 193, 'w': 37, 'h': 58},
        'green_flag_station': {'x': 1859, 'y': 196, 'w': 60, 'h': 53},

        'edgecoin': {'x': 972, 'y': 269, 'w': 41, 'h': 50},
        'edgecoin_roll1_old': {'x': 978, 'y': 331, 'w': 29, 'h': 51},
        'rock3': {'x': 385, 'y': 300, 'w': 123, 'h': 69},
        'rock4': {'x': 514, 'y': 270, 'w': 125, 'h': 105},
        'rock5': {'x': 638, 'y': 299, 'w': 130, 'h': 74},
        'bigtree1': {'x': 773, 'y': 260, 'w': 53, 'h': 117},
        'bigtree2': {'x': 834, 'y': 263, 'w': 62, 'h': 117},
        'bigtree3': {'x': 895, 'y': 255, 'w': 65, 'h': 125},

        'edgecoin_roll2_old': {'x': 979, 'y': 396, 'w': 26, 'h': 53},
        'smallsnow': {'x': 384, 'y': 393, 'w': 32, 'h': 21},
        'grassflower': {'x': 419, 'y': 401, 'w': 22, 'h': 12},
        'smallicelake': {'x': 442, 'y': 387, 'w': 40, 'h': 29},
        'smallbush': {'x': 483, 'y': 395, 'w': 25, 'h': 20},
        'smallplant': {'x': 517, 'y': 384, 'w': 24, 'h': 32},
        'blue_panel': {'x': 545, 'y': 384, 'w': 30, 'h': 31},
        'green_panel_star': {'x': 577, 'y': 384, 'w': 30, 'h': 31},
        'red_panel_cancel': {'x': 609, 'y': 384, 'w': 30, 'h': 31},

        'chair_table': {'x': 385, 'y': 420, 'w': 30, 'h': 25},
        'tea_table': {'x': 419, 'y': 416, 'w': 26, 'h': 31},
        'hot_coffee_table': {'x': 449, 'y': 417, 'w': 30, 'h': 30},
        'stand_light': {'x': 486, 'y': 417, 'w': 21, 'h': 30},
        'little_snow': {'x': 511, 'y': 422, 'w': 32, 'h': 23},
        'little_ice': {'x': 544, 'y': 428, 'w': 32, 'h': 17}, 

        'edgecoin_roll3_old': {'x': 976, 'y': 459, 'w': 32, 'h': 56},

        'start_point_gate_bridge': {'x': 0, 'y': 290, 'w': 384, 'h': 225}, 
        'bridge': {'x': 385, 'y': 447, 'w': 62, 'h': 62},
        'big_bridge': {'x': 448, 'y': 448, 'w': 134, 'h': 52},
        'big_house_full': {'x': 641, 'y': 382, 'w': 127, 'h': 130}, 
        'tower': {'x': 769, 'y': 382, 'w': 62, 'h': 131},
        'giant_tree1': {'x': 834, 'y': 391, 'w': 58, 'h': 114},
        'giant_tree2': {'x': 895, 'y': 391, 'w': 67, 'h': 116},
    }

    SCENERY_ELEMENTS_KEYS = [
        'snowflake1', 'snowflake2', 'snowflake3', 'snowflake4', 'snowflake5', 'snowflake6',
        'snow1_land1', 'snow2_land1', 'snow3_land1',
        'grass1_land1', 'grass2_land1', 'grass3_land1',
        'snow1_land2', 'snow2_land2', 'snow3_land2',
        'grass1_land2', 'grass2_land2', 'grass3_land2',
        'ice_lake1', 'ice_lake2', 'ice_lake3',
        'snow1_land3', 'snow2_land3', 'snow3_land3',
        'grass1_land3', 'grass2_land3', 'grass3_land3',
        'fall_skier', 'boy_on_buoy', 'girl_on_sleigh', 'white_flag_station', 'green_flag_station',
        'smallsnow', 'grassflower', 'smallicelake', 'smallbush', 'smallplant',
        'chair_table', 'tea_table', 'hot_coffee_table', 'stand_light', 'little_snow', 'little_ice',
        'bridge', 'big_bridge', 'tower'
    ]

    RAMPS_ELEMENTS_KEYS = [
        'slide_to_jump_1', 
        'slide_to_jump_2',
        'slide_to_jump_3',
        'slide_to_jump_4',
    ]

    COLLECTIBLES = [
        'edgecoin', 'edgecoin_animated',
        'energy1', 'heart1', 'energy2', 'heart2', 'energy3', 'heart3', 'energy4', 'heart4',
    ]
    HAZARDS = [
        'slippery_warning', 'wind_flag', 'red_panel', 'camping_fire', 'snowboard1', 'snowboard2', 'bin', 'tree_trunk',
        'snowman1', 'snowman2', 'firewood1', 'firewood2', 'bush1', 'bush2',
        'tree1', 'tree2', 'tree3', 'tree4', 'tree5', 'smalltree1', 'smalltree2', 'smalltree3',
        'rock1', 'rock2', 'rock3', 'rock4', 'rock5',
        'bigtree1', 'bigtree2', 'bigtree3', 'giant_tree1', 'giant_tree2',
        'blue_panel', 'green_panel_star', 'red_panel_cancel'
    ]
    STRUCTURES = ['house', 'big_house_full']
    ANIMALS = [
        'rabbit_animated', 'squirrel_animated', 'wolf_animated', 'dog_animated', 'polar_bear'
    ] 
    NPC_SKIERS = ['skier1_bot', 'skier2_bot', 'skier3_bot', 'skier4_bot'] 
    MONSTERS = ['monster_animated_states'] 
    SCENERY = SCENERY_ELEMENTS_KEYS 
    RAMPS = RAMPS_ELEMENTS_KEYS 

    OBSTACLE_TYPE_WEIGHTS = {
        'collectible': 0.20,  
        'hazard': 0.25,       
        'structure': 0.10,    
        'animal': 0.10,       
        'npc_skier': 0.10,    
        'monster': 0.08,      
        'scenery': 0.12,      
        'ramp': 0.05          
    }
    ALL_OBSTACLE_CATEGORIES = list(OBSTACLE_TYPE_WEIGHTS.keys())

    SKIER_ANIMATION_MAP = {
        'stand': '_style1',
        'left_wide': '_style2', 
        'left_narrow': '_style3',
        'forward': '_style4',
        'right_wide': '_style5', 
        'right_narrow': '_style6',
        'fall_big': '_style7',
        'fall_small': '_style8',
        'boost': '_style9',
        'jump': '_style10'
    }

'''Helper function for drawing a rounded rectangle (for buttons)'''
def draw_rounded_rect(surface, color, rect, radius, border_color=None, border_width=0, shadow_offset=(0,0), shadow_color=(0,0,0,50)):
    # Draw shadow first
    if shadow_offset != (0,0) and shadow_color[3] > 0: # Check if shadow is enabled and has alpha
        shadow_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=int(radius))
        surface.blit(shadow_surface, (rect.x + shadow_offset[0], rect.y + shadow_offset[1]))

    # Draw the main rectangle
    pygame.draw.rect(surface, color, rect, border_radius=int(radius))
    
    # Draw border if specified
    if border_color and border_width > 0:
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=int(radius))


'''Button Class'''
class Button():
    def __init__(self, rect, text, font, base_color, hover_color, text_color, action=None, border_color=None, border_width=0, shadow_offset=(0,0), shadow_color=(0,0,0,50), click_sound=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.current_color = base_color
        self.border_color = border_color
        self.border_width = border_width
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color
        self.click_sound = click_sound # Pygame sound object

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.is_hovered = False

    def draw(self, surface):
        draw_rounded_rect(surface, self.current_color, self.rect, self.rect.height * 0.25, # Radius based on height
                          border_color=self.border_color, border_width=self.border_width,
                          shadow_offset=self.shadow_offset, shadow_color=self.shadow_color)
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if not self.is_hovered:
                    self.current_color = self.hover_color
                    self.is_hovered = True
            else:
                if self.is_hovered:
                    self.current_color = self.base_color
                    self.is_hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.click_sound:
                    self.click_sound.play()
                if self.action:
                    self.action()
                    return True # Indicate button was clicked
        return False


'''Skier Class (Player)'''
class SkierSprite(pygame.sprite.Sprite):
    def __init__(self, selected_skier_animations_data, skateboard_fire_effects):
        pygame.sprite.Sprite.__init__(self)
        self.all_skier_styles = selected_skier_animations_data
        self.skateboard_fire_effects = skateboard_fire_effects

        self.current_horizontal_state = 'forward'
        self.image = self.all_skier_styles.get(Config.SKIER_ANIMATION_MAP['forward'])
        if self.image is None:
            self.image = pygame.Surface((30, 60), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), self.image.get_rect())
            print("Warning: Skier 'forward' animation missing. Using placeholder.")

        self.rect = self.image.get_rect()
        self.rect.center = [pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2] 
        
        self.speed = [0, 6]
        self.fallen = False
        
        self.vertical_move_speed = 10
        self.min_vertical_scroll_speed = 3 
        self.max_vertical_scroll_speed = 15 
        self.vertical_scroll_speed_increment = 2.0 
        self.horizontal_move_factor = 2.5 

        self.is_jumping = False
        self.jump_velocity = 0 
        self.gravity = 0.8 
        self.jump_boost_timer = 0 
        self.jump_boost_duration = 30
        self.jump_boost_multiplier = 1.8 
        self.jump_land_effect_timer = 0 
        self.jump_land_effect_duration = 10

        self.max_hearts = 5
        self.current_hearts = self.max_hearts
        self.max_power = 5
        self.current_power = 0
        self.max_defense = 5
        self.current_defense = self.max_defense
        
        self.is_boosting = False
        self.boost_duration_timer = 0
        self.total_boost_duration = 200
        self.boost_speed_multiplier = 2.5

        self.left_press_count = 0
        self.right_press_count = 0
        self.last_left_press_time = 0
        self.last_right_press_time = 0
        self.turn_threshold_time = 200

        self.fire_effect_frame_index = 0
        self.fire_effect_animation_speed = 0.3
        self.fire_effect_timer = 0

        # State to keep track of continuous key press for turns
        self.is_left_key_pressed = False
        self.is_right_key_pressed = False


    def turn(self, direction_input, current_time):
        if self.fallen or self.is_jumping or self.is_boosting:
            return self.speed

        if direction_input == -1: # Left
            if not self.is_left_key_pressed: # This is the initial KEYDOWN event
                self.is_left_key_pressed = True
                if (current_time - self.last_left_press_time) < self.turn_threshold_time:
                    self.left_press_count = 2 # Double press detected
                else:
                    self.left_press_count = 1 # Single press
                self.last_left_press_time = current_time
            self.right_press_count = 0 # Reset opposite direction counter
            self.is_right_key_pressed = False # Ensure opposite key is not considered pressed

            if self.left_press_count == 2:
                self.current_horizontal_state = 'left_wide'
                self.speed[0] = -2 * self.horizontal_move_factor
            elif self.left_press_count == 1:
                self.current_horizontal_state = 'left_narrow'
                self.speed[0] = -1 * self.horizontal_move_factor

        elif direction_input == 1: # Right
            if not self.is_right_key_pressed: # This is the initial KEYDOWN event
                self.is_right_key_pressed = True
                if (current_time - self.last_right_press_time) < self.turn_threshold_time:
                    self.right_press_count = 2 # Double press detected
                else:
                    self.right_press_count = 1 # Single press
                self.last_right_press_time = current_time
            self.left_press_count = 0 # Reset opposite direction counter
            self.is_left_key_pressed = False # Ensure opposite key is not considered pressed

            if self.right_press_count == 2:
                self.current_horizontal_state = 'right_wide'
                self.speed[0] = 2 * self.horizontal_move_factor
            elif self.right_press_count == 1:
                self.current_horizontal_state = 'right_narrow'
                self.speed[0] = 1 * self.horizontal_move_factor

        self._update_image_from_state()
        return self.speed

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(self.rect.width / 2, self.rect.centerx)
        self.rect.centerx = min(pygame.display.get_surface().get_width() - self.rect.width / 2, self.rect.centerx)

    def stop_horizontal_movement(self, direction_input):
        # This will be called on KEYUP for left/right arrows
        if direction_input == -1: # Left key released
            self.is_left_key_pressed = False
            self.left_press_count = 0 
        elif direction_input == 1: # Right key released
            self.is_right_key_pressed = False
            self.right_press_count = 0 

        # If both horizontal keys are now released
        if not self.is_left_key_pressed and not self.is_right_key_pressed:
            self.speed[0] = 0
            if not self.fallen and not self.is_jumping and not self.is_boosting and self.jump_land_effect_timer == 0:
                if self.speed[1] > 0:
                    self.current_horizontal_state = 'forward'
                else:
                    self.current_horizontal_state = 'stand'
                self._update_image_from_state()
        else: # One key is still pressed, re-evaluate the state based on the active key
            if self.is_left_key_pressed:
                if self.left_press_count == 2:
                    self.current_horizontal_state = 'left_wide'
                    self.speed[0] = -2 * self.horizontal_move_factor
                elif self.left_press_count == 1:
                    self.current_horizontal_state = 'left_narrow'
                    self.speed[0] = -1 * self.horizontal_move_factor
            elif self.is_right_key_pressed:
                if self.right_press_count == 2:
                    self.current_horizontal_state = 'right_wide'
                    self.speed[0] = 2 * self.horizontal_move_factor
                elif self.right_press_count == 1:
                    self.current_horizontal_state = 'right_narrow'
                    self.speed[0] = 1 * self.horizontal_move_factor
            self._update_image_from_state()


    def accelerate_vertical(self):
        if not self.fallen and not self.is_jumping:
            if self.is_boosting:
                self.speed[1] = self.max_vertical_scroll_speed * self.boost_speed_multiplier
            else:
                self.speed[1] = min(self.max_vertical_scroll_speed, self.speed[1] + self.vertical_scroll_speed_increment)
            if not self.is_left_key_pressed and not self.is_right_key_pressed: 
                self.current_horizontal_state = 'forward'
            self._update_image_from_state()

    def decelerate_vertical(self):
        if not self.fallen and not self.is_jumping:
            if self.is_boosting:
                self.speed[1] = self.max_vertical_scroll_speed * self.boost_speed_multiplier
            else:
                self.speed[1] = max(self.min_vertical_scroll_speed, self.speed[1] - self.vertical_scroll_speed_increment)
            if not self.is_left_key_pressed and not self.is_right_key_pressed: 
                self.current_horizontal_state = 'forward'
            self._update_image_from_state()


    def setFall(self, collision_type='small'):
        self.fallen = True
        self.is_jumping = False 
        self.jump_velocity = 0 
        self.jump_boost_timer = 0 
        self.is_boosting = False
        self.boost_duration_timer = 0
        self.left_press_count = 0
        self.right_press_count = 0
        self.is_left_key_pressed = False
        self.is_right_key_pressed = False

        if collision_type == 'big':
            self.current_horizontal_state = 'fall_big'
        else:
            self.current_horizontal_state = 'fall_small'
            
        self._update_image_from_state()
        self.speed = [0, 0] 

    def setForward(self):
        self.fallen = False
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_boost_timer = 0
        self.is_boosting = False
        self.boost_duration_timer = 0 
        self.left_press_count = 0
        self.right_press_count = 0
        self.is_left_key_pressed = False
        self.is_right_key_pressed = False
        self.current_horizontal_state = 'forward'
        self.speed = [0, 6] 
        self._update_image_from_state()

    def start_jump(self):
        if not self.is_jumping and not self.fallen:
            self.is_jumping = True
            self.jump_velocity = -25
            self.current_horizontal_state = 'jump'
            self.jump_boost_timer = self.jump_boost_duration
            self.is_boosting = False
            self.boost_duration_timer = 0
            self.left_press_count = 0
            self.right_press_count = 0
            self.is_left_key_pressed = False
            self.is_right_key_pressed = False
            self._update_image_from_state()

    def update_jump(self):
        if self.is_jumping:
            self.rect.centery += self.jump_velocity 
            self.jump_velocity += self.gravity

            if self.jump_boost_timer > 0:
                self.speed[1] = self.max_vertical_scroll_speed * self.jump_boost_multiplier
                self.jump_boost_timer -= 1
            else:
                self.speed[1] = min(self.max_vertical_scroll_speed, max(self.min_vertical_scroll_speed, self.speed[1]))

            ground_y = pygame.display.Info().current_h - self.rect.height / 2 
            if self.rect.centery >= ground_y:
                self.rect.centery = ground_y
                self.is_jumping = False
                self.jump_velocity = 0
                self.jump_boost_timer = 0 
                self.jump_land_effect_timer = self.jump_land_effect_duration
                self.setForward() 

        if self.jump_land_effect_timer > 0:
            if not self.is_boosting:
                self.current_horizontal_state = 'boost' 
                self._update_image_from_state()
            self.jump_land_effect_timer -= 1
            if self.jump_land_effect_timer == 0:
                if not self.is_boosting:
                    self.setForward() 


    def draw_skateboard_fire(self, screen):
        if (self.is_jumping or self.is_boosting) and self.skateboard_fire_effects:
            self.fire_effect_timer += self.fire_effect_animation_speed
            if self.fire_effect_timer >= 1:
                self.fire_effect_frame_index = (self.fire_effect_frame_index + int(self.fire_effect_timer)) % len(self.skateboard_fire_effects)
                self.fire_effect_timer %= 1

            fire_image = self.skateboard_fire_effects[self.fire_effect_frame_index]
            fire_rect = fire_image.get_rect(centerx=self.rect.centerx, top=self.rect.bottom - 10) 
            screen.blit(fire_image, fire_rect)

    def lose_heart(self, amount=1, collision_type='small'):
        if not self.fallen:
            self.current_hearts = max(0, self.current_hearts - amount)
            self.setFall(collision_type=collision_type)
            return self.current_hearts <= 0
        return False

    def gain_heart(self, amount=1):
        self.current_hearts = min(self.max_hearts, self.current_hearts + amount)

    def gain_power(self, amount=1):
        self.current_power = min(self.max_power, self.current_power + amount)

    def gain_defense(self, amount=1):
        self.current_defense = min(self.max_defense, self.current_defense + amount)

    def start_boost(self):
        if not self.fallen and not self.is_jumping and not self.is_boosting and self.current_power >= self.max_power:
            self.is_boosting = True
            self.boost_duration_timer = self.total_boost_duration
            self.current_power = 0
            self.speed[1] = self.max_vertical_scroll_speed * self.boost_speed_multiplier
            self.current_horizontal_state = 'boost'
            self.left_press_count = 0
            self.right_press_count = 0
            self.is_left_key_pressed = False
            self.is_right_key_pressed = False
            self._update_image_from_state()

    def update_boost(self):
        if self.is_boosting:
            self.boost_duration_timer -= 1
            if self.boost_duration_timer <= 0:
                self.is_boosting = False
                self.speed[1] = self.max_vertical_scroll_speed
                self.setForward()

    def _update_image_from_state(self):
        new_image_key = None

        if self.fallen:
            new_image_key = Config.SKIER_ANIMATION_MAP[self.current_horizontal_state]
        elif self.is_jumping:
            new_image_key = Config.SKIER_ANIMATION_MAP['jump']
        elif self.is_boosting or self.jump_land_effect_timer > 0:
            new_image_key = Config.SKIER_ANIMATION_MAP['boost']
        elif self.is_left_key_pressed: # Left key is currently held down
            new_image_key = Config.SKIER_ANIMATION_MAP['left_wide'] if self.left_press_count == 2 else Config.SKIER_ANIMATION_MAP['left_narrow']
        elif self.is_right_key_pressed: # Right key is currently held down
            new_image_key = Config.SKIER_ANIMATION_MAP['right_wide'] if self.right_press_count == 2 else Config.SKIER_ANIMATION_MAP['right_narrow']
        elif self.speed[1] > 0: # Moving vertically but no horizontal turn key pressed
            new_image_key = Config.SKIER_ANIMATION_MAP['forward']
        else: # Completely stopped
            new_image_key = Config.SKIER_ANIMATION_MAP['stand']
        
        if new_image_key not in self.all_skier_styles:
            print(f"Warning: Skier '{self.selected_skier_id}' missing animation for state: {self.current_horizontal_state} (key: {new_image_key}). Falling back to 'forward'.")
            new_image_key = Config.SKIER_ANIMATION_MAP['forward']

        old_center = self.rect.center
        self.image = self.all_skier_styles[new_image_key]
        self.rect = self.image.get_rect(center=old_center)


'''Obstacle Class (now versatile for animals and NPC skiers)'''
class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, images_or_image, location, attribute, is_npc_animal=False, is_npc_skier=False, is_monster=False): 
        pygame.sprite.Sprite.__init__(self)
        self.location = list(location)
        self.attribute = attribute
        self.passed = False 

        self.animation_frames = None
        self.current_frame_index = 0
        self.animation_speed = 0.2 
        self.animation_timer = 0 

        self.is_npc_skier = is_npc_skier
        self.is_npc_animal = is_npc_animal 
        self.is_monster = is_monster

        self.npc_skier_fallen = False 
        self.npc_skier_recovery_timer = 0 
        self.npc_vertical_speed_factor = random.uniform(0.8, 1.2)
        self.npc_speed_change_timer = random.randint(60, 200)
        self.npc_speed_timer_current = 0

        self.npc_move_speed_x = 0.0 
        self.npc_move_direction_x = 0 
        self.npc_move_duration = 0 
        self.npc_move_timer = 0 
        self.skier_move_speed_x = 0.0 
        self.skier_move_duration = 0
        self.skier_move_timer = 0
        self.direction = 0

        self.monster_state = 'in_snow'
        self.monster_chase_speed = 4.5
        self.monster_chase_range_y = 250
        self.loaded_monster_frames = None

        if self.is_npc_skier:
            self.images_movement = images_or_image['images'] 
            self.image_fall_npc = images_or_image['fall'] 
            self.direction = random.choice([-1, 0, 1]) 
            if self.direction == 0: image_index = 0
            elif self.direction == 1: image_index = 1
            else: image_index = 2 
            self.image = self.images_movement[image_index]

            self.skier_move_speed_x = random.uniform(0.8, 1.8) 
            self.skier_move_duration = random.randint(40, 150) 
            self.skier_move_timer = 0
            
        elif isinstance(images_or_image, list):
            self.animation_frames = images_or_image
            self.image = self.animation_frames[self.current_frame_index]
            if self.is_npc_animal: 
                self.npc_move_speed_x = random.uniform(0.5, 1.5) 
                self.npc_move_direction_x = random.choice([-1, 0, 1]) 
                self.npc_move_duration = random.randint(30, 120) 
                self.npc_move_timer = 0 
        elif self.is_monster:
            self.loaded_monster_frames = images_or_image
            self.animation_frames = self.loaded_monster_frames['in_snow']
            self.image = self.animation_frames[self.current_frame_index]
            self.animation_speed = 0.2
        else:
            self.image = images_or_image
        
        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def move(self, num, skier_rect=None):
        effective_num = num * self.npc_vertical_speed_factor 
        self.location[1] -= effective_num
        self.rect.centery = self.location[1]

        if self.is_npc_animal and not self.is_npc_skier and not self.is_monster:
            self.location[0] += self.npc_move_direction_x * self.npc_move_speed_x
            self.rect.centerx = self.location[0]
            if self.rect.centerx < -self.rect.width / 2: 
                self.npc_move_direction_x = 1 
            elif self.rect.centerx > pygame.display.get_surface().get_width() + pygame.display.get_surface().get_width(): 
                self.npc_move_direction_x = -1 
        elif self.is_npc_skier and not self.npc_skier_fallen: 
            self.location[0] += self.direction * self.skier_move_speed_x 
            self.rect.centerx = self.location[0]
            screen_width = pygame.display.get_surface().get_width()
            if self.rect.centerx < 20: 
                self.direction = 1 
                self.location[0] = 20 
            elif self.rect.centerx > screen_width - 20: 
                self.direction = -1 
                self.location[0] = screen_width - 20
        elif self.is_monster and self.monster_state == 'chase' and skier_rect is not None: 
            if self.rect.centerx < skier_rect.centerx:
                self.location[0] += self.monster_chase_speed
            elif self.rect.centerx > skier_rect.centerx:
                self.location[0] -= self.monster_chase_speed
            self.rect.centerx = self.location[0]
            
            if self.rect.centery < skier_rect.centery:
                self.location[1] += self.monster_chase_speed / 1.5
            elif self.rect.centery > skier_rect.centery:
                self.location[1] -= self.monster_chase_speed / 1.5
            self.rect.centery = self.location[1]

            self.npc_vertical_speed_factor = 1.5

    def update_animation(self):
        if self.is_monster:
            frames = []
            if self.monster_state == 'in_snow':
                frames = self.loaded_monster_frames['in_snow']
                self.animation_speed = 0.2
            elif self.monster_state == 'chase':
                frames = self.loaded_monster_frames['chase']
                self.animation_speed = 0.5
            elif self.monster_state == 'catch':
                self.image = self.loaded_monster_frames['catch'][0] 
                return
            
            if frames:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1: 
                    self.current_frame_index = (self.current_frame_index + int(self.animation_timer)) % len(frames)
                    self.image = frames[self.current_frame_index]
                    self.animation_timer %= 1 
        elif self.animation_frames and not self.is_npc_skier:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1: 
                self.current_frame_index = (self.current_frame_index + int(self.animation_timer)) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame_index]
                self.animation_timer %= 1 
        elif self.is_npc_skier and not self.npc_skier_fallen:
            if self.direction == 0: image_key = 'forward'
            elif self.direction == 1: image_key = 'left_turning'
            else: image_key = 'right_turning'
            
            if image_key == 'forward':
                self.image = self.images_movement[0]
            elif image_key == 'left_turning':
                self.image = self.images_movement[1]
            elif image_key == 'right_turning':
                self.image = self.images_movement[2]


    def update_npc_movement(self):
        if not self.is_monster:
            self.npc_speed_timer_current += 1
            if self.npc_speed_timer_current >= self.npc_speed_change_timer:
                self.npc_vertical_speed_factor = random.uniform(0.8, 1.2)
                self.npc_speed_change_timer = random.randint(60, 200)
                self.npc_speed_timer_current = 0

        if self.is_npc_animal and not self.is_npc_skier and not self.is_monster:
            self.npc_move_timer += 1
            if self.npc_move_timer >= self.npc_move_duration:
                self.npc_move_direction_x = random.choice([-1, 0, 1]) 
                self.npc_move_speed_x = random.uniform(0.5, 1.5)
                self.npc_move_duration = random.randint(30, 120) 
                self.npc_move_timer = 0
        elif self.is_npc_skier: 
            if self.npc_skier_fallen:
                self.npc_skier_recovery_timer -= 1
                if self.npc_skier_recovery_timer <= 0:
                    self.npc_skier_setForward() 
            else: 
                self.skier_move_timer += 1
                if self.skier_move_timer >= self.skier_move_duration:
                    self.direction = random.choice([-1, 0, 1]) 
                    self.skier_move_speed_x = random.uniform(0.8, 1.8)
                    self.skier_move_duration = random.randint(40, 150)
                    self.skier_move_timer = 0
            
    def npc_skier_setFall(self):
        self.image = self.image_fall_npc
        self.npc_skier_fallen = True
        self.skier_move_timer = 0 
        self.npc_skier_recovery_timer = 60 
        self.direction = 0 
        self.rect = self.image.get_rect(center=self.location)
    
    def npc_skier_setForward(self):
        self.npc_skier_fallen = False
        self.direction = 0 
        self.image = self.images_movement[0] 
        self.skier_move_duration = random.randint(40, 150) 
        self.rect = self.image.get_rect(center=self.location)

    def update_monster_state(self, skier_rect):
        if not self.is_monster or self.monster_state == 'catch':
            return

        distance_y = skier_rect.centery - self.rect.centery 
        
        if self.monster_state == 'in_snow' and distance_y > 0 and distance_y < self.monster_chase_range_y:
            self.monster_state = 'chase'
            self.animation_frames = self.loaded_monster_frames['chase']
            self.animation_speed = 0.5
            self.npc_vertical_speed_factor = 1.5
        elif self.monster_state == 'chase' and (distance_y < -100 or self.rect.top > pygame.display.get_surface().get_height()): 
             self.monster_state = 'in_snow'
             self.animation_frames = self.loaded_monster_frames['in_snow']
             self.animation_speed = 0.2
             self.npc_vertical_speed_factor = random.uniform(0.8, 1.2)


'''Ski Game Class'''
class SkiGame(PygameBaseGame):
    game_type = 'ski'
    def __init__(self, **kwargs):
        self.cfg = Config()
        
        # Initialize screen with resizable flag
        # Pass the screen object to the base class
        # Initial screen setup happens before super().__init__ as PygameBaseGame expects screen to be set
        self.screen = pygame.display.set_mode(self.cfg.SCREENSIZE, pygame.RESIZABLE)
        pygame.display.set_caption(self.cfg.TITLE)

        super(SkiGame, self).__init__(config=self.cfg, screen=self.screen, **kwargs) # Pass screen to base class

        self.snowflakes = [(random.randint(0, self.cfg.SCREENSIZE[0]), random.randint(0, self.cfg.SCREENSIZE[1])) for _ in range(50)]

        self.env_map_image = pygame.image.load(self.cfg.IMAGE_PATHS_DICT['env_map']).convert_alpha()
        self.env_map_sprites_loaded = self._load_env_map_sprites(self.env_map_image)

        self.skiers_map_image = pygame.image.load(self.cfg.IMAGE_PATHS_DICT['skiers_map']).convert_alpha()
        self.skier_animations_all, self.skateboard_fire_effects_loaded, self.dog_skins_loaded = self._load_skiers_data(self.skiers_map_image)

        self.selected_skier_id = 'player1'
        
        raw_background_image = pygame.image.load(self.cfg.IMAGE_PATHS_DICT['background']).convert_alpha()
        self.tiled_background = self._create_tiled_background(raw_background_image)

        self.start_gate_active = True
        if 'start_point_gate_bridge' in self.env_map_sprites_loaded:
            self.start_gate_instance = ObstacleSprite(
                self.env_map_sprites_loaded['start_point_gate_bridge'],
                [self.cfg.SCREENSIZE[0] // 2, self.cfg.SCREENSIZE[1] + 100],
                'start_gate_once'
            )
        else:
            print("Warning: 'start_point_gate_bridge' sprite not loaded, skipping start gate initialization.")
            self.start_gate_active = False

    def _create_tiled_background(self, raw_image):
        """Creates a tiled background surface to fill the current screen size."""
        current_screen_w, current_screen_h = self.screen.get_size()
        tiled_surface = pygame.Surface((current_screen_w, current_screen_h), pygame.SRCALPHA)
        for x in range(0, current_screen_w, raw_image.get_width()):
            for y in range(0, current_screen_h, raw_image.get_height()):
                tiled_surface.blit(raw_image, (x, y))
        return tiled_surface

    def _load_env_map_sprites(self, env_map_image):
        """Helper to load sprites from env_map.png based on Config.ENV_MAP_SPRITES."""
        loaded_sprites = {}
        image_width, image_height = env_map_image.get_size()

        for name, data in self.cfg.ENV_MAP_SPRITES.items():
            if isinstance(data, dict) and 'images' in data and 'fall' in data: # NPC skier data structure
                npc_skier_data = {'images': [], 'fall': None}
                for frame_data in data['images']:
                    rect = self._get_clamped_rect(frame_data, image_width, image_height, name)
                    if rect: npc_skier_data['images'].append(env_map_image.subsurface(rect).convert_alpha())
                
                fall_rect = self._get_clamped_rect(data['fall'], image_width, image_height, name + " fall")
                if fall_rect: npc_skier_data['fall'] = env_map_image.subsurface(fall_rect).convert_alpha()
                else: npc_skier_data['fall'] = pygame.Surface((1,1)).convert_alpha() # Placeholder

                if not npc_skier_data['images']: # Ensure 'images' list is not empty
                    npc_skier_data['images'] = [pygame.Surface((1,1)).convert_alpha()]
                loaded_sprites[name] = npc_skier_data

            elif isinstance(data, list): # Animated animals/objects
                loaded_sprites[name] = []
                for frame_data in data:
                    rect = self._get_clamped_rect(frame_data, image_width, image_height, name)
                    if rect: loaded_sprites[name].append(env_map_image.subsurface(rect).convert_alpha())
                if not loaded_sprites[name]: # If all frames were skipped
                    loaded_sprites[name] = [pygame.Surface((1,1)).convert_alpha()]

            elif name == 'monster_animated_states': # Special handling for monster
                monster_states_data = {}
                for state_name, frames_list in data.items():
                    loaded_frames = []
                    for frame_data in frames_list:
                        rect = self._get_clamped_rect(frame_data, image_width, image_height, f"monster {state_name}")
                        if rect: loaded_frames.append(env_map_image.subsurface(rect).convert_alpha())
                    if not loaded_frames: loaded_frames = [pygame.Surface((1,1)).convert_alpha()]
                    monster_states_data[state_name] = loaded_frames
                loaded_sprites[name] = monster_states_data

            else: # Single image sprites
                rect = self._get_clamped_rect(data, image_width, image_height, name)
                if rect: loaded_sprites[name] = env_map_image.subsurface(rect).convert_alpha()
                else: loaded_sprites[name] = pygame.Surface((1,1)).convert_alpha() # Placeholder
        return loaded_sprites

    def _get_clamped_rect(self, data, img_w, img_h, name=""):
        """Helper to create a clamped Rect for subsurface to prevent errors."""
        x, y, w, h = data['x'], data['y'], data['w'], data['h']
        
        # Calculate valid region within the image bounds
        clamped_x = max(0, x)
        clamped_y = max(0, y)
        clamped_w = min(w, img_w - clamped_x)
        clamped_h = min(h, img_h - clamped_y)
        
        clamped_w = max(1, clamped_w) # Ensure min 1x1 size
        clamped_h = max(1, clamped_h)

        if clamped_x >= img_w or clamped_y >= img_h:
            print(f"Warning: Sprite '{name}' origin ({x},{y}) is outside image bounds ({img_w},{img_h}). Skipping.")
            return None
        if x + w > img_w or y + h > img_h:
            print(f"Warning: Sprite '{name}' dimensions ({w}x{h}) from origin ({x},{y}) extend outside image bounds ({img_w},{img_h}). Clamping.")
        
        return pygame.Rect(clamped_x, clamped_y, clamped_w, clamped_h)


    def _load_skiers_data(self, skiers_map_image):
        """
        Parses skiers.txt and loads all skier animations, dog skins,
        and skateboard fire effects from skiers_map.png.
        """
        skier_animations_all = {}
        skateboard_fire_effects = {}
        dog_skins = {}

        image_width, image_height = skiers_map_image.get_size()

        try:
            with open(self.cfg.SKIER_DATA_PATH, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: skiers.txt not found at {self.cfg.SKIER_DATA_PATH}")
            return {}, {}, {}

        current_row_category = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('\\\\\\'):
                continue
            
            if line.endswith('_ROW'):
                current_row_category = line.split('_ROW')[0].lower()
                continue

            parts = line.split('img: position:')
            if len(parts) < 2: continue

            name_part = parts[0].strip()
            
            pos_size_part = parts[1].strip()
            pos_match = re.search(r'(\d+)x(\d+)px', pos_size_part)
            size_match = re.search(r'size:\s*(\d+)x(\d+)px', pos_size_part)

            if not pos_match or not size_match:
                print(f"Warning: Could not parse position or size from line: {line}")
                continue

            x, y = int(pos_match.group(1)), int(pos_match.group(2))
            w, h = int(size_match.group(1)), int(size_match.group(2))

            rect = self._get_clamped_rect({'x':x, 'y':y, 'w':w, 'h':h}, image_width, image_height, name_part)
            if rect:
                sprite_image = skiers_map_image.subsurface(rect).convert_alpha()
            else:
                sprite_image = pygame.Surface((1,1)).convert_alpha()

            if name_part.startswith('player') and '_style' in name_part:
                player_id_match = re.search(r'(player\d+)', name_part)
                style_id_match = re.search(r'(_style\d+)', name_part)
                if player_id_match and style_id_match:
                    player_id = player_id_match.group(1)
                    style_id = style_id_match.group(1)
                    if player_id not in skier_animations_all:
                        skier_animations_all[player_id] = {}
                    skier_animations_all[player_id][style_id] = sprite_image
            elif name_part.startswith('skateboard_fire'):
                skateboard_fire_effects[name_part] = sprite_image
            elif name_part.startswith('dog') and current_row_category == 'fourth':
                dog_skins[name_part] = sprite_image

        skateboard_fire_effect_list = []
        for i in range(1, 7):
            key = f'skateboard_fire{i}'
            if key in skateboard_fire_effects:
                skateboard_fire_effect_list.append(skateboard_fire_effects[key])
        
        for skier_id in skier_animations_all:
            skier_animations_all[skier_id] = dict(sorted(skier_animations_all[skier_id].items()))

        return skier_animations_all, skateboard_fire_effect_list, dog_skins


    def run(self):
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        
        clock = pygame.time.Clock()
        
        resource_loader.playbgm()
        
        # --- Skin Selection Interface ---
        self.selected_skier_id = self.display_skin_selection_interface_graphical(screen)
        
        selected_skier_animations = self.skier_animations_all.get(self.selected_skier_id)
        if selected_skier_animations is None:
             print(f"Error: Skier skin '{self.selected_skier_id}' not found. Using 'player1' as default.")
             self.selected_skier_id = 'player1'
             selected_skier_animations = self.skier_animations_all.get('player1')
             if selected_skier_animations is None:
                 print("FATAL ERROR: 'player1' animations also missing. Cannot start game.")
                 QuitGame()

        skier = SkierSprite(selected_skier_animations, self.skateboard_fire_effects_loaded)
        skier.selected_skier_id = self.selected_skier_id
        
        self.display_start_interface(screen) 
        
        obstacles = pygame.sprite.Group() 
        
        distance = 0
        score = 0 
        obstaclesflag = 0 
        self.reset_game_state(skier, obstacles, True)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.VIDEORESIZE:
                    # Update screen size and re-create surfaces/elements that depend on it
                    new_width, new_height = event.size
                    self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    # Update Config.SCREENSIZE to reflect new dimensions
                    self.cfg.SCREENSIZE = (new_width, new_height)
                    # Re-create tiled background for new size
                    raw_background_image = pygame.image.load(self.cfg.IMAGE_PATHS_DICT['background']).convert_alpha()
                    self.tiled_background = self._create_tiled_background(raw_background_image)
                    # Recalculate positions for UI elements if they are static
                    skier.rect.center = [self.cfg.SCREENSIZE[0] // 2, self.cfg.SCREENSIZE[1] // 2]
                    # Snowflakes also need recalculation
                    self.snowflakes = [(random.randint(0, self.cfg.SCREENSIZE[0]), random.randint(0, self.cfg.SCREENSIZE[1])) for _ in range(50)]
                    
                if event.type == pygame.KEYDOWN: 
                    current_time = pygame.time.get_ticks()
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        skier.turn(-1, current_time)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        skier.turn(1, current_time)
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        skier.accelerate_vertical()
                        skier.rect.centery -= skier.vertical_move_speed
                        skier.rect.centery = max(skier.rect.height / 2, skier.rect.centery)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]: 
                        skier.decelerate_vertical()
                        skier.rect.centery += skier.vertical_move_speed
                        skier.rect.centery = min(cfg.SCREENSIZE[1] - skier.rect.height / 2, skier.rect.centery)
                    elif event.key == pygame.K_SPACE:
                        skier.start_boost()
                
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        skier.stop_horizontal_movement(-1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        skier.stop_horizontal_movement(1)
                    elif event.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                        # If no horizontal movement and not falling/jumping/boosting, default to forward
                        if skier.speed[0] == 0 and not skier.fallen and not skier.is_jumping and not skier.is_boosting:
                            skier.current_horizontal_state = 'forward'
                            skier._update_image_from_state()

            skier.move() 
            skier.update_jump() 
            skier.update_boost()

            scroll_speed = skier.speed[1] 
            distance += scroll_speed

            for obstacle in obstacles:
                obstacle.move(scroll_speed, skier_rect=skier.rect) 
                obstacle.update_animation() 
                obstacle.update_npc_movement() 
                if obstacle.is_monster:
                    obstacle.update_monster_state(skier.rect)

            if distance >= cfg.SCREENSIZE[1] * 1 and obstaclesflag == 0: 
                obstaclesflag = 1
                new_obstacles = self.createObstacles(20, 29, num=40) 
                obstacles.add(new_obstacles) 
            if distance >= cfg.SCREENSIZE[1] * 2 and obstaclesflag == 1:
                obstaclesflag = 0
                distance -= cfg.SCREENSIZE[1] * 2 
                for obstacle in list(obstacles): 
                    if obstacle.rect.top > cfg.SCREENSIZE[1]:
                        obstacles.remove(obstacle)
                    else: 
                        obstacle.location[1] = obstacle.location[1] - cfg.SCREENSIZE[1] * 2 
                new_obstacles = self.createObstacles(10, 19, num=40) 
                obstacles.add(new_obstacles)
            
            hitted_obstacles_player = pygame.sprite.spritecollide(skier, obstacles, False)
            
            player_hazard_hit_in_frame = False

            for obstacle in hitted_obstacles_player: 
                if obstacle.attribute == 'start_gate_once' and self.start_gate_active:
                    obstacles.remove(obstacle)
                    self.start_gate_active = False 
                    obstacle.passed = True 
                    continue 

                if obstacle.is_monster and obstacle.monster_state == 'chase':
                    obstacle.monster_state = 'catch'
                    skier.lose_heart(amount=skier.max_hearts, collision_type='big')
                    self.updateFrame(screen, self.tiled_background, obstacles, skier, score, skier.rect)
                    game_restarted = self.display_game_over_interface(screen, skier, obstacles, score, distance, clock) 
                    if game_restarted:
                        distance = 0
                        score = 0
                        obstaclesflag = 0
                        self.start_gate_active = True
                        break
                    else:
                        QuitGame()

                if obstacle.attribute in self.cfg.HAZARDS or obstacle.attribute in self.cfg.STRUCTURES: 
                    if not obstacle.passed and not skier.is_jumping and not skier.is_boosting:
                        collision_type = 'small'
                        if obstacle.attribute in ['rock1', 'rock2', 'rock3', 'rock4', 'rock5', 'bigtree1', 'bigtree2', 'bigtree3', 'giant_tree1', 'giant_tree2', 'house', 'big_house_full']:
                            collision_type = 'big'

                        if skier.lose_heart(collision_type=collision_type):
                            self.updateFrame(screen, self.tiled_background, obstacles, skier, score, skier.rect)
                            game_restarted = self.display_game_over_interface(screen, skier, obstacles, score, distance, clock) 
                            if game_restarted:
                                distance = 0
                                score = 0
                                obstaclesflag = 0 
                                self.start_gate_active = True
                                break
                            else:
                                QuitGame()
                        else:
                            player_hazard_hit_in_frame = True 
                            obstacle.passed = True 
                elif obstacle.attribute in self.cfg.COLLECTIBLES: 
                    if not obstacle.passed: 
                        if obstacle.attribute in ['edgecoin', 'edgecoin_animated']:
                            score += 10
                        elif obstacle.attribute in ['heart1', 'heart2', 'heart3', 'heart4']: 
                            skier.gain_heart()
                        elif obstacle.attribute in ['energy1', 'energy2', 'energy3', 'energy4']: 
                            skier.gain_power()
                        elif obstacle.attribute in ['defense']:
                            skier.gain_defense()
                        obstacles.remove(obstacle) 
                        obstacle.passed = True 
                elif obstacle.attribute in self.cfg.RAMPS: 
                    if not obstacle.passed and not skier.is_jumping:
                        skier.start_jump()
                        obstacle.passed = True 

            if player_hazard_hit_in_frame and skier.fallen and not skier.is_boosting:
                self.updateFrame(screen, self.tiled_background, obstacles, skier, score, skier.rect) 
                pygame.time.delay(1000)
                skier.setForward() 

            npc_skiers_group_active = pygame.sprite.Group([o for o in obstacles if o.is_npc_skier and not o.npc_skier_fallen])
            other_obstacles_for_npc_collision = pygame.sprite.Group([o for o in obstacles if o.attribute in self.cfg.HAZARDS or o.attribute in self.cfg.STRUCTURES or o.attribute in self.cfg.RAMPS or o.attribute == 'start_gate_once']) 

            for npc_skier_obj in npc_skiers_group_active:
                npc_hitted_obstacles = pygame.sprite.spritecollide(npc_skier_obj, other_obstacles_for_npc_collision, False)
                if npc_hitted_obstacles:
                    npc_obstacle_hit = npc_hitted_obstacles[0] 
                    if npc_obstacle_hit.attribute in self.cfg.HAZARDS or npc_obstacle_hit.attribute in self.cfg.STRUCTURES:
                        if not npc_skier_obj.npc_skier_fallen: 
                            npc_skier_obj.npc_skier_setFall() 
                    elif npc_obstacle_hit.attribute in self.cfg.RAMPS:
                        pass 
                    elif npc_obstacle_hit.attribute == 'start_gate_once':
                        pass 
            
            self.updateFrame(screen, self.tiled_background, obstacles, skier, score, skier.rect) 
            clock.tick(cfg.FPS)
        
        pygame.quit() 

    def reset_game_state(self, skier, obstacles, initial_setup=False):
        skier.setForward()
        skier.rect.center = [self.cfg.SCREENSIZE[0] // 2, self.cfg.SCREENSIZE[1] // 2]
        
        skier.current_hearts = skier.max_hearts
        skier.current_power = 0
        skier.current_defense = skier.max_defense

        obstacles.empty()
        obstacles0 = self.createObstacles(20, 29, num=40)
        obstacles1 = self.createObstacles(10, 19, num=40)
        obstacles.add(obstacles0, obstacles1)
        
        self.start_gate_active = True
        if 'start_point_gate_bridge' in self.env_map_sprites_loaded:
            self.start_gate_instance = ObstacleSprite(
                self.env_map_sprites_loaded['start_point_gate_bridge'],
                [self.cfg.SCREENSIZE[0] // 2, self.cfg.SCREENSIZE[1] + 100], 
                'start_gate_once'
            )
            obstacles.add(self.start_gate_instance)
        elif not initial_setup:
            print("Warning: 'start_point_gate_bridge' sprite not loaded during reset.")

    def createObstacles(self, s_idx, e_idx, num):
        """
        Create obstacles and NPCs based on defined categories.
        s_idx: start index (used for vertical positioning).
        e_idx: end index (used for vertical positioning).
        num: total number of obstacles to create.
        """
        obstacles_group = pygame.sprite.Group()
        screen_width, screen_height = self.cfg.SCREENSIZE

        all_categories = self.cfg.ALL_OBSTACLE_CATEGORIES
        weights = [self.cfg.OBSTACLE_TYPE_WEIGHTS[cat] for cat in all_categories]

        for _ in range(num):
            # Choose obstacle type based on weights
            obstacle_type = random.choices(all_categories, weights=weights, k=1)[0]
            
            selected_list = []
            is_npc_animal = False
            is_npc_skier = False
            is_monster = False

            if obstacle_type == 'collectible': selected_list = self.cfg.COLLECTIBLES
            elif obstacle_type == 'hazard': selected_list = self.cfg.HAZARDS
            elif obstacle_type == 'structure': selected_list = self.cfg.STRUCTURES
            elif obstacle_type == 'animal': 
                selected_list = self.cfg.ANIMALS
                is_npc_animal = True
            elif obstacle_type == 'npc_skier': 
                selected_list = self.cfg.NPC_SKIERS
                is_npc_skier = True
            elif obstacle_type == 'monster': 
                selected_list = self.cfg.MONSTERS
                is_monster = True
            elif obstacle_type == 'scenery': selected_list = self.cfg.SCENERY
            elif obstacle_type == 'ramp': selected_list = self.cfg.RAMPS
            
            if not selected_list: # Skip if category has no items
                continue

            obstacle_name = random.choice(selected_list)
            
            if obstacle_name in self.env_map_sprites_loaded:
                sprite_data = self.env_map_sprites_loaded[obstacle_name]
            elif obstacle_name in self.skier_animations_all: # For NPC skiers
                sprite_data = self.skier_animations_all[obstacle_name]
            elif obstacle_name in self.env_map_sprites_loaded['monster_animated_states'] and is_monster: # For monsters
                sprite_data = self.env_map_sprites_loaded[obstacle_name]
            else:
                # Fallback or error if sprite data is not found
                print(f"Warning: Sprite data not found for obstacle: {obstacle_name}. Skipping.")
                continue

            # Determine initial y position
            # This logic needs refinement for continuous generation.
            # For now, let's distribute them within a reasonable visible range.
            start_y = random.randint(s_idx * 100, e_idx * 100) # Simple range for now, assuming 100px per 'unit'
            
            # Use random.choice for horizontal distribution
            # A fixed set of x-coordinates might be useful for lane-like placement,
            # but for now, random across screen width
            x_pos = random.randint(50, screen_width - 50) # Avoid edges

            obstacle = ObstacleSprite(
                sprite_data,
                [x_pos, start_y],
                obstacle_name,
                is_npc_animal=is_npc_animal,
                is_npc_skier=is_npc_skier,
                is_monster=is_monster
            )
            obstacles_group.add(obstacle)

        return obstacles_group


    def display_skin_selection_interface_graphical(self, screen):
        tfont_title = self.resource_loader.fonts['small']
        cfont_instructions = self.resource_loader.fonts['medium']
        cfont_arrows = self.resource_loader.fonts['small']
        cfont_name = self.resource_loader.fonts['default']
        button_font = self.resource_loader.fonts['button']

        clock = pygame.time.Clock()
        
        skier_options = sorted(list(self.skier_animations_all.keys()))
        if not skier_options:
            print("Error: No skier skins loaded! Cannot display selection screen.")
            return 'player1'

        current_selection_index = 0

        # Calculate dynamic positions based on current screen size
        current_screen_w, current_screen_h = screen.get_size()

        title_text_surface = tfont_title.render("Select Your Skier", True, (0, 0, 0))
        title_rect = title_text_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 5))

        instructions_text_surface = cfont_instructions.render("Use LEFT/RIGHT arrows to choose, ENTER to confirm", True, (50, 50, 50))
        instructions_rect = instructions_text_surface.get_rect(center=(current_screen_w // 2, current_screen_h - 100))

        # Button dimensions relative to screen size
        button_width = current_screen_w // 8
        button_height = current_screen_h // 15
        button_y = current_screen_h // 2 + current_screen_h // 4 # Below skier preview

        confirm_button = Button(
            rect=(current_screen_w // 2 - button_width // 2, button_y, button_width, button_height),
            text="Confirm",
            font=button_font,
            base_color=(50, 200, 50),  # Green
            hover_color=(70, 220, 70),
            text_color=(255, 255, 255),
            action=lambda: None, # Action will be handled in event loop directly
            border_color=(30, 180, 30),
            border_width=3,
            shadow_offset=(5, 5),
            shadow_color=(0, 0, 0, 100)
        )
        buttons = [confirm_button]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.VIDEORESIZE:
                    # Re-create screen and update positions based on new size
                    current_screen_w, current_screen_h = event.size
                    self.screen = pygame.display.set_mode((current_screen_w, current_screen_h), pygame.RESIZABLE)
                    self.cfg.SCREENSIZE = (current_screen_w, current_screen_h) # Update Config for consistency
                    
                    # Re-render texts and reposition them
                    title_text_surface = tfont_title.render("Select Your Skier", True, (0, 0, 0))
                    title_rect = title_text_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 5))
                    instructions_text_surface = cfont_instructions.render("Use LEFT/RIGHT arrows to choose, ENTER to confirm", True, (50, 50, 50))
                    instructions_rect = instructions_text_surface.get_rect(center=(current_screen_w // 2, current_screen_h - 100))

                    # Recalculate button position
                    confirm_button.rect.topleft = (current_screen_w // 2 - button_width // 2, button_y)
                    confirm_button.text_rect.center = confirm_button.rect.center


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_selection_index = (current_selection_index - 1 + len(skier_options)) % len(skier_options)
                    elif event.key == pygame.K_RIGHT:
                        current_selection_index = (current_selection_index + 1) % len(skier_options)
                    elif event.key == pygame.K_RETURN:
                        return skier_options[current_selection_index]
                
                # Handle button events
                if confirm_button.handle_event(event):
                    return skier_options[current_selection_index] # Confirm button clicked

            # Draw background gradient
            self._draw_gradient_background(screen, (200, 220, 255), (150, 180, 230)) # Light blue to slightly darker blue

            screen.blit(title_text_surface, title_rect)
            screen.blit(instructions_text_surface, instructions_rect)
            
            # Draw skier preview
            skier_id = skier_options[current_selection_index]
            skier_preview_image = self.skier_animations_all[skier_id].get(Config.SKIER_ANIMATION_MAP['forward'])
            
            if skier_preview_image:
                preview_width = current_screen_w // 6
                preview_height = current_screen_h // 3.5
                original_width, original_height = skier_preview_image.get_size()
                scale_factor = min(preview_width / original_width, preview_height / original_height)
                scaled_image_w = int(original_width * scale_factor)
                scaled_image_h = int(original_height * scale_factor)
                
                scaled_preview = pygame.transform.scale(skier_preview_image, (scaled_image_w, scaled_image_h))
                
                center_x_pos = current_screen_w // 2
                center_y_pos = current_screen_h // 2.5 # Adjust Y to be higher for preview
                
                preview_rect = scaled_preview.get_rect(center=(center_x_pos, center_y_pos))
                
                # Highlight the selected skier
                highlight_color = (0, 150, 255)
                padding = 15
                highlight_rect = preview_rect.inflate(padding * 2, padding * 2)
                draw_rounded_rect(screen, (255, 255, 255, 100), highlight_rect, 10, border_color=highlight_color, border_width=5) # Semi-transparent white background for highlight
                
                screen.blit(scaled_preview, preview_rect)

                name_text_surface = cfont_name.render(skier_id.replace('player', 'Skier '), True, (50, 50, 50))
                name_rect = name_text_surface.get_rect(midtop=(preview_rect.centerx, preview_rect.bottom + 20))
                screen.blit(name_text_surface, name_rect)

            # Draw buttons
            for btn in buttons:
                btn.draw(screen)

            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    def _draw_gradient_background(self, surface, color1, color2):
        """Draws a vertical gradient background."""
        width, height = surface.get_size()
        for y in range(height):
            # Interpolate colors
            r = color1[0] + (float(y) / height) * (color2[0] - color1[0])
            g = color1[1] + (float(y) / height) * (color2[1] - color1[1])
            b = color1[2] + (float(y) / height) * (color2[2] - color1[2])
            pygame.draw.line(surface, (int(r), int(g), int(b)), (0, y), (width, y))

    '''Show game start interface'''
    def display_start_interface(self, screen):
        clock = pygame.time.Clock()
        current_screen_w, current_screen_h = screen.get_size()

        title_font = self.resource_loader.fonts['large']
        content_font = self.resource_loader.fonts['medium']
        button_font = self.resource_loader.fonts['button']

        title_surface = title_font.render(u'Ski Games', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 4))
        
        content_surface = content_font.render(u'Press "Start Game" to begin your adventure!', True, (240, 240, 240))
        content_rect = content_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 2))

        # Start Game Button
        button_width = current_screen_w // 6
        button_height = current_screen_h // 12
        start_button_y = current_screen_h * 0.7

        start_button = Button(
            rect=(current_screen_w // 2 - button_width // 2, start_button_y, button_width, button_height),
            text="Start Game",
            font=button_font,
            base_color=(0, 150, 255), # Blue
            hover_color=(0, 180, 255), # Lighter Blue on hover
            text_color=(255, 255, 255),
            action=lambda: None, # Action handled in loop
            border_color=(0, 100, 200), # Darker blue border
            border_width=3,
            shadow_offset=(5,5),
            shadow_color=(0,0,0,100)
        )
        buttons = [start_button]


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.VIDEORESIZE:
                    current_screen_w, current_screen_h = event.size
                    self.screen = pygame.display.set_mode((current_screen_w, current_screen_h), pygame.RESIZABLE)
                    self.cfg.SCREENSIZE = (current_screen_w, current_screen_h)

                    # Re-render texts and reposition
                    title_surface = title_font.render(u'Ski Games', True, (255, 255, 255))
                    title_rect = title_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 4))
                    content_surface = content_font.render(u'Press "Start Game" to begin your adventure!', True, (240, 240, 240))
                    content_rect = content_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 2))

                    # Recalculate button position
                    start_button.rect.topleft = (current_screen_w // 2 - button_width // 2, start_button_y)
                    start_button.text_rect.center = start_button.rect.center

                # Handle button events for start_button
                if start_button.handle_event(event):
                    return # Start game

            self._draw_gradient_background(screen, (50, 100, 150), (20, 50, 80)) # Dark blue gradient
            
            screen.blit(title_surface, title_rect)
            screen.blit(content_surface, content_rect)
            
            for btn in buttons:
                btn.draw(screen)

            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    '''Show game over interface'''
    def display_game_over_interface(self, screen, skier, obstacles, current_score, current_distance, clock):
        current_screen_w, current_screen_h = screen.get_size()
        
        title_font = self.resource_loader.fonts['large']
        content_font = self.resource_loader.fonts['medium']
        button_font = self.resource_loader.fonts['button']

        game_over_text_surface = title_font.render(u'Game Over!', True, (255, 50, 50)) # Red color for game over
        game_over_rect = game_over_text_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 4))
        
        final_score_text_surface = content_font.render(f"Final Score: {current_score}", True, (255, 255, 255))
        final_score_rect = final_score_text_surface.get_rect(center=(current_screen_w // 2, game_over_rect.bottom + 20))

        # Buttons
        button_width = current_screen_w // 7
        button_height = current_screen_h // 12
        button_spacing = 20

        play_again_y = final_score_rect.bottom + current_screen_h // 8
        play_again_button = Button(
            rect=(current_screen_w // 2 - button_width // 2, play_again_y, button_width, button_height),
            text="Play Again",
            font=button_font,
            base_color=(50, 200, 50),
            hover_color=(70, 220, 70),
            text_color=(255, 255, 255),
            action=lambda: None,
            border_color=(30, 180, 30),
            border_width=3,
            shadow_offset=(5, 5),
            shadow_color=(0, 0, 0, 100)
        )

        quit_game_y = play_again_button.rect.bottom + button_spacing
        quit_game_button = Button(
            rect=(current_screen_w // 2 - button_width // 2, quit_game_y, button_width, button_height),
            text="Quit Game",
            font=button_font,
            base_color=(200, 50, 50), # Red
            hover_color=(220, 70, 70),
            text_color=(255, 255, 255),
            action=lambda: None,
            border_color=(180, 30, 30),
            border_width=3,
            shadow_offset=(5, 5),
            shadow_color=(0, 0, 0, 100)
        )
        buttons = [play_again_button, quit_game_button]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.VIDEORESIZE:
                    current_screen_w, current_screen_h = event.size
                    self.screen = pygame.display.set_mode((current_screen_w, current_screen_h), pygame.RESIZABLE)
                    self.cfg.SCREENSIZE = (current_screen_w, current_screen_h)

                    # Re-render texts and reposition
                    game_over_text_surface = title_font.render(u'Game Over!', True, (255, 50, 50))
                    game_over_rect = game_over_text_surface.get_rect(center=(current_screen_w // 2, current_screen_h // 4))
                    final_score_text_surface = content_font.render(f"Final Score: {current_score}", True, (255, 255, 255))
                    final_score_rect = final_score_text_surface.get_rect(center=(current_screen_w // 2, game_over_rect.bottom + 20))

                    # Recalculate button positions
                    play_again_button.rect.topleft = (current_screen_w // 2 - button_width // 2, play_again_y)
                    play_again_button.text_rect.center = play_again_button.rect.center
                    quit_game_button.rect.topleft = (current_screen_w // 2 - button_width // 2, quit_game_y)
                    quit_game_button.text_rect.center = quit_game_button.rect.center


                # Handle button events
                if play_again_button.handle_event(event):
                    self.reset_game_state(skier, obstacles)
                    return True
                if quit_game_button.handle_event(event):
                    return False

            self._draw_gradient_background(screen, (80, 80, 80), (30, 30, 30)) # Dark grey gradient
            
            screen.blit(game_over_text_surface, game_over_rect)
            screen.blit(final_score_text_surface, final_score_rect)
            
            for btn in buttons:
                btn.draw(screen)

            pygame.display.flip()
            clock.tick(self.cfg.FPS)

    '''Show score'''
    def showScore(self, screen, score):
        font = self.resource_loader.fonts['small']
        score_text = font.render(f"{score}", True, (0, 0, 0))
        
        icon_y_initial = 10
        icon_spacing_y = 25
        defense_row_y = icon_y_initial + (2 * icon_spacing_y) 
        coin_icon_y = defense_row_y + icon_spacing_y
        
        coin_icon_x = 10
        
        score_pos_x = coin_icon_x + self.env_map_sprites_loaded['coin_count'].get_width() + 5
        score_pos_y = coin_icon_y + (self.env_map_sprites_loaded['coin_count'].get_height() // 2) - (score_text.get_height() // 2)
        
        screen.blit(score_text, (score_pos_x, score_pos_y))

    '''Draw snow particles'''
    def drawSnow(self, screen):
        # Update snowflake positions relative to current screen size
        current_screen_w, current_screen_h = screen.get_size()
        for i in range(len(self.snowflakes)):
            x, y = self.snowflakes[i]
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 3)
            # Reset snowflake to top if it goes off screen, relative to current height
            self.snowflakes[i] = (x, y + 2 if y < current_screen_h else 0)

    '''Show player stats (hearts, power, defense)'''
    def show_player_stats(self, screen, skier):
        icon_start_x = 10
        icon_y_initial = 10
        icon_spacing_x = 30 
        icon_spacing_y = 25

        heart_row_y = icon_y_initial
        for i in range(skier.max_hearts):
            if i < skier.current_hearts:
                icon_image = self.env_map_sprites_loaded['heart']
            else:
                icon_image = self.env_map_sprites_loaded['heart_loss']
            screen.blit(icon_image, (icon_start_x + i * icon_spacing_x, heart_row_y))

        power_row_y = heart_row_y + icon_spacing_y
        for i in range(skier.max_power):
            if i < skier.current_power:
                icon_image = self.env_map_sprites_loaded['power']
            else:
                icon_image = self.env_map_sprites_loaded['power_loss']
            screen.blit(icon_image, (icon_start_x + i * icon_spacing_x, power_row_y))

        defense_row_y = power_row_y + icon_spacing_y
        for i in range(skier.max_defense):
            if i < skier.current_defense:
                icon_image = self.env_map_sprites_loaded['defense']
            else:
                icon_image = self.env_map_sprites_loaded['defense_loss']
            screen.blit(icon_image, (icon_start_x + i * icon_spacing_x, defense_row_y))

        coin_icon_y = defense_row_y + icon_spacing_y
        coin_icon_image = self.env_map_sprites_loaded['coin_count']
        screen.blit(coin_icon_image, (icon_start_x, coin_icon_y))


    '''Update current frame of game screen'''
    def updateFrame(self, screen, background_surface, obstacles, skier, score, skier_render_rect=None):
        screen.fill((255, 255, 255)) # Fill with white or clear
        screen.blit(background_surface, (0, 0))
        self.drawSnow(screen) 
        
        if skier.is_jumping or skier.is_boosting:
            skier.draw_skateboard_fire(screen)

        obstacles.draw(screen)
        screen.blit(skier.image, skier_render_rect if skier_render_rect else skier.rect) 
        self.showScore(screen, score)
        self.show_player_stats(screen, skier)
        pygame.display.update()


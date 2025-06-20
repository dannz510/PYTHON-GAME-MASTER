import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import gemSprite, gemGame


'''Config Class'''
class Config():
    # Root directory
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 30
    # Screen size
    SCREENSIZE = (600, 600)
    # Title
    TITLE = 'Match 3 - Dannz'
    # Game element dimensions
    NUMGRID = 8
    GRIDSIZE = 64
    XMARGIN = (SCREENSIZE[0] - GRIDSIZE * NUMGRID) // 2
    YMARGIN = (SCREENSIZE[1] - GRIDSIZE * NUMGRID) // 2
    # Background music path
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bg.mp3')
    # Game sound effects paths
    SOUND_PATHS_DICT = {
        'mismatch': os.path.join(rootdir, 'resources/audios/badswap.wav'),
        'match': [
            os.path.join(rootdir, 'resources/audios/match0.wav'),
            os.path.join(rootdir, 'resources/audios/match1.wav'),
            os.path.join(rootdir, 'resources/audios/match2.wav'),
            os.path.join(rootdir, 'resources/audios/match3.wav'),
            os.path.join(rootdir, 'resources/audios/match4.wav'),
            os.path.join(rootdir, 'resources/audios/match5.wav'),
        ],
    }
    # Font paths
    FONT_PATHS_DICT = {
        'default': {'name': os.path.join(rootdir.replace('gemgem', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 25},
        'score_font': {'name': os.path.join(rootdir.replace('gemgem', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 35}, # Use a different font file here if you have one
        'game_over_font': {'name': os.path.join(rootdir.replace('gemgem', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 40}, # Use a different font file here if you have one
    }
    # Game image paths
    IMAGE_PATHS_DICT = {
        'gem': {
            '1': os.path.join(rootdir, 'resources/images/gem1.png'),
            '2': os.path.join(rootdir, 'resources/images/gem2.png'),
            '3': os.path.join(rootdir, 'resources/images/gem3.png'),
            '4': os.path.join(rootdir, 'resources/images/gem4.png'),
            '5': os.path.join(rootdir, 'resources/images/gem5.png'),
            '6': os.path.join(rootdir, 'resources/images/gem6.png'),
            '7': os.path.join(rootdir, 'resources/images/gem7.png'),
        },
        'grid_cell': os.path.join(rootdir, 'resources/images/grid_cell_hollow.png'), # Path for the hollow grid cell image
        'background_texture': os.path.join(rootdir, 'resources/images/background_texture.png'), # Optional background texture
    }


'''GemGemGame Class'''
class GemGemGame(PygameBaseGame):
    game_type = 'gemgem'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(GemGemGame, self).__init__(config=self.cfg, **kwargs)
    '''Run the game'''
    def run(self):
        # Initialization
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # Play background music
        resource_loader.playbgm()
        # Sound effects
        sounds = resource_loader.sounds
        # Fonts
        font = resource_loader.fonts['default']
        score_font = resource_loader.fonts['score_font']
        game_over_font = resource_loader.fonts['game_over_font']
        # Image loading
        gem_imgs = resource_loader.images['gem']
        grid_cell_image = resource_loader.images['grid_cell']
        background_texture = resource_loader.images.get('background_texture')

        # Main game instance
        game = gemGame(screen, sounds, font, score_font, game_over_font, gem_imgs, cfg, grid_cell_image, background_texture) # Pass all new assets

        while True:
            score = game.start()
            flag = False
            # After a round, player chooses to restart or quit
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                        QuitGame()
                    elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                        flag = True
                if flag:
                    break

                # Draw game over screen
                if background_texture:
                    screen.blit(pygame.transform.scale(background_texture, cfg.SCREENSIZE), (0, 0)) # Use scaled texture
                else:
                    screen.fill((135, 206, 235)) # Fallback to plain blue

                # Use draw_outlined_text for game over messages for better appearance
                game.draw_outlined_text(
                    'Final score: %s' % score,
                    game_over_font,
                    (85, 65, 0), # Text color
                    (0, 0, 0),   # Outline color
                    (screen.get_width() // 2 - game_over_font.size('Final score: %s' % score)[0] // 2, 150)
                )
                game.draw_outlined_text(
                    'Press <R> to restart the game.',
                    font,
                    (85, 65, 0),
                    (0, 0, 0),
                    (screen.get_width() // 2 - font.size('Press <R> to restart the game.')[0] // 2, 250)
                )
                game.draw_outlined_text(
                    'Press <Esc> to quit the game.',
                    font,
                    (85, 65, 0),
                    (0, 0, 0),
                    (screen.get_width() // 2 - font.size('Press <Esc> to quit the game.')[0] // 2, 350)
                )

                pygame.display.update()
            game.reset()
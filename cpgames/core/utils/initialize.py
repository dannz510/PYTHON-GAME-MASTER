
import pygame


'''Game initialization based on pygame'''
def InitPygame(screensize, title='Author: Dannz', init_mixer=True):
    pygame.init()
    if init_mixer: pygame.mixer.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption(title)
    return screen
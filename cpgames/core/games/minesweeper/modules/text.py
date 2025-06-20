# text.py (No changes needed for visual enhancement, as it's just displaying text)

import pygame


'''Text Board Class'''
class TextBoard(pygame.sprite.Sprite):
    def __init__(self, text, font, position, color, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = font
        self.position = position
        self.color = color
        
    def draw(self, screen):
        # Render the text surface
        text_render = self.font.render(self.text, True, self.color)
        # Blit the text onto the screen at the specified position
        screen.blit(text_render, self.position)
        
    def update(self, text):
        self.text = text

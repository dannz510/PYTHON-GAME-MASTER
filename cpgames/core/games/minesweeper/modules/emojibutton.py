# emojibutton.py

import pygame


'''Emoji Button Class'''
class EmojiButton(pygame.sprite.Sprite):
    def __init__(self, images, position, status_code=0, size=(40, 40), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # Load images
        self.images = images
        self.image_surface = self.images['face_normal'] # Store original image surface
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        # Current status of the emoji button
        self.status_code = status_code
        self.size = size

    '''Draw to screen'''
    def draw(self, screen):
        # Get config for colors (assuming Config is accessible, or passed down)
        # Corrected import for Config: go up one level from current directory
        from ..minesweeper import Config as cfg 

        # Determine 3D effect colors based on status
        if self.status_code == 0: # Normal/Raised state
            top_left_color = cfg.LIGHT_GREY
            bottom_right_color = cfg.DARK_GREY
            center_color = cfg.BACKGROUND_COLOR
        else: # Pressed/Sunken state (game over or won)
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR # Can be adjusted for a different sunken color

        # Draw the 3D button effect
        pygame.draw.rect(screen, top_left_color, self.rect)
        pygame.draw.rect(screen, bottom_right_color, self.rect, 0, 3) # Rounded corners, no border
        
        # Draw inner "face" area
        inner_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
        pygame.draw.rect(screen, center_color, inner_rect)

        # Update the image based on status code
        if self.status_code == 0:
            self.image_surface = self.images['face_normal']
        elif self.status_code == 1:
            self.image_surface = self.images['face_fail']
        elif self.status_code == 2:
            self.image_surface = self.images['face_success']
        
        # Center the emoji image on the button
        image_rect = self.image_surface.get_rect(center=self.rect.center)
        screen.blit(self.image_surface, image_rect)

    '''Set the current status of the button'''
    def setstatus(self, status_code):
        self.status_code = status_code


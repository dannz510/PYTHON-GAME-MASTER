# mine.py

import pygame


'''Mine Cell Class'''
class Mine(pygame.sprite.Sprite):
    def __init__(self, images, position, status_code=0, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # Load images dictionary
        self.images = images
        # Initial image is 'blank' (unopened)
        self.image_surface = self.images['blank'] # Store original surface
        self.rect = self.image_surface.get_rect()
        self.rect.topleft = position
        # Current status of the mine cell (0: unopened, 1: opened, 2: flag, etc.)
        self.status_code = status_code
        # True if it's a mine, False otherwise
        self.is_mine_flag = False
        # Number of mines around (-1 means not calculated/opened yet)
        self.num_mines_around = -1
        
    '''Set the current status code'''
    def setstatus(self, status_code):
        self.status_code = status_code
        
    '''Bury a mine in this cell'''
    def burymine(self):
        self.is_mine_flag = True
        
    '''Set the number of mines around this cell'''
    def setnumminesaround(self, num_mines_around):
        self.num_mines_around = num_mines_around
        
    '''Draw to screen with 3D effects'''
    def draw(self, screen):
        # Import Config to access color definitions from the parent directory
        from ..minesweeper import Config as cfg # Corrected import for colors

        # Determine 3D effect colors based on status
        if self.status_code == 0: # Unopened state (raised button)
            top_left_color = cfg.LIGHT_GREY
            bottom_right_color = cfg.DARK_GREY
            center_color = cfg.BACKGROUND_COLOR # Inner color of the raised button
            
            # Draw the raised 3D effect
            pygame.draw.rect(screen, top_left_color, self.rect)
            # Inner rectangle for the face of the button
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            # Bottom and right shadows
            pygame.draw.line(screen, bottom_right_color, self.rect.bottomleft, self.rect.bottomright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topright, self.rect.bottomright, 2)

            # Set image for unopened state
            self.image_surface = self.images['blank']
            
        elif self.status_code == 1: # Opened state (sunken)
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR # Inner color of the sunken cell

            # Draw the sunken 3D effect
            pygame.draw.rect(screen, top_left_color, self.rect)
            # Inner rectangle for the face of the cell
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            # Top and left highlights for sunken effect
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)

            # Set image based on whether it's a mine or a number
            self.image_surface = self.images['mine'] if self.is_mine_flag else self.images[str(self.num_mines_around)]
            
        elif self.status_code == 2: # Flagged state (sunken appearance for visual consistency)
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR
            pygame.draw.rect(screen, top_left_color, self.rect)
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)
            self.image_surface = self.images['flag']
            
        elif self.status_code == 3: # Question mark state (sunken appearance)
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR
            pygame.draw.rect(screen, top_left_color, self.rect)
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)
            self.image_surface = self.images['ask']
            
        elif self.status_code == 4: # Being double-clicked (sunken, assert not mine)
            assert not self.is_mine_flag
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR
            pygame.draw.rect(screen, top_left_color, self.rect)
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)
            self.image_surface = self.images[str(self.num_mines_around)]
            
        elif self.status_code == 5: # Around double-clicked (temporary sunken for visual feedback)
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR
            pygame.draw.rect(screen, top_left_color, self.rect)
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)
            self.image_surface = self.images['0'] # Show blank/0 for visual
            
        elif self.status_code == 6: # Mine clicked (blood)
            assert self.is_mine_flag
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR
            pygame.draw.rect(screen, top_left_color, self.rect)
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)
            self.image_surface = self.images['blood']
            
        elif self.status_code == 7: # Mis-flagged (error)
            assert not self.is_mine_flag
            top_left_color = cfg.PRESSED_DARK
            bottom_right_color = cfg.PRESSED_LIGHT
            center_color = cfg.BACKGROUND_COLOR
            pygame.draw.rect(screen, top_left_color, self.rect)
            face_rect = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)
            pygame.draw.rect(screen, center_color, face_rect)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.topright, 2)
            pygame.draw.line(screen, bottom_right_color, self.rect.topleft, self.rect.bottomleft, 2)
            self.image_surface = self.images['error']

        # Blit the actual image (number, flag, mine, etc.) onto the center of the cell
        image_rect = self.image_surface.get_rect(center=self.rect.center)
        screen.blit(self.image_surface, image_rect)

    @property
    def opened(self):
        return self.status_code == 1

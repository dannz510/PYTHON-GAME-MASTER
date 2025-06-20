# sprites.py
import pygame


'''Pusher (Player) Sprite class'''
class pusherSprite(pygame.sprite.Sprite):
    def __init__(self, col, row, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = resource_loader.images['player'].convert_alpha() # Use convert_alpha for transparency
        self.image = pygame.transform.scale(self.original_image, (cfg.BLOCKSIZE, cfg.BLOCKSIZE))
        self.rect = self.image.get_rect()
        self.col = col
        self.row = row
        self.cfg = cfg # Store cfg for blocksize reference

    '''Move'''
    def move(self, direction, is_test=False):
        # Test mode represents simulated movement
        new_col, new_row = self.col, self.row
        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1
        
        if is_test:
            return new_col, new_row
        else:
            self.col = new_col
            self.row = new_row

    '''Draw player to game surface'''
    def draw(self, screen):
        # Calculate screen position based on col, row and block size
        self.rect.x = self.col * self.cfg.BLOCKSIZE
        self.rect.y = self.row * self.cfg.BLOCKSIZE
        screen.blit(self.image, self.rect)


'''Game Element Sprite class'''
class elementSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, col, row, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        # Load and scale image
        self.original_image = resource_loader.images[sprite_name].convert_alpha() # Use convert_alpha for transparency
        self.image = pygame.transform.scale(self.original_image, (cfg.BLOCKSIZE, cfg.BLOCKSIZE))
        self.rect = self.image.get_rect()
        
        self.sprite_type = sprite_name.split('.')[0] # e.g., 'box', 'target', 'wall'
        self.col = col
        self.row = row
        self.cfg = cfg # Store cfg for blocksize reference

    '''Draw game element to game surface'''
    def draw(self, screen):
        # Calculate screen position based on col, row and block size
        self.rect.x = self.col * self.cfg.BLOCKSIZE
        self.rect.y = self.row * self.cfg.BLOCKSIZE
        screen.blit(self.image, self.rect)

    '''Move game element (only applicable to boxes)'''
    def move(self, direction, is_test=False):
        if self.sprite_type == 'box':
            new_col, new_row = self.col, self.row
            if direction == 'up':
                new_row -= 1
            elif direction == 'down':
                new_row += 1
            elif direction == 'left':
                new_col -= 1
            elif direction == 'right':
                new_col += 1
            
            if is_test:
                return new_col, new_row
            else:
                self.col = new_col
                self.row = new_row
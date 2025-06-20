import pygame
import random

'''
Class: Bullet
Description: Represents a bullet fired by a ship.
'''
class Bullet(pygame.sprite.Sprite):
    def __init__(self, idx, position, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.image = resource_loader.images['bullet'].convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20)) # Slightly taller bullet
        self.rect = self.image.get_rect()
        self.position = position[0] - self.rect.width // 2, position[1] - self.rect.height # Center bullet horizontally, place above ship
        self.rect.left, self.rect.top = self.position
        self.speed = 15 # Increased bullet speed
        self.player_idx = idx # Player ID (1 or 2)
    '''
    Method: move
    Description: Moves the bullet upwards on the screen.
    '''
    def move(self):
        self.position = self.position[0], self.position[1] - self.speed
        self.rect.left, self.rect.top = self.position
    '''
    Method: draw
    Description: Draws the bullet on the screen.
    Parameters:
        screen: Pygame display surface.
    '''
    def draw(self, screen):
        screen.blit(self.image, self.rect)


'''
Class: Asteroid
Description: Represents an asteroid that moves down the screen and rotates.
'''
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = resource_loader.images['asteroid'].convert_alpha()
        
        # Randomize asteroid size
        size_scale = random.uniform(0.7, 1.3) # Asteroids can be 70% to 130% of original size
        original_width, original_height = self.original_image.get_size()
        new_width = int(original_width * size_scale)
        new_height = int(original_height * size_scale)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect()

        # Location: Start from top, random X position
        self.position = (random.randrange(20, cfg.SCREENSIZE[0] - 20 - self.rect.width), -self.rect.height)
        self.rect.left, self.rect.top = self.position

        # Speed: Randomized vertical speed
        self.speed_y = random.randrange(2, 6) # Asteroids move at varying speeds
        self.speed_x = random.randrange(-2, 3) # Small horizontal movement
        
        # Rotation
        self.angle = 0
        self.rotation_speed = random.choice([-3, -2, 2, 3]) # Random rotation direction and speed

    '''
    Method: move
    Description: Moves the asteroid down and horizontally.
    '''
    def move(self):
        self.position = (self.position[0] + self.speed_x, self.position[1] + self.speed_y)
        self.rect.left, self.rect.top = self.position

    '''
    Method: rotate
    Description: Rotates the asteroid image.
    '''
    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center) # Keep center same after rotation

    '''
    Method: draw
    Description: Draws the asteroid on the screen.
    Parameters:
        screen: Pygame display surface.
    '''
    def draw(self, screen):
        screen.blit(self.image, self.rect)


'''
Class: Ship
Description: Represents a player's spacecraft.
'''
class Ship(pygame.sprite.Sprite):
    def __init__(self, idx, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.image = resource_loader.images['ship'].convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60)) # Scale ship image
        self.explode_image = resource_loader.images['ship_exploded'].convert_alpha() # 48x48 sprite sheet

        # Initial position based on player index
        if idx == 1:
            self.position = {'x': cfg.SCREENSIZE[0] // 2 - 100, 'y': cfg.SCREENSIZE[1] - 80}
        else: # Player 2
            self.position = {'x': cfg.SCREENSIZE[0] // 2 + 50, 'y': cfg.SCREENSIZE[1] - 80}
            
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position['x'], self.position['y']
        
        self.speed = {'x': 10, 'y': 8} # Increased speed for better responsiveness
        self.player_idx = idx
        self.cooling_time = 0 # Bullet cooldown timer
        self.fire_rate = 15 # Frames between shots (lower = faster)

        self.explode_step = 0 # Step for explosion animation
        self.max_explode_steps = 16 # Adjust based on your sprite sheet (4 frames * 4 rows or similar)
        # Assuming ship_exploded.png is a sprite sheet with 4 frames horizontally for explosion
        self.explosion_frame_width = self.explode_image.get_width() // 4 
        self.explosion_frame_height = self.explode_image.get_height()

        self.lives = 3 # Initial lives for each player
        self.is_invincible = False # Invincibility after hit
        self.invincible_timer = 0
        self.invincible_duration = cfg.FPS * 2 # 2 seconds of invincibility

    '''
    Method: explode
    Description: Animates the ship explosion.
    Parameters:
        screen: Pygame display surface.
    '''
    def explode(self, screen):
        if self.explode_step < self.max_explode_steps:
            # Assuming a single row sprite sheet for explosion
            frame_x = (self.explode_step % 4) * self.explosion_frame_width
            img = self.explode_image.subsurface((frame_x, 0, self.explosion_frame_width, self.explosion_frame_height))
            screen.blit(img, (self.position['x'], self.position['y']))
            self.explode_step += 1
        else:
            self.explode_step = 0 # Reset or signal explosion complete
            return True # Indicate explosion finished
        return False

    '''
    Method: move
    Description: Moves the ship based on direction input.
    Parameters:
        direction: String ('left', 'right', 'up', 'down').
    '''
    def move(self, direction):
        # Get screen dimensions dynamically
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        if direction == 'left':
            self.position['x'] = max(self.position['x'] - self.speed['x'], 0) # Strict left boundary
        elif direction == 'right':
            self.position['x'] = min(self.position['x'] + self.speed['x'], screen_width - self.rect.width) # Strict right boundary
        elif direction == 'up':
            # Allow movement from top (0) to bottom of screen (screen_height - self.rect.height)
            self.position['y'] = max(self.position['y'] - self.speed['y'], 0) 
        elif direction == 'down':
            # Allow movement from top (0) to bottom of screen (screen_height - self.rect.height)
            self.position['y'] = min(self.position['y'] + self.speed['y'], screen_height - self.rect.height) 
        self.rect.left, self.rect.top = self.position['x'], self.position['y']

    '''
    Method: update_cooldown
    Description: Decrements the bullet cooldown timer.
    '''
    def update_cooldown(self):
        if self.cooling_time > 0:
            self.cooling_time -= 1
    
    '''
    Method: can_shoot
    Description: Checks if the ship can fire a bullet based on cooldown.
    Returns:
        bool: True if the ship can shoot, False otherwise.
    '''
    def can_shoot(self):
        return self.cooling_time == 0

    '''
    Method: reset_cooldown
    Description: Resets the bullet cooldown timer after firing.
    '''
    def reset_cooldown(self):
        self.cooling_time = self.fire_rate

    '''
    Method: take_hit
    Description: Reduces player lives and activates invincibility.
    '''
    def take_hit(self):
        if not self.is_invincible:
            self.lives -= 1
            if self.lives > 0:
                self.is_invincible = True
                self.invincible_timer = self.invincible_duration
            return True # Indicates hit taken
        return False # Indicates no hit due to invincibility

    '''
    Method: update_invincibility
    Description: Updates the invincibility timer and state.
    '''
    def update_invincibility(self):
        if self.is_invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.is_invincible = False
    
    '''
    Method: draw
    Description: Draws the ship on the screen, with a flashing effect if invincible.
    Parameters:
        screen: Pygame display surface.
    '''
    def draw(self, screen):
        if self.is_invincible and (self.invincible_timer // 5) % 2 == 0: # Flashing effect
            return # Don't draw if invisible part of flash
        screen.blit(self.image, self.rect)

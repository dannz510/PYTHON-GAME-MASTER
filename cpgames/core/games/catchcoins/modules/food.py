import pygame
import random
import os # Import os to check for bomb image if needed (optional)

# Assuming bomb.png exists in resources/images, or create a placeholder if not
# For now, if 'bomb' image is not found, it will default to a gold image with a red tint.
# You can create a simple red circle or explosion image for 'bomb.png'

'''定义食物类'''
class Food(pygame.sprite.Sprite):
    def __init__(self, images_dict, selected_key, screensize, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.screensize = screensize
        self.selected_key = selected_key # Store selected key

        # Load image based on key
        if selected_key == 'bomb':
            # Check if a bomb image exists, otherwise use a placeholder or gold with tint
            bomb_image_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resources/images/bomb.png')
            if os.path.exists(bomb_image_path):
                self.image = pygame.image.load(bomb_image_path).convert_alpha()
            else:
                # Placeholder: use gold image and tint it red for a 'bomb' effect
                self.image = images_dict['gold'].copy()
                # Apply a red tint for the 'bomb' visual
                red_tint = pygame.Surface(self.image.get_size()).convert_alpha()
                red_tint.fill((255, 0, 0, 100)) # Red color with 100 alpha (semi-transparent)
                self.image.blit(red_tint, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            self.image = images_dict[selected_key].copy() # .copy() to allow individual tinting if needed

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = random.randint(20, screensize[0]-self.rect.width-20), -10 # Adjusted to prevent spawning off-screen
        self.speed = random.randrange(4, 8) # Slightly adjusted speed range
        self.score = 1 if selected_key == 'gold' else (-5 if selected_key == 'bomb' else 5) # Bomb subtracts score
    '''更新食物位置'''
    def update(self):
        self.rect.bottom += self.speed
        if self.rect.top > self.screensize[1]:
            return True
        return False
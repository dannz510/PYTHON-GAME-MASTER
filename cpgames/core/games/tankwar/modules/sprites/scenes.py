
import pygame


'''砖墙'''
class Brick(pygame.sprite.Sprite):
    def __init__(self, position, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position


'''铁墙'''
class Iron(pygame.sprite.Sprite):
    def __init__(self, position, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position


'''冰'''
class Ice(pygame.sprite.Sprite):
    def __init__(self, position, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        for i in range(2):
            for j in range(2):
                self.image.blit(image, (12*i, 12*j))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position


'''河流'''
class River(pygame.sprite.Sprite):
    def __init__(self, position, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        for i in range(2):
            for j in range(2):
                self.image.blit(image, (12*i, 12*j))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position


'''树'''
class Tree(pygame.sprite.Sprite):
    def __init__(self, position, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        for i in range(2):
            for j in range(2):
                self.image.blit(image, (12*i, 12*j))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
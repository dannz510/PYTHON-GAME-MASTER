import pygame
import random

'''画游戏网格'''
def drawGameGrid(cfg, screen):
    # Use the new grid color from config
    color = cfg.GRID_COLOR
    for x in range(0, cfg.SCREENSIZE[0], cfg.BLOCK_SIZE):
        pygame.draw.line(screen, color, (x, 0), (x, cfg.SCREENSIZE[1]))
    for y in range(0, cfg.SCREENSIZE[1], cfg.BLOCK_SIZE):
        pygame.draw.line(screen, color, (0, y), (cfg.SCREENSIZE[0], y))


'''显示得分'''
def showScore(cfg, score, screen, resource_loader):
    color = (255, 255, 255)
    font = resource_loader.fonts['score_font'] # Use the larger score font
    text = font.render('Score: %s' % score, True, color)
    rect = text.get_rect()
    rect.topleft = (10, 10)
    screen.blit(text, rect)


'''粒子效果类 (New)'''
class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, block_size, color):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = (position[0] + 0.5) * block_size, (position[1] + 0.5) * block_size
        self.color = color
        self.radius = random.randint(2, 5)
        self.lifetime = random.randint(30, 60) # Frames
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.alpha = 255 # For fading out

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime -= 1
        self.alpha = max(0, self.alpha - (255 / self.lifetime if self.lifetime > 0 else 255)) # Fade out

        if self.lifetime <= 0:
            self.kill() # Remove particle when its lifetime is over

        # Update color with fading alpha
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (self.color[0], self.color[1], self.color[2], int(self.alpha)), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
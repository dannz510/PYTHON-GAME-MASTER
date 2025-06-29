
import pygame
from .....utils import QuitGame


'''游戏结束主界面'''
class MainInterface(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.image = resource_loader.images['end']['gameover'].convert()
        self.rect = self.image.get_rect()
        self.rect.center = cfg.SCREENSIZE[0] / 2, cfg.SCREENSIZE[1] / 2
    '''更新函数'''
    def update(self):
        pass


'''继续游戏按钮'''
class ContinueButton(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader, position=(400, 409)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = resource_loader.images['end']['continue_black'].convert()
        self.image_2 = resource_loader.images['end']['continue_red'].convert()
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = position
    '''更新函数: 不断地更新检测鼠标是否在按钮上'''
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_2
        else:
            self.image = self.image_1


'''游戏结束类'''
class EndInterface():
    def __init__(self, cfg, resource_loader):
        self.cfg = cfg
        self.main_interface = MainInterface(cfg, resource_loader)
        self.continue_btn = ContinueButton(cfg, resource_loader)
        self.components = pygame.sprite.LayeredUpdates(self.main_interface, self.continue_btn)
    '''外部调用'''
    def update(self, screen):
        clock = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        count = 0
        flag = True
        while True:
            count += 1
            clock.tick(self.cfg.FPS)
            self.components.clear(screen, background)
            self.components.update()
            if count % 10 == 0:
                count = 0
                flag = not flag
            if flag:
                self.components.draw(screen)
            else:
                screen.blit(self.main_interface.image, self.main_interface.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.continue_btn.rect.collidepoint(mouse_pos):
                            return True
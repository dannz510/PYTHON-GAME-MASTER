import copy
import random
import pygame


'''贪吃蛇类'''
class Snake(pygame.sprite.Sprite):
    def __init__(self, cfg, skin='default', **kwargs): # Added 'skin' parameter with default
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        self.skin = skin # Initialize self.skin
        self.head_coord = [random.randint(5, cfg.GAME_MATRIX_SIZE[0]-6), random.randint(5, cfg.GAME_MATRIX_SIZE[1]-6)]
        self.tail_coords = []
        for i in range(1, 3):
            self.tail_coords.append([self.head_coord[0]-i, self.head_coord[1]])
        self.direction = 'right'
        
        # Use the skin from config
        self.head_colors = cfg.SNAKE_SKINS[self.skin]['head']
        self.tail_colors = cfg.SNAKE_SKINS[self.skin]['tail']
    '''设置方向'''
    def setDirection(self, direction):
        assert direction in ['up', 'down', 'right', 'left']
        if direction == 'up':
            if self.head_coord[1]-1 != self.tail_coords[0][1]:
                self.direction = direction
        elif direction == 'down':
            if self.head_coord[1]+1 != self.tail_coords[0][1]:
                self.direction = direction
        elif direction == 'left':
            if self.head_coord[0]-1 != self.tail_coords[0][0]:
                self.direction = direction
        elif direction == 'right':
            if self.head_coord[0]+1 != self.tail_coords[0][0]:
                self.direction = direction
    '''更新蛇的位置'''
    def update(self, apple):
        self.tail_coords.insert(0, copy.copy(self.head_coord))
        if self.direction == 'up':
            self.head_coord[1] -= 1
        elif self.direction == 'down':
            self.head_coord[1] += 1
        elif self.direction == 'left':
            self.head_coord[0] -= 1
        elif self.direction == 'right':
            self.head_coord[0] += 1
        # --判断是否死亡
        self.isgameover = False
        if self.head_coord[0] < 0 or self.head_coord[0] >= self.cfg.GAME_MATRIX_SIZE[0] or \
           self.head_coord[1] < 0 or self.head_coord[1] >= self.cfg.GAME_MATRIX_SIZE[1] or \
           self.head_coord in self.tail_coords[:-1]:
            self.isgameover = True
        # --判断是否吃到食物
        if self.head_coord == apple.coord:
            return True
        else:
            self.tail_coords = self.tail_coords[:-1]
            return False
    '''在屏幕上画出来'''
    def draw(self, screen):
        head_x, head_y = self.head_coord[0] * self.cfg.BLOCK_SIZE, self.head_coord[1] * self.cfg.BLOCK_SIZE
        rect = pygame.Rect(head_x, head_y, self.cfg.BLOCK_SIZE, self.cfg.BLOCK_SIZE)
        
        # Draw head with multiple colors for effect
        pygame.draw.rect(screen, self.head_colors[0], rect) # Outer color
        rect_inner = pygame.Rect(head_x+4, head_y+4, self.cfg.BLOCK_SIZE-8, self.cfg.BLOCK_SIZE-8)
        pygame.draw.rect(screen, self.head_colors[1], rect_inner) # Inner color
        
        # Draw eyes (simplified example)
        eye_size = 3
        eye_offset = 5
        if self.direction == 'up' or self.direction == 'down':
            left_eye_pos = (head_x + self.cfg.BLOCK_SIZE // 2 - eye_offset, head_y + self.cfg.BLOCK_SIZE // 2 - eye_size)
            right_eye_pos = (head_x + self.cfg.BLOCK_SIZE // 2 + eye_offset, head_y + self.cfg.BLOCK_SIZE // 2 - eye_size)
        else: # left or right
            left_eye_pos = (head_x + self.cfg.BLOCK_SIZE // 2 - eye_size, head_y + self.cfg.BLOCK_SIZE // 2 - eye_offset)
            right_eye_pos = (head_x + self.cfg.BLOCK_SIZE // 2 - eye_size, head_y + self.cfg.BLOCK_SIZE // 2 + eye_offset)
        
        # Draw the main eye part (larger circle)
        pygame.draw.circle(screen, self.head_colors[2], left_eye_pos, eye_size)
        pygame.draw.circle(screen, self.head_colors[2], right_eye_pos, eye_size)
        # Draw the pupil (smaller circle)
        pygame.draw.circle(screen, self.head_colors[3], left_eye_pos, eye_size // 2)
        pygame.draw.circle(screen, self.head_colors[3], right_eye_pos, eye_size // 2)

        # Draw tail
        for coord in self.tail_coords:
            x, y = coord[0] * self.cfg.BLOCK_SIZE, coord[1] * self.cfg.BLOCK_SIZE
            rect = pygame.Rect(x, y, self.cfg.BLOCK_SIZE, self.cfg.BLOCK_SIZE)
            pygame.draw.rect(screen, self.tail_colors[0], rect) # Outer color
            rect_inner = pygame.Rect(x+4, y+4, self.cfg.BLOCK_SIZE-8, self.cfg.BLOCK_SIZE-8)
            pygame.draw.rect(screen, self.tail_colors[1], rect_inner) # Inner color

    '''获得完整的蛇身矩阵'''
    @property
    def coords(self):
        return [self.head_coord] + self.tail_coords
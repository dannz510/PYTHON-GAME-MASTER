import random
import pygame
# import os # No longer needed if not using image for food


'''食物类'''
class Apple(pygame.sprite.Sprite):
    def __init__(self, cfg, snake_coords, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        # Randomly generate coordinate for the apple
        while True:
            self.coord = [random.randint(0, cfg.GAME_MATRIX_SIZE[0]-1), random.randint(0, cfg.GAME_MATRIX_SIZE[1]-1)]
            if self.coord not in snake_coords:
                break
        
        # Define colors for a "beautiful" procedural apple (New)
        self.color_outer = (200, 0, 0)      # Dark red
        self.color_inner = (255, 50, 50)    # Bright red
        self.color_highlight = (255, 255, 255) # White for shine
        self.color = self.color_outer # For particle effects
        
        # self.image and self.rect will be dynamically created in draw
        # No image loading here

    '''获得苹果中心像素坐标 (New helper method)'''
    def get_center_grid_coords(self): # Renamed to better reflect it's grid coords
        return [self.coord[0], self.coord[1]] # Return grid coordinates for particle effect

    '''画到屏幕上'''
    def draw(self, screen):
        cx, cy = int((self.coord[0] + 0.5) * self.cfg.BLOCK_SIZE), int((self.coord[1] + 0.5) * self.cfg.BLOCK_SIZE)
        radius = self.cfg.BLOCK_SIZE // 2 - 2

        # Draw outer circle (base of the apple)
        pygame.draw.circle(screen, self.color_outer, (cx, cy), radius)

        # Draw inner circle (lighter part)
        pygame.draw.circle(screen, self.color_inner, (cx, cy), radius - 3)

        # Draw a small highlight for a shiny effect
        highlight_radius = radius // 3
        # Adjust highlight position based on a fixed light source (e.g., top-left)
        highlight_x = cx - radius // 3
        highlight_y = cy - radius // 3
        pygame.draw.circle(screen, self.color_highlight, (highlight_x, highlight_y), highlight_radius)

        # Optional: A small "stem" or leaf can be added with lines/polygons
        stem_color = (100, 70, 0) # Brown
        leaf_color = (0, 150, 0)  # Green
        # Stem
        pygame.draw.line(screen, stem_color, (cx, cy - radius), (cx, cy - radius - 5), 2)
        # Leaf (simple triangle)
        leaf_points = [(cx, cy - radius - 5), (cx + 5, cy - radius - 10), (cx + 2, cy - radius - 5)]
        pygame.draw.polygon(screen, leaf_color, leaf_points)
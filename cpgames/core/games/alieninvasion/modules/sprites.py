import pygame
import random

# Base colors for the futuristic/holographic look
NEON_BLUE = (0, 200, 255)
NEON_CYAN = (0, 255, 255)
NEON_RED = (255, 50, 100)
NEON_PURPLE = (150, 0, 255)
NEON_ORANGE = (255, 150, 50)
NEON_YELLOW = (255, 255, 50)
TRANSPARENT_BLUE_SHIELD = (50, 150, 255, 128) # RGBA for semi-transparency

# Updated Player Aircraft Sprite
class AircraftSprite(pygame.sprite.Sprite):
    def __init__(self, color, bullet_color, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.num_life = 3
        self.max_num_life = 5
        self.base_color = color # Base color for the ship

        self.cell = [3, 3] # Pixel cell size
        self.num_cols = 15
        self.num_rows = 8
        self.rect = pygame.Rect(0, 550, self.cell[0] * self.num_cols, self.cell[0] * self.num_rows)

        # Futuristic pixel design for the aircraft
        self.filled_cells_frame1 = [ # Main body outline
            7, 21, 22, 23, 36, 37, 38,
            46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
            60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119
        ]
        # Adding some "engine glow" pixels
        self.engine_glow_pixels = [11, 12, 13, 24, 25, 26, 39, 40, 41] # Example glow pixels

        self.bullet_color = bullet_color
        self.is_cooling = False
        self.init_cooling_frames = 35 # Cooldown for normal shot
        self.charge_cooling_frames = 60 # Cooldown for charge shot
        self.cooling_count = self.init_cooling_frames

        self.score = 0
        self.old_score = -1

        # Shielding variables
        self.is_shielded = False
        self.shield_duration = 1500 # milliseconds
        self.shield_timer_start = 0

        self.resetBoom()

    def shot(self, charge=False):
        """Fires a bullet. If 'charge' is True, fires a more powerful bullet."""
        if self.is_cooling:
            return None
        self.is_cooling = True
        self.cooling_count = self.charge_cooling_frames if charge else self.init_cooling_frames
        return MyBulletSprite(self.rect.x + self.rect.width // 2, self.rect.y, self.bullet_color, is_charged=charge)

    def draw(self, screen):
        """Draws the aircraft with a subtle animation or glow."""
        # Main ship body
        for i in range(0, len(self.filled_cells_frame1)):
            y = self.filled_cells_frame1[i] // self.num_cols
            x = self.filled_cells_frame1[i] % self.num_cols
            rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
            pygame.draw.rect(screen, self.base_color, rect)

        # Engine glow (flickering effect)
        if pygame.time.get_ticks() % 200 < 100: # Flicker every 100ms
            for i in self.engine_glow_pixels:
                y = i // self.num_cols
                x = i % self.num_cols
                rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
                pygame.draw.rect(screen, NEON_YELLOW, rect) # Yellowish glow

    def draw_shield(self, screen, color):
        """Draws a semi-transparent shield around the aircraft."""
        shield_surface = pygame.Surface((self.rect.width * 1.2, self.rect.height * 1.2), pygame.SRCALPHA)
        shield_rect = shield_surface.get_rect(center=self.rect.center)
        pygame.draw.ellipse(shield_surface, color, shield_surface.get_rect(), 0) # Fill ellipse
        screen.blit(shield_surface, shield_rect)

    def update(self, WIDTH):
        """Updates aircraft position and cooldowns."""
        x = pygame.mouse.get_pos()[0] - (self.rect.width // 2)
        if x < 0:
            x = pygame.mouse.get_pos()[0]
        elif x > WIDTH - self.rect.width:
            x = WIDTH - self.rect.width
        self.rect.x = x

        if self.is_cooling:
            self.cooling_count -= 1
            if self.cooling_count == 0:
                self.is_cooling = False

        # Shield timer logic
        if self.is_shielded:
            if pygame.time.get_ticks() - self.shield_timer_start > self.shield_duration:
                self.is_shielded = False

    def boom(self, screen, outer_color, core_color):
        """Draws explosion animation."""
        self.boomed_rect.x = self.rect.x
        self.boomed_rect.y = self.rect.y
        self.boomed_count += 1
        if self.boomed_count % 1 == 0: # Control animation speed
            self.boomed_frame += 1
            if self.boomed_frame <= len(self.boomed_filled_cells_outer):
                # Outer ring of explosion
                for i in self.boomed_filled_cells_outer[self.boomed_frame - 1]:
                    y = i // self.boomed_num_cols
                    x = i % self.boomed_num_cols
                    rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
                    pygame.draw.rect(screen, outer_color, rect)
            if self.boomed_frame <= len(self.boomed_filled_cells_core):
                # Inner core of explosion
                for i in self.boomed_filled_cells_core[self.boomed_frame - 1]:
                    y = i // self.boomed_num_cols
                    x = i % self.boomed_num_cols
                    rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
                    pygame.draw.rect(screen, core_color, rect)

        if self.boomed_frame > max(len(self.boomed_filled_cells_outer), len(self.boomed_filled_cells_core)):
            return True # Explosion finished
        else:
            return False

    def resetBoom(self):
        """Resets explosion animation state."""
        self.one_dead = False
        # Define explosion frames as lists of pixels
        self.boomed_filled_cells_outer = [
            [3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95],
            [2,8,11,16,19,23,29,35,41,43,46,52,55,59,61,69,73,79,82,85,90,92,96],
            [1,9,10,14,20,22,28,34,42,47,51,56,60,67,70,72,76,80,84,89,94],
            [0,4,5,6,13,18,21,25,26,27,33,39,40,48,50,57,63,65,66,71,75,87,88,93]
        ]
        self.boomed_filled_cells_core = [
            [44,45,53,54,58,62],
            [30,36,40,41,49,50,51,52,59,60,61,67],
            [24,25,26,27,33,37,38,46,47,48,55,56],
            [12,13,14,15,16,17,19,20,21,22,23]
        ]
        self.boomed_cell = [3, 3]
        self.boomed_num_cols = 11
        self.boomed_num_rows = 9
        self.boomed_rect = pygame.Rect(0, 0, self.boomed_num_cols * self.boomed_cell[0], self.boomed_num_rows * self.boomed_cell[1])
        self.boomed_count = 0
        self.boomed_frame = 0


# Updated UFO Sprite
class UFOSprite(pygame.sprite.Sprite):
    def __init__(self, color, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.reward = 500 # Higher reward for UFO
        self.base_color = color
        self.health = 3 # UFO has health
        self.reset()

    def draw(self, screen):
        if self.is_dead:
            return None
        # Subtle flickering effect for holographic appearance
        if pygame.time.get_ticks() % 100 < 50:
            current_color = self.base_color
        else:
            # Clamping color components to ensure they stay within 0-255 range
            r = min(255, self.base_color[0] + 50)
            g = min(255, self.base_color[1] + 50)
            b = min(255, self.base_color[2] + 50)
            current_color = (r, g, b) # Brighter flicker

        for i in range(0, len(self.filled_cells)):
            y = self.filled_cells[i] // self.num_cols
            x = self.filled_cells[i] % self.num_cols
            rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
            pygame.draw.rect(screen, current_color, rect)

    def update(self, WIDTH):
        if self.is_dead: # Don't update if dead
            return

        # UFO moves across screen and then resets
        self.rect.x += self.speed
        if self.rect.x > WIDTH + 100: # Move further off screen before resetting
            self.reset()

    def boom(self, screen, outer_color, core_color):
        """Draws explosion animation."""
        self.boomed_rect.x = self.rect.x
        self.boomed_rect.y = self.rect.y
        self.boomed_count += 1
        if self.boomed_count % 1 == 0:
            self.boomed_frame += 1
            if self.boomed_frame <= len(self.boomed_filled_cells_outer):
                for i in self.boomed_filled_cells_outer[self.boomed_frame - 1]:
                    y = i // self.boomed_num_cols
                    x = i % self.boomed_num_cols
                    rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
                    pygame.draw.rect(screen, outer_color, rect)
            if self.boomed_frame <= len(self.boomed_filled_cells_core):
                for i in self.boomed_filled_cells_core[self.boomed_frame - 1]:
                    y = i // self.boomed_num_cols
                    x = i % self.boomed_num_cols
                    rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
                    pygame.draw.rect(screen, core_color, rect)

        if self.boomed_frame > max(len(self.boomed_filled_cells_outer), len(self.boomed_filled_cells_core)):
            return True
        else:
            return False

    def reset(self):
        """Resets UFO to initial state, off-screen."""
        self.cell = [3, 3]
        self.num_cols = 16
        self.num_rows = 7
        self.rect = pygame.Rect(random.randint(-800, -200), 60, self.num_cols * self.cell[0], self.num_rows * self.cell[1]) # Random starting X
        # More complex UFO design
        self.filled_cells = [
            5,6,7,8,9,10,
            19,20,21,22,23,24,25,26,27,28,
            34,35,36,37,38,39,40,41,42,43,44,45,
            49,50,52,53,55,56,58,59,61,62,
            64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
            82,83,84,87,88,91,92,93,
            99,108 # Antennas or lights
        ]
        self.speed = 2 # Fixed speed for now
        self.is_dead = False
        self.has_boomed = False
        self.health = 3 # Reset health

        # Explosion frames (same as player, or custom for UFO)
        self.boomed_filled_cells_outer = [
            [3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95],
            [2,8,11,16,19,23,29,35,41,43,46,52,55,59,61,69,73,79,82,85,90,92,96],
            [1,9,10,14,20,22,28,34,42,47,51,56,60,67,70,72,76,80,84,89,94],
            [0,4,5,6,13,18,21,25,26,27,33,39,40,48,50,57,63,65,66,71,75,87,88,93]
        ]
        self.boomed_filled_cells_core = [
            [44,45,53,54,58,62],
            [30,36,40,41,49,50,51,52,59,60,61,67],
            [24,25,26,27,33,37,38,46,47,48,55,56],
            [12,13,14,15,16,17,19,20,21,22,23]
        ]
        self.boomed_cell = [3, 3]
        self.boomed_num_cols = 11
        self.boomed_num_rows = 9
        self.boomed_rect = pygame.Rect(0, 0, self.boomed_num_cols * self.boomed_cell[0], self.boomed_num_rows * self.boomed_cell[1])
        self.boomed_count = 0
        self.boomed_frame = 0


# Updated Enemy Sprite
class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, category, number, color, bullet_color, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.cell = [3, 3]
      
        self.number = number

        self.category = category
        self.base_color = color
        self.health = 1 # All enemies start with 1 health, charged shot takes 2

        # Define different futuristic shapes based on category
        if category == 'small':
            self.reward = 20
            self.num_cols = 8
            self.num_rows = 8
            self.rect = pygame.Rect(0, 0, self.num_cols * self.cell[0], self.num_rows * self.cell[1])
            self.filled_cells_frame1 = [3,4,10,11,12,13,17,18,19,20,21,22,24,25,27,28,30,31,32,33,34,35,36,37,38,39,42,45,49,51,52,54,56,58,61,63]
            self.filled_cells_frame2 = [3,4,10,11,12,13,17,18,19,20,21,22,24,25,27,28,30,31,32,33,34,35,36,37,38,39,41,43,44,46,48,55,57,62]
        elif category == 'medium':
            self.reward = 15
            self.num_cols = 11
            self.num_rows = 8
            self.rect = pygame.Rect(0, 0, self.num_cols * self.cell[0], self.num_rows * self.cell[1])
            self.filled_cells_frame1 = [2,8,11,14,18,21,22,24,25,26,27,28,29,30,32,33,34,35,37,38,39,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,64,68,74,78,86]
            self.filled_cells_frame2 = [2,8,14,18,24,25,26,27,28,29,30,34,35,37,38,39,41,42,44,45,46,47,48,49,50,51,52,53,54,55,57,58,59,60,61,62,63,65,66,68,74,76,80,81,83,84]
        elif category == 'large':
            self.reward = 10
            self.num_cols = 12
            self.num_rows = 8
            self.rect = pygame.Rect(0, 0, self.num_cols * self.cell[0], self.num_rows * self.cell[1])
            self.filled_cells_frame1 = [4,5,6,7,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,62,63,64,67,68,69,73,74,77,78,81,82,86,87,92,93]
            self.filled_cells_frame2 = [4,5,6,7,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,63,64,67,68,74,75,77,78,80,81,84,85,94,95]

        self.bullet_color = bullet_color
        self.speed = [8, 20]
        self.change_count = 0
        self.change_flag = False # For animation frames

        # Explosion frames (similar to player/UFO for consistency)
        self.boomed_filled_cells_outer = [
            [3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95],
            [2,8,11,16,19,23,29,35,41,43,46,52,55,59,61,69,73,79,82,85,90,92,96],
            [1,9,10,14,20,22,28,34,42,47,51,56,60,67,70,72,76,80,84,89,94],
            [0,4,5,6,13,18,21,25,26,27,33,39,40,48,50,57,63,65,66,71,75,87,88,93]
        ]
        self.boomed_filled_cells_core = [
            [44,45,53,54,58,62],
            [30,36,40,41,49,50,51,52,59,60,61,67],
            [24,25,26,27,33,37,38,46,47,48,55,56],
            [12,13,14,15,16,17,19,20,21,22,23]
        ]
        self.boomed_cell = [3, 3]
        self.boomed_num_cols = 11
        self.boomed_num_rows = 9
        self.boomed_rect = pygame.Rect(0, 0, self.boomed_num_cols * self.boomed_cell[0], self.boomed_num_rows * self.boomed_cell[1])
        self.boomed_count = 0
        self.boomed_frame = 0

    def shot(self):
        """Enemy fires a bullet."""
        return EnemyBulletSprite(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height, self.bullet_color)
   
    def draw(self, screen):
        """Draws the enemy, flickering between two frames."""
        self.change_count += 1
        if self.change_count > 30: # Flicker speed for enemies
            self.change_count = 0
            self.change_flag = not self.change_flag

        current_cells = self.filled_cells_frame1 if self.change_flag else self.filled_cells_frame2
        for i in range(0, len(current_cells)):
            y = current_cells[i] // self.num_cols
            x = current_cells[i] % self.num_cols
            rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
            pygame.draw.rect(screen, self.base_color, rect)

    def update(self, direction, HEIGHT):
        """Updates enemy position."""
        if direction == 'right':
            self.rect.x += self.speed[0]
        elif direction == 'left':
            self.rect.x -= self.speed[0]
        elif direction == 'down':
            self.rect.y += self.speed[1]
        if self.rect.y >= HEIGHT - self.rect.height:
            return True # Enemy reached bottom
        else:
            return False

    def boom(self, screen, outer_color, core_color):
        """Draws explosion animation."""
        self.boomed_rect.x = self.rect.x
        self.boomed_rect.y = self.rect.y
        self.boomed_count += 1
        if self.boomed_count % 1 == 0:
            self.boomed_frame += 1
            if self.boomed_frame <= len(self.boomed_filled_cells_outer):
                for i in self.boomed_filled_cells_outer[self.boomed_frame - 1]:
                    y = i // self.boomed_num_cols
                    x = i % self.boomed_num_cols
                    rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
                    pygame.draw.rect(screen, outer_color, rect)
            if self.boomed_frame <= len(self.boomed_filled_cells_core):
                for i in self.boomed_filled_cells_core[self.boomed_frame - 1]:
                    y = i // self.boomed_num_cols
                    x = i % self.boomed_num_cols
                    rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
                    pygame.draw.rect(screen, core_color, rect)

        if self.boomed_frame > max(len(self.boomed_filled_cells_outer), len(self.boomed_filled_cells_core)):
            return True
        else:
            return False


# Updated My Bullet Sprite
class MyBulletSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, color, is_charged=False, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.is_charged = is_charged
        self.color = color if not is_charged else NEON_YELLOW # Charged shots are yellow
        self.speed = 12 if not is_charged else 18 # Charged shots are faster

        # Different shapes/sizes for charged vs. normal bullets
        if self.is_charged:
            self.cell = [4, 4]
            self.num_cols = 3
            self.num_rows = 6
            self.filled_cells = [1, 4, 5, 7, 8, 10, 13, 16] # Example charged shot shape
        else:
            self.cell = [2, 2]
            self.num_cols = 1
            self.num_rows = 4
            self.filled_cells = [0, 1, 2, 3] # Original bullet shape

        self.rect = pygame.Rect(x - (self.num_cols * self.cell[0] // 2), y, self.num_cols * self.cell[0], self.num_rows * self.cell[1])

    def draw(self, screen):
        """Draws the bullet with potential glow/trail."""
        for i in range(0, len(self.filled_cells)):
            y = self.filled_cells[i] // self.num_cols
            x = self.filled_cells[i] % self.num_cols
            rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
            pygame.draw.rect(screen, self.color, rect)

        # Simple trail effect for charged bullets
        if self.is_charged:
            trail_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50), 100) # Lighter, semi-transparent
            trail_surface = pygame.Surface((self.rect.width, self.rect.height * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(trail_surface, trail_color, trail_surface.get_rect(), 0)
            screen.blit(trail_surface, (self.rect.x, self.rect.y + self.rect.height))


    def update(self):
        """Updates bullet position."""
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            return True # Bullet went off screen
        else:
            return False


# Updated Enemy Bullet Sprite
class EnemyBulletSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.cell = [3, 3]
        self.num_cols = 3
        self.num_rows = 7
        self.rect = pygame.Rect(x - (self.num_cols * self.cell[0] // 2), y, self.num_cols * self.cell[0], self.num_rows * self.cell[1])
        # Two frames for a pulsating/wobbling effect
        self.filled_cells_frame1 = [0,4,8,10,12,16,20]
        self.filled_cells_frame2 = [2,4,6,10,14,16,18]
        self.change_count = 0
        self.change_flag = False
        self.speed = 5 # Slightly faster enemy bullets
        self.color = color

    def draw(self, screen):
        """Draws the enemy bullet with a pulsating effect."""
        self.change_count += 1
        if self.change_count > 5: # Faster flicker for bullets
            self.change_count = 0
            self.change_flag = not self.change_flag

        current_cells = self.filled_cells_frame1 if self.change_flag else self.filled_cells_frame2
        for i in range(0, len(current_cells)):
            y = current_cells[i] // self.num_cols
            x = current_cells[i] % self.num_cols
            rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
            pygame.draw.rect(screen, self.color, rect)

    def update(self, HEIGHT):
        """Updates enemy bullet position."""
        self.change_count += 1 # Continue animation count
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            return True # Bullet went off screen
        else:
            return False


import pygame
import sys
import random
import os # Keep os for future pathing if resources were to be added
import math # Import the math module for radians conversion

# --- Minimal Utility Functions and Base Class (replacing external dependencies) ---
def QuitGame():
    """Quits Pygame and exits the system."""
    pygame.quit()
    sys.exit()

class PygameBaseGame:
    """A minimalistic base class for Pygame games, handling basic initialization."""
    def __init__(self, config=None, **kwargs):
        pygame.init()
        self.cfg = config
        self.screen = pygame.display.set_mode(self.cfg.SCREENSIZE)
        pygame.display.set_caption(self.cfg.TITLE)
        # This will now load actual resources
        self.resource_loader = self._create_resource_loader()

    def _create_resource_loader(self):
        """Loads actual game resources (images and fonts)."""
        class GameResourceLoader:
            def __init__(self, cfg):
                self.images = {}
                # Load icon
                try:
                    self.images['icon'] = pygame.image.load(cfg.IMAGE_PATHS_DICT['icon']).convert_alpha()
                except pygame.error:
                    print(f"Warning: Could not load icon image from {cfg.IMAGE_PATHS_DICT['icon']}. Using placeholder.")
                    self.images['icon'] = pygame.Surface((32, 32), pygame.SRCALPHA)
                    pygame.draw.circle(self.images['icon'], cfg.YELLOW, (16, 16), 16) # Placeholder circle

                # Load Pacman image
                try:
                    self.images['pacman'] = pygame.image.load(cfg.IMAGE_PATHS_DICT['pacman']).convert_alpha()
                except pygame.error:
                    print(f"Warning: Could not load pacman image from {cfg.IMAGE_PATHS_DICT['pacman']}. Using placeholder.")
                    self.images['pacman'] = pygame.Surface((30, 30), pygame.SRCALPHA)
                    pygame.draw.circle(self.images['pacman'], cfg.RED, (15, 15), 15) # Placeholder pacman

                # Load Ghost images
                self.images['ghost'] = {}
                for ghost_name, path in cfg.IMAGE_PATHS_DICT['ghost'].items():
                    try:
                        self.images['ghost'][ghost_name] = pygame.image.load(path).convert_alpha()
                    except pygame.error:
                        print(f"Warning: Could not load {ghost_name} image from {path}. Using placeholder.")
                        self.images['ghost'][ghost_name] = pygame.Surface((30, 30), pygame.SRCALPHA)
                        pygame.draw.rect(self.images['ghost'][ghost_name], cfg.GHOST_COLORS[ghost_name], [0, 0, 30, 30], border_radius=5)


                # Load fonts
                self.fonts = {
                    'default_s': pygame.font.Font(None, 24),
                    'default_l': pygame.font.Font(None, 48),
                }
                self.cfg = cfg
            def playbgm(self):
                # Placeholder for background music. Requires a sound file.
                if os.path.exists(self.cfg.BGM_PATH):
                    try:
                        pygame.mixer.music.load(self.cfg.BGM_PATH)
                        pygame.mixer.music.play(-1) # Loop indefinitely
                    except pygame.error:
                        print(f"Warning: Could not load BGM from {self.cfg.BGM_PATH}.")
                pass
        return GameResourceLoader(self.cfg)

    def run(self):
        """Abstract run method, to be implemented by child classes."""
        raise NotImplementedError("run() method must be implemented by subclasses.")

# --- sprites.py content ---

class Wall(pygame.sprite.Sprite):
    """Wall class with enhanced drawing for a 'hollow' 3D effect."""
    def __init__(self, x, y, width, height, color, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface([width, height], pygame.SRCALPHA) # SRCALPHA for transparency
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self._draw_wall()

    def _draw_wall(self):
        """Draws the wall with a gradient and a hollow center."""
        self.image.fill((0, 0, 0, 0)) # Start with a transparent surface

        # Define gradient colors
        outer_color = self.color
        inner_color = tuple(max(0, c - 50) for c in self.color) # Slightly darker for inner part

        # Draw outer rectangle (simulating depth)
        pygame.draw.rect(self.image, outer_color, [0, 0, self.width, self.height], 0, border_radius=5)

        # Draw inner rectangle for hollow effect
        # Adjust dimensions for the 'hollow' effect
        border_thickness = 4
        inner_width = max(0, self.width - 2 * border_thickness)
        inner_height = max(0, self.height - 2 * border_thickness)
        inner_rect_pos = [border_thickness, border_thickness, inner_width, inner_height]

        # Fill the center with a darker shade or background color for depth
        pygame.draw.rect(self.image, inner_color, inner_rect_pos, 0, border_radius=3)
        # Draw a highlight on the top/left edge for more depth
        pygame.draw.rect(self.image, (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50)),
                         [0, 0, self.width, border_thickness], 0, border_radius=5)
        pygame.draw.rect(self.image, (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50)),
                         [0, 0, border_thickness, self.height], 0, border_radius=5)


class Food(pygame.sprite.Sprite):
    """Food class with improved visual appearance."""
    def __init__(self, x, y, width, height, color, bg_color, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height], pygame.SRCALPHA) # SRCALPHA for transparency
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        # Draw the food as a glowing circle
        radius = width // 2
        center_x = width // 2
        center_y = height // 2

        # Outer glow (larger, more transparent circle)
        pygame.draw.circle(self.image, (color[0], color[1], color[2], 100), (center_x, center_y), radius + 2)
        # Inner glow (medium, less transparent circle)
        pygame.draw.circle(self.image, (color[0], color[1], color[2], 180), (center_x, center_y), radius)
        # Core food (solid circle)
        pygame.draw.circle(self.image, color, (center_x, center_y), radius - 1)


class Player(pygame.sprite.Sprite):
    """Player class for Pacman and Ghosts, with animation and improved visuals."""
    size = 20 # **Reduced size for better maze navigation - now a class attribute**

    def __init__(self, x, y, role_name, image_surface): # Now takes an image surface
        pygame.sprite.Sprite.__init__(self)
        self.role_name = role_name
        self.base_image = image_surface # Store the base image
        
        # Scale the base image to the desired size (using the class attribute)
        self.image = pygame.transform.scale(self.base_image, (Player.size, Player.size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.prev_x = x
        self.prev_y = y
        self.base_speed = [2, 2] # Adjusted speed for new size
        self.speed = [0, 0]
        self.is_move = False
        self.tracks = [] # Only for ghosts with fixed paths (e.g., in a specific mode)
        self.tracks_loc = [0, 0]

        # Pacman animation specific
        self.mouth_open = 0 # 0 to 100, representing mouth open percentage
        self.mouth_direction = 1 # 1 for opening, -1 for closing
        self.mouth_speed = 10 # Speed of mouth animation
        self.rotation_angle = 0 # For Pacman's direction

        # Ghost AI specific
        self.target = None # For chasing logic
        # Ghosts start outside the gate, so no initial escape needed
        self.is_escaping_gate = False


    def changeSpeed(self, direction):
        """Changes speed and updates Pacman's rotation or ghost's base image."""
        # Normalize direction to ensure consistent speed
        magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
        if magnitude > 0:
            norm_direction_x = direction[0] / magnitude
            norm_direction_y = direction[1] / magnitude
        else:
            norm_direction_x, norm_direction_y = 0, 0

        self.speed = [norm_direction_x * self.base_speed[0], norm_direction_y * self.base_speed[1]]

        if self.role_name == 'pacman':
            # Adjust rotation for Pacman based on direction
            if direction[0] < 0: # Left
                self.rotation_angle = 180
            elif direction[0] > 0: # Right
                self.rotation_angle = 0
            elif direction[1] < 0: # Up
                self.rotation_angle = 90
            elif direction[1] > 0: # Down
                self.rotation_angle = 270 # Corrected: 270 for down (clockwise 90 from right)
            self.is_move = True # Ensure Pacman starts moving when direction changes
            # No need to redraw here, update handles it.
        # Ghosts do not rotate or animate like Pacman from their images, their direction is implicit.
        return self.speed

    def update(self, wall_sprites, gate_sprites, pacman_pos=None): # Added pacman_pos for ghost AI
        """Updates player position and handles collisions."""
        if not self.is_move and self.role_name != 'pacman' and self.role_name != 'ghost': # Pacman and Ghosts always update
            return False

        x_prev = self.rect.left
        y_prev = self.rect.top
        
        # Ghost AI logic - simple chasing
        if self.role_name != 'pacman': # Only apply AI to ghosts
            # Determine ideal direction towards Pacman
            dx = pacman_pos[0] - self.rect.centerx
            dy = pacman_pos[1] - self.rect.centery

            # Prioritize horizontal or vertical movement based on which is closer to target
            potential_directions = []
            if abs(dx) > abs(dy):
                potential_directions.append([1, 0] if dx > 0 else [-1, 0])
                potential_directions.append([0, 1] if dy > 0 else [0, -1])
            else:
                potential_directions.append([0, 1] if dy > 0 else [0, -1])
                potential_directions.append([1, 0] if dx > 0 else [-1, 0])

            # Try directions in order of priority, avoiding walls
            valid_move_found = False
            for direction_attempt in potential_directions:
                temp_speed = [direction_attempt[0] * self.base_speed[0], direction_attempt[1] * self.base_speed[1]]
                test_rect = self.rect.copy()
                test_rect.left += temp_speed[0]
                test_rect.top += temp_speed[1]
                
                # Manual collision check of the test_rect against wall_sprites' rects
                temp_collide = False
                for wall in wall_sprites:
                    if test_rect.colliderect(wall.rect):
                        temp_collide = True
                        break
                
                # Ghosts should avoid walls, but not the gate (as they can pass through).
                if not temp_collide: # If the proposed move does not collide with any wall
                    self.changeSpeed(direction_attempt)
                    valid_move_found = True
                    break
            
            # If all preferred moves are blocked by walls, try a random direction
            if not valid_move_found:
                self.changeSpeed(self.randomDirection())


        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]

        # Handle collisions
        # For Pacman: collide with walls AND gates.
        # For Ghosts: collide with walls (they can pass through the gate as part of AI).
        collision_sprites_to_check = pygame.sprite.Group()
        if self.role_name == 'pacman':
            collision_sprites_to_check.add(wall_sprites)
            if gate_sprites: # Pacman collides with gate
                collision_sprites_to_check.add(gate_sprites)
        else: # Ghosts only collide with walls for general movement
            collision_sprites_to_check.add(wall_sprites)

        is_collide = pygame.sprite.spritecollide(self, collision_sprites_to_check, False)
        

        if is_collide:
            self.rect.left = x_prev
            self.rect.top = y_prev
            if self.role_name == 'pacman':
                self.is_move = False # Stop Pacman if hits a wall
            elif self.role_name != 'pacman': # For ghosts, try new random direction if hit a wall
                self.changeSpeed(self.randomDirection())
            return False

        # Pacman mouth animation update and image rotation
        if self.role_name == 'pacman' and self.is_move:
            self.mouth_open += self.mouth_speed * self.mouth_direction
            if self.mouth_open >= 100 or self.mouth_open <= 0:
                self.mouth_direction *= -1 # Reverse direction
                self.mouth_open = max(0, min(100, self.mouth_open)) # Clamp value

            # Create a dynamic image for Pacman with mouth animation and rotation
            current_image = pygame.transform.scale(self.base_image, (Player.size, Player.size)).convert_alpha() # Use Player.size
            
            # Apply mouth cut-out
            temp_surface = pygame.Surface(current_image.get_size(), pygame.SRCALPHA)
            temp_surface.blit(current_image, (0, 0))
            
            center = (Player.size // 2, Player.size // 2) # Use Player.size
            radius = Player.size // 2 # Use Player.size
            mouth_angle = 45 * (self.mouth_open / 100.0)
            
            # Use math.radians directly for angles
            # These angles need to correspond to the rotation_angle logic
            # If base image is right-facing (0 degrees):
            # 0 for right, 90 for up, 180 for left, 270 for down
            # The polygon points need to be relative to the temp_surface,
            # then the whole surface is rotated.
            # For Pacman image facing right, angles are clockwise from positive x-axis for drawing
            # and then converted to radians.

            # Re-calculating points for the mouth based on original Pacman image facing right (0 degrees)
            # Mouth opens symmetrically around the current direction.
            
            # The rotation_angle is applied AFTER the mouth cut.
            # So, the mouth drawing itself should always be for a right-facing Pacman,
            # and then the `temp_surface` is rotated.
            
            # Angles for a right-facing mouth:
            mouth_start_rad = math.radians(-mouth_angle) # Top jaw, relative to horizontal
            mouth_end_rad = math.radians(mouth_angle)    # Bottom jaw, relative to horizontal

            points = [center,
                      (center[0] + radius * math.cos(mouth_start_rad),
                       center[1] + radius * math.sin(mouth_start_rad)),
                      (center[0] + radius * math.cos(mouth_end_rad),
                       center[1] + radius * math.sin(mouth_end_rad))]
            
            pygame.draw.polygon(temp_surface, (0, 0, 0, 0), points)

            # Rotate the combined image (after mouth is cut).
            # Pygame's rotate is counter-clockwise.
            # Use self.rotation_angle directly.
            rotated_image = pygame.transform.rotate(temp_surface, self.rotation_angle) 
            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.rect.center) # Keep center consistent

        elif self.role_name != 'pacman': # For ghosts, just update image if necessary (e.g. for scaling)
            self.image = pygame.transform.scale(self.base_image, (Player.size, Player.size)).convert_alpha() # Use Player.size
            self.rect = self.image.get_rect(center=self.rect.center) # Keep center consistent


        return True

    def randomDirection(self):
        """Generates a random direction for ghosts."""
        return random.choice([[-1, 0], [1, 0], [0, 1], [0, -1]])


# --- levels.py content ---

'''Number of levels'''
NUMLEVELS = 1

'''Level One'''
class Level1():
    def __init__(self):
        self.info = 'level1'
        self.wall_sprites = pygame.sprite.Group() # Initialize here for setupFood collision check
        self.gate_sprites = pygame.sprite.Group() # Initialize here for setupFood collision check


    def setupWalls(self, wall_color):
        """Creates and returns a sprite group of walls."""
        wall_positions = [
            [0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606], [300, 0, 6, 66], [60, 60, 186, 6],
            [360, 60, 186, 6], [60, 120, 66, 6], [60, 120, 6, 126], [180, 120, 246, 6], [300, 120, 6, 66],
            [480, 120, 66, 6], [540, 120, 6, 126], [120, 180, 126, 6], [120, 180, 6, 126], [360, 180, 126, 6],
            [480, 180, 6, 126], [180, 240, 6, 126], [180, 360, 246, 6], [420, 240, 6, 126], [240, 240, 42, 6],
            [324, 240, 42, 6], [240, 240, 6, 66], [240, 300, 126, 6], [360, 240, 6, 66], [0, 300, 66, 6],
            [540, 300, 66, 6], [60, 360, 66, 6], [60, 360, 6, 186], [480, 360, 66, 6], [540, 360, 6, 186],
            [120, 420, 366, 6], [120, 420, 6, 66], [480, 420, 6, 66], [180, 480, 246, 6], [300, 480, 6, 66],
            [120, 540, 126, 6], [360, 540, 126, 6]
        ]
        for wall_position in wall_positions:
            wall = Wall(*wall_position, wall_color)
            self.wall_sprites.add(wall)
        return self.wall_sprites

    def setupGate(self, gate_color):
        """Creates and returns a sprite group for the gate."""
        self.gate_sprites = pygame.sprite.Group()
        self.gate_sprites.add(Wall(282, 242, 42, 2, gate_color))
        return self.gate_sprites

    def setupPlayers(self, hero_image, ghost_images_dict): # Now takes image surfaces
        """Creates and returns sprite groups for hero and ghosts."""
        self.hero_sprites = pygame.sprite.Group()
        self.ghost_sprites = pygame.sprite.Group()
        # Pass the actual image surface to the Player constructor
        self.hero_sprites.add(Player(287, 439, 'pacman', hero_image))

        # Adjusted Ghost start positions to be outside the gate
        ghost_start_positions = {
            'Blinky': (287, 199), # Already outside
            'Pinky': (287, 180), # Moved up to be outside
            'Inky': (255, 180),  # Moved up to be outside
            'Clyde': (319, 180)  # Moved up to be outside
        }

        for name, img_surface in ghost_images_dict.items():
            start_x, start_y = ghost_start_positions[name]
            player = Player(start_x, start_y, name, img_surface)
            player.is_move = True # Ghosts always move
            self.ghost_sprites.add(player)
        return self.hero_sprites, self.ghost_sprites

    def setupFood(self, food_color, bg_color):
        """Creates and returns a sprite group of food pellets."""
        self.food_sprites = pygame.sprite.Group()
        # Iterate through a grid to place food
        # Adjusted range and step for smaller characters and food
        for row in range(1, 20): # Start from 1 to avoid placing food directly on border walls
            for col in range(1, 20): # Start from 1
                food_x = 15 + col * 30 - 4 # Adjust for smaller food size and center
                food_y = 15 + row * 30 - 4 # Adjust for smaller food size and center
                food = Food(food_x, food_y, 8, 8, food_color, bg_color)

                # Check for collisions with walls and gate.
                # A smaller collision rect for food check to allow more precise placement.
                temp_food_rect = pygame.Rect(food_x, food_y, 8, 8)

                collide_with_wall = any(wall.rect.colliderect(temp_food_rect) for wall in self.wall_sprites)
                collide_with_gate = any(gate.rect.colliderect(temp_food_rect) for gate in self.gate_sprites)

                # Ensure food is not placed where characters start or gates are.
                # We need to consider the new smaller character size here (Player.size = 20)
                pacman_start_rect = pygame.Rect(287, 439, Player.size, Player.size)
                # Updated ghost start positions
                ghost_start_rects = [
                    pygame.Rect(287, 199, Player.size, Player.size),
                    pygame.Rect(287, 180, Player.size, Player.size),
                    pygame.Rect(255, 180, Player.size, Player.size),
                    pygame.Rect(319, 180, Player.size, Player.size)
                ]

                if not collide_with_wall and not collide_with_gate:
                    # Also avoid placing food too close to player/ghost start positions
                    is_too_close_to_start = False
                    if pacman_start_rect.colliderect(temp_food_rect):
                        is_too_close_to_start = True
                    for ghost_rect in ghost_start_rects:
                        if ghost_rect.colliderect(temp_food_rect):
                            is_too_close_to_start = True
                            break

                    if not is_too_close_to_start:
                        self.food_sprites.add(food)
        return self.food_sprites


# --- pacman.py content ---

class Config():
    """Game configuration settings."""
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    FPS = 60 # Increased FPS for smoother gameplay
    SCREENSIZE = (606, 606)
    TITLE = 'Pacman Enhanced'

    # Enhanced Color Palette (Modern & Vibrant)
    BLACK = (20, 20, 20) # Darker background
    WHITE = (230, 230, 230) # Off-white for text
    BLUE = (0, 100, 255) # Walls: Brighter blue
    GREEN = (50, 205, 50) # Ghosts: Lime green
    RED = (255, 69, 0) # Pacman/Score: Orange-red
    YELLOW = (255, 255, 0) # Food: Bright yellow
    PURPLE = (147, 112, 219) # Ghosts: Medium Purple
    SKYBLUE = (0, 191, 255) # Walls: Lighter blue

    # Ghost specific colors (these will be primarily for placeholders if images fail)
    GHOST_COLORS = {
        'Blinky': (255, 0, 0),    # Red
        'Pinky': (255, 182, 193), # Pink
        'Inky': (0, 255, 255),    # Cyan
        'Clyde': (255, 165, 0)    # Orange
    }

    # Resource Paths (Updated to use provided images)
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3') # Assuming this path exists if used

    IMAGE_PATHS_DICT = {
        'icon': os.path.join(rootdir, 'resources/images/icon.png'),
        'pacman': os.path.join(rootdir, 'resources/images/pacman.png'),
        'ghost': {
            'Blinky': os.path.join(rootdir, 'resources/images/Blinky.png'),
            'Clyde': os.path.join(rootdir, 'resources/images/Clyde.png'),
            'Inky': os.path.join(rootdir, 'resources/images/Inky.png'),
            'Pinky': os.path.join(rootdir, 'resources/images/Pinky.png'),
        },
    }


class PacmanGame(PygameBaseGame):
    """The main Pacman game class."""
    game_type = 'pacman'

    def __init__(self, **kwargs):
        self.cfg = Config()
        super(PacmanGame, self).__init__(config=self.cfg, **kwargs)
        # Initialize mixer for sounds (optional, uncomment if adding sounds)
        pygame.mixer.init()
        # Example of loading a sound, replace with your actual sound file
        # self.eat_sound = pygame.mixer.Sound(os.path.join(self.cfg.rootdir, 'resources/audios/eat_food.wav'))
        # You'll need an 'audios' folder in 'resources' with a 'eat_food.wav' file
        self.eat_sound = None # Placeholder if no sound provided

    def run(self):
        """Runs the main game loop, including start screen and level progression."""
        self.showStartScreen()
        while True: # Loop to allow replaying after game over/win
            # No longer importing Levels, use NUMLEVELS and Level1 directly
            for num_level in range(1, NUMLEVELS + 1):
                level = Level1() # Directly instantiate Level1 as it's in scope
                is_clearance = self.startLevelGame(self.cfg, self.resource_loader, level, self.screen, self.resource_loader.fonts['default_s'])

                if num_level == NUMLEVELS:
                    self.showText(self.cfg, self.screen, self.resource_loader.fonts['default_l'], is_clearance, True)
                else:
                    self.showText(self.cfg, self.screen, self.resource_loader.fonts['default_l'], is_clearance)

    def showStartScreen(self):
        """Displays the start screen with game title and instructions."""
        screen, cfg = self.screen, self.cfg
        font_l = self.resource_loader.fonts['default_l']
        font_s = self.resource_loader.fonts['default_s']
        clock = pygame.time.Clock()

        title_text = font_l.render(cfg.TITLE, True, cfg.YELLOW)
        instructions_text = font_s.render("Press ENTER to start", True, cfg.WHITE)
        quit_text = font_s.render("Press ESCAPE to quit", True, cfg.WHITE)

        title_rect = title_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 50))
        instructions_rect = instructions_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 30))
        quit_rect = quit_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 70))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                # Corrected: Check for KEYDOWN event type first
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return # Start the game
                    elif event.key == pygame.K_ESCAPE: # Use elif here
                        QuitGame()

            screen.fill(cfg.BLACK)
            screen.blit(title_text, title_rect)
            screen.blit(instructions_text, instructions_rect)
            screen.blit(quit_text, quit_rect)

            pygame.display.flip()
            clock.tick(cfg.FPS)


    def startLevelGame(self, cfg, resource_loader, level, screen, font):
        """Manages a single level's gameplay."""
        clock = pygame.time.Clock()
        SCORE = 0

        # Setup walls and gate first as food placement depends on them
        wall_sprites = level.setupWalls(cfg.BLUE)
        gate_sprites = level.setupGate(cfg.WHITE)

        # Pass the actual image surfaces from resource_loader to setupPlayers
        hero_sprites, ghost_sprites = level.setupPlayers(
            resource_loader.images['pacman'],
            resource_loader.images['ghost']
        )
        food_sprites = level.setupFood(cfg.YELLOW, cfg.BLACK)

        is_clearance = False
        game_paused = False

        # Set initial direction for Pacman to face right
        for hero in hero_sprites:
            hero.changeSpeed([1, 0]) # Ensure Pacman faces right initially

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                # Corrected: Check for KEYDOWN event type first for both pause and movement keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: # 'P' for Pause
                        game_paused = not game_paused
                    elif not game_paused: # Only process movement if not paused and if key is pressed
                        if event.key == pygame.K_LEFT:
                            for hero in hero_sprites:
                                hero.changeSpeed([-1, 0])
                        elif event.key == pygame.K_RIGHT:
                            for hero in hero_sprites:
                                hero.changeSpeed([1, 0])
                        elif event.key == pygame.K_UP:
                            for hero in hero_sprites:
                                hero.changeSpeed([0, -1])
                        elif event.key == pygame.K_DOWN:
                            for hero in hero_sprites:
                                hero.changeSpeed([0, 1])
                if event.type == pygame.KEYUP:
                    # Optional: stop movement on key release if not moving (for smoother control)
                    pass # We want continuous movement until a new direction is pressed or collision occurs

            if game_paused:
                # Display pause message
                pause_text = font.render("PAUSED", True, cfg.WHITE)
                pause_rect = pause_text.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2))
                screen.blit(pause_text, pause_rect)
                pygame.display.flip()
                clock.tick(cfg.FPS)
                continue # Skip game logic updates while paused

            screen.fill(cfg.BLACK) # Fill background

            # Get Pacman's current position for ghost AI
            pacman_center_pos = None
            for hero in hero_sprites:
                pacman_center_pos = hero.rect.center
                hero.update(wall_sprites, gate_sprites) # Update Pacman's position and animation
                food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
                SCORE += len(food_eaten)
                # Play sound effect for eating food (if sound is loaded)
                if food_eaten and self.eat_sound:
                    self.eat_sound.play()

            # Update and draw Ghosts (now with AI)
            for ghost in ghost_sprites:
                # Ghosts should not consider the gate as a wall when moving,
                # as they can pass through. Only walls are obstacles for them.
                ghost.update(wall_sprites, None, pacman_center_pos) # Do NOT pass gate_sprites to ghost.update

            wall_sprites.draw(screen)
            gate_sprites.draw(screen)
            food_sprites.draw(screen)
            hero_sprites.draw(screen)
            ghost_sprites.draw(screen)


            # Display Score with better styling
            score_text_surface = font.render(f"Score: {SCORE}", True, cfg.WHITE)
            score_text_rect = score_text_surface.get_rect(topleft=(10, 10))
            screen.blit(score_text_surface, score_text_rect)

            # Check win/lose conditions
            if len(food_sprites) == 0:
                is_clearance = True
                break # Level cleared
            if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
                is_clearance = False
                break # Game over

            pygame.display.flip()
            clock.tick(cfg.FPS) # Control frame rate
        return is_clearance

    def showText(self, cfg, screen, font, is_clearance, allow_replay=False):
        """Displays game over/win messages with enhanced visuals."""
        clock = pygame.time.Clock()
        msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
        main_color = cfg.RED if not is_clearance else cfg.GREEN

        # Create a semi-transparent overlay
        overlay = pygame.Surface(cfg.SCREENSIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Black with 180 alpha (more transparent than 10)
        screen.blit(overlay, (0, 0))

        # Initialize fonts with different sizes
        main_font = pygame.font.Font(None, 30)      # Smaller for the main message
        continue_font = pygame.font.Font(None, 24)  # Even smaller for the continue hint
        quit_font = pygame.font.Font(None, 18)      # Smallest for quit prompt

        # Render texts
        main_text_surface = main_font.render(msg, True, main_color)
        continue_text_surface = continue_font.render('Press ENTER to continue or play again.', True, cfg.WHITE)
        quit_text_surface = quit_font.render('Press ESCAPE to quit.', True, cfg.WHITE)

        # Position texts
        main_text_rect = main_text_surface.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 - 60))
        continue_text_rect = continue_text_surface.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 20))
        quit_text_rect = quit_text_surface.get_rect(center=(cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] // 2 + 80))


        # Blit texts onto the screen
        screen.blit(main_text_surface, main_text_rect)
        screen.blit(continue_text_surface, continue_text_rect)
        screen.blit(quit_text_surface, quit_text_rect)

        pygame.display.flip() # Update the entire screen

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if is_clearance and not allow_replay:
                            return # Exit to main menu or next level (if more levels existed)
                        else:
                            self.run() # Restart the game
                    elif event.key == pygame.K_ESCAPE:
                        QuitGame()
            clock.tick(cfg.FPS) # Keep clock ticking even on text screen


if __name__ == '__main__':
    # Initialize Pygame and run the game
    game = PacmanGame()
    game.run()

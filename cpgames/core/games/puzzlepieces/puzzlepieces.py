import os
import random
import pygame
import tkinter as tk # Import tkinter for file dialog
from tkinter import filedialog # Import filedialog specifically
# Assuming utils and base are in parent directories as implied by original import
from ...utils import QuitGame
from ..base import PygameBaseGame


'''Configuration class for game settings and resources'''
class Config():
    # Root directory of the current script
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # Frames Per Second
    FPS = 40
    # Define colors for modern aesthetics (these are class attributes)
    BACKGROUNDCOLOR = (235, 235, 235) # Light Gray background for a clean look
    TITLE_COLOR = (35, 35, 35)       # Dark gray for main title
    INSTRUCTION_COLOR = (75, 75, 75) # Medium gray for instructional text
    BUTTON_BORDER_COLOR = (110, 110, 110) # Gray for button borders
    BUTTON_FILL_COLOR = (190, 190, 190)   # Lighter gray for button fill (normal state)
    BUTTON_HOVER_FILL_COLOR = (170, 170, 170) # Slightly darker gray on button hover
    BUTTON_TEXT_COLOR = (45, 45, 45)      # Dark text for buttons
    BUTTON_SHADOW_COLOR = (140, 140, 140) # For 3D effect shadow on buttons
    SCORE_COLOR = (55, 55, 55) # Darker gray for score text
    CONGRATS_COLOR = (0, 140, 0) # Green for congratulations message
    BLACK = (0, 0, 0) # Standard black for grid lines
    DARK_GRAY = (100, 100, 100)  # For inactive input box border
    # Number of random shuffles to perform when creating a puzzle board
    NUMRANDOM = 100
    # Screen dimensions
    SCREENSIZE = (640, 640)
    # Window title
    TITLE = 'Jigsaw Puzzle - Dannz'
    # Dictionary to store paths to game images (now mainly for default random selection)
    IMAGE_PATHS_DICT = {}
    IMAGE_DIR = os.path.join(rootdir, 'resources/images')
    if os.path.exists(IMAGE_DIR):
        for item in os.listdir(IMAGE_DIR):
            if item.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')): # Filter for common image types
                IMAGE_PATHS_DICT[item] = os.path.join(IMAGE_DIR, item)
    
    # Font paths and sizes - Adjusted for better visibility and modern look
    FONT_PATHS_DICT = {
        'title': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 10}, # Main title font size
        'subtitle': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 25}, # Subtitle/instruction font size
        'button': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 20}, # Button text font size
        'info': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 30}, # Steps/best score information font size
    }

    # Best scores for each game mode (least steps taken) - accessible via class
    # Initialized to infinity to ensure any first score is recorded as the best
    BEST_SCORES = {
        3: float('inf'), # For 3x3 mode
        4: float('inf'), # For 4x4 mode
        5: float('inf')  # For 5x5 mode
    }


'''Jigsaw Puzzle Game class'''
class PuzzlePiecesGame(PygameBaseGame):
    game_type = 'puzzlepieces'
    def __init__(self, **kwargs):
        self.cfg = Config # self.cfg is assigned the Config class itself, allowing direct access to its class attributes
        super(PuzzlePiecesGame, self).__init__(config=self.cfg, **kwargs)
        self.current_steps = 0 # Initialize step counter for the current game
        self.selected_game_image_path = None # Stores path to custom image if selected

    '''Runs the main game loop'''
    def run(self):
        # Initialize screen, resource loader, and config from parent class
        # Initial assignment. This 'screen' variable needs to be updated if self.screen changes.
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        
        # Scale all pre-loaded images to the screen size (initial setup)
        # This part ensures any default images loaded by PygameBaseGame are scaled.
        # Custom images loaded later will be scaled at load time.
        for key in list(resource_loader.images.keys()):
            resource_loader.images[key] = pygame.transform.scale(resource_loader.images[key], cfg.SCREENSIZE)
        
        # Main game loop allowing multiple plays without restarting the application
        while True:
            # Display the start interface and get the chosen puzzle size
            # IMPORTANT: Pass self.screen here to ensure the most up-to-date screen object is used
            size = self.ShowStartInterface(self.screen) 
            assert isinstance(size, int) # Ensure `size` is a valid integer (e.g., 3, 4, 5)

            # CRUCIAL FIX: Re-assign the local 'screen' variable after ShowStartInterface returns.
            # This ensures that if the Pygame display was quit and re-initialized (e.g., by _openNativeImageFileDialog),
            # 'screen' in this scope now refers to the new, valid display surface.
            screen = self.screen 

            num_rows, num_cols = size, size
            num_cells = size * size

            # Reset step counter for a new game session
            self.current_steps = 0

            # Determine which image to use for the puzzle: custom selected or random library image
            game_img_used = None
            if self.selected_game_image_path and os.path.exists(self.selected_game_image_path):
                try:
                    # Attempt to load and scale the custom selected image
                    game_img_used = pygame.image.load(self.selected_game_image_path).convert_alpha()
                    game_img_used = pygame.transform.scale(game_img_used, cfg.SCREENSIZE)
                except pygame.error as e:
                    # Fallback to a random image if custom image fails to load (e.g., corrupted file)
                    print(f"Error loading custom image '{self.selected_game_image_path}': {e}. Falling back to random image.")
                    game_img_used = random.choice(list(resource_loader.images.values()))
                    self.selected_game_image_path = None # Clear custom path on failure
            else:
                # If no custom image selected or path is invalid, pick a random one from pre-loaded images
                # Ensure IMAGE_PATHS_DICT is not empty before attempting random.choice
                if cfg.IMAGE_PATHS_DICT:
                    random_image_key = random.choice(list(cfg.IMAGE_PATHS_DICT.keys()))
                    game_img_used = pygame.image.load(cfg.IMAGE_PATHS_DICT[random_image_key]).convert_alpha()
                    game_img_used = pygame.transform.scale(game_img_used, cfg.SCREENSIZE)
                else:
                    # Handle case where no images are available at all (e.g., provide a blank screen or error)
                    print("Warning: No images found in resources/images directory. Game might not function correctly.")
                    game_img_used = pygame.Surface(cfg.SCREENSIZE, pygame.SRCALPHA)
                    game_img_used.fill((100, 100, 100, 255)) # Grey placeholder for missing image


            # Get the rectangle of the chosen game image for dimensions
            game_img_used_rect = game_img_used.get_rect()
            
            # Calculate the dimensions of each individual puzzle cell
            cell_width = game_img_used_rect.width // num_cols
            cell_height = game_img_used_rect.height // num_rows
            
            # Create a scrambled puzzle board, ensuring it is not initially solved
            game_board, blank_cell_idx = self.CreateBoard(num_rows, num_cols, num_cells)
            while self.isGameOver(game_board, size): # Loop until a truly scrambled board is created
                game_board, blank_cell_idx = self.CreateBoard(num_rows, num_cols, num_cells)
            
            # Game play loop: This loop runs while the current puzzle is being played
            is_running = True
            clock = pygame.time.Clock() # Used to control the frame rate
            while is_running:
                # -- Event handling: Process user input
                for event in pygame.event.get():
                    # ---- Quit game (Window close button or ESC key press)
                    if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        QuitGame() # Call the utility function to terminate the game

                    # ---- Keyboard input for moves (WASD keys or Arrow keys)
                    elif event.type == pygame.KEYDOWN:
                        prev_blank_idx = blank_cell_idx # Store current blank index to check if a move occurred
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                            blank_cell_idx = self.moveL(game_board, blank_cell_idx, num_cols)
                        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                            blank_cell_idx = self.moveR(game_board, blank_cell_idx, num_cols)
                        elif event.key == pygame.K_UP or event.key == ord('w'):
                            blank_cell_idx = self.moveU(game_board, blank_cell_idx, num_rows, num_cols)
                        elif event.key == pygame.K_DOWN or event.key == ord('s'):
                            blank_cell_idx = self.moveD(game_board, blank_cell_idx, num_cols)
                        
                        # Increment steps only if a valid move (blank cell index changed) occurred
                        if prev_blank_idx != blank_cell_idx:
                            self.current_steps += 1

                    # ---- Mouse input for moves (clicking adjacent pieces)
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click
                        x, y = pygame.mouse.get_pos() # Get the current mouse click position
                        x_pos = x // cell_width # Calculate the column index of the clicked cell
                        y_pos = y // cell_height # Calculate the row index of the clicked cell
                        idx = x_pos + y_pos * num_cols # Convert 2D position to 1D array index
                        
                        prev_blank_idx = blank_cell_idx # Store current blank index to check if a move occurred
                        # Check if the clicked piece is directly adjacent to the blank cell and move it
                        if idx == blank_cell_idx - 1: # Clicked piece is to the right of the blank
                            blank_cell_idx = self.moveR(game_board, blank_cell_idx, num_cols)
                        elif idx == blank_cell_idx + 1: # Clicked piece is to the left of the blank
                            blank_cell_idx = self.moveL(game_board, blank_cell_idx, num_cols)
                        elif idx == blank_cell_idx + num_cols: # Clicked piece is above the blank
                            blank_cell_idx = self.moveU(game_board, blank_cell_idx, num_rows, num_cols)
                        elif idx == blank_cell_idx - num_cols: # Clicked piece is below the blank
                            blank_cell_idx = self.moveD(game_board, blank_cell_idx, num_cols)
                        
                        # Increment steps only if a valid move (blank cell index changed) occurred
                        if prev_blank_idx != blank_cell_idx:
                            self.current_steps += 1

                # -- Check if the game is over (puzzle is solved)
                if self.isGameOver(game_board, size):
                    game_board[blank_cell_idx] = num_cells - 1 # Restore the last piece to complete the image
                    is_running = False # End the current game play loop
                
                # -- Update display: Draw the current state of the puzzle
                screen.fill(cfg.BACKGROUNDCOLOR) # Clear the screen with the background color
                for i in range(num_cells):
                    if game_board[i] == -1: # Skip drawing the blank cell
                        continue # Move to the next piece
                    
                    # Calculate the (x, y) position of the current piece on the board
                    x_cell_on_board = i % num_cols
                    y_cell_on_board = i // num_cols
                    
                    # Define the destination rectangle on the screen where this piece will be drawn
                    dest_rect = pygame.Rect(x_cell_on_board * cell_width, y_cell_on_board * cell_height, cell_width, cell_height)
                    
                    # Define the source area on the original image from where this piece's content is taken
                    img_area_x = (game_board[i] % num_cols) * cell_width
                    img_area_y = (game_board[i] // num_cols) * cell_height
                    src_area = pygame.Rect(img_area_x, img_area_y, cell_width, cell_height)
                    
                    screen.blit(game_img_used, dest_rect, src_area) # Draw the piece on the screen

                # Draw grid lines to visually separate puzzle pieces
                for i in range(num_cols + 1):
                    # Vertical lines
                    pygame.draw.line(screen, cfg.BLACK, (i * cell_width, 0), (i * cell_width, game_img_used_rect.height), 2) 
                for i in range(num_rows + 1):
                    # Horizontal lines
                    pygame.draw.line(screen, cfg.BLACK, (0, i * cell_height), (game_img_used_rect.width, i * cell_height), 2)
                
                pygame.display.update() # Update the entire display surface to show the new frame
                clock.tick(cfg.FPS) # Control the game's frame rate
            
            # After the game is over, update the best score and display the end interface
            if self.current_steps < self.cfg.BEST_SCORES[size]:
                self.cfg.BEST_SCORES[size] = self.current_steps # Update if current steps are better than the recorded best
            self.ShowEndInterface(screen, self.current_steps, size) # Display the end screen with current and best scores

    '''Checks if the puzzle is in its solved state'''
    def isGameOver(self, board, size):
        assert isinstance(size, int)
        num_cells = size * size
        # Check if each piece (except the last blank one) is in its correct sequential position
        for i in range(num_cells - 1):
            if board[i] != i: return False # If any piece is out of place, the game is not over
        return True # All pieces are in their correct positions, puzzle is solved

    '''Moves the piece to the left of the blank cell to the blank cell's position (blank moves right)'''
    def moveR(self, board, blank_cell_idx, num_cols):
        # Cannot move right if the blank cell is in the leftmost column
        if blank_cell_idx % num_cols == 0: return blank_cell_idx
        # Swap the piece at (blank_cell_idx - 1) with the blank cell
        board[blank_cell_idx-1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-1]
        return blank_cell_idx - 1 # Return the new index of the blank cell

    '''Moves the piece to the right of the blank cell to the blank cell's position (blank moves left)'''
    def moveL(self, board, blank_cell_idx, num_cols):
        # Cannot move left if the blank cell is in the rightmost column
        if (blank_cell_idx + 1) % num_cols == 0: return blank_cell_idx
        # Swap the piece at (blank_cell_idx + 1) with the blank cell
        board[blank_cell_idx+1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+1]
        return blank_cell_idx + 1 # Return the new index of the blank cell

    '''Moves the piece above the blank cell to the blank cell's position (blank moves down)'''
    def moveD(self, board, blank_cell_idx, num_cols):
        # Cannot move down if the blank cell is in the top row
        if blank_cell_idx < num_cols: return blank_cell_idx
        # Swap the piece at (blank_cell_idx - num_cols) with the blank cell
        board[blank_cell_idx-num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-num_cols]
        return blank_cell_idx - num_cols # Return the new index of the blank cell

    '''Moves the piece below the blank cell to the blank cell's position (blank moves up)'''
    def moveU(self, board, blank_cell_idx, num_rows, num_cols):
        # Cannot move up if the blank cell is in the bottom row
        if blank_cell_idx >= (num_rows-1) * num_cols: return blank_cell_idx
        # Swap the piece at (blank_cell_idx + num_cols) with the blank cell
        board[blank_cell_idx+num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+num_cols]
        return blank_cell_idx + num_cols # Return the new index of the blank cell

    '''Creates a new scrambled puzzle board'''
    def CreateBoard(self, num_rows, num_cols, num_cells):
        board = []
        for i in range(num_cells): board.append(i) # Initialize board with pieces in sequential order
        
        # The last cell is designated as the blank (empty) space
        blank_cell_idx = num_cells - 1
        board[blank_cell_idx] = -1 # Mark the last cell as blank (conventionally, -1 represents the empty slot)
        
        # Randomly scramble the board by performing a series of valid moves
        for _ in range(self.cfg.NUMRANDOM): # Perform NUMRANDOM random moves
            direction = random.randint(0, 3) # Randomly choose a direction: 0: left, 1: right, 2: up, 3: down
            if direction == 0: blank_cell_idx = self.moveL(board, blank_cell_idx, num_cols)
            elif direction == 1: blank_cell_idx = self.moveR(board, blank_cell_idx, num_cols)
            elif direction == 2: blank_cell_idx = self.moveU(board, blank_cell_idx, num_rows, num_cols)
            elif direction == 3: blank_cell_idx = self.moveD(board, blank_cell_idx, num_cols)
        return board, blank_cell_idx # Return the scrambled board configuration and the final blank cell index
    
    '''Helper function to open a native file dialog for image selection.'''
    def _openNativeImageFileDialog(self):
        # Uninitialize Pygame modules that might conflict with Tkinter
        # This is a more aggressive approach to ensure Tkinter has full control
        # and avoids potential display surface conflicts.
        pygame.joystick.quit()
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.display.quit()
        pygame.quit() # Fully uninitialize Pygame

        root = tk.Tk()
        root.withdraw() # Hide the main Tkinter window (we only want the file dialog)

        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ],
            initialdir=self.cfg.rootdir # Start browsing from the game's root directory
        )
        
        root.destroy() # Destroy the Tkinter root window after the dialog closes
        
        # Reinitialize Pygame modules in the correct order
        pygame.init() # Initializes all Pygame modules
        
        # Re-create the display surface and assign it back to self.screen (crucial fix)
        self.screen = pygame.display.set_mode(self.cfg.SCREENSIZE)
        pygame.display.set_caption(self.cfg.TITLE) # Restore the Pygame window title

        # Re-load fonts after Pygame is re-initialized
        # This assumes resource_loader.fonts is a dictionary holding pygame.font.Font objects
        self.resource_loader.fonts = {} # Clear old, invalid font objects
        for font_key, font_info in self.cfg.FONT_PATHS_DICT.items():
            font_path = font_info['name']
            font_size = font_info['size']
            try:
                self.resource_loader.fonts[font_key] = pygame.font.Font(font_path, font_size)
            except pygame.error as e:
                print(f"Error loading font '{font_path}': {e}. Using default font if available.")
                # Fallback to a default font if possible or handle error gracefully
                self.resource_loader.fonts[font_key] = pygame.font.SysFont("Arial", font_size) # Fallback to a system font


        return file_path # Returns empty string if cancelled, or full path to selected file

    '''Helper function to draw all elements of the start screen.
       Separated from ShowStartInterface to handle redrawing for hover effects/feedback.'''
    def _drawStartScreenElements(self, screen, button_info, load_custom_image_button_rect, mouse_pos, feedback_message=None):
        title_font = self.resource_loader.fonts['title']
        subtitle_font = self.resource_loader.fonts['subtitle']
        button_font = self.resource_loader.fonts['button']
        info_font = self.resource_loader.fonts['info']

        # Game Title
        title = title_font.render('', True, self.cfg.TITLE_COLOR)
        trect = title.get_rect(center=(self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 6))
        screen.blit(title, trect)

        # Instruction for choosing difficulty
        instruction_text = subtitle_font.render('', True, self.cfg.INSTRUCTION_COLOR)
        instruction_rect = instruction_text.get_rect(center=(self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.8))
        screen.blit(instruction_text, instruction_rect)

        # Draw difficulty buttons and their associated best scores
        shadow_offset = 8 # Offset for 3D shadow effect
        for button in button_info:
            rect = button['rect']
            
            # Draw 3D shadow effect (darker rectangle slightly offset)
            shadow_rect = rect.move(shadow_offset, shadow_offset)
            pygame.draw.rect(screen, self.cfg.BUTTON_SHADOW_COLOR, shadow_rect, border_radius=10) # Rounded corners for shadow

            # Determine button's inner fill color based on mouse hover state
            current_button_fill = self.cfg.BUTTON_FILL_COLOR
            if rect.collidepoint(mouse_pos):
                current_button_fill = self.cfg.BUTTON_HOVER_FILL_COLOR

            # Draw the hollow button (outer border and inner fill)
            pygame.draw.rect(screen, self.cfg.BUTTON_BORDER_COLOR, rect, 5, border_radius=10) # Outer border with rounded corners
            pygame.draw.rect(screen, current_button_fill, rect.inflate(-10, -10), border_radius=8) # Inner fill with rounded corners

            # Draw button text (e.g., "3 x 3")
            text_surface = button_font.render(button['text'], True, self.cfg.BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
            
            # Display best score text next to the button
            best_score_render = info_font.render(button['best_score_text'], True, self.cfg.SCORE_COLOR)
            # Position best score text to the right of the button, with increased spacing
            best_score_rect_display = best_score_render.get_rect(midleft=(rect.right + 25, rect.center[1]))
            screen.blit(best_score_render, best_score_rect_display)

        # Draw "Load Custom Image" button
        custom_image_fill = self.cfg.BUTTON_FILL_COLOR
        if load_custom_image_button_rect.collidepoint(mouse_pos):
            custom_image_fill = self.cfg.BUTTON_HOVER_FILL_COLOR

        # Draw 3D shadow for the custom image button
        shadow_offset_custom = 6
        custom_image_shadow_rect = load_custom_image_button_rect.move(shadow_offset_custom, shadow_offset_custom)
        pygame.draw.rect(screen, self.cfg.BUTTON_SHADOW_COLOR, custom_image_shadow_rect, border_radius=8)

        # Draw the custom image button (hollow effect)
        pygame.draw.rect(screen, self.cfg.BUTTON_BORDER_COLOR, load_custom_image_button_rect, 5, border_radius=8)
        pygame.draw.rect(screen, custom_image_fill, load_custom_image_button_rect.inflate(-8, -8), border_radius=6)

        custom_image_text_surface = subtitle_font.render('Load Custom Image', True, self.cfg.BUTTON_TEXT_COLOR)
        custom_image_text_rect = custom_image_text_surface.get_rect(center=load_custom_image_button_rect.center)
        screen.blit(custom_image_text_surface, custom_image_text_rect)

        # Display feedback if a custom image is currently selected or an error occurred
        if feedback_message:
            feedback_render = info_font.render(feedback_message, True, self.cfg.SCORE_COLOR)
            # Position feedback below the custom image button
            feedback_rect = feedback_render.get_rect(center=(self.cfg.SCREENSIZE[0] / 2, load_custom_image_button_rect.bottom + 20))
            screen.blit(feedback_render, feedback_rect)


    '''Displays the game start screen with difficulty options and a button to load a custom image'''
    def ShowStartInterface(self, screen):
        # Button properties for difficulty selection
        button_width = 180
        button_height = 80
        button_spacing = 25 # Vertical space between difficulty buttons
        
        button_info = [] # List to store button rectangle, value, text, and best score text
        difficulties = [(3, '3 x 3'), (4, '4 x 4'), (5, '5 x 5')] # (Puzzle size, Button text)
        
        # Calculate start Y position for difficulty buttons to center them vertically
        total_difficulty_buttons_height = len(difficulties) * button_height + (len(difficulties) - 1) * button_spacing
        # Adjusted to ensure buttons don't touch the bottom, leaving room for custom image button
        start_y_difficulty_buttons = self.cfg.SCREENSIZE[1] / 2 - (total_difficulty_buttons_height / 2) - 30

        # Define "Load Custom Image" button properties
        load_custom_image_button_width = 300
        load_custom_image_button_height = 60
        # Position this button near the bottom, with sufficient padding
        load_custom_image_button_y = self.cfg.SCREENSIZE[1] - load_custom_image_button_height - 40 
        load_custom_image_button_rect = pygame.Rect(0, 0, load_custom_image_button_width, load_custom_image_button_height)
        load_custom_image_button_rect.center = (self.cfg.SCREENSIZE[0] / 2, load_custom_image_button_y)

        # Populate button_info list with rectangle and text data
        for i, (value, text) in enumerate(difficulties):
            center_x = self.cfg.SCREENSIZE[0] / 2
            y_pos = start_y_difficulty_buttons + i * (button_height + button_spacing)
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.center = (center_x, y_pos)
            
            best_score_value = self.cfg.BEST_SCORES[value]
            best_score_text_display = f'Best: {best_score_value}' if best_score_value != float('inf') else 'Best: N/A'
            
            button_info.append({'rect': rect, 'value': value, 'text': text, 'best_score_text': best_score_text_display})

        feedback_message = None # Initialize feedback message for user (e.g., "Image not found!")

        # Event loop for the start screen
        while True:
            # Get current mouse position for drawing hover effects
            current_mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame() # Exit the game
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click
                    mouse_pos = event.pos
                    feedback_message = None # Clear previous feedback on new click

                    # Check if any difficulty button was clicked
                    for button in button_info:
                        if button['rect'].collidepoint(mouse_pos):
                            return button['value'] # Return selected difficulty to start game

                    # Check if "Load Custom Image" button was clicked
                    if load_custom_image_button_rect.collidepoint(mouse_pos):
                        # Call _openNativeImageFileDialog, which handles Pygame display re-init
                        selected_image_path = self._openNativeImageFileDialog() 
                        # After the dialog closes, the self.screen object has been recreated by _openNativeImageFileDialog
                        # So, we update the local 'screen' variable to reflect this change.
                        screen = self.screen # Crucial update: re-assign the valid screen surface

                        if selected_image_path: # If a file was selected (path is not empty)
                            self.selected_game_image_path = selected_image_path
                            feedback_message = f"Using: {os.path.basename(selected_image_path)}"
                        else: # User cancelled the dialog
                            if self.selected_game_image_path:
                                feedback_message = f"Still using: {os.path.basename(self.selected_game_image_path)}"
                            else:
                                feedback_message = "No custom image selected. Will use random."
            
            # --- Drawing all elements for the current frame ---
            screen.fill(self.cfg.BACKGROUNDCOLOR) # Clear the screen
            self._drawStartScreenElements(screen, button_info, load_custom_image_button_rect, current_mouse_pos, feedback_message)
            pygame.display.update() # Update the entire display
    
    '''Displays the game over screen with scores and a play again option'''
    def ShowEndInterface(self, screen, current_steps, game_size):
        screen.fill(self.cfg.BACKGROUNDCOLOR) # Clear screen with background color
        
        # Get fonts
        title_font = self.resource_loader.fonts['subtitle']
        info_font = self.resource_loader.fonts['info']
        button_font = self.resource_loader.fonts['button']

        # Congratulations message
        title_text = 'Congratulations! Puzzle Solved!'
        title_render = title_font.render(title_text, True, self.cfg.CONGRATS_COLOR)
        # Position the title centrally near the top
        title_rect = title_render.get_rect(center=(self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 4))
        screen.blit(title_render, title_rect)

        # Display steps taken in the current game
        steps_text = f'Your steps: {current_steps}'
        steps_render = info_font.render(steps_text, True, self.cfg.SCORE_COLOR)
        # Position steps below the title
        steps_rect = steps_render.get_rect(center=(self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.2))
        screen.blit(steps_render, steps_rect)

        # Display the best score for the completed game mode
        best_score_value = self.cfg.BEST_SCORES[game_size]
        # Format the best score text; show "N/A" if no best score is recorded yet
        best_score_text = f'Best for {game_size}x{game_size} mode: {best_score_value}' \
                            if best_score_value != float('inf') else f'Best for {game_size}x{game_size} mode: N/A'
        best_score_render = info_font.render(best_score_text, True, self.cfg.SCORE_COLOR)
        # Position best score below current steps
        best_score_rect = best_score_render.get_rect(center=(self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 1.8))
        screen.blit(best_score_render, best_score_rect)

        # Play Again Button - with hollow graphic and fluency color effect
        play_button_rect = pygame.Rect(0, 0, 200, 70) # Define button size
        play_button_rect.center = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] * 0.75) # Position button
        
        # Get current mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()
        current_button_fill = self.cfg.BUTTON_FILL_COLOR
        if play_button_rect.collidepoint(mouse_pos):
            current_button_fill = self.cfg.BUTTON_HOVER_FILL_COLOR

        # Draw 3D shadow for the button
        shadow_offset = 6
        shadow_rect = play_button_rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, self.cfg.BUTTON_SHADOW_COLOR, shadow_rect, border_radius=8)

        # Draw the hollow button (outer border and inner fill)
        pygame.draw.rect(screen, self.cfg.BUTTON_BORDER_COLOR, play_button_rect, 5, border_radius=8)
        pygame.draw.rect(screen, current_button_fill, play_button_rect.inflate(-10, -10), border_radius=6)

        # Render and position "Play Again" text on the button
        play_text_surface = button_font.render('Play Again', True, self.cfg.BUTTON_TEXT_COLOR)
        play_text_rect = play_text_surface.get_rect(center=play_button_rect.center)
        screen.blit(play_text_surface, play_text_rect)

        pygame.display.update() # Update the display to show the end screen

        # Event loop for the end screen (waiting for user input to play again or quit)
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame() # Quit the game
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click
                    if play_button_rect.collidepoint(event.pos):
                        return # Exit the end interface to restart the game loop in run()
                elif event.type == pygame.MOUSEMOTION: # Update on mouse motion for hover effect
                    # Re-render the end screen to update button color
                    # This ensures the hover effect is dynamically updated
                    self.ShowEndInterface(screen, current_steps, game_size) 
            pygame.display.update() # Keep updating to show the screen

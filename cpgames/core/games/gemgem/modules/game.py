import time
import random
import pygame
from ....utils import QuitGame


'''Gem Sprite Class'''
class gemSprite(pygame.sprite.Sprite):
    def __init__(self, image, gem_type, size, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image # Store original for potential scaling/effects
        self.image = pygame.transform.smoothscale(image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position # Initial drawing position
        self.target_x = position[0] # Initial target for x
        self.target_y = position[1] # Initial target for y

        self.type = gem_type
        self.fixed = False # True when gem is at its final grid position
        self.speed_x = 15 # Speed for horizontal movement during swaps
        self.speed_y = 15 # Speed for vertical movement during drops/swaps
        self.direction = None # 'down', 'up', 'left', 'right' for current movement

    '''Move the gem towards its target position'''
    def move(self):
        if self.direction == 'down':
            self.rect.top += self.speed_y
            if self.rect.top >= self.target_y:
                self.rect.top = self.target_y # Snap to target
                self.fixed = True
        elif self.direction == 'up':
            self.rect.top -= self.speed_y
            if self.rect.top <= self.target_y:
                self.rect.top = self.target_y # Snap to target
                self.fixed = True
        elif self.direction == 'left':
            self.rect.left -= self.speed_x
            if self.rect.left <= self.target_x:
                self.rect.left = self.target_x # Snap to target
                self.fixed = True
        elif self.direction == 'right':
            self.rect.left += self.speed_x
            if self.rect.left >= self.target_x:
                self.rect.left = self.target_x # Snap to target
                self.fixed = True
        elif self.direction is None: # If no specific direction, just check if it's fixed
            if self.rect.top == self.target_y and self.rect.left == self.target_x:
                self.fixed = True


'''Game Class'''
class gemGame():
    def __init__(self, screen, sounds, font, score_font, game_over_font, gem_imgs, cfg, grid_cell_image, background_texture, **kwargs):
        self.info = 'Gemgem - Dannz'
        self.screen = screen
        self.sounds = sounds
        self.font = font
        self.score_font = score_font
        self.game_over_font = game_over_font
        self.gem_imgs = gem_imgs
        self.cfg = cfg
        self.grid_cell_image = pygame.transform.smoothscale(grid_cell_image, (self.cfg.GRIDSIZE, self.cfg.GRIDSIZE))
        self.background_texture = background_texture
        if self.background_texture:
            # Scale background once to screen size if it's a static background
            self.background_texture = pygame.transform.scale(self.background_texture, self.cfg.SCREENSIZE)

        self.reset()

        # For add score animation
        self.add_score_alpha = 255
        self.add_score_y_offset = 0

    '''Start the game round'''
    def start(self):
        clock = pygame.time.Clock()
        
        overall_moving = True # True if gems are falling/moving due to gravity or generation
        individual_moving = False # True if selected gems are swapping

        gem_selected_xy = None # [x, y] of the first selected gem
        gem_selected_xy2 = None # [x, y] of the second selected gem
        swap_attempt_failed = False # Flag to indicate if a swap didn't result in a match and needs to revert

        add_score = 0
        
        time_pre = int(time.time())

        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    QuitGame() # This function should handle pygame.quit() and sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Only allow selection if no animations are active
                    if (not overall_moving) and (not individual_moving) and (add_score == 0):
                        position = pygame.mouse.get_pos()
                        clicked_gem_coords = self.checkSelected(position)
                        if clicked_gem_coords:
                            if gem_selected_xy is None:
                                gem_selected_xy = clicked_gem_coords
                            else:
                                gem_selected_xy2 = clicked_gem_coords
                                # Attempt swap only if different gems
                                if gem_selected_xy != clicked_gem_coords: # Ensure it's not the same gem clicked twice
                                    if self.swapGem(gem_selected_xy, gem_selected_xy2):
                                        individual_moving = True
                                        swap_attempt_failed = False # Reset for new swap
                                    else: # Not adjacent
                                        gem_selected_xy = None # Deselect the first one
                                else: # Clicked the same gem twice
                                    gem_selected_xy = None # Deselect

            # Handle overall gem movement (gravity/new gem drops)
            if overall_moving:
                # dropGems moves all non-fixed gems
                all_gems_fixed = self.dropGems()
                if all_gems_fixed:
                    overall_moving = False
                    # After all drops, check for matches
                    res_match = self.isMatch()
                    if res_match[0] > 0: # If there's a match after a drop
                        add_score = self.removeMatched(res_match) # This will re-trigger overall_moving
                        if add_score > 0:
                            self.add_score_alpha = 255 # Reset score animation
                            self.add_score_y_offset = 0
                            overall_moving = True # Keep overall moving as new gems need to drop


            # Handle individual gem movement (swapping)
            if individual_moving:
                gem1 = self.getGemByPos(*gem_selected_xy)
                gem2 = self.getGemByPos(*gem_selected_xy2)
                
                # Move both gems
                gem1.move()
                gem2.move()

                if gem1.fixed and gem2.fixed: # If both gems have reached their targets
                    # Check for matches after the swap
                    res_match = self.isMatch()
                    if res_match[0] == 0 and not swap_attempt_failed: # No match found, and it's the first check after swap
                        # Swap back to original positions
                        self.swapGem(gem_selected_xy, gem_selected_xy2)
                        self.sounds['mismatch'].play()
                        swap_attempt_failed = True # Mark that we're swapping back
                        gem1.fixed = False # Unfix to trigger reverse movement
                        gem2.fixed = False # Unfix to trigger reverse movement
                    else: # Match found or successfully swapped back
                        add_score = self.removeMatched(res_match)
                        individual_moving = False # Swap animation finished
                        gem_selected_xy = None # Clear selection
                        gem_selected_xy2 = None # Clear selection
                        overall_moving = True # Trigger general gravity check as board changed
                        if add_score > 0:
                            self.add_score_alpha = 255 # Reset score animation
                            self.add_score_y_offset = 0

            # --- Drawing Section with Error Handling ---
            try:
                if self.background_texture:
                    self.screen.blit(self.background_texture, (0, 0))
                else:
                    self.screen.fill((135, 206, 235))

                self.drawGrids()
                self.gems_group.draw(self.screen) # Draw all gems

                if gem_selected_xy:
                    # Enhanced selection highlight
                    self.drawSelectionHighlight(self.getGemByPos(*gem_selected_xy).rect)

                if add_score > 0: # Only draw add score if there's a score to show
                    self.drawAddScore(add_score)
                    # The fading animation in drawAddScore will eventually set alpha to 0.
                    # Once alpha is 0, we can reset add_score.
                    if self.add_score_alpha <= 0:
                        add_score = 0
                        self.add_score_alpha = 255 # Reset for next use
                        self.add_score_y_offset = 0

                self.remaining_time -= (int(time.time()) - time_pre)
                time_pre = int(time.time())

                self.showRemainingTime()
                self.drawScore()

                if self.remaining_time <= 0:
                    return self.score

                pygame.display.update()
                clock.tick(self.cfg.FPS)

            except pygame.error as e:
                # Catch the specific error indicating the display surface is gone
                if "display Surface quit" in str(e):
                    print("Pygame display surface quit unexpectedly. Attempting graceful exit.")
                    QuitGame() # Call QuitGame to perform pygame.quit() and sys.exit()
                    return self.score # Return score to exit this function
                else:
                    # Re-raise any other pygame errors
                    raise e

    '''Initialize/Reset game board'''
    def reset(self):
        # Randomly generate gems (initialize game map elements)
        while True:
            self.all_gems = []
            self.gems_group = pygame.sprite.Group()
            for x in range(self.cfg.NUMGRID):
                self.all_gems.append([])
                for y in range(self.cfg.NUMGRID):
                    gem_type = random.choice(list(self.gem_imgs.keys()))
                    # Initial position above the screen, they will drop down
                    initial_y = self.cfg.YMARGIN + y * self.cfg.GRIDSIZE - self.cfg.NUMGRID * self.cfg.GRIDSIZE
                    gem = gemSprite(
                        image=self.gem_imgs[gem_type],
                        gem_type=gem_type,
                        size=(self.cfg.GRIDSIZE, self.cfg.GRIDSIZE),
                        position=[self.cfg.XMARGIN + x * self.cfg.GRIDSIZE, initial_y]
                    )
                    # Set target_y for initial drop
                    gem.target_y = self.cfg.YMARGIN + y * self.cfg.GRIDSIZE
                    gem.fixed = False # They start unfixed
                    gem.direction = 'down' # They start by falling down

                    self.all_gems[x].append(gem)
                    self.gems_group.add(gem)
            # Ensure no initial matches
            if self.isMatch()[0] == 0:
                break
        # Score
        self.score = 0
        # Reward for a match
        self.reward = 10
        # Time
        self.remaining_time = 300

    '''Helper for outlined text rendering'''
    def draw_outlined_text(self, text, font, color, outline_color, position):
        # Render outline
        outline_text_surface = font.render(text, True, outline_color)
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            self.screen.blit(outline_text_surface, (position[0] + dx, position[1] + dy))
        # Render main text
        main_text_surface = font.render(text, True, color)
        self.screen.blit(main_text_surface, position)

    '''Display remaining time'''
    def showRemainingTime(self):
        self.draw_outlined_text(
            'CountDown: %ss' % str(self.remaining_time),
            self.font,
            (85, 65, 0), # Text color
            (0, 0, 0),   # Outline color
            (self.cfg.SCREENSIZE[0]-201, 6)
        )

    '''Display current score'''
    def drawScore(self):
        self.draw_outlined_text(
            'SCORE:'+str(self.score),
            self.score_font, # Using the dedicated score font
            (85, 65, 0),
            (0, 0, 0),
            (10, 6)
        )

    '''Display floating score addition with animation'''
    def drawAddScore(self, add_score):
        score_text = '+' + str(add_score)
        add_score_surface = self.font.render(score_text, True, (255, 100, 100))
        add_score_surface.set_alpha(self.add_score_alpha) # Apply fade effect

        rect = add_score_surface.get_rect()
        # Center horizontally, move upwards
        rect.center = (self.cfg.SCREENSIZE[0] // 2, self.cfg.SCREENSIZE[1] // 2 - self.add_score_y_offset)

        self.screen.blit(add_score_surface, rect)

        # Update for next frame for animation
        self.add_score_alpha = max(0, self.add_score_alpha - 5) # Decrease alpha (faster fade)
        self.add_score_y_offset += 1.5 # Move up (faster movement)

    '''Generate new gems after a match, handle gravity'''
    def generateNewGems(self, matched_gems_coords):
        # Matched_gems_coords is a list of [x, y] coordinates of all gems that were matched.
        # This function processes each affected column.

        affected_columns = set()
        for x, y in matched_gems_coords:
            gem = self.getGemByPos(x, y)
            if gem:
                self.gems_group.remove(gem) # Remove from sprite group for drawing
                self.all_gems[x][y] = None # Mark as empty in the grid
                affected_columns.add(x)

        # Process each affected column to apply "gravity" and create new gems
        for col_x in sorted(list(affected_columns)): # Process columns in ascending order
            empty_slots_in_col = 0
            # Iterate from bottom to top of the column to find empty slots and shift gems down
            for row_y in range(self.cfg.NUMGRID - 1, -1, -1):
                if self.all_gems[col_x][row_y] is None:
                    empty_slots_in_col += 1
                elif empty_slots_in_col > 0:
                    # Move the gem down to fill the empty slot below it
                    gem = self.getGemByPos(col_x, row_y)
                    self.all_gems[col_x][row_y + empty_slots_in_col] = gem # Update grid position
                    gem.target_y = self.cfg.YMARGIN + (row_y + empty_slots_in_col) * self.cfg.GRIDSIZE # Set new target Y
                    gem.fixed = False # Mark as not fixed to trigger movement
                    gem.direction = 'down' # Set direction
                    self.all_gems[col_x][row_y] = None # Clear original spot in grid

            # Create new gems at the top to fill the newly empty slots
            for i in range(empty_slots_in_col):
                # New gems fill the topmost empty slots in this column (row 0, 1, 2...)
                new_gem_row_y = i
                gem_type = random.choice(list(self.gem_imgs.keys()))
                new_gem = gemSprite(
                    image=self.gem_imgs[gem_type],
                    gem_type=gem_type,
                    size=(self.cfg.GRIDSIZE, self.cfg.GRIDSIZE),
                    # Initial position: start above the board, offset by 'i' to stack them
                    position=[self.cfg.XMARGIN + col_x * self.cfg.GRIDSIZE,
                              self.cfg.YMARGIN - (empty_slots_in_col - i) * self.cfg.GRIDSIZE]
                )
                # Set the final resting target Y
                new_gem.target_y = self.cfg.YMARGIN + new_gem_row_y * self.cfg.GRIDSIZE
                new_gem.fixed = False # New gems need to fall
                new_gem.direction = 'down' # They are falling down

                self.all_gems[col_x][new_gem_row_y] = new_gem # Place new gem in grid
                self.gems_group.add(new_gem) # Add to sprite group


    '''Remove matched gems and trigger new gem generation'''
    def removeMatched(self, res_match):
        if res_match[0] > 0: # If a match was found
            matched_coords = []
            if res_match[0] == 1: # Horizontal match
                start_x, start_y = res_match[1], res_match[2]
                for dx in range(3):
                    matched_coords.append([start_x + dx, start_y])
            elif res_match[0] == 2: # Vertical match
                start_x, start_y = res_match[1], res_match[2]
                for dy in range(3):
                    matched_coords.append([start_x, start_y + dy])
            # Call the new generateNewGems with all matched coordinates
            self.generateNewGems(matched_coords)
            self.score += self.reward
            return self.reward
        return 0

    '''Draw the game board grids with hollow effect'''
    def drawGrids(self):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                # Blit the pre-designed hollow grid cell image
                self.screen.blit(self.grid_cell_image, (self.cfg.XMARGIN + x * self.cfg.GRIDSIZE, self.cfg.YMARGIN + y * self.cfg.GRIDSIZE))

    '''Draw a block (now primarily used for selection highlight)'''
    def drawBlock(self, block, color=(255, 0, 255), size=4):
        pygame.draw.rect(self.screen, color, block, size)

    '''Animated selection highlight for selected gems'''
    def drawSelectionHighlight(self, rect):
        current_time = pygame.time.get_ticks()
        pulse_frequency = 500 # milliseconds for one pulse cycle
        pulse_value = (current_time % pulse_frequency) / pulse_frequency # 0.0 to 1.0

        # Alpha will pulse from a lower value (e.g., 100) to full (255) and back
        alpha = int(100 + 155 * abs(1 - 2 * pulse_value)) # Pulses from 100 to 255 and back

        # Create a temporary surface for the highlight rectangle with alpha
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((255, 255, 0, alpha)) # Yellow highlight with pulsing alpha
        self.screen.blit(s, rect)

        # Optional: draw a slightly larger outline for more emphasis
        pygame.draw.rect(self.screen, (255, 255, 0), rect, 3) # Static yellow outline

    '''Handles all gem falling (gravity)'''
    def dropGems(self):
        all_fixed = True
        # Iterate through all gems and move them if they are not fixed
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                gem = self.getGemByPos(x, y)
                if gem and not gem.fixed:
                    gem.move()
                    if not gem.fixed: # If still moving after this update, then not all are fixed
                        all_fixed = False
        return all_fixed

    '''Check if all positions in the grid have fixed gems'''
    def isFull(self):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                if not self.getGemByPos(x, y).fixed: # Check if a gem is still moving/not settled
                    return False
        return True

    '''Check if a mouse position has selected a gem, returns [x, y] grid coords'''
    def checkSelected(self, position):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                gem = self.getGemByPos(x, y)
                if gem and gem.rect.collidepoint(*position):
                    return [x, y]
        return None

    '''Check for 3-in-a-row matches (horizontal or vertical)'''
    def isMatch(self):
        # Check horizontal matches
        for y in range(self.cfg.NUMGRID):
            for x in range(self.cfg.NUMGRID - 2):
                if self.getGemByPos(x, y) and \
                   self.getGemByPos(x+1, y) and \
                   self.getGemByPos(x+2, y) and \
                   self.getGemByPos(x, y).type == self.getGemByPos(x+1, y).type == self.getGemByPos(x+2, y).type:
                    return [1, x, y] # [type_of_match (1=horizontal), start_x, start_y]

        # Check vertical matches
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID - 2):
                if self.getGemByPos(x, y) and \
                   self.getGemByPos(x, y+1) and \
                   self.getGemByPos(x, y+2) and \
                   self.getGemByPos(x, y).type == self.getGemByPos(x, y+1).type == self.getGemByPos(x, y+2).type:
                    return [2, x, y] # [type_of_match (2=vertical), start_x, start_y]
        return [0, 0, 0] # No match found

    '''Get gem object by its grid coordinates (x, y)'''
    def getGemByPos(self, x, y):
        if 0 <= x < self.cfg.NUMGRID and 0 <= y < self.cfg.NUMGRID:
            return self.all_gems[x][y]
        return None # Return None if out of bounds or no gem at that position

    '''Swap two gems in the grid'''
    def swapGem(self, gem1_grid_pos, gem2_grid_pos):
        # Ensure gems are adjacent
        dx = abs(gem1_grid_pos[0] - gem2_grid_pos[0])
        dy = abs(gem1_grid_pos[1] - gem2_grid_pos[1])

        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1): # If adjacent (horizontally or vertically)
            gem1 = self.getGemByPos(*gem1_grid_pos)
            gem2 = self.getGemByPos(*gem2_grid_pos)

            if not gem1 or not gem2: # Should not happen if checkSelected works, but good for safety
                return False

            # Determine movement directions and target positions for animation
            if gem1_grid_pos[0] < gem2_grid_pos[0]: # gem1 is left of gem2
                gem1.direction = 'right'
                gem2.direction = 'left'
            elif gem1_grid_pos[0] > gem2_grid_pos[0]: # gem1 is right of gem2
                gem1.direction = 'left'
                gem2.direction = 'right'
            elif gem1_grid_pos[1] < gem2_grid_pos[1]: # gem1 is above gem2
                gem1.direction = 'down'
                gem2.direction = 'up'
            elif gem1_grid_pos[1] > gem2_grid_pos[1]: # gem1 is below gem2
                gem1.direction = 'up'
                gem2.direction = 'down'

            # Set target pixel positions for the sprites
            gem1.target_x, gem1.target_y = gem2.rect.left, gem2.rect.top
            gem2.target_x, gem2.target_y = gem1.rect.left, gem1.rect.top

            # Mark as not fixed to trigger movement in the main loop
            gem1.fixed = False
            gem2.fixed = False

            # Swap gem objects in the underlying all_gems grid immediately
            self.all_gems[gem2_grid_pos[0]][gem2_grid_pos[1]] = gem1
            self.all_gems[gem1_grid_pos[0]][gem1_grid_pos[1]] = gem2
            return True
        return False # Not adjacent

    '''Information about the game'''
    def __repr__(self):
        return self.info
# gamemap.py (No changes needed for visual enhancement)

import random
from .mine import Mine


'''Minesweeper Map Class'''
class MinesweeperMap():
    def __init__(self, cfg, images, **kwargs):
        self.cfg = cfg
        # Mine matrix to store Mine objects
        self.mines_matrix = []
        for j in range(cfg.GAME_MATRIX_SIZE[1]):
            mines_line = []
            for i in range(cfg.GAME_MATRIX_SIZE[0]):
                # Calculate position for each mine cell
                position = i * cfg.GRIDSIZE + cfg.BORDERSIZE, (j + 2) * cfg.GRIDSIZE
                mines_line.append(Mine(images=images, position=position))
            self.mines_matrix.append(mines_line)
        
        # Randomly bury mines
        # Generates a list of unique random indices to place mines
        for i in random.sample(range(cfg.GAME_MATRIX_SIZE[0]*cfg.GAME_MATRIX_SIZE[1]), cfg.NUM_MINES):
            # Convert linear index back to 2D matrix coordinates
            self.mines_matrix[i//cfg.GAME_MATRIX_SIZE[0]][i%cfg.GAME_MATRIX_SIZE[0]].burymine()
        
        # This count variable seems unused, can be removed.
        # count = 0
        # for item in self.mines_matrix:
        #     for i in item:
        #         count += int(i.is_mine_flag)
        
        # Game current status code: -1: not started, 0: in progress, 1: game over (lost), 2: game over (won)
        self.status_code = -1
        # Store mouse press position and button state
        self.mouse_pos = None
        self.mouse_pressed = None
        
    '''Draw the current game state map'''
    def draw(self, screen):
        for row in self.mines_matrix:
            for item in row: 
                item.draw(screen)
                
    '''Set the current game status'''
    def setstatus(self, status_code):
        self.status_code = status_code
        
    '''Update the game state based on player's mouse operations'''
    def update(self, mouse_pressed=None, mouse_pos=None, type_='down'):
        assert type_ in ['down', 'up']
        
        # Record mouse press details on 'down' event
        if type_ == 'down' and mouse_pos is not None and mouse_pressed is not None:
            self.mouse_pos = mouse_pos
            self.mouse_pressed = mouse_pressed
            
        # Check if mouse click is outside the game map area
        if self.mouse_pos[0] < self.cfg.BORDERSIZE or self.mouse_pos[0] > self.cfg.SCREENSIZE[0] - self.cfg.BORDERSIZE or \
           self.mouse_pos[1] < self.cfg.GRIDSIZE * 2 or self.mouse_pos[1] > self.cfg.SCREENSIZE[1] - self.cfg.BORDERSIZE:
            return
            
        # If game hasn't started, start it upon first click within the map
        if self.status_code == -1:
            self.status_code = 0
            
        # If game is already over, no more mouse actions are processed for the map
        if self.status_code != 0:
            return
            
        # Convert mouse position to grid coordinates
        coord_x = (self.mouse_pos[0] - self.cfg.BORDERSIZE) // self.cfg.GRIDSIZE
        coord_y = self.mouse_pos[1] // self.cfg.GRIDSIZE - 2 # Adjust for top bar
        
        # Get the clicked mine object
        mine_clicked = self.mines_matrix[coord_y][coord_x]
        
        # Mouse button down actions
        if type_ == 'down':
            # --Both left and right mouse buttons pressed
            if self.mouse_pressed[0] and self.mouse_pressed[2]:
                # If the clicked cell is already opened and has mines around it
                if mine_clicked.opened and mine_clicked.num_mines_around > 0:
                    mine_clicked.setstatus(status_code=4) # Set status to 'double-clicking'
                    num_flags_around = 0
                    coords_around = self.getaround(coord_y, coord_x)
                    # Count flags around the clicked cell
                    for (j, i) in coords_around:
                        if self.mines_matrix[j][i].status_code == 2: # Status 2 is 'flagged'
                            num_flags_around += 1
                    
                    # If number of flags matches the number of mines around, open surrounding unflagged cells
                    if num_flags_around == mine_clicked.num_mines_around:
                        for (j, i) in coords_around:
                            if self.mines_matrix[j][i].status_code == 0: # Status 0 is 'unopened'
                                self.openmine(i, j) # Open the cell
                    else:
                        # If flag count doesn't match, highlight surrounding unopened cells
                        for (j, i) in coords_around:
                            if self.mines_matrix[j][i].status_code == 0:
                                self.mines_matrix[j][i].setstatus(status_code=5) # Set status to 'around double-clicked'
        # Mouse button up actions
        else:
            # --Left mouse button released
            if self.mouse_pressed[0] and not self.mouse_pressed[2]:
                # If the cell is not flagged or marked with a question mark
                if not (mine_clicked.status_code == 2 or mine_clicked.status_code == 3):
                    if self.openmine(coord_x, coord_y): # Attempt to open the mine
                        self.setstatus(status_code=1) # If it was a mine, game over (loss)
            # --Right mouse button released
            elif self.mouse_pressed[2] and not self.mouse_pressed[0]:
                # Cycle through unopened, flagged, question mark states
                if mine_clicked.status_code == 0:
                    mine_clicked.setstatus(status_code=2) # Unopened -> Flag
                elif mine_clicked.status_code == 2:
                    mine_clicked.setstatus(status_code=3) # Flag -> Question Mark
                elif mine_clicked.status_code == 3:
                    mine_clicked.setstatus(status_code=0) # Question Mark -> Unopened
            # --Both left and right mouse buttons released
            elif self.mouse_pressed[0] and self.mouse_pressed[2]:
                # Reset status of the double-clicked cell and its surrounding temporary highlights
                mine_clicked.setstatus(status_code=1) # The original clicked cell becomes opened
                coords_around = self.getaround(coord_y, coord_x)
                for (j, i) in coords_around:
                    if self.mines_matrix[j][i].status_code == 5:
                        self.mines_matrix[j][i].setstatus(status_code=0) # Reset temporary highlights to unopened
                        
    '''Open a mine cell'''
    def openmine(self, x, y):
        mine_clicked = self.mines_matrix[y][x]
        if mine_clicked.is_mine_flag:
            # Game over (clicked on a mine)
            for row in self.mines_matrix:
                for item in row:
                    if not item.is_mine_flag and item.status_code == 2:
                        item.setstatus(status_code=7) # Mark incorrectly flagged non-mines
                    elif item.is_mine_flag and item.status_code == 0:
                        item.setstatus(status_code=1) # Reveal unflagged mines
            mine_clicked.setstatus(status_code=6) # Mark the exploded mine
            return True # Game lost
        
        # If not a mine, open it
        mine_clicked.setstatus(status_code=1)
        
        # Calculate number of mines around
        coords_around = self.getaround(y, x)
        num_mines = 0
        for (j, i) in coords_around:
            num_mines += int(self.mines_matrix[j][i].is_mine_flag)
        mine_clicked.setnumminesaround(num_mines)
        
        # If no mines around, recursively open adjacent empty cells
        if num_mines == 0:
            for (j, i) in coords_around:
                # Only open if not already opened or processed (num_mines_around == -1 indicates unopened)
                if self.mines_matrix[j][i].num_mines_around == -1:
                    self.openmine(i, j)
        return False # Game continues
        
    '''Get coordinates of surrounding cells'''
    def getaround(self, row, col):
        coords = []
        # Iterate through a 3x3 grid centered at (row, col)
        for j in range(max(0, row-1), min(row+1, self.cfg.GAME_MATRIX_SIZE[1]-1)+1):
            for i in range(max(0, col-1), min(col+1, self.cfg.GAME_MATRIX_SIZE[0]-1)+1):
                if j == row and i == col:
                    continue # Skip the center cell itself
                coords.append((j, i))
        return coords
        
    '''Check if game is currently in progress'''
    @property
    def gaming(self):
        return self.status_code == 0
        
    '''Count of flagged mines'''
    @property
    def flags(self):
        num_flags = 0
        for row in self.mines_matrix:
            for item in row: 
                num_flags += int(item.status_code == 2) # Status 2 is 'flagged'
        return num_flags
        
    '''Count of opened cells'''
    @property
    def openeds(self):
        num_openeds = 0
        for row in self.mines_matrix:
            for item in row: 
                num_openeds += int(item.opened) # Check if cell is opened (status 1)
        return num_openeds

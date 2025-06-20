import sys
import warnings

# Hide the console window on Windows.
if sys.platform.startswith("win"):
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QGridLayout, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor, QFont

# Conditional import for core game implementations.
# This assumes a 'core.py' file exists with your game classes.
if __name__ == '__main__':
    from core import *
else:
    from .core import *

warnings.filterwarnings('ignore')

class CPGames():
    """
    Manages the collection of supported games and their respective classes.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.supported_games = self.initialize()

    def initialize(self):
        """
        Initializes and returns a dictionary of supported games.
        Each game maps to its corresponding game class.
        """
        supported_games = {
            'ski': SkiGame,
            'maze': MazeGame,
            'pacman': PacmanGame,
            'gemgem': GemGemGame,
            'tankwar': TankWarGame,
            'sokoban': SokobanGame,
            'pingpong': PingpongGame,
            'trexrush': TRexRushGame,
            'bomberman': BomberManGame,
            'whacamole': WhacAMoleGame,
            'catchcoins': CatchCoinsGame,
            'flappybird': FlappyBirdGame,
            'angrybirds': AngryBirdsGame,
            'magictower': MagicTowerGame,
            'aircraftwar': AircraftWarGame,
            'bunnybadger': BunnyBadgerGame,
            'minesweeper': MineSweeperGame,
            'greedysnake': GreedySnakeGame,
            'puzzlepieces': PuzzlePiecesGame,
            'towerdefense': TowerDefenseGame,
            'bloodfootball': BloodFootballGame,
            'alieninvasion': AlienInvasionGame,
            'breakoutclone': BreakoutcloneGame,
            'twozerofoureight': TwoZeroFourEightGame,
        }
        return supported_games

    def get_game_keys(self):
        """
        Returns a list of all game names (keys) available.
        """
        return list(self.supported_games.keys())

# --- New Custom GameCard Widget ---
class GameCard(QWidget):
    """
    A custom widget representing a single game, designed to look like an interactive card.
    It displays an icon and the game name, with visual feedback for hover and selection.
    """
    # Signal emitted when this card is clicked, carrying its game name.
    clicked = pyqtSignal(str)

    # Dictionary mapping game names to simple emoji/text icons.
    # Note: For actual game icons, you would typically load image files (e.g., .png, .svg).
    # This uses emojis for demonstration as direct image embedding for all games is complex
    # in PyQt5 without external files or a robust asset management system.
    GAME_ICONS = {
        'ski': '⛷️',
        'maze': '🌀',
        'pacman': '🟡',
        'gemgem': '💎',
        'tankwar': '🔫',
        'sokoban': '📦',
        'pingpong': '🏓',
        'trexrush': '🦖',
        'bomberman': '💣',
        'whacamole': '🔨',
        'catchcoins': '💰',
        'flappybird': '🐦',
        'angrybirds': '😡',
        'magictower': '🏰',
        'aircraftwar': '✈️',
        'bunnybadger': '🐰',
        'minesweeper': '💣',
        'greedysnake': '🐍',
        'puzzlepieces': '🧩',
        'towerdefense': '⚔️', # Reusing a castle icon for tower defense
        'bloodfootball': '⚽',
        'alieninvasion': '👽',
        'breakoutclone': '🧱',
        'twozerofoureight': '🔢',
    }

    def __init__(self, game_name, parent=None):
        super().__init__(parent)
        self.game_name = game_name
        self._is_selected = False # Internal state for selection
        self.setFixedSize(160, 140) # Fixed size for each card

        self.setup_ui()
        self.apply_base_style()
        self.setCursor(Qt.PointingHandCursor) # Change cursor on hover

    def setup_ui(self):
        """
        Sets up the layout and widgets for the game card (icon and name).
        """
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon Label
        self.icon_label = QLabel(self.GAME_ICONS.get(self.game_name.lower(), '🎮')) # Default icon
        self.icon_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(40) # Large font size for emoji icons
        self.icon_label.setFont(font)
        self.icon_label.setStyleSheet("color: white;") # Icon color
        layout.addWidget(self.icon_label)

        # Game Name Label
        self.name_label = QLabel(self.game_name.replace('_', ' ').title()) # Format name nicely
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 11pt;
        """)
        layout.addWidget(self.name_label)

        # Add a subtle drop shadow for a 3D effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100)) # Black, 100 alpha (semi-transparent)
        self.setGraphicsEffect(shadow)

    def apply_base_style(self):
        """
        Applies the default (unselected) style to the card.
        This gives a "hollow" appearance with a border.
        """
        self.setStyleSheet("""
            GameCard {
                background-color: transparent; /* Hollow effect */
                border: 2px solid #00539C; /* Outer border */
                border-radius: 12px;
                margin: 5px; /* Spacing between cards */
                /* Simulating inner shadow/depth */
            }
            GameCard:hover {
                background-color: rgba(0, 83, 156, 0.3); /* Lighter on hover, semi-transparent */
                border: 2px solid #0074D9;
            }
        """)
        self.graphicsEffect().setColor(QColor(0, 0, 0, 100)) # Reset shadow color

    def apply_selected_style(self):
        """
        Applies the selected style to the card, making it more prominent.
        """
        self.setStyleSheet("""
            GameCard {
                background-color: #0074D9; /* Solid background when selected */
                border: 2px solid #00DDFF; /* Bright border for selection */
                border-radius: 12px;
                margin: 5px;
            }
            GameCard:hover {
                background-color: #0088FF; /* Slightly different hover when selected */
            }
        """)
        self.graphicsEffect().setColor(QColor(0, 200, 255, 150)) # Brighter shadow for selection

    def set_selected(self, selected):
        """
        Sets the selection state of the card and updates its visual style.
        """
        if self._is_selected == selected:
            return

        self._is_selected = selected
        if self._is_selected:
            self.apply_selected_style()
        else:
            self.apply_base_style()

    def is_selected(self):
        """
        Returns the current selection state of the card.
        """
        return self._is_selected

    def mousePressEvent(self, event):
        """
        Handles mouse press events to emit the clicked signal.
        """
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.game_name)
        super().mousePressEvent(event)

# --- Main GameLauncherWindow updated ---
class GameLauncherWindow(QMainWindow):
    """
    The main window for the game launcher, featuring a grid-based selection
    of game cards instead of a dropdown.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Launcher")
        # Set the window icon. Replace "game.png" with an actual icon path if desired.
        # Otherwise, the default application icon will be used.
        self.setWindowIcon(QIcon("game.png"))
        self.setGeometry(100, 100, 800, 600) # Increased window size for card display
        self.selected_game_card = None # To keep track of the currently selected GameCard widget
        self.cp_games = CPGames()
        # The self.qt_games list is no longer needed as we're performing a dynamic check.
        # However, to maintain the structure and for potential future use if specific
        # PyQt5 games need special handling, an empty list or a very minimal one can be kept.
        # For now, it's removed for clarity as the dynamic check replaces its purpose.
        self.setup_ui()
        self.populate_game_grid() # Populate the grid with game cards

        # Overall window style with a navy-to-blue gradient background.
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #001f3f, stop:1 #0074D9);
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #001f3f;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #0074D9;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def setup_ui(self):
        """
        Sets up the main UI components, including the title, game grid, and launch button.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter) # Center content

        # Modern title label.
        self.title_label = QLabel("Select a Game")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif; /* Modern font */
            font-size: 32pt; /* Larger title */
            font-weight: bold;
            color: #E0E0E0; /* Lighter white */
            margin-bottom: 25px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* Subtle text shadow for depth */
        """)
        main_layout.addWidget(self.title_label)

        # Scrollable area for game cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # No horizontal scroll
        self.scroll_area_content = QWidget()
        self.game_grid_layout = QGridLayout(self.scroll_area_content)
        self.game_grid_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # Center items horizontally, align to top
        self.game_grid_layout.setSpacing(20) # Spacing between cards
        self.scroll_area.setWidget(self.scroll_area_content)
        main_layout.addWidget(self.scroll_area)

        # Launch button.
        self.launch_button = QPushButton("Launch Game")
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #0074D9; /* Primary blue */
                border: none;
                border-radius: 12px; /* More rounded */
                padding: 15px 30px; /* Larger padding */
                font-size: 18pt;
                font-weight: bold;
                color: white;
                margin-top: 30px; /* Space above button */
                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.4); /* Deeper shadow */
                transition: all 0.3s ease; /* Smooth transition for hover */
            }
            QPushButton:hover {
                background-color: #00539C; /* Darker blue on hover */
                box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.6); /* More intense shadow on hover */
                transform: translateY(-2px); /* Slight lift effect */
            }
            QPushButton:pressed {
                background-color: #003F7F; /* Even darker blue on press */
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3); /* Flatter shadow on press */
                transform: translateY(0px); /* Return to original position */
            }
            QPushButton:disabled {
                background-color: #333;
                color: #888;
                box-shadow: none;
            }
        """)
        self.launch_button.clicked.connect(self.launch_game)
        self.launch_button.setEnabled(False) # Initially disabled until a game is selected
        main_layout.addWidget(self.launch_button, alignment=Qt.AlignCenter) # Center the button

    def populate_game_grid(self):
        """
        Populates the QGridLayout with GameCard widgets for each available game.
        """
        game_keys = self.cp_games.get_game_keys()
        row = 0
        col = 0
        max_cols = 4 # Number of columns in the grid

        for game_name in game_keys:
            card = GameCard(game_name)
            card.clicked.connect(self.on_game_card_clicked) # Connect card's click signal
            self.game_grid_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Adjust column stretch to center items if fewer than max_cols in the last row
        if col > 0:
            for i in range(col, max_cols):
                self.game_grid_layout.setColumnStretch(i, 1) # Stretch empty columns

    def on_game_card_clicked(self, game_name):
        """
        Handles the event when a GameCard is clicked.
        Updates the selection state and enables the launch button.
        """
        # Deselect the previously selected card, if any
        if self.selected_game_card:
            self.selected_game_card.set_selected(False)

        # Find the new selected card widget
        # Iterating through layout items to find the clicked card.
        # This is less efficient for very large numbers of items, but fine for dozens of games.
        for i in range(self.game_grid_layout.count()):
            item = self.game_grid_layout.itemAt(i)
            if item and item.widget():
                card_widget = item.widget()
                if isinstance(card_widget, GameCard) and card_widget.game_name == game_name:
                    self.selected_game_card = card_widget
                    self.selected_game_card.set_selected(True)
                    break

        self.launch_button.setEnabled(True) # Enable launch button once a game is selected
        self.title_label.setText(f"Selected: {game_name.replace('_', ' ').title()}") # Update title to show selection

    def launch_game(self):
        """
        Launches the currently selected game.
        """
        if not self.selected_game_card:
            QMessageBox.warning(self, "No Selection", "Please select a game before launching.")
            return

        selected_game_name = self.selected_game_card.game_name
        game_class = self.cp_games.supported_games[selected_game_name]

        # Dynamically check if the game class is a PyQt5 QWidget (or subclass)
        # This is more robust than maintaining a manual list.
        if issubclass(game_class, QWidget):
            game_window = game_class()
            game_window.setWindowTitle(f"{selected_game_name.replace('_', ' ').title()} - Game")
            game_window.show()  # Display the game window.
        else:
            # For non-GUI games (like Pygame ones or console apps), use a thread to keep the launcher responsive.
            import threading
            threading.Thread(target=game_class().run, daemon=True).start()
            QMessageBox.information(self, "Game Launched", f"{selected_game_name.replace('_', ' ').title()} is running in the background.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = GameLauncherWindow()
    launcher.show()
    sys.exit(app.exec_())


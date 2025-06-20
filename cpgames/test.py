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
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Conditional import for core game implementations.
if __name__ == '__main__':
    from core import *
else:
    from .core import *

warnings.filterwarnings('ignore')


class CPGames():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.supported_games = self.initialize()

    def initialize(self):
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
        return list(self.supported_games.keys())


class GameLauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Launcher")
        # Set the window icon. Replace "your_icon.png" with the actual icon path.
        self.setWindowIcon(QIcon("game.png"))
        self.setGeometry(100, 100, 500, 300)
        self.setup_ui()
        self.cp_games = CPGames()
        # Define which games use a Qt-based GUI.
        self.qt_games = ['pacman'] # 'gobang' removed from here too if it was a Qt game
        self.populate_combo_box()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Modern title label.
        self.title_label = QLabel("Select a Game")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        self.layout.addWidget(self.title_label)

        # Combo box for game selection.
        self.combo_box = QComboBox()
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: #0074D9;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16pt;
                color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid white;
            }
            QComboBox QAbstractItemView {
                background-color: #001f3f;
                border: 1px solid #00539C;
                color: white;
                selection-background-color: #00539C;
            }
        """)
        self.layout.addWidget(self.combo_box)

        # Launch button.
        self.launch_button = QPushButton("Launch Game")
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #0074D9;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16pt;
                color: white;
            }
            QPushButton:hover {
                background-color: #00539C;
            }
        """)
        self.launch_button.clicked.connect(self.launch_game)
        self.layout.addWidget(self.launch_button)

        # Overall window style with a navy-to-blue gradient background.
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #001f3f, stop:1 #0074D9);
            }
        """)

    def populate_combo_box(self):
        game_keys = self.cp_games.get_game_keys()
        self.combo_box.clear()
        self.combo_box.addItems(game_keys)

    def launch_game(self):
        selected_game = self.combo_box.currentText()
        if not selected_game:
            QMessageBox.warning(self, "No Selection", "Please select a game before launching.")
            return

        # Launch the game without closing the launcher.
        if selected_game in self.qt_games:
            game_class = self.cp_games.supported_games[selected_game]
            game_window = game_class()
            game_window.setWindowTitle(f"{selected_game.capitalize()} - Game")
            game_window.show()  # Display the game window.
        else:
            # For non-GUI games, use a thread to keep the launcher responsive.
            import threading
            game_class = self.cp_games.supported_games[selected_game]
            threading.Thread(target=game_class().run, daemon=True).start()
            QMessageBox.information(self, "Game Launched", f"{selected_game.capitalize()} is running in the background.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = GameLauncherWindow()
    launcher.show()
    sys.exit(app.exec_())
'''initialize for alieninvasion modules'''
# This __init__.py file should expose the sprite classes
# defined in sprites.py within the same directory.
from .sprites import (
    AircraftSprite,
    UFOSprite,
    EnemySprite,
    MyBulletSprite,
    EnemyBulletSprite
)

# Also expose utility functions from utils.py which is in the same directory
from .utils import (
    showLife,
    showText,
    endInterface,
    BackgroundStar
)

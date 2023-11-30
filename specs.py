from ast import List
from enum import Enum

from dataclasses import dataclass

# Screen constant definitons
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BUSY_SCREEN_BASE = 400
OFFSET_750 = 750

MAIN_SCREEN = 1
GAME_SCREEN = 2
LOAD_SCREEN = 3
EDITOR_SCREEN = 4

# Board constants
BOARD_SIZE = 6

# Menu constants
BUTTON_HEIGHT = 75
BUTTON_WIDTH_REDUCTION = 40
BUTTON_INITIAL_X = 20
BUTTON_INITIAL_Y = 30
BUTTON_X_OFFSET = 10

# Action buttons constants
BUTTON_ACTION_FREE_SCREEN_OFFSET = 200
BUTTON_ACTION_WIDTH = 250
BUTTON_ACTION_Y_OFFSET = 100

# Numeric constants
TEN_PERCENT_DECIMAL = 0.1

class PlayerType(Enum):
    BLACK_PLAYER = 1
    WHITE_PLAYER = 2
    NONE = 6

class StateFlags(Enum):
    VOID = 0
    BLACK_PIECE = PlayerType.BLACK_PLAYER.value
    WHITE_PIECE = PlayerType.WHITE_PLAYER.value
    HELPER = 3

@dataclass
class DirectoryEntry:
    directories: list[str]
    NumberOfDirectories: int

@dataclass
class Slider:
    collision: bool
    difference: float
    offset: float
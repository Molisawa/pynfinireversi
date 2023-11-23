from pyray import *
from engine_classes import *
from dataclasses import dataclass
from typing import List

@dataclass
class Menu:
    goBackButton: Rectangle
    goForwardButton: Rectangle
    saveGameButton: Rectangle

@dataclass
class MenuOptions:
    startGameButton: Rectangle
    loadGameButton: Rectangle
    editorButton: Rectangle

class ScreenFlag(Enum):
    MENU = 0
    GAME = 1
    SAVE = 2
    LOAD = 3
    EDITOR = 4
    CONFIG_GAME = 5

@dataclass
class DirectoryEntry:
    directories: List[str]
    NumberOfDirectories: int

@dataclass
class Slider:
    collision: bool
    difference: float
    offset: float

@dataclass
class ScreenFeatures:
    screenWidth: int
    screenHeight: int
    squareSize: float
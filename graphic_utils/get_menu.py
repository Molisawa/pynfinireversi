from pyray import *
from engine import *
from graphic_classes import *

def getMenu(board, ScreenFeatures: ScreenFeatures):
    goBackButton = Rectangle(board.size * ScreenFeatures.squareSize + 20, 30,
                               ScreenFeatures.screenWidth - board.size * ScreenFeatures.squareSize - 40, 75)

    goForwardButton = Rectangle(goBackButton.x, goBackButton.height + goBackButton.y + 10,
                                  ScreenFeatures.screenWidth - board.size * ScreenFeatures.squareSize - 40, 75)
    saveGameButton = Rectangle(goForwardButton.x, goForwardButton.height + goForwardButton.y + 10,
                                 ScreenFeatures.screenWidth - board.size * ScreenFeatures.squareSize - 40, 75)
    return Menu(goBackButton, goForwardButton, saveGameButton)

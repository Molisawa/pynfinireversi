from pyray import *
from engine import *
from graphic_classes import *

def getMenuOptions(ScreenFeatures: ScreenFeatures) -> MenuOptions:
    bussy_screen = 400 + ScreenFeatures.screenHeight * 0.1
    free_screen = ScreenFeatures.screenHeight - bussy_screen
    number = (ScreenFeatures.screenWidth - (3 * 250)) / 4
    startGameButton = Rectangle(number, bussy_screen + 100, 250, free_screen - 200)
    loadGameButton = Rectangle(number + startGameButton.x + startGameButton.width, bussy_screen + 100, 250, free_screen - 200)
    editorButton = Rectangle(number + loadGameButton.x + loadGameButton.width, bussy_screen + 100, 250, free_screen - 200)

    return MenuOptions(startGameButton, loadGameButton, editorButton)

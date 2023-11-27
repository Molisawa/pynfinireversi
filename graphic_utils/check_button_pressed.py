from pyray import *
from engine import *
from graphic_classes import *

def CheckButtonPressed(menu: Menu, board, screen_list, mouse) -> None:
    if check_collision_point_rec(mouse, menu.goBackButton):
        goBack(board)
        goBack(board)
    elif check_collision_point_rec(mouse, menu.goForwardButton):
        goForward(board)
    elif check_collision_point_rec(mouse, menu.saveGameButton):
        screen_list[0] = ScreenFlag.SAVE

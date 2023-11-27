from pyray import *
from engine import *
from graphic_classes import *

def CheckMenuButtonPressed(menuOptions: MenuOptions, screen_list, board:Board, next_screen_list) -> any:
    clicked = is_mouse_button_pressed(0)
    mouse = get_mouse_position()

    if clicked and check_collision_point_rec(mouse, menuOptions.startGameButton):
        screen_list[0] = ScreenFlag.CONFIG_GAME
        next_screen_list[0] = ScreenFlag.GAME

    if clicked and check_collision_point_rec(mouse, menuOptions.loadGameButton):
        screen_list[0] = ScreenFlag.LOAD

    if clicked and check_collision_point_rec(mouse, menuOptions.editorButton):
        screen_list[0] = ScreenFlag.CONFIG_GAME
        next_screen_list[0] = ScreenFlag.EDITOR
        board.custom = True

    return screen_list[0], next_screen_list[0]

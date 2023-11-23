from pyray import *
from engine import *
from graphic_classes import *
from graphic_utils.get_directories import *
from graphic_utils.destroy_directory import *

def LoadFileScreen(board_container, ScreenFeatures, screen_list, slider):
    directory = getDirectories()
    clear_background(RAYWHITE)
    bar = (50 * directory.NumberOfDirectories + 10) > (ScreenFeatures.screenHeight - 80)
    bar_size = (
            (ScreenFeatures.screenHeight - 80) / (50 * directory.NumberOfDirectories + 10)) * (ScreenFeatures.screenHeight - 70)

    cancel_rect = Rectangle(25, ScreenFeatures.screenHeight - 60, ScreenFeatures.screenWidth - 50, 50)

    scroll_rect = Rectangle(ScreenFeatures.screenWidth - 20,
                            5 +
                            min(max(0, int(slider.offset + slider.difference)),
                                ScreenFeatures.screenHeight - 70 - bar_size),
                            15,
                            int(bar_size))
    if bar:
        draw_rectangle(int(ScreenFeatures.screenWidth - 20), 5, 15, int(cancel_rect.y - 10), fade(LIGHTGRAY, 0.6))

        if slider.collision:
            slider.offset = int(get_mouse_position().y)
            if not is_mouse_button_down(0):
                slider.collision = False

        if check_collision_point_rec(get_mouse_position(), scroll_rect) and is_mouse_button_pressed(0):
            slider.offset = int(get_mouse_position().y)
            slider.difference = int(scroll_rect.y - slider.offset)
            slider.collision = True

        draw_rectangle_rec(scroll_rect, GRAY if slider.collision else fade(GRAY, 0.65))

    percent = (scroll_rect.y - 5) / (ScreenFeatures.screenHeight - 70 - bar_size) if bar else 0

    for i in range(directory.NumberOfDirectories):
        rec = Rectangle(10, i * 50 + 10 - (((50 * directory.NumberOfDirectories + 10) - ScreenFeatures.screenHeight + 60) * percent),
                        int(measure_text(directory.directories[i], 20) + 20), 30)
        over = check_collision_point_rec(get_mouse_position(), rec)
        if is_mouse_button_pressed(0) and over:
            board_temp = loadGame(load_file_text(f"saved/{directory.directories[i]}"), board_container)
            if board_temp.initialized != 1:
                screen_list[0] = ScreenFlag.GAME
                DestroyDirectory(directory)
                return
            board_container[0] = board_temp  # Modificación aquí
            ScreenFeatures.squareSize = int(ScreenFeatures.screenHeight / board_container[0].size)
            screen_list[0] = ScreenFlag.GAME
        draw_rectangle_rec(rec, LIGHTGRAY if over else RAYWHITE)
        draw_text(directory.directories[i], 20, int(rec.y + 5), 20, BLACK)

    draw_rectangle(0, int(ScreenFeatures.screenHeight - 70), ScreenFeatures.screenWidth, 70, RAYWHITE)
    over = check_collision_point_rec(get_mouse_position(), cancel_rect)
    draw_rectangle_rec(cancel_rect, LIGHTGRAY if over else GRAY)
    if over and is_mouse_button_pressed(0):
        screen_list[0] = ScreenFlag.MENU
    draw_text("CANCEL", int(ScreenFeatures.screenWidth / 2 - measure_text("CANCEL", 30) / 2 + int(cancel_rect.x / 2)), int(cancel_rect.y + 10), 30, WHITE)

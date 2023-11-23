import os
from pyray import *
from engine import *
from graphic_classes import *


def ShowFileSaverScreen(board, ScreenFeatures, filename, frame_counter, mouse, screen_list, num_of_chars, last_screen):
    clear_background(RAYWHITE)

    width = max(measure_text(filename, 30), measure_text("XXXXXXXX", 30)) + 30

    save_width = measure_text("Save", 20) + 20
    cancel_width = measure_text("Cancel", 20) + 20

    save_rect = Rectangle(
        int(ScreenFeatures.screenWidth / 2 - (save_width + cancel_width + 40) / 2),
        int(ScreenFeatures.screenHeight / 2 + 50),
        int(save_width),
        30
    )

    cancel_rect = Rectangle(
        int(save_rect.x + save_rect.width + 40),
        int(save_rect.y),
        int(cancel_width),
        30
    )


    over_save = check_collision_point_rec(mouse, save_rect)
    over_cancel = check_collision_point_rec(mouse, cancel_rect)

    draw_rectangle_rec(save_rect, LIGHTGRAY if over_save else GRAY)
    draw_text("Save", int(save_rect.x + 10), int(save_rect.y + 5), 20, WHITE)
    draw_rectangle_rec(cancel_rect, LIGHTGRAY if over_cancel else GRAY)
    draw_text("Cancel", int(cancel_rect.x + 10), int(save_rect.y + 5), 20, WHITE)

    draw_rectangle_lines(int(ScreenFeatures.screenWidth / 2 - width / 2), int(ScreenFeatures.screenHeight / 2 - 20), int(width), 40, BLACK)
    draw_text(filename, int(ScreenFeatures.screenWidth / 2 - width / 2 + 10), int(ScreenFeatures.screenHeight / 2 - 15), 30, BLACK)

    if (frame_counter // 20) % 2 == 0:
        draw_text("_", int(ScreenFeatures.screenWidth / 2 - width / 2 + measure_text(filename, 30) + 10), int(ScreenFeatures.screenHeight / 2 - 15), 30, BLACK)

    if is_mouse_button_pressed(0) and over_save:
        os.makedirs("saved", exist_ok=True)
        save_file_text(f"saved/{filename}.brd", saveGame(board))
        filename = ""
        num_of_chars = 0
        # return screen_list, last_screen  # Return a tuple here
        screen_list[0] = last_screen


    if is_mouse_button_pressed(0) and over_cancel:
        filename = ""
        num_of_chars = 0
        screen_list[0] = last_screen
        # return screen_list, last_screen  # Return a tuple here

    # return screen_list, last_screen

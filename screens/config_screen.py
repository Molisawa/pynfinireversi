from pyray import *
from engine import *
from graphic_classes import *

def ConfigGameScreen(ScreenFeatures: ScreenFeatures, board, screen_list, customBoardSize_list, difficulty_list, next_screen_list):
    clear_background(RAYWHITE)

    draw_text("Chose your board size", int(ScreenFeatures.screenWidth / 3 - measure_text("Chose your board size", 30) / 2), int(ScreenFeatures.screenHeight / 2 - 300), 30, GRAY)
    margin = int((2 * (ScreenFeatures.screenWidth / 3) - 2 * 130) / 3)
    sum_rect = Rectangle(margin, int(ScreenFeatures.screenHeight / 2 - 30), 130, 130)
    subs_rect = Rectangle(margin + sum_rect.x + sum_rect.width, sum_rect.y, sum_rect.width, sum_rect.height)

    mouse = get_mouse_position()
    clicked = is_mouse_button_pressed(0)
    over_sum = check_collision_point_rec(mouse, sum_rect)
    over_subs = check_collision_point_rec(mouse, subs_rect)

    draw_rectangle_rec(sum_rect, LIGHTGRAY if over_sum else RAYWHITE)
    draw_text("+", int(sum_rect.x + sum_rect.width / 2 - measure_text("+", 70) / 2), int(sum_rect.y + sum_rect.height / 2 - 35), 70, BLACK)
    draw_rectangle_rec(subs_rect, LIGHTGRAY if over_subs else RAYWHITE)
    draw_text("-", int(subs_rect.x + subs_rect.width / 2 - measure_text("-", 70) / 2), int(subs_rect.y + subs_rect.height / 2 - 35), 70, BLACK)

    accept_button = Rectangle(int(ScreenFeatures.screenWidth / 2 - 100), int(ScreenFeatures.screenHeight / 2 + 120), 200, 80)
    cancel_button = Rectangle(int(ScreenFeatures.screenWidth / 2 - 100), int(accept_button.y + accept_button.height + 50), accept_button.width, accept_button.height)

    draw_rectangle_rec(accept_button, LIGHTGRAY)
    draw_rectangle_rec(cancel_button, LIGHTGRAY)

    draw_text("Accept", int(accept_button.x + accept_button.width / 2 - measure_text("Accept", 40) / 2), int(accept_button.y + accept_button.height / 2 - 20), 40, WHITE)
    draw_text("Cancel", int(cancel_button.x + cancel_button.width / 2 - measure_text("Cancel", 40) / 2), int(cancel_button.y + cancel_button.height / 2 - 20), 40, WHITE)

    margin_difficulty = int((ScreenFeatures.screenHeight - 340) / 2)

    easy_button = Rectangle(int(ScreenFeatures.screenWidth * 3 / 4 - (ScreenFeatures.screenWidth / 3 - 80) / 2), margin_difficulty, int(ScreenFeatures.screenWidth / 3 - 80), 80)
    intermediate_button = Rectangle(easy_button.x, int(easy_button.y + easy_button.height + 50), easy_button.width, easy_button.height)
    hard_button = Rectangle(int(intermediate_button.x), int(intermediate_button.y + intermediate_button.height + 50), intermediate_button.width, intermediate_button.height)

    draw_rectangle_rec(easy_button, GRAY if difficulty_list[0] == Difficulty.EASY else LIGHTGRAY)
    draw_rectangle_rec(intermediate_button, GRAY if difficulty_list[0] == Difficulty.INTERMEDIATE else LIGHTGRAY)
    draw_rectangle_rec(hard_button, GRAY if difficulty_list[0] == Difficulty.HARD else LIGHTGRAY)

    draw_text("EASY", int(easy_button.x + easy_button.width / 2 - measure_text("EASY", 20) / 2), int(easy_button.y + easy_button.height / 2 - 10), 20, WHITE)
    draw_text("INTERMEDIATE", int(intermediate_button.x + intermediate_button.width / 2 - measure_text("INTERMEDIATE", 20) / 2), int(intermediate_button.y + intermediate_button.height / 2 - 10), 20, WHITE)
    draw_text("HARD", int(hard_button.x + hard_button.width / 2 - measure_text("HARD", 20) / 2), int(hard_button.y + hard_button.height / 2 - 10), 20, WHITE)

    over_easy = check_collision_point_rec(mouse, easy_button)
    over_intermediate = check_collision_point_rec(mouse, intermediate_button)
    over_hard = check_collision_point_rec(mouse, hard_button)

    if clicked and over_easy:
        difficulty_list[0] = Difficulty.EASY
    if clicked and over_intermediate:
        difficulty_list[0] = Difficulty.INTERMEDIATE
    if clicked and over_hard:
        difficulty_list[0] = Difficulty.HARD

    if over_sum and clicked:
        customBoardSize_list[0] += 1 
    if over_subs and clicked and customBoardSize_list[0] > 0:
        customBoardSize_list[0] -= 1 

    size =  6 + 2 * customBoardSize_list[0]
    text = str(6 + 2 * customBoardSize_list[0])
    draw_text(text, int(ScreenFeatures.screenWidth / 3 - measure_text(text, 100) / 2), int(ScreenFeatures.screenHeight / 2 - 180), 100, BLACK)

    if check_collision_point_rec(mouse, accept_button) and clicked:
        initializeGame(board, size, difficulty_list[0], True, Player(True), Player(False))
        screen_list[0] = next_screen_list[0]
        difficulty_list[0] = Difficulty.EASY
        ScreenFeatures.squareSize = int(ScreenFeatures.screenHeight / size)
    if check_collision_point_rec(mouse, cancel_button) and clicked:
        screen_list[0] = ScreenFlag.MENU
        difficulty_list[0] = Difficulty.EASY

    return customBoardSize_list

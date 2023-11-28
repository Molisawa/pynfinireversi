import math
from pyray import *
from engine import *
from graphic_classes import *
from graphic_utils.update_drawing_state import *
from graphic_utils.draw_board_grid import *
from piece import Piece

def EditorScreen(screenFeatures: ScreenFeatures, board: Board, piece: Piece, screen_list):
    clear_background(DARKGREEN)
    DrawBoardGrid(board, screenFeatures)
    margin = board.size * screenFeatures.squareSize
    free_space = screenFeatures.screenWidth - margin
    radius = free_space / 4
    black = Vector2(2 * radius + margin, 50 + radius)
    white = Vector2(black.x, 50 + black.y + 2 * radius)
    draw_circle_v(black, radius, BLACK)
    draw_circle_v(white, radius, WHITE)
    is_black = piece.pieceType == PlayerType.BLACK_PLAYER.value
    draw_circle_v(black if is_black else white, radius // 10, RED)

    mouse = get_mouse_position()
    clicked = is_mouse_button_pressed(0)

    UpdateDrawingState(board, screenFeatures)
    if 0 <= mouse.x < margin and 0 <= mouse.x < screenFeatures.screenHeight:
        clicked = is_mouse_button_down(0)
        x = math.floor(mouse.x / screenFeatures.squareSize)
        y = math.floor(mouse.y / screenFeatures.squareSize)
        helper = Vector2(x * screenFeatures.squareSize + radius, y * screenFeatures.squareSize + radius)

        helper_rect = Rectangle(helper.x + 1 - radius, helper.y + 1 - radius, screenFeatures.squareSize - 2, screenFeatures.squareSize - 2)
        draw_rectangle_rec(helper_rect, DARKGREEN)

        circle = Vector2(x * screenFeatures.squareSize + screenFeatures.squareSize / 2, y * screenFeatures.squareSize + screenFeatures.squareSize / 2)

        if piece.pieceType == PlayerType.BLACK_PLAYER.value:
            draw_circle_v(circle, screenFeatures.squareSize / 2 - 5, fade(BLACK, 0.5))
        elif piece.pieceType == PlayerType.WHITE_PLAYER.value:
            draw_circle_v(circle, screenFeatures.squareSize / 2 - 5, fade(WHITE, 0.5))

        if check_collision_point_rec(mouse, helper_rect) and clicked:
            board.state[x][y].pieceType = PlayerType.BLACK_PLAYER.value if is_black else PlayerType.WHITE_PLAYER.value
            board.initialState[x][y].pieceType = PlayerType.BLACK_PLAYER.value if is_black else PlayerType.WHITE_PLAYER.value

        if check_collision_point_rec(mouse, helper_rect) and (is_mouse_button_pressed(1) or is_mouse_button_down(1)):
            board.state[x][y].pieceType = StateFlags.VOID.value
            board.initialState[x][y].pieceType = StateFlags.VOID.value

    exit_rect = Rectangle(int(margin + 30), int(screenFeatures.screenHeight - 150), int((free_space - 60)), 100)
    draw_rectangle_rec(exit_rect, LIGHTGRAY)
    draw_text("Exit", int(exit_rect.x + exit_rect.width / 2 - measure_text("Exit", 30) / 2), int(exit_rect.y + exit_rect.height / 2 - 15), 30, WHITE)

    save_rect = Rectangle(int(margin + 30), int(exit_rect.y - exit_rect.height - 50), int((free_space - 60)), 100)
    draw_rectangle_rec(save_rect, LIGHTGRAY)
    draw_text("Save", int(save_rect.x + save_rect.width / 2 - measure_text("Save", 30) / 2), int(save_rect.y + save_rect.height / 2 - 15), 30, WHITE)

    if clicked and check_collision_point_circle(mouse, black, radius):
        piece.pieceType = PlayerType.BLACK_PLAYER.value
    if clicked and check_collision_point_circle(mouse, white, radius):
        piece.pieceType = PlayerType.WHITE_PLAYER.value

    if clicked and check_collision_point_rec(mouse, save_rect):
        screen_list[0] = ScreenFlag.SAVE

    if clicked and check_collision_point_rec(mouse, exit_rect):
        board = None
        screen_list[0] = ScreenFlag.MENU

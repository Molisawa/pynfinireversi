from pyray import *
from engine import *
from graphic_classes import *
from graphic_utils.check_button_pressed import *
from graphic_utils.check_piece_played import *
from graphic_utils.draw_board_grid import *
from graphic_utils.update_drawing_state import *

def PlayScreen(board:Board, menu:Menu, ScreenFeatures:ScreenFeatures, screen_list, mouse, clicked):
    clear_background(DARKGREEN)
    DrawBoardGrid(board, ScreenFeatures)

    draw_rectangle(int(menu.goBackButton.x), int(menu.goBackButton.y), int(menu.goBackButton.width), int(menu.goBackButton.height), WHITE)
    draw_rectangle(int(menu.goForwardButton.x), int(menu.goForwardButton.y), int(menu.goForwardButton.width), int(menu.goForwardButton.height), WHITE)
    draw_rectangle(int(menu.saveGameButton.x), int(menu.saveGameButton.y), int(menu.saveGameButton.width), int(menu.saveGameButton.height), WHITE)

    draw_text("Go back", int(menu.goBackButton.x - measure_text("Go back", 30) / 2 + menu.goBackButton.width / 2),
              int(menu.goBackButton.y + menu.goBackButton.height / 2 - 15), 30, BLACK if canGoBack(board) else GRAY)
    draw_text("Go foward", int(menu.goForwardButton.x - measure_text("Go foward", 30) / 2 + menu.goForwardButton.width / 2),
              int(menu.goForwardButton.y + menu.goForwardButton.height / 2 - 15), 30, BLACK if canGoFoward(board) else GRAY)
    draw_text("Save game", int(menu.saveGameButton.x - measure_text("Save game", 30) / 2 + menu.saveGameButton.width / 2),
              int(menu.saveGameButton.y + menu.saveGameButton.height / 2 - 15), 30, BLACK)
    if clicked:
        CheckButtonPressed(menu, board, screen_list, mouse)
    UpdateDrawingState(board, ScreenFeatures)
    if nextTurn(board) == PlayerType.BLACK_PLAYER.value:
        SetHelpers(board, PlayerType.BLACK_PLAYER.value)
        CheckPiecePlayed(board, ScreenFeatures, clicked, mouse)
    elif nextTurn(board) == PlayerType.WHITE_PLAYER.value:
        computerMove(board, PlayerType.WHITE_PLAYER.value)

    draw_text("Your score:", int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 30), 20, WHITE)
    val = getScore(board, PlayerType.BLACK_PLAYER.value)
    draw_text(str(val), int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 50), 20, WHITE)

    draw_text("CPU score:", int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 100), 20, WHITE)
    val = getScore(board, PlayerType.WHITE_PLAYER.value)
    draw_text(str(val), int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 120), 20, WHITE)

    if isGameOver(board):
        draw_text("Game Over", int((ScreenFeatures.squareSize * board.size) / 2 - measure_text("Game Over", 80) / 2),
                  int(ScreenFeatures.screenHeight / 2 - 40), 80, GRAY)
        text = ""
        color = GRAY
        if getWinner(board) == Winners.WINNER.name:
            text = "You win!"
            color = GREEN
        elif getWinner(board) == Winners.LOSER.name:
            text = "You lose!"
            color = RED
        elif getWinner(board) == Winners.TIE.name:
            text = "It's a tie!"
        draw_text(text, int((ScreenFeatures.squareSize * board.size) / 2 - measure_text(text, 60) / 2),
                  int(ScreenFeatures.screenHeight / 2 - 30 + 80 + 10), 60, color)

    margin = board.size * ScreenFeatures.squareSize
    free_space = ScreenFeatures.screenWidth - margin
    exit_rect = Rectangle(int(margin + 30), int(ScreenFeatures.screenHeight - 150), int((free_space - 60)), 100)
    draw_rectangle_rec(exit_rect, WHITE)
    draw_text("Exit", int(exit_rect.x + exit_rect.width / 2 - measure_text("Exit", 30) / 2), int(exit_rect.y + exit_rect.height / 2 - 15), 30, BLACK)
    if clicked and check_collision_point_rec(mouse, exit_rect):
        destructBoard(board)
        screen_list[0] = ScreenFlag.MENU

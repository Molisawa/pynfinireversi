from pyray import *
from engine import *
from graphic_classes import *

def DrawBoardGrid(board: Board, screenFeatures: ScreenFeatures) -> None:
    for i in range(board.size + 1):
        draw_line_v((int(screenFeatures.squareSize * i), 0), (int(screenFeatures.squareSize * i), int(board.size * screenFeatures.squareSize)), BLACK)

    for i in range(board.size + 1):
        draw_line_v((0, int(screenFeatures.squareSize * i)), (int(board.size * screenFeatures.squareSize), int(screenFeatures.squareSize * i)), BLACK)

    draw_rectangle(int(board.size * screenFeatures.squareSize) + 1, 0, int(screenFeatures.screenWidth - 1), int(screenFeatures.screenHeight), WHITE)
    draw_rectangle(int(board.size * screenFeatures.squareSize) + 1, 0, int(screenFeatures.screenWidth - 1), int(screenFeatures.screenHeight), fade(DARKGREEN, 0.5))

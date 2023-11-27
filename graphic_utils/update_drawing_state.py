from pyray import *
from engine import *
from graphic_classes import *

def UpdateDrawingState(board:Board, screenFeatures: ScreenFeatures)->None:

    offset = int((screenFeatures.squareSize / 2 - 5) * 0.25)
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == StateFlags.VOID.value:
                pass
            elif board.state[i][j].pieceType == StateFlags.BLACK_PIECE.value:
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 5), BLACK)
                draw_circle_gradient(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int((screenFeatures.squareSize / 2 - 5) * 0.5), fade(WHITE, 0.15), fade(WHITE, 0))
            elif board.state[i][j].pieceType == StateFlags.WHITE_PIECE.value:
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 5), RAYWHITE)
                draw_circle_gradient(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int((screenFeatures.squareSize / 2 - 5) * 0.5), fade(BLACK, 0.15), fade(BLACK, 0))
            elif board.state[i][j].pieceType == StateFlags.HELPER.value:
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 5), DARKGRAY)
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 7), DARKGREEN)

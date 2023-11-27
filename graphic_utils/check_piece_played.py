from pyray import *
from engine import *
from graphic_classes import *
from graphic_utils.update_drawing_state import *

def CheckPiecePlayed(board: Board, screenFeatures: ScreenFeatures, clicked, mouse) -> None:
    for i in range(board.size):
        for j in range(board.size):
            vector = None
            if board.state[i][j].pieceType == StateFlags.HELPER.value:
                vector = (i * screenFeatures.squareSize + screenFeatures.squareSize / 2,
                          j * screenFeatures.squareSize + screenFeatures.squareSize / 2)
                if check_collision_point_circle(mouse, vector, screenFeatures.squareSize / 2 - 5):
                    if not clicked:
                        draw_rectangle(int(i * screenFeatures.squareSize + 1), int(j * screenFeatures.squareSize + 1),
                                       int(screenFeatures.squareSize - 2), int(screenFeatures.squareSize - 2), DARKGREEN)
                        draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                                    int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                                    int(screenFeatures.squareSize / 2 - 5), fade(BLACK, 0.4))
                    else:
                        m = Movement(pieceType=PlayerType.BLACK_PLAYER.value, x=i, y=j)
                        makeRealMove(board, m)
                        removeHistoryFoward(board)
                        UpdateDrawingState(board, screenFeatures)

from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def saveGame(board:Board):
    data = {
        "board_size": board.size,
        "game_difficulty": board.difficulty.name,
        "movements": [
            {"piece_type": move.pieceType, "x": move.x, "y": move.y} for move in board.historyBack
        ],
        "custom": board.custom
    }

    if board.custom:
        data["initial_board"] = [
            {"piece_type": cell.pieceType} for row in board.initialState for cell in row
        ]

    return json.dumps(data)
from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def setCustomBoardState(board:Board) -> None:
    for k in range(board.size):
        for l in range(board.size):
            board.state[k][l].pieceType = board.initialState[k][l].pieceType
    return board
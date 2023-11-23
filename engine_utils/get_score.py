from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def getScore(board, piece):
    score = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == piece:
                score += 1
    return score
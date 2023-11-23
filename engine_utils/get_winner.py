from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def getWinner(board:Board):

    white_moves = 0
    black_moves = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == 2:
                white_moves += 1
            if board.state[i][j].pieceType == 1:
                black_moves += 1
    if white_moves == black_moves:
        return "TIE"
    if white_moves > black_moves:
        return "LOSER"
    else:
        return "WINNER"
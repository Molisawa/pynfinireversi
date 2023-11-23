from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def getScorePosition(board:Board, pieceType):
    valores = [[0] * board.size for _ in range(board.size)]

    for i in range(board.size):
        valores[1][i] = -20
        valores[board.size - 2][i] = -20
        if i < board.size - 4:
            valores[0][i + 2] = 7
            valores[board.size - 1][i + 2] = 7
        for j in range(board.size):
            valores[j][1] = -20
            valores[j][board.size - 2] = -20
            if j < board.size - 4:
                valores[j + 2][0] = 7
                valores[j + 2][board.size - 1] = 7
            if j < board.size - 4 and i < board.size - 4:
                valores[j + 2][i + 2] = 4

    for value in range(1, 3):
        is_negative = -1 if value % 2 else 1
        tmp = 100 / (value + 1) * is_negative
        valores[value][value] = tmp
        valores[board.size - 1 - value][value] = tmp
        valores[value][board.size - 1 - value] = tmp
        valores[board.size - 1 - value][board.size - value - 1] = tmp

    score = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == pieceType:
                score += valores[i][j]

    return score
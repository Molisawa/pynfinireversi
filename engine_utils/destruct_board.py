from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def destructBoard(board):
    for i in range(board.size):
        board.state[i] = None

    for i in range(board.size):
        board.initialState[i] = None

    board.state = None
    board.initialState = None
    board.historyBack = None
    board.historyForward = None
    board = None
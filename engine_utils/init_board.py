from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def initializeBoard(board:Board) -> None:
    '''
    Funciton to initialize the board states.
    Initially, it restards to zero
    Then, it gives the deffault values for a game with stat
    '''
    board.lastPiecetypeMoved = 2

    set_states(board)
    initialize_values(board)

def set_states(board: Board) -> None:
    '''
    Reset the states
    '''
    board.state = [[Piece() for _ in range(board.size)] for _ in range(board.size)]
    for i in range(board.size):
        for j in range(board.size):
            board.state[i][j].pieceType = 0

    board.initialState = [[Piece() for _ in range(board.size)] for _ in range(board.size)]
    for i in range(board.size):
        for j in range(board.size):
            board.initialState[i][j].pieceType = 0

def initialize_values(board: Board):
    '''
    Initialize with player values
    '''
    board.state[board.size // 2 - 1][board.size // 2 - 1].pieceType = 2
    board.state[board.size // 2][board.size // 2].pieceType = 2
    board.state[board.size // 2 - 1][board.size // 2].pieceType = 1
    board.state[board.size // 2][board.size // 2 - 1].pieceType = 1

    board.initialState[board.size // 2 - 1][board.size // 2 - 1].pieceType = 2
    board.initialState[board.size // 2][board.size // 2].pieceType = 2
    board.initialState[board.size // 2 - 1][board.size // 2].pieceType = 1
    board.initialState[board.size // 2][board.size // 2 - 1].pieceType = 1
from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def isValidMove(board:Board, lastMove:Movement) -> bool:
    opponent = PlayerType.BLACK_PLAYER.value if lastMove.pieceType == PlayerType.WHITE_PLAYER.value else PlayerType.WHITE_PLAYER.value
    colIndex = lastMove.x - 1
    rowIndex = lastMove.y
    offset = 0

    if ( vertical_review(board, rowIndex, colIndex, opponent, lastMove, offset) or 
        horizontal_review(board, rowIndex, colIndex, opponent, lastMove, offset) or 
        diagonal_above(board, rowIndex, colIndex, opponent, lastMove, offset) or
        diagonal_below(board, rowIndex, colIndex, opponent, lastMove, offset) ): 
            return True

    # when all hopes fade away
    return False

def vertical_review(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int) -> bool:
    '''
    This is the movement review for the up and down position
    '''
    # Move up
    while colIndex > 0 and board.state[colIndex][rowIndex].pieceType == opponent:
        colIndex -= 1
        offset += 1
    if colIndex >= 0 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True
    
    # move down
    colIndex = lastMove.x + 1
    rowIndex = lastMove.y
    offset = 0

    while colIndex < board.size - 1 and board.state[colIndex][rowIndex].pieceType == opponent:
        colIndex += 1
        offset += 1
    if colIndex <= board.size - 1 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True

    return False

def horizontal_review(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int) -> bool:
    '''
    This is the movement review for the right and left position
    '''
    # move left
    colIndex = lastMove.x
    rowIndex = lastMove.y - 1
    offset = 0
    while rowIndex > 0 and board.state[colIndex][rowIndex].pieceType == opponent:
        rowIndex -= 1
        offset += 1
    if rowIndex >= 0 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True
    
    # move right
    colIndex = lastMove.x
    rowIndex = lastMove.y + 1
    offset = 0
    while rowIndex < board.size - 1 and board.state[colIndex][rowIndex].pieceType == opponent:
        rowIndex += 1
        offset += 1
    if rowIndex <= board.size - 1 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True

    return False

def diagonal_above(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int) -> bool:
    '''
    This is the movement review for the right and left diagonal position above
    '''
    # move up left
    colIndex = lastMove.x - 1
    rowIndex = lastMove.y - 1
    offset = 0
    while colIndex > 0 and rowIndex > 0 and board.state[colIndex][rowIndex].pieceType == opponent:
        colIndex -= 1
        rowIndex -= 1
        offset += 1
    if colIndex >= 0 and rowIndex >= 0 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True

    # move up right
    colIndex = lastMove.x - 1
    rowIndex = lastMove.y + 1
    offset = 0
    while colIndex > 0 and rowIndex < board.size - 1 and board.state[colIndex][rowIndex].pieceType == opponent:
        colIndex -= 1
        rowIndex += 1
        offset += 1
    if colIndex >= 0 and rowIndex <= board.size - 1 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True

    return False

def diagonal_below(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int)->bool:
    '''
    This is the movement review for the right and left diagonal position below
    '''
    # move down left
    colIndex = lastMove.x + 1
    rowIndex = lastMove.y - 1
    offset = 0
    while colIndex < board.size - 1 and rowIndex > 0 and board.state[colIndex][rowIndex].pieceType == opponent:
        colIndex += 1
        rowIndex -= 1
        offset += 1
    if colIndex <= board.size - 1 and rowIndex >= 0 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True

    # move down right
    colIndex = lastMove.x + 1
    rowIndex = lastMove.y + 1
    offset = 0
    while colIndex < board.size - 1 and rowIndex < board.size - 1 and board.state[colIndex][rowIndex].pieceType == opponent:
        colIndex += 1
        rowIndex += 1
        offset += 1
    if colIndex <= board.size - 1 and rowIndex <= board.size - 1 and board.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
        return True

    return False
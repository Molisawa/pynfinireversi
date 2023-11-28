from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from board import Board
from engine_classes import *
from engine_utils.can_go_back import *
from engine_utils.can_go_forward import *
from engine_utils.clean_helpers import *
from engine_utils.get_point_evaluator import *
from engine_utils.get_score_position import *
from engine_utils.get_score import *
from engine_utils.get_winner import *
from engine_utils.is_valid_move import *
from engine_utils.remove_history_forward import *


def initializeGame(board:Board, size, difficulty, custom, player1, player2):
    board.initialized = 1
    board.difficulty = difficulty
    board.noOfMovesBack = 0
    board.historyBack = []
    board.noOfMovesFoward = 0
    board.historyForward = []
    board.size = size
    board.custom = custom
    board.player1 = player1
    board.player2 = player2
    board.initializeBoard(board)
    return
    # Después de initializeBoard(board)

def isGameOver(board):
    return not canMove(board, 1) and not canMove(board, 0)

def SetHelpers(board:Board, player:PlayerType):
    possibleMoves = 0
    cleanHelpers(board)
    opponent = 0 if player == 1 else 1
    if board.lastPiecetypeMoved == player and canMove(board, opponent):
        return
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == 0:
                m = Movement(player, i, j)
                if isValidMove(board, m):
                    possibleMoves += 1
                    board.state[i][j].pieceType = 3
    print("Possible moves: ", possibleMoves)



def canSkipBlackPiece(board):
    return not isGameOver(board) and not canMove(board, 1) and board.lastPiecetypeMoved == 2 and board.noOfMovesFoward == 0

def bestMinimaxMove(board, player):
    global nodes
    nodes = 0

    all_moves = getAllPossibleMoves(board, player)
    best_move = Movement(pieceType=PlayerType.NONE, x=-1, y=1)
    score = -sys.maxsize
    number_of_moves = getNumberOfMoves(board, player)

    boards = [copy.deepcopy(board) for _ in range(number_of_moves)]
    for i in range(number_of_moves):
        tmp = copy.deepcopy(board)

        m = Movement(pieceType=player, x=all_moves[i].x, y=all_moves[i].y)

        score_temp = MinimaxSolver(5, -sys.maxsize, sys.maxsize, tmp, m, player)
        if score_temp > score:
            score = score_temp
            best_move = m

def getNumberOfMoves(board:Board, pieceType:PlayerType):
    moves = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == StateFlags.VOID.value or board.state[i][j].pieceType == StateFlags.HELPER.value:
                m_black = Movement(pieceType, i, j) # Inicializar directamente con valores
                if isValidMove(board, m_black):
                    moves += 1
    print("Moves: ", moves, "Piece: ", pieceType)
    return moves



def canMove(board, pieceType:PlayerType):
    return getNumberOfMoves(board, pieceType) > 0

def copyBoard(board:Board):
    tmp = copy.deepcopy(board)
    return tmp

def nextTurn(board:Board):
    if not isGameOver(board):
        next_turn = PlayerType.WHITE_PLAYER.value if board.lastPiecetypeMoved == PlayerType.BLACK_PLAYER.value else PlayerType.BLACK_PLAYER.value
        if board.noOfMovesFoward <= 0:
            if canMove(board, next_turn):
                return next_turn
            else:
                return board.lastPiecetypeMoved
        else:
            if board.player1.isHuman and next_turn == PlayerType.BLACK_PLAYER.value:
                return PlayerType.BLACK_PLAYER.value
            if board.player2.isHuman and next_turn == PlayerType.WHITE_PLAYER.value:
                return PlayerType.WHITE_PLAYER.value
            return PlayerType.NONE.value
    else:
        return PlayerType.NONE.value

def MinimaxSolver(depth, alpha, beta, board1, move_eval, player):
    global nodes
    nodes += 1

    makeMove(board1, move_eval)
    if depth == 0:
        return getPointEvaluator(board1, move_eval.pieceType)
    elif isGameOver(board1):
        return getScore(board1, move_eval.pieceType)

    max_turn = move_eval.pieceType == player

    opponent = PlayerType.WHITE_PLAYER if move_eval.pieceType == PlayerType.BLACK_PLAYER else PlayerType.BLACK_PLAYER

    if (max_turn and not canMove(board1, PlayerType.WHITE_PLAYER)) or (not max_turn and not canMove(board1, opponent)):
        return MinimaxSolver(depth - 1, alpha, beta, board1, move_eval, player)

    board = copy.deepcopy(board1)
    total_score = 0

    if max_turn:
        total_score = -sys.maxsize
        all_moves = getAllPossibleMoves(board, PlayerType.WHITE_PLAYER)
        number_of_moves = getNumberOfMoves(board, PlayerType.WHITE_PLAYER)
        for i in range(number_of_moves):
            move = all_moves[i]
            score = MinimaxSolver(depth - 1, alpha, beta, board, move, player)
            total_score = fmax(total_score, score)
            alpha = fmax(alpha, score)
            if beta <= alpha:
                break
    else:
        total_score = sys.maxsize
        all_moves = getAllPossibleMoves(board, PlayerType.BLACK_PLAYER)
        number_of_moves = getNumberOfMoves(board, PlayerType.BLACK_PLAYER)
        for i in range(number_of_moves):
            move = all_moves[i]
            score = MinimaxSolver(depth - 1, alpha, beta, board, move, player)
            total_score = fmin(total_score, score)
            beta = fmin(beta, score)
            if beta <= alpha:
                break

    return total_score


def loadGame(data, board_container):
    data_json = json.loads(data)
    size = data_json["board_size"]
    difficulty_list = Difficulty[data_json["game_difficulty"]]
    is_custom = data_json["custom"]
    
    # Crear una instancia de la clase Board sin parámetros
    board = Board()
    initializeGame(board, size, difficulty_list, is_custom, Player(True), Player(True))

    if is_custom:
        initial_board = data_json["initial_board"]
        matrix_6x6 = [initial_board[i*size:(i+1)*size] for i in range(size)]
        for i in range(size):
            for j in range(size):
                board.initialState[i][j].pieceType = matrix_6x6[i][j]["piece_type"]
                print(board.initialState[i][j].pieceType)
        custom_b = setCustomBoardState(board)
        printBoard(custom_b)

    for move in data_json["movements"]:
        pieceType = move["piece_type"]
        x = move["x"]
        y = move["y"]
        m = Movement(pieceType, x, y)
        makeRealMove(board, m)
    printBoard(board)

    board_container[0] = board  # Actualizar la referencia al objeto board
    return board
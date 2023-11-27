from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *
from engine_utils.can_go_back import *
from engine_utils.can_go_forward import *
from engine_utils.clean_helpers import *
from engine_utils.destruct_board import *
from engine_utils.get_point_evaluator import *
from engine_utils.get_score_position import *
from engine_utils.get_score import *
from engine_utils.get_winner import *
from engine_utils.init_board import *
from engine_utils.is_valid_move import *
from engine_utils.print_board import *
from engine_utils.remove_history_forward import *
from engine_utils.set_custom_board_state import *


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
    initializeBoard(board)
    return
    # Después de initializeBoard(board)


def computerMove(board, player):
    random.seed(time.time())
    cleanHelpers(board)
    difficulty = board.difficulty
    if difficulty == Difficulty.EASY:
        makeRealMove(board, randomMovement(board, player))
    elif difficulty == Difficulty.INTERMEDIATE:
        makeRealMove(board, bestMove(board, player))
    elif difficulty == Difficulty.HARD:
        makeRealMove(board, bestMinimaxMove(board, player))

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

def bestMove(board, player):
    bestScore = 0
    x = 0
    y = 0

    allMoves = getAllPossibleMoves(board, player)
    for i in range(getNumberOfMoves(board, player)):
        tmp = copyBoard(board)

        m = Movement()
        m.pieceType = player
        m.x = allMoves[i].x
        m.y = allMoves[i].y

        makeMove(tmp, m)
        if getScore(tmp, player) - getScore(board, player) > bestScore:
            bestScore = getScore(tmp, player) - getScore(board, player)
            x = m.x
            y = m.y

        destructBoard(tmp)
    m = Movement()
    m.pieceType = player
    m.x = x
    m.y = y

    return m

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

def randomMovement(board, player):
    possibleMoves = getNumberOfMoves(board, player)
    moves = getAllPossibleMoves(board, player)
    move = Movement()
    if possibleMoves > 0:
        move = moves[random.randint(0, possibleMoves - 1)]
    # moves = realloc(moves, 0) - No es necesario en Python
    return move

def getAllPossibleMoves(board, pieceType):
    possibleMoves = 0
    moves = [Movement()]
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == 0 or board.state[i][j].pieceType == 3:
                m = Movement(pieceType, i, j)
                if isValidMove(board, m):
                    moves.append(m)
                    possibleMoves += 1
    return moves

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



def goBack(board:Board):
    if canGoBack(board):
        m = board.historyBack[:-1]
        board_tmp = None
        if board.custom:
            board_tmp = copyBoard(board)
        board.historyForward.append(board.historyBack[-1])
        board.noOfMovesFoward += 1
        moves = board.noOfMovesBack
        initializeBoard(board)
        if board_tmp and board_tmp.custom:
            for i, row in enumerate(board.initialState):
                for j, cell in enumerate(row):
                    board.initialState[i][j].pieceType = board_tmp.initialState[i][j].pieceType
            setCustomBoardState(board)
            destructBoard(board_tmp)
        board.historyBack = board.historyBack[:-1]
        board.noOfMovesBack = 0
        for move in m:
            makeRealMove(board, move)

def goForward(board:Board):
    if canGoFoward(board):
        m = board.historyForward[:-1]
        board.historyBack += [board.historyForward[-1]]
        board.noOfMovesFoward -= 1
        movesForward = board.noOfMovesFoward
        moves = board.noOfMovesBack + 1
        historyRebuild = board.historyBack
        boardTmp = None
        if board.custom:
            boardTmp = copyBoard(board)
        initializeBoard(board)
        if boardTmp is not None and boardTmp.custom:
            for i in range(board.size):
                for j in range(board.size):
                    board.initialState[i][j].pieceType = boardTmp.initialState[i][j].pieceType
            setCustomBoardState(board)
            destructBoard(boardTmp)
        board.historyForward = m
        board.noOfMovesBack = 0
        for move in historyRebuild:
            makeRealMove(board, move)



def makeRealMove(board: Board, lastMove: Movement):
    if (
        lastMove is not None
        and 0 <= lastMove.x < board.size
        and 0 <= lastMove.y < board.size
        and lastMove.pieceType in {PlayerType.BLACK_PLAYER.value, PlayerType.WHITE_PLAYER.value}
    ):
        board.lastPiecetypeMoved = lastMove.pieceType
        board.historyBack.append(lastMove)
        board.noOfMovesBack += 1
        makeMove(board, lastMove)


def makeMove(board: Board, lastMove: Movement):
    opponent = PlayerType.BLACK_PLAYER.value if lastMove.pieceType == PlayerType.WHITE_PLAYER.value else PlayerType.WHITE_PLAYER.value

    tmp = copyBoard(board)

    tmp.state[lastMove.x][lastMove.y].pieceType = lastMove.pieceType

    # Función para realizar un movimiento en una dirección
    def make_move_direction(board, lastMove, row_dir, col_dir):
        moves = []
        x = lastMove.x + row_dir
        y = lastMove.y + col_dir

        while x >= 0 and x < board.size and y >= 0 and y < board.size and board.state[x][y].pieceType == opponent:
            moves.append(Movement(lastMove.pieceType, x, y))
            x += row_dir
            y += col_dir

        if x >= 0 and x < board.size and y >= 0 and y < board.size and board.state[x][y].pieceType == lastMove.pieceType and len(moves) > 0:
            for move in moves:
                tmp.state[move.x][move.y].pieceType = lastMove.pieceType

    make_move_direction(tmp, lastMove, -1, 0)  # move up
    make_move_direction(tmp, lastMove, 1, 0)   # move down
    make_move_direction(tmp, lastMove, 0, -1)  # move left
    make_move_direction(tmp, lastMove, 0, 1)   # move right
    make_move_direction(tmp, lastMove, -1, -1)  # move up left
    make_move_direction(tmp, lastMove, -1, 1)   # move up right
    make_move_direction(tmp, lastMove, 1, -1)   # move down left
    make_move_direction(tmp, lastMove, 1, 1)    # move down right

    for k in range(board.size):
        for l in range(board.size):
            board.state[k][l].pieceType = tmp.state[k][l].pieceType

    destructBoard(tmp)




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

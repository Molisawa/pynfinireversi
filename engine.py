from enum import Enum
import random
import time
import sys
import json


class PlayerType(Enum):
    BLACK_PLAYER = 1
    WHITE_PLAYER = 2
    NONE = 6

class StateFlags(Enum):
    VOID = 0
    BLACK_PIECE = PlayerType.BLACK_PLAYER
    WHITE_PIECE = PlayerType.WHITE_PLAYER
    HELPER = 3

class Winners(Enum):
    WINNER = 0
    LOSER = 1
    TIE = 2

class Difficulty(Enum):
    EASY = 0
    INTERMEDIATE = 1
    HARD = 2

class Piece:
    def __init__(self, pieceType):
        self.pieceType = pieceType

class Movement:
    def __init__(self, pieceType, x, y):
        self.pieceType = pieceType
        self.x = x
        self.y = y

class Player:
    def __init__(self, isHuman):
        self.isHuman = isHuman

class Board:
    def __init__(self):
        self.state = None
        self.difficulty = None
        self.historyBack = None
        self.historyForward = None
        self.noOfMovesBack = None
        self.lastPiecetypeMoved = None
        self.noOfMovesFoward = None
        self.initialized = None
        self.size = 8
        self.custom = None
        self.initialState = None
        self.player1 = None
        self.player2 = None

def setDefaultInitialBoardState(board):
    pass

def setCustomBoardState(board):
    pass

def initializeGame(board, size, difficulty, custom, player1, player2):
    pass

def initializeBoard(board):
    pass

def getNumberOfMoves(board, pieceType):
    pass

def getPointEvaluator(board, pieceType):
    pass

def getScorePosition(board, pieceType):
    pass

def getAllPossibleMoves(board, pieceType):
    pass

def goBack(board):
    pass

def goForward(board):
    pass

def canGoBack(board):
    pass

def canGoFoward(board):
    pass

def nextTurn(board):
    pass

def endGame():
    pass

def saveGame(board):
    pass

def loadGame(filename):
    pass

def isValidMove(board, lastMove):
    pass

def isGameOver(board):
    pass

def getWinner(board):
    pass

def SetHelpers(board, player):
    pass

def cleanHelpers(board):
    pass

def makeMove(board, lastMove):
    pass

def makeRealMove(board, lastMove):
    pass

def removeHistoryFoward(board):
    pass

def randomMovement(board, player):
    pass

def copyBoard(board):
    pass

def destructBoard(board):
    pass

def MinimaxSolver(depth, alpha, beta, board, move, player):
    pass

def bestMinimaxMove(board, player):
    pass

def computerMove(board, player):
    pass

def canMove(board, pieceType):
    pass

def bestMove(board, player):
    pass

def canSkipBlackPiece(board):
    pass

def getScore(board, pieceType):
    pass


def initializeGame(board, size, difficulty, custom, player1, player2):
    board.initialized = 1
    board.difficulty = difficulty
    board.noOfMovesBack = 0
    board.historyBack = [Movement()]
    board.noOfMovesFoward = 0
    board.historyForward = [Movement()]
    board.size = 8
    board.custom = custom
    board.player1 = player1
    board.player2 = player2
    initializeBoard(board)

def getPointEvaluator(board, pieceType):
    return getScorePosition(board, pieceType)

def getScorePosition(board, pieceType):
    valores = [[0 for _ in range(board.size)] for _ in range(board.size)]

    for i in range(board.size):
        valores[i] = [0 for _ in range(board.size)]

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

    for i in range(1, 3):
        value = i % 2
        isNegative = -1 if value else 1
        tmp = (100 // (value + 1) * isNegative)
        valores[value][value] = (100 // (value + 1) * isNegative)
        valores[board.size - 1 - value][value] = (100 // (value + 1) * isNegative)
        valores[value][board.size - 1 - value] = (100 // (value + 1) * isNegative)
        valores[board.size - 1 - value][board.size - value - 1] = (100 // (value + 1) * isNegative)

    score = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == pieceType:
                score += valores[i][j]

    for i in range(board.size):
        del valores[i]
    del valores
    return score

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

def initializeBoard(board):
    board.lastPiecetypeMoved = "WHITE_PLAYER"

    board.state = [[Piece() for _ in range(board.size)] for _ in range(board.size)]
    for i in range(board.size):
        for j in range(board.size):
            board.state[i][j].pieceType = "VOID"

    board.initialState = [[Piece() for _ in range(board.size)] for _ in range(board.size)]
    for i in range(board.size):
        for j in range(board.size):
            board.initialState[i][j].pieceType = "VOID"

    board.state[board.size // 2 - 1][board.size // 2 - 1].pieceType = "WHITE_PIECE"
    board.state[board.size // 2][board.size // 2].pieceType = "WHITE_PIECE"
    board.state[board.size // 2 - 1][board.size // 2].pieceType = "BLACK_PIECE"
    board.state[board.size // 2][board.size // 2 - 1].pieceType = "BLACK_PIECE"

    board.initialState[board.size // 2 - 1][board.size // 2 - 1].pieceType = "WHITE_PIECE"
    board.initialState[board.size // 2][board.size // 2].pieceType = "WHITE_PIECE"
    board.initialState[board.size // 2 - 1][board.size // 2].pieceType = "BLACK_PIECE"
    board.initialState[board.size // 2][board.size // 2 - 1].pieceType = "BLACK_PIECE"

def setCustomBoardState(board):
    for k in range(board.size):
        for l in range(board.size):
            board.state[k][l].pieceType = board.initialState[k][l].pieceType

def isGameOver(board):
    return not canMove(board, "BLACK_PLAYER") and not canMove(board, "WHITE_PLAYER")

def getWinner(board):
    white_moves = 0
    black_moves = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == "WHITE_PLAYER":
                white_moves += 1
            if board.state[i][j].pieceType == "BLACK_PLAYER":
                black_moves += 1
    if white_moves == black_moves:
        return "TIE"
    if white_moves > black_moves:
        return "LOSER"
    else:
        return "WINNER"

def canGoBack(board):
    return board.noOfMovesBack > 0

def canGoFoward(board):
    return board.noOfMovesFoward > 0

def SetHelpers(board, player):
    possibleMoves = 0
    cleanHelpers(board)
    opponent = "WHITE_PLAYER" if player == "BLACK_PLAYER" else "BLACK_PLAYER"
    if board.lastPiecetypeMoved == player and canMove(board, opponent):
        return
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == "VOID":
                m = Movement()
                m.pieceType = player
                m.x = i
                m.y = j
                if isValidMove(board, m):
                    possibleMoves += 1
                    board.state[i][j].pieceType = "HELPER"

def getScore(board, piece):
    score = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == piece:
                score += 1
    return score

def canSkipBlackPiece(board):
    return not isGameOver(board) and not canMove(board, "BLACK_PLAYER") and board.lastPiecetypeMoved == "WHITE_PLAYER" and board.noOfMovesFoward == 0

def cleanHelpers(board):
    bestScore = 0
    x = 0
    y = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == "HELPER":
                board.state[i][j].pieceType = "VOID"

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

    allMoves = getAllPossibleMoves(board, player)
    bestMove = Movement()
    bestMove.pieceType = "NONE"
    bestMove.x = -1
    bestMove.y = 1
    score = -sys.maxsize
    numberOfMoves = getNumberOfMoves(board, player)

    boards = [Board() for _ in range(numberOfMoves)]
    for i in range(numberOfMoves):
        tmp = copyBoard(board)

        m = Movement()
        m.pieceType = player
        m.x = allMoves[i].x
        m.y = allMoves[i].y

        scoreTemp = MinimaxSolver(5, -sys.maxsize, sys.maxsize, tmp, m, player)
        if scoreTemp > score:
            score = scoreTemp
            bestMove = m
        destructBoard(tmp)

    print("Nodes searched = ", nodes)
    return bestMove

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
            if board.state[i][j].pieceType == "VOID" or board.state[i][j].pieceType == "HELPER":
                m = Movement()
                m.pieceType = pieceType
                m.x = i
                m.y = j
                if isValidMove(board, m):
                    moves.append(m)
                    possibleMoves += 1
    return moves

def getNumberOfMoves(board, pieceType):
    moves = 0
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == "VOID" or board.state[i][j].pieceType == "HELPER":
                m_black = Movement()
                m_black.pieceType = pieceType
                m_black.x = i
                m_black.y = j
                if isValidMove(board, m_black):
                    moves += 1
    return moves

def isValidMove(board, lastMove):
    opponent = "BLACK_PLAYER" if lastMove.pieceType == "WHITE_PLAYER" else "WHITE_PLAYER"

    colIndex = lastMove.x - 1
    rowIndex = lastMove.y
    offset = 0
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

    # when all hopes fade away
    return False

def canMove(board, pieceType):
    return getNumberOfMoves(board, pieceType) > 0

def copyBoard(board):
    tmp = Board()
    initializeGame(tmp, board.size, board.difficulty, board.custom, board.player1, board.player2)

    if board.custom:
        for k in range(board.size):
            for l in range(board.size):
                tmp.initialState[k][l].pieceType = board.initialState[k][l].pieceType
        setCustomBoardState(tmp)
    for k in range(board.size):
        for l in range(board.size):
            tmp.state[k][l].pieceType = board.state[k][l].pieceType
    return tmp

def nextTurn(board):
    if not isGameOver(board):
        next_turn = PlayerType.WHITE_PLAYER if board.lastPiecetypeMoved == PlayerType.BLACK_PLAYER else PlayerType.BLACK_PLAYER
        if board.noOfMovesFoward <= 0:
            if canMove(board, next_turn):
                return next_turn
            else:
                return board.lastPiecetypeMoved
        else:
            if board.player1.isHuman and next_turn == PlayerType.BLACK_PLAYER:
                return PlayerType.BLACK_PLAYER
            if board.player2.isHuman and next_turn == PlayerType.WHITE_PLAYER:
                return PlayerType.WHITE_PLAYER
            return PlayerType.NONE
    else:
        return PlayerType.NONE

def MinimaxSolver(depth, alpha, beta, board1, moveEval, player):
    global nodes
    nodes += 1

    makeMove(board1, moveEval)
    if depth == 0:
        return getPointEvaluator(board1, moveEval.pieceType)
    elif isGameOver(board1):
        return getScore(board1, moveEval.pieceType)

    max = moveEval.pieceType == player

    opponent = PlayerType.BLACK_PLAYER if moveEval.pieceType == PlayerType.WHITE_PLAYER else PlayerType.WHITE_PLAYER

    if (max and not canMove(board1, PlayerType.WHITE_PLAYER)) or (not max and not canMove(board1, opponent)):
        return MinimaxSolver(depth - 1, alpha, beta, board1, moveEval, player)

    board = copyBoard(board1)
    totalScore = 0
    if max:
        totalScore = float('-inf')
        all_moves = getAllPossibleMoves(board, PlayerType.WHITE_PLAYER)
        number_of_moves = getNumberOfMoves(board, PlayerType.WHITE_PLAYER)
        for i in range(number_of_moves):
            move = all_moves[i]
            score = MinimaxSolver(depth - 1, alpha, beta, board, move, player)
            if score > totalScore:
                totalScore = score
            alpha = max(alpha, score)
            if beta <= alpha:
                break
    else:
        totalScore = float('inf')
        all_moves = getAllPossibleMoves(board, PlayerType.BLACK_PLAYER)
        number_of_moves = getNumberOfMoves(board, PlayerType.BLACK_PLAYER)
        for i in range(number_of_moves):
            move = all_moves[i]
            score = MinimaxSolver(depth - 1, alpha, beta, board, move, player)
            if score < totalScore:
                totalScore = score
            beta = min(beta, score)
            if beta <= alpha:
                break
    destructBoard(board)
    return totalScore

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

def goBack(board):
    if canGoBack(board):
        m = board.historyBack[:-1]
        boardTmp = None
        if board.custom:
            boardTmp = copyBoard(board)
        board.historyForward += [board.historyBack[-1]]
        board.noOfMovesFoward += 1
        moves = board.noOfMovesBack
        initializeBoard(board)
        if boardTmp is not None and boardTmp.custom:
            for i in range(board.size):
                for j in range(board.size):
                    board.initialState[i][j].pieceType = boardTmp.initialState[i][j].pieceType
            setCustomBoardState(board)
            destructBoard(boardTmp)
        board.historyBack = board.historyBack[:-1]
        board.noOfMovesBack = 0
        for move in m:
            makeRealMove(board, move)

def goForward(board):
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

def removeHistoryFoward(board):
    board.historyForward = [Movement()]
    board.noOfMovesFoward = 0

def makeRealMove(board, lastMove):
    board.lastPiecetypeMoved = lastMove.pieceType
    if (
        lastMove.x < 0
        or lastMove.x > board.size - 1
        or lastMove.y < 0
        or lastMove.y > board.size - 1
        or not (lastMove.pieceType == PlayerType.BLACK_PLAYER or lastMove.pieceType == PlayerType.WHITE_PLAYER)
    ):
        return
    board.historyBack.append(lastMove)
    board.noOfMovesBack += 1
    makeMove(board, lastMove)

def makeMove(board, lastMove):
    opponent = PlayerType.BLACK_PLAYER if lastMove.pieceType == PlayerType.WHITE_PLAYER else PlayerType.WHITE_PLAYER

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

def saveGame(board):
    data = {
        "board_size": board.size,
        "game_difficulty": board.difficulty,
        "movements": [
            {"piece_type": move.pieceType, "x": move.x, "y": move.y} for move in board.historyBack
        ],
        "custom": board.custom
    }
    if board.custom:
        data["initial_board"] = [
            [{"piece_type": cell.pieceType} for cell in row] for row in board.initialState
        ]
    return json.dumps(data, indent=None)

def loadGame(data):
    data_json = json.loads(data)
    size = data_json["board_size"]
    difficulty = data_json["game_difficulty"]
    is_custom = data_json["custom"]
    board = Board(size, difficulty, is_custom)

    if is_custom:
        initial_board = data_json["initial_board"]
        for i in range(size):
            for j in range(size):
                board.initialState[i][j] = Piece(initial_board[i][j]["piece_type"])
        setCustomBoardState(board)

    for move in data_json["movements"]:
        pieceType = move["piece_type"]
        x = move["x"]
        y = move["y"]
        m = Movement(pieceType, x, y)
        makeRealMove(board, m)

    return board
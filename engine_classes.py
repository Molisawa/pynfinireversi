from enum import Enum
from builtins import max as fmax
from builtins import min as fmin

class PlayerType(Enum):
    BLACK_PLAYER = 1
    WHITE_PLAYER = 2
    NONE = 6

class StateFlags(Enum):
    VOID = 0
    BLACK_PIECE = PlayerType.BLACK_PLAYER.value
    WHITE_PIECE = PlayerType.WHITE_PLAYER.value
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
    def __init__(self, pieceType=None):
        self.pieceType = pieceType

class Movement:
    def __init__(self, pieceType=None, x=None, y=None):
        self.pieceType = pieceType
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0

class Player:
    def __init__(self, isHuman):
        self.isHuman = isHuman

class Board:
    def __init__(self):
        self.size = 6
        self.state = [[Piece() for _ in range(self.size)] for _ in range(self.size)]  # Inicializar con objetos Piece()
        self.difficulty = None
        self.historyBack = []
        self.historyForward = None
        self.noOfMovesBack = 0
        self.lastPiecetypeMoved = None
        self.noOfMovesFoward = 0
        self.initialized = None
        self.custom = False
        self.initialState = [[Piece() for _ in range(self.size)] for _ in range(self.size)]  # Inicializar con objetos Piece()
        self.player1 = None
        self.player2 = None
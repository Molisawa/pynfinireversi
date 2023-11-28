from engine_classes import Piece
from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from pyray import *
from engine import *
from graphic_classes import *

class Board():
    def __init__(self) -> None:

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
    
    def initializeBoard(self) -> None:
        '''
        Funciton to initialize the board states.
        Initially, it restards to zero
        Then, it gives the deffault values for a game with stat
        '''
        self.lastPiecetypeMoved = 2

        self.set_states()
        self.initialize_values()

    def printBoard(self) -> None:
        '''
        This is a simple method to print the board
        '''
        for row in self.state:
            print([piece.pieceType for piece in row])
    
    def setCustomBoardState(self) -> any:
        '''
        This method changes the states within the board grid to the initial states
        '''
        for k in range(self.size):
            for l in range(self.size):
                self.state[k][l].pieceType = self.initialState[k][l].pieceType
        return self

    def DrawBoardGrid(self, screenFeatures: ScreenFeatures) -> None:
        '''
        This function draws the board grid inside the screen by using two loops with an offset
        '''
        for i in range(self.size + 1):
            draw_line_v((int(screenFeatures.squareSize * i), 0), (int(screenFeatures.squareSize * i), int(self.size * screenFeatures.squareSize)), BLACK)

        for i in range(self.size + 1):
            draw_line_v((0, int(screenFeatures.squareSize * i)), (int(self.size * screenFeatures.squareSize), int(screenFeatures.squareSize * i)), BLACK)

        draw_rectangle(int(self.size * screenFeatures.squareSize) + 1, 0, int(screenFeatures.screenWidth - 1), int(screenFeatures.screenHeight), WHITE)
        draw_rectangle(int(self.size * screenFeatures.squareSize) + 1, 0, int(screenFeatures.screenWidth - 1), int(screenFeatures.screenHeight), fade(DARKGREEN, 0.5))

    def __set_states(self) -> None:
        '''
        Reset the states
        '''
        self.state = [[Piece() for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.state[i][j].pieceType = 0

        self.initialState = [[Piece() for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.initialState[i][j].pieceType = 0

    def __initialize_values(self):
        '''
        Initialize with player values
        '''
        self.state[self.size // 2 - 1][self.size // 2 - 1].pieceType = 2
        self.state[self.size // 2][self.size // 2].pieceType = 2
        self.state[self.size // 2 - 1][self.size // 2].pieceType = 1
        self.state[self.size // 2][self.size // 2 - 1].pieceType = 1

        self.initialState[self.size // 2 - 1][self.size // 2 - 1].pieceType = 2
        self.initialState[self.size // 2][self.size // 2].pieceType = 2
        self.initialState[self.size // 2 - 1][self.size // 2].pieceType = 1
        self.initialState[self.size // 2][self.size // 2 - 1].pieceType = 1
    
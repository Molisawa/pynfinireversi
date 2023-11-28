from enum import Enum
import random
import time
import sys
import json
import copy

from board import Board
from engine_classes import Difficulty, Movement, PlayerType
from engine_utils.get_score import getScore

class Player:
    def __init__(self, isHuman):
        self.isHuman = isHuman

    def computerMove(self, board: Board) -> None:
        '''
        This method splits the actions according to the difficulty
        '''
        random.seed(time.time())
        board.cleanHelpers()
        difficulty = board.difficulty
        if difficulty == Difficulty.EASY:
            self.makeRealMove(board, self.randomMovement(board))
        elif difficulty == Difficulty.INTERMEDIATE:
            self.makeRealMove(board, self.bestMove(board))
        elif difficulty == Difficulty.HARD:
            self.makeRealMove(board, self.bestMinimaxMove(board))
    
    def makeRealMove(self, board: Board, lastMove: Movement) -> None:
        '''
        The move starts with an analysis and allows us to make the next move
        '''
        if (
            lastMove is not None
            and 0 <= lastMove.x < board.size
            and 0 <= lastMove.y < board.size
            and lastMove.pieceType in {PlayerType.BLACK_PLAYER.value, PlayerType.WHITE_PLAYER.value}
        ):
            board.lastPiecetypeMoved = lastMove.pieceType
            board.historyBack.append(lastMove)
            board.noOfMovesBack += 1
            self.makeMove(board, lastMove)
    
    def makeMove(self, board: Board, lastMove: Movement) -> None:
        '''
        This is the function that does the real move
        '''
        opponent = PlayerType.BLACK_PLAYER.value if lastMove.pieceType == PlayerType.WHITE_PLAYER.value else PlayerType.WHITE_PLAYER.value

        tmp = board.copyBoard()

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

        tmp.destructBoard()
    
    def __randomMovement(self, board) -> Movement:
        '''
        This is the movement for the easy difficulty
        '''
        possibleMoves = self.getNumberOfMoves(board)
        moves = self.__getAllPossibleMoves(board)
        move = Movement()
        if possibleMoves > 0:
            move = moves[random.randint(0, possibleMoves - 1)]
        # moves = realloc(moves, 0) - No es necesario en Python
        return move
    
    def __bestMove(self, board: Board) -> Movement:
        '''
        This is the method to find the best move for the computer,
        it is mainly used for the medium difficulty
        '''
        bestScore = 0
        x = 0
        y = 0

        allMoves = self.__getAllPossibleMoves(board)
        
        self.__get_best_move(board, allMoves)

        m = Movement()
        m.pieceType = self.isHuman
        m.x = x
        m.y = y

        return m

    def __get_best_move(self, board: Board, allMoves: list) -> None:
        '''
        This cycle goes thorugh all the possible movements and finds the best one
        '''
        for i in range(self.getNumberOfMoves(board)):
            tmp = board.copyBoard()

            m = Movement()
            m.pieceType = self.isHuman
            m.x = allMoves[i].x
            m.y = allMoves[i].y

            self.makeMove(tmp, m)
            if getScore(tmp, self) - getScore(board, self) > bestScore:
                bestScore = getScore(tmp, self) - getScore(board, self)
                x = m.x
                y = m.y

            board.destructBoard(tmp)
    
    def __getAllPossibleMoves(self, board: Board) -> list:
        '''
        Here, we obtain all the possible moves
        '''
        possibleMoves = 0
        moves = [Movement()]
        for i in range(board.size):
            for j in range(board.size):
                if board.state[i][j].pieceType == 0 or board.state[i][j].pieceType == 3:
                    m = Movement(self.isHuman, i, j)
                    if self.isValidMove(board, m):
                        moves.append(m)
                        possibleMoves += 1
        return moves
    
    def isValidMove(self, board:Board, lastMove:Movement) -> bool:
        opponent = PlayerType.BLACK_PLAYER.value if lastMove.pieceType == PlayerType.WHITE_PLAYER.value else PlayerType.WHITE_PLAYER.value
        colIndex = lastMove.x - 1
        rowIndex = lastMove.y
        offset = 0

        if ( self.__vertical_review(board, rowIndex, colIndex, opponent, lastMove, offset) or 
            self.__horizontal_review(board, rowIndex, colIndex, opponent, lastMove, offset) or 
            self.__diagonal_above(board, rowIndex, colIndex, opponent, lastMove, offset) or
            self.__diagonal_below(board, rowIndex, colIndex, opponent, lastMove, offset) ): 
                return True

        # when all hopes fade away
        return False

    def __vertical_review(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int) -> bool:
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

    def __horizontal_review(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int) -> bool:
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

    def __diagonal_above(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int) -> bool:
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

    def __diagonal_below(board: Board, rowIndex: int, colIndex:int, opponent: int, lastMove: Movement, offset: int)->bool:
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

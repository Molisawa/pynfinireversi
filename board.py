from __future__ import annotations
import copy
import json
import random
import sys
import time
from movement import Movement
from piece import Piece
from player import Player
import specs as board_specs
from builtins import max as fmax
from builtins import min as fmin
import copy

class Board():
    '''
    This class handles every visual matter in the game
    '''
    def __init__(self) -> None:
        self.size = board_specs.BOARD_SIZE
        self.no_of_moves_forward = 0
        self.no_of_moves_back = 0
        self.state = [[Piece() for _ in range(self.size)] for _ in range(self.size)]
        self.initialState = [[Piece() for _ in range(self.size)] for _ in range(self.size)]  # Inicializar con objetos Piece()
        self.custome_board = False  
        self.player1 = None
        self.player2 = None
        self.initialized = None
        self.historyForward = None
        self.lastPiecetypeMoved = None
        self.difficulty = None
        self.historyBack = []

    def can_go_forward(self)->bool:
        '''
        This method checks if the board can go forward
        '''
        return self.no_of_moves_forward > 0

    def can_go_back(self)->bool:
        '''
        This method checks if the board can go back
        '''
        return self.no_of_moves_back > 0

    def can_move(self, pieceType:board_specs.PlayerType)->bool:
        self.getNumberOfMoves() > 0

    def get_score(self, player: int)->int:
        '''
        This method gets the score for a given player
        '''
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == player:
                    score += 1
        return score

    def destroy(self)->None:
        '''
        This method destroys the board
        '''
        for i in range(self.size):
            self.state[i] = None

        for i in range(self.size):
            self.initialState[i] = None

        self.state = None
        self.initialState = None
        self.historyBack = None
        self.historyForward = None
        self = None
    
    def save_game(self)->None:
        '''
        This method saves the game
        '''
        data = {
        "board_size": self.size,
        "game_difficulty": self.difficulty.name,
        "movements": [
            {"piece_type": move.pieceType, "x": move.x, "y": move.y} for move in self.historyBack
        ],
        "custom": self.custom
        }

        if self.custom:
            data["initial_board"] = [
                {"piece_type": cell.pieceType} for row in self.initialState for cell in row
            ]
        
        print(data)

        return json.dumps(data)

    def go_back(self)->None:
        ''''This method goes back'''
        if self.can_go_back():
            m = self.historyBack[:-1]
            board_tmp = None
            if self.custom:
                board_tmp = self.__copy_board(self)
            self.historyForward.append(self.historyBack[-1])
            self.noOfMovesFoward += 1
            moves = self.noOfMovesBack
            self.__initalize_board()
            if board_tmp and board_tmp.custom:
                for i, row in enumerate(self.initialState):
                    for j, cell in enumerate(row):
                        self.initialState[i][j].pieceType = board_tmp.initialState[i][j].pieceType
                self.set_custom_board_state()
                board_tmp.destroy()
            self.historyBack = self.historyBack[:-1]
            self.noOfMovesBack = 0
            for move in m:
                self.make_real_move(move)
        
    def go_forward(self)->None:
        ''''This method goes back'''
        if self.can_go_forward():
            m = self.historyBack[:-1]
            self.historyBack += [self.historyForward[-1]]
            self.noOfMovesFoward -= 1
            movesForward = self.noOfMovesFoward
            moves = self.noOfMovesBack + 1
            historyRebuild = self.historyBack
            selfTmp = None
            if self.custom:
                boardTmp = self.__copy_board(self)
            self.initialize_board()
            if boardTmp is not None and boardTmp.custom:
                for i in range(self.size):
                    for j in range(self.size):
                        self.initialState[i][j].pieceType = boardTmp.initialState[i][j].pieceType
                self.set_custom_board_state()
                boardTmp.destroy()
            self.historyForward = m
            self.noOfMovesBack = 0
            for move in historyRebuild:
                self.makeRealMove(move)
    
    def initialize_board(self)->None:
        ''''This method initializes the board'''
        self.lastPiecetypeMoved = 2

        self.state = [[Piece() for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.state[i][j].pieceType = 0

        self.initialState = [[Piece() for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.initialState[i][j].pieceType = 0

        self.__initialize_states()

    def __initialize_states(self):
        ''''This method initializes the states'''
        self.state[self.size // 2 - 1][self.size // 2 - 1].pieceType = 2
        self.state[self.size // 2][self.size // 2].pieceType = 2
        self.state[self.size // 2 - 1][self.size // 2].pieceType = 1
        self.state[self.size // 2][self.size // 2 - 1].pieceType = 1

        self.initialState[self.size // 2 - 1][self.size // 2 - 1].pieceType = 2
        self.initialState[self.size // 2][self.size // 2].pieceType = 2
        self.initialState[self.size // 2 - 1][self.size // 2].pieceType = 1
        self.initialState[self.size // 2][self.size // 2 - 1].pieceType = 1

    def set_custom_board_state(self)->None:
        '''This method sets the custom board state'''
        for k in range(self.size):
            for l in range(self.size):
                self.state[k][l].pieceType = self.initialState[k][l].pieceType
    
    def make_real_move(self, lastMove: Movement)->None:
        '''
        This method makes a real move
        '''
        if (
            lastMove is not None
            and 0 <= lastMove.x < self.size
            and 0 <= lastMove.y < self.size
            and lastMove.pieceType in {board_specs.PlayerType.BLACK_PLAYER.value, board_specs.PlayerType.WHITE_PLAYER.value}
        ):
            self.lastPiecetypeMoved = lastMove.pieceType
            self.historyBack.append(lastMove)
            self.noOfMovesBack += 1
            self.__make_move(lastMove)
    
    # Función para realizar un movimiento en una dirección
    def make_move_direction(self, tmp: Board, lastMove:Movement, row_dir: int, col_dir: int, opponent: any)->None:
        moves = []
        x = lastMove.x + row_dir
        y = lastMove.y + col_dir

        while x >= 0 and x < self.size and y >= 0 and y < self.size and self.state[x][y].pieceType == opponent:
            moves.append(Movement(lastMove.pieceType, x, y))
            x += row_dir
            y += col_dir

        if x >= 0 and x < self.size and y >= 0 and y < self.size and self.state[x][y].pieceType == lastMove.pieceType and len(moves) > 0:
            for move in moves:
                tmp.state[move.x][move.y].pieceType = lastMove.pieceType

    def __make_move(self, lastMove: Movement)->None:
        '''
        This method makes a move
        '''
        opponent = board_specs.PlayerType.BLACK_PLAYER.value if lastMove.pieceType == board_specs.PlayerType.WHITE_PLAYER.value else board_specs.PlayerType.WHITE_PLAYER.value

        tmp = self.__copy_board()

        tmp.state[lastMove.x][lastMove.y].pieceType = lastMove.pieceType

        self.make_move_direction(tmp, lastMove, -1, 0, opponent)  # move up
        self.make_move_direction(tmp, lastMove, 1, 0, opponent)   # move down
        self.make_move_direction(tmp, lastMove, 0, -1, opponent)  # move left
        self.make_move_direction(tmp, lastMove, 0, 1, opponent)   # move right
        self.make_move_direction(tmp, lastMove, -1, -1, opponent)  # move up left
        self.make_move_direction(tmp, lastMove, -1, 1, opponent)   # move up right
        self.make_move_direction(tmp, lastMove, 1, -1, opponent)   # move down left
        self.make_move_direction(tmp, lastMove, 1, 1, opponent)    # move down right

        for k in range(self.size):
            for l in range(self.size):
                self.state[k][l].pieceType = tmp.state[k][l].pieceType
        tmp.destroy()

    def __get_number_of_moves(self, pieceType:board_specs.PlayerType)->int:
        moves = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j].pieceType == board_specs.StateFlags.VOID.value or self.state[i][j].pieceType == board_specs.StateFlags.HELPER.value:
                    m_black = Movement(pieceType, i, j) # Inicializar directamente con valores
                    if self.is_valid_move( m_black):
                        moves += 1
        # print("Moves: ", moves, "Piece: ", pieceType)
        return moves
    
    def __copy_board(self)->any:
        tmp = copy.deepcopy(self)
        return tmp
    
    def next_turn(self)->int:
        '''
        This method returns the next turn
        '''
        if not self.is_game_over():
            next_turn = board_specs.PlayerType.WHITE_PLAYER.value if self.lastPiecetypeMoved == board_specs.PlayerType.BLACK_PLAYER.value else board_specs.PlayerType.BLACK_PLAYER.value
            if self.noOfMovesFoward <= 0:
                if self.canMove(next_turn):
                    return next_turn
                else:
                    return self.lastPiecetypeMoved
            else:
                if self.player1.isHuman and next_turn == board_specs.PlayerType.BLACK_PLAYER.value:
                    return board_specs.PlayerType.BLACK_PLAYER.value
                if self.player2.isHuman and next_turn == board_specs.PlayerType.WHITE_PLAYER.value:
                    return board_specs.PlayerType.WHITE_PLAYER.value
                return board_specs.PlayerType.NONE.value
        else:
            return board_specs.PlayerType.NONE.value
    
    def is_game_over(self)->bool:
        '''
        This method checks if the game is over
        '''
        return not self.can_move(1) and not self.can_move(0)

    def can_move(self, pieceType:board_specs.PlayerType)->bool:
        '''
        This method checks if a piece can move
        '''
        return self.__get_number_of_moves(pieceType) > 0

    def next_turn(self)->board_specs.PlayerType:
        '''This method returns the next turn'''
        if not self.is_game_over():
            next_turn = board_specs.PlayerType.WHITE_PLAYER.value if self.lastPiecetypeMoved == board_specs.PlayerType.BLACK_PLAYER.value else board_specs.PlayerType.BLACK_PLAYER.value
            if self.noOfMovesFoward <= 0:
                if self.can_move(next_turn):
                    return next_turn
                else:
                    return self.lastPiecetypeMoved
            else:
                if self.player1.isHuman and next_turn == board_specs.PlayerType.BLACK_PLAYER.value:
                    return board_specs.PlayerType.BLACK_PLAYER.value
                if self.player2.isHuman and next_turn == board_specs.PlayerType.WHITE_PLAYER.value:
                    return board_specs.PlayerType.WHITE_PLAYER.value
                return board_specs.PlayerType.NONE.value
        else:
            return board_specs.PlayerType.NONE.value
    
    def set_helpers(self, player:board_specs.PlayerType)->None:
        '''
        This method sets the helpers
        '''
        possibleMoves = 0
        self.clean_helpers()
        opponent = 0 if player == 1 else 1
        if self.lastPiecetypeMoved == player and self.can_move(opponent):
            return
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j].pieceType == 0:
                    m = Movement(player, i, j)
                    if self.is_valid_move(m):
                        possibleMoves += 1
                        self.state[i][j].pieceType = 3
        print("Possible moves: ", possibleMoves)
    
    def clean_helpers(self)->None:
        '''
        This method cleans the helpers
        '''
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j].pieceType == 3:
                    self.state[i][j].pieceType = 3
    
    def remove_history_forward(self)->None:
        '''
        This method removes the history
        '''
        self.historyForward = [Movement()]
        self.noOfMovesFoward = 0
        
    def is_valid_move(self, lastMove: Movement)->bool:
        '''This method checks if a move is valid'''	
        opponent = board_specs.PlayerType.BLACK_PLAYER.value if lastMove.pieceType == board_specs.PlayerType.WHITE_PLAYER.value else board_specs.PlayerType.WHITE_PLAYER.value
        colIndex = lastMove.x - 1
        rowIndex = lastMove.y
        offset = 0

        while colIndex > 0 and self.state[colIndex][rowIndex].pieceType == opponent:
            colIndex -= 1
            offset += 1
        if colIndex >= 0 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move down
        colIndex = lastMove.x + 1
        rowIndex = lastMove.y
        offset = 0
        while colIndex < self.size - 1 and self.state[colIndex][rowIndex].pieceType == opponent:
            colIndex += 1
            offset += 1
        if colIndex <= self.size - 1 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move left
        colIndex = lastMove.x
        rowIndex = lastMove.y - 1
        offset = 0
        while rowIndex > 0 and self.state[colIndex][rowIndex].pieceType == opponent:
            rowIndex -= 1
            offset += 1
        if rowIndex >= 0 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move right
        colIndex = lastMove.x
        rowIndex = lastMove.y + 1
        offset = 0
        while rowIndex < self.size - 1 and self.state[colIndex][rowIndex].pieceType == opponent:
            rowIndex += 1
            offset += 1
        if rowIndex <= self.size - 1 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move up left
        colIndex = lastMove.x - 1
        rowIndex = lastMove.y - 1
        offset = 0
        while colIndex > 0 and rowIndex > 0 and self.state[colIndex][rowIndex].pieceType == opponent:
            colIndex -= 1
            rowIndex -= 1
            offset += 1
        if colIndex >= 0 and rowIndex >= 0 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move up right
        colIndex = lastMove.x - 1
        rowIndex = lastMove.y + 1
        offset = 0
        while colIndex > 0 and rowIndex < self.size - 1 and self.state[colIndex][rowIndex].pieceType == opponent:
            colIndex -= 1
            rowIndex += 1
            offset += 1
        if colIndex >= 0 and rowIndex <= self.size - 1 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move down left
        colIndex = lastMove.x + 1
        rowIndex = lastMove.y - 1
        offset = 0
        while colIndex < self.size - 1 and rowIndex > 0 and self.state[colIndex][rowIndex].pieceType == opponent:
            colIndex += 1
            rowIndex -= 1
            offset += 1
        if colIndex <= self.size - 1 and rowIndex >= 0 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # move down right
        colIndex = lastMove.x + 1
        rowIndex = lastMove.y + 1
        offset = 0
        while colIndex < self.size - 1 and rowIndex < self.size - 1 and self.state[colIndex][rowIndex].pieceType == opponent:
            colIndex += 1
            rowIndex += 1
            offset += 1
        if colIndex <= self.size - 1 and rowIndex <= self.size - 1 and self.state[colIndex][rowIndex].pieceType == lastMove.pieceType and offset > 0:
            return True

        # when all hopes fade away
        return False
    
    def computer_move(self, player: Player)->None:
        '''This method makes a computer move'''
        random.seed(time.time())
        self.clean_helpers()
        difficulty = self.difficulty
        if difficulty == board_specs.Difficulty.EASY:
            self.make_real_move(self.random_movement(player))
        elif difficulty == board_specs.Difficulty.INTERMEDIATE:
            self.make_real_move(self.best_move(player))
        elif difficulty == board_specs.Difficulty.HARD:
            self.make_real_move(self.best_min_max_movement(player))
    
    def random_movement(self, player: Player)->Movement:
        '''
        This method gets a random movement
        '''
        possibleMoves = self.__get_number_of_moves(player)
        print("Possible moves: ", possibleMoves)
        moves = self.get_all_possible_movements(player)
        move = Movement()
        if possibleMoves > 0:
            move = moves[random.randint(0, possibleMoves - 1)]
        return move
    
    def get_all_possible_movements(self, pieceType: Piece)->None:
        '''
        This method gets all the possible moves
        '''
        possibleMoves = 0
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j].pieceType == 0 or self.state[i][j].pieceType == 3:
                    m = Movement(pieceType, i, j)
                    if self.is_valid_move(m):
                        moves.append(m)
                        possibleMoves += 1
        return moves
    
    def best_move(self, player: Player) -> Movement:
        '''This method gets the best move'''
        bestScore = 0
        x = 0
        y = 0
        allMoves = self.get_all_possible_movements(player)
        for i in range(self.__get_number_of_moves(player)):
            tmp = self.__copy_board()

            m = Movement()
            m.pieceType = player
            m.x = allMoves[i].x
            m.y = allMoves[i].y

            tmp.__make_move(m)
            if tmp.get_score(player) - self.get_score( player) > bestScore: # Diferencia de posible score entre el tablero actual y el temporal para ver cual es mejor
                bestScore = tmp.get_score(player) - tmp.get_score(player)
                x = m.x
                y = m.y

            tmp.destroy()
        m = Movement()
        m.pieceType = player
        m.x = x
        m.y = y

        return m
        
    
    def get_score(self, piece:Piece)->int:
        '''
        This method gets the score
        '''
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j].pieceType == piece:
                    score += 1
        return score
    
    def best_min_max_movement(self, player: Player)->Movement:
        '''This method gets the best minimax move'''
        global nodes
        nodes = 0

        all_moves = self.get_all_possible_movements(player)
        best_move = Movement(pieceType=board_specs.PlayerType.NONE, x=-1, y=1)
        score = -sys.maxsize
        number_of_moves = self.__get_number_of_moves(player)

        clone = copy.deepcopy(self)

        boards = [clone for _ in range(number_of_moves)]
        for i in range(number_of_moves):
            tmp = copy.deepcopy(self)
            print(tmp)

            m = Movement(pieceType=player, x=all_moves[i].x, y=all_moves[i].y)

            score_temp = self.min_max_solver(5, -sys.maxsize, sys.maxsize, tmp, m, player)
            if score_temp > score:
                score = score_temp
                best_move = m
        return best_move

    def min_max_solver(self, depth, alpha, beta, board1, move_eval, player) -> int:
        '''This method solves the minimax'''
        global nodes
        nodes += 1

        board1.__make_move(move_eval)
        if depth == 0:
            return self.get_point_evaluator(board1, move_eval.pieceType)
        elif board1.is_game_over():
            return board1.get_score(move_eval.pieceType)

        max_turn = move_eval.pieceType == player

        opponent = board_specs.PlayerType.WHITE_PLAYER if move_eval.pieceType == board_specs.PlayerType.BLACK_PLAYER else board_specs.PlayerType.BLACK_PLAYER

        if (max_turn and not board1.can_move(board_specs.PlayerType.WHITE_PLAYER)) or (not max_turn and not board1.can_move(opponent)):
            return self.min_max_solver(depth - 1, alpha, beta, board1, move_eval, player)

        board = board1.deepcopy()
        total_score = 0

        if max_turn:
            total_score = -sys.maxsize
            all_moves = self.get_all_possible_movements(board_specs.PlayerType.WHITE_PLAYER)
            number_of_moves = self.__get_number_of_moves(board_specs.PlayerType.WHITE_PLAYER)
            for i in range(number_of_moves):
                move = all_moves[i]
                score = self.min_max_solver(depth - 1, alpha, beta, board, move, player)
                total_score = fmax(total_score, score)
                alpha = fmax(alpha, score)
                if beta <= alpha:
                    break
        else:
            total_score = sys.maxsize
            all_moves = self.get_all_possible_movements(board_specs.PlayerType.BLACK_PLAYER)
            number_of_moves = self.__get_number_of_moves(board_specs.PlayerType.BLACK_PLAYER)
            for i in range(number_of_moves):
                move = all_moves[i]
                score = self.min_max_solver(depth - 1, alpha, beta, board, move, player)
                total_score = fmin(total_score, score)
                beta = fmin(beta, score)
                if beta <= alpha:
                    break

        return total_score

    def get_point_evaluator(self, board:Board, pieceType:Piece) -> int:
        '''This method gets the point evaluator'''	
        return self.get_score_position(board, pieceType)

    def get_score_position(self, board:Board, pieceType:Piece)->int:
        '''This method gets the score position'''	
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
    
    def get_winner(self)->str:
        white_moves = 0
        black_moves = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j].pieceType == 2:
                    white_moves += 1
                if self.state[i][j].pieceType == 1:
                    black_moves += 1
        if white_moves == black_moves:
            return "TIE"
        if white_moves > black_moves:
            return "LOSER"
        else:
            return "WINNER"
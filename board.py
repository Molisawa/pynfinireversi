from piece import Piece
import specs as board_specs

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
    



        
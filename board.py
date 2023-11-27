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
    
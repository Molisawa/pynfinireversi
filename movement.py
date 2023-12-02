class Movement:
    def __init__(self, pieceType=None, x=None, y=None):
        self.pieceType = pieceType
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0
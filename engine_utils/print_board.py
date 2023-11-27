from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def printBoard(board) -> None:
    for row in board.state:
        print([piece.pieceType for piece in row])
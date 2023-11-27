from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def removeHistoryFoward(board) -> None:
    board.historyForward = [Movement()]
    board.noOfMovesFoward = 0
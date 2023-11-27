from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *

def canGoFoward(board:Board) -> bool:
    return board.noOfMovesFoward > 0
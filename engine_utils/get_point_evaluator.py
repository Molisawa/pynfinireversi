from enum import Enum
import random
import time
import sys
import json
import copy
from builtins import max as fmax
from builtins import min as fmin
from engine_classes import *
from engine_utils.get_score_position import *

def getPointEvaluator(board, pieceType)->int:
    return getScorePosition(board, pieceType)
import os
from pyray import *
from engine import *
from graphic_classes import *

def getDirectories():
    path = "saved/"
    dirs = []
    count = 0

    for file in os.listdir(path):
        if file.endswith(".brd"):
            count += 1
            dirs.append(file)
    
    return DirectoryEntry(dirs, count)

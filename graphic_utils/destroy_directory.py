from pyray import *
from engine import *
from graphic_classes import *

def DestroyDirectory(directory: DirectoryEntry):
    for dir in directory.directories:
        del dir
    del directory.directories

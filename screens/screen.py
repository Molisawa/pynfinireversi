from pyray import *
from Menu import Menu
from filename import Filename
from piece import Piece
import specs as screen_specs
from board import Board
from abc import ABC
import os

# Mediator interface
class ScreenMediatorInterface(ABC):
    '''This class is an interface for the screen mediator'''	
    def notify(self, event):
        pass

# Mediator
class Screen(ScreenMediatorInterface):
    '''
    This class handles every section of the screen and allows us to draw all the graphic elements.
    It contains the board.
    '''
    def __init__(self, board:Board, frame_count: int, menu_options: Menu, 
                 screen_flag: bool, slider: screen_specs.Slider, selected_piece: Piece,
                 filename: Filename, num_of_chars: int, clicked: bool, mouse: tuple, custom_board_size: int,
                 difficulty: screen_specs.Difficulty) -> None:
        '''
        This constructor asks for the following:
        1. A board to base the draw on
        '''
        self.screen_width = screen_specs.SCREEN_WIDTH
        self.screen_height = screen_specs.SCREEN_HEIGHT
        self.square_size = self.screen_height / board.size
        self.board = board
        self.menu_options = menu_options
        self.frame_count = frame_count
        self.screen_flag = screen_flag
        self.screen_to_show = screen_specs.MAIN_SCREEN
        self.slider = slider
        self.piece = selected_piece
        self.filename = filename
        self.num_of_chars = num_of_chars
        self.clicked = clicked
        self.mouse = mouse
        self.custom_board_size = custom_board_size
        self.difficulty = difficulty
        self.creating_new_board = False
        self.__initalize_components()
        
    def notify(self, mouse: tuple, clicked: bool, filename: str, num_of_chars: int)->None:
        ''' This method notifies the screen to draw'''
        self.mouse = mouse
        self.clicked = clicked
        self.filename = filename
        self.num_of_chars = num_of_chars
        if self.screen_to_show == screen_specs.MAIN_SCREEN:
            self.__componentMainScreen.display_screen()
        elif self.screen_to_show == screen_specs.GAME_SCREEN:
            self.__componentGameScreen.display_screen()
        elif self.screen_to_show == screen_specs.LOAD_SCREEN:
            self.__componentLoadScreen.display_screen()
        elif self.screen_to_show == screen_specs.EDITOR_SCREEN:
            self.__componentEditorScreen.display_screen()
        elif self.screen_to_show == screen_specs.SAVE_SCREEN:
            self.__componentFileSaver.display_screen()
        elif self.screen_to_show == screen_specs.CONFIG_SCREEN:
            self.__componentConfigScreen.display_screen()
        elif self.screen_to_show == screen_specs.LOAD_FILE_SCREEN:
            self.__componentLoadFileScreen.display_screen()
            
    def __initalize_components(self)->None:
        '''This method initializes the components'''
        import main_screen, game_screen, load_screen, editor_screen, file_saver, config_screen, load_file_screen
        self.__componentMainScreen = main_screen.MainScreenComponent(self)
        self.__componentGameScreen = game_screen.GameScreenComponent(self, self.board, self.menu_options)
        self.__componentLoadScreen = load_screen.LoadScreenComponent(self, self.board, self.menu_options, self.slider)
        self.__componentEditorScreen = editor_screen.EditorScreenComponent(self, self.board, self.piece)
        self.__componentFileSaver = file_saver.FileSaverScreenComponent(self, self.board, self.menu_options, self.filename, 
                                                                        self.frame_count, self.num_of_chars)
        self.__componentConfigScreen = config_screen.ConfigScreenComponent(self, self.board, self.custom_board_size, self.difficulty,
                                                                           self.clicked, self.mouse)
        self.__componentLoadFileScreen = load_file_screen.FileLoadScreenComponent(self, self.board, self.slider)

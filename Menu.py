from pyray import *
from board import Board
import specs as screen_specs
class Menu():
    def __init__(self, board: Board)->None:
        # basic buttons
        self.go_back_button = None
        self.go_forward_button = None
        self.save_game_button = None
        # Screen specs calculations
        self.busy_screen = screen_specs.BUSY_SCREEN_BASE + screen_specs.SCREEN_HEIGHT * screen_specs.TEN_PERCENT_DECIMAL
        self.free_screen = screen_specs.SCREEN_HEIGHT - self.busy_screen
        self.number = (screen_specs.SCREEN_WIDTH - screen_specs.OFFSET_750)/4
        # Action buttons
        self.start_game_button = None
        self.load_game_button = None
        self.editor_button = None
        self.board = board
        # Constants translation
        self.square_size = screen_specs.SCREEN_HEIGHT / self.board.size
        self.screen_width = screen_specs.SCREEN_WIDTH
        self.screen_height = screen_specs.SCREEN_HEIGHT
        # Executions
        self.__get_menu()
        self.__get_menu_options()


    def __get_menu(self) -> None:
        '''
        This method creates the three main menu buttons
        '''
        self.go_back_button = Rectangle(self.board.size * self.square_size + screen_specs.BUTTON_INITIAL_X, screen_specs.BUTTON_INITIAL_Y,
                               self.screen_width - self.board.size * self.square_size - screen_specs.BUTTON_WIDTH_REDUCTION, screen_specs.BUTTON_HEIGHT)

        self.go_forward_button = Rectangle(self.go_back_button.x, self.go_back_button.height + self.go_back_button.y + screen_specs.BUTTON_X_OFFSET,
                                    self.screen_width - self.board.size * self.square_size - screen_specs.BUTTON_WIDTH_REDUCTION, screen_specs.BUTTON_HEIGHT)
        
        self.save_game_button = Rectangle(self.go_forward_button.x, self.go_forward_button.height + self.go_forward_button.y + screen_specs.BUTTON_X_OFFSET,
                                    self.screen_width - self.board.size * self.square_size - screen_specs.BUTTON_WIDTH_REDUCTION, screen_specs.BUTTON_HEIGHT)
    
    def __get_menu_options(self)->None:
        '''
        This method creates the action buttons
        '''
        self.start_game_button = Rectangle(self.number, self.busy_screen + screen_specs.BUTTON_ACTION_Y_OFFSET, 
                                    screen_specs.BUTTON_ACTION_WIDTH, self.free_screen - screen_specs.BUTTON_ACTION_FREE_SCREEN_OFFSET)
        self.load_game_button = Rectangle(self.number + self.start_game_button.x + self.start_game_button.width, self.busy_screen + screen_specs.BUTTON_ACTION_Y_OFFSET, 
                                   screen_specs.BUTTON_ACTION_WIDTH, self.free_screen - screen_specs.BUTTON_ACTION_FREE_SCREEN_OFFSET)
        self.editor_button = Rectangle(self.number + self.load_game_button.x + self.load_game_button.width, self.busy_screen + screen_specs.BUTTON_ACTION_Y_OFFSET, 
                                 screen_specs.BUTTON_ACTION_WIDTH, self.free_screen - screen_specs.BUTTON_ACTION_FREE_SCREEN_OFFSET)
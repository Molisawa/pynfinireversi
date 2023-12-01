from __future__ import annotations
import sys

from piece import Piece
sys.path.append('./screens')
from pyray import *
from Menu import Menu
from board import Board
from screens.screen import Screen
import specs as screen_specs

class Game():
    '''
    This is the main class for the Game itself.
    All the basic setup happens here.
    '''
    def __init__(self) -> None:
        '''
        Constructor for the game. The game itself contains a board, players and a series of other components
        '''
        # Music definition and play
        self.music = None
        self.board = Board()
        self.frame_counter = 0
        self.mouse = None
        self.clicked = False
        self.key = 0
        #########################
        self.num_of_chars = 0
        self.filename = ""
        self.difficulty = screen_specs.Difficulty.EASY.value
        self.custom_board_size = 0
        #########################
        self.key_pressed_reference = 8
        self.screen_mediator = None
        self.menu_options = None
        self.slider = screen_specs.Slider(False, 0.0, 0.0)
        self.selected_piece = Piece(screen_specs.PlayerType.BLACK_PLAYER.value)

    def __start_music(self)->None:
        '''
        Method to start the music track
        '''
        init_audio_device()
        self.music = load_music_stream("./resources/background.mp3")
        play_music_stream(self.music)
    
    def __start_mouse_and_frame_counter(self)->None:
        '''
        This method is in charge of feeding a frame counter value and obtaining the mouse position
        '''
        # Frame counter
        self.frame_counter = (self.frame_counter + 1) % 60
        
        # Mouse data
        self.mouse = get_mouse_position()

        if is_mouse_button_pressed(0):
            self.clicked = True
        else:
            self.clicked = False

    def __start_keys_review(self)->None:
        '''
        Check for cerain keys to change the filename, get any key that is presed and ensure they are in range
        '''
        # Check for key "8" 
        if is_key_pressed(self.key_pressed_reference):
                self.num_of_chars -= 1
                if self.num_of_chars < 0:
                    self.num_of_chars = 0
                self.filename = self.filename[:-1]

        # Get any pressed key
        self.key = get_key_pressed()

        # Ensure the range to change the filename
        if self.key > 0 and 32 <= self.key <= 125 and self.num_of_chars < 10:
            self.num_of_chars += 1
            self.filename += chr(self.key)

    def __start_screen(self)->None:
        '''
        This method is in charge of starting the screen
        '''
        self.__init_slider()
        self.window = init_window(screen_specs.SCREEN_WIDTH, screen_specs.SCREEN_HEIGHT, "Reversi")
        set_target_fps(60)
        self.menu_options = Menu(self.board)
        self.screen_mediator = Screen(self.board, self.frame_counter, 
                                      self.menu_options, True, self.slider, 
                                      self.selected_piece, self.filename,
                                      self.num_of_chars, self.clicked,
                                      self.mouse, self.custom_board_size, 
                                      self.difficulty)

    def __init_slider(self)->None:
        self.slider.collision = False
        self.slider.offset = 0.0
        self.slider.difference = 0.0

    def game_loop(self)->None:
        '''The whole gameloop is defined here'''
        self.__start_music()
        self.__start_screen()
        
        while not window_should_close():
            draw_fps(10, 10)
            # update_music_stream(self.music)
            self.__start_mouse_and_frame_counter()
            self.__start_keys_review()
            
            begin_drawing()
            
            self.screen_mediator.notify(self.mouse, self.clicked, self.filename, self.num_of_chars)
            
            end_drawing()
        
        unload_music_stream(self.music)
        close_audio_device()
        close_window()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
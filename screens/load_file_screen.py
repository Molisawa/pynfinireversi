from __future__ import annotations
import json
import math
from pyray import *
from Menu import Menu
from board import Board
from movement import Movement
from piece import Piece
from player import Player
from screens.screen import Screen
import specs as screen_specs
import os

class FileLoadScreenComponent():
    def __init__(self, screen: Screen, board: Board, slider: screen_specs.Slider) -> None:
        self.board = board
        self.slider = slider
        self.screen = screen
        self.directory = None

    def get_directories(self):
        '''This method gets the directories'''
        path = "saved/"
        dirs = []
        count = 0

        for file in os.listdir(path):
            if file.endswith(".brd"):
                count += 1
                dirs.append(file)
        
        return screen_specs.DirectoryEntry(dirs, count)
    
    def destroy_directory(self):
        '''This method destroys the directory'''
        for dir in self.directories:
            del dir
        del self.directories
    
    def display_screen(self)->None:
        '''This method displays the screen'''
        self.directory = self.get_directories()
        self.__draw()

    def __draw(self):
        self.__draw_background_and_create_elements()
        self.__analyze_bar_and_get_percentage()
        self.__draw_files()
        self.__draw_cancel_button()

    def __draw_background_and_create_elements(self)->None:
        '''This method draws the background of the screen'''
        clear_background(RAYWHITE)
        self.bar = (50 * self.directory.NumberOfDirectories + 10) > (self.screen.screen_height - 80)
        self.bar_size = (
                (self.screen.screen_height - 80) / (50 * self.directory.NumberOfDirectories + 10)) * (self.screen.screen_height - 70)

        self.cancel_rect = Rectangle(25, self.screen.screen_height - 60, self.screen.screen_width - 50, 50)

        self.scroll_rect = Rectangle(self.screen.screen_width - 20,
                                5 +
                                min(max(0, int(self.slider.offset + self.slider.difference)),
                                    self.screen.screen_height - 70 - self.bar_size),
                                15,
                                int(self.bar_size))
    
    def __analyze_bar_and_get_percentage(self)->None:
        '''This method analyzes the bar and gets the percentage'''
        if self.bar:
            draw_rectangle(int(self.screen.screen_width - 20), 5, 15, int(self.cancel_rect.y - 10), fade(LIGHTGRAY, 0.6))

        if self.slider.collision:
            self.slider.offset = int(get_mouse_position().y)
            if not is_mouse_button_down(0):
                self.slider.collision = False

        if check_collision_point_rec(get_mouse_position(), self.scroll_rect) and is_mouse_button_pressed(0):
            self.slider.offset = int(get_mouse_position().y)
            self.slider.difference = int(self.scroll_rect.y - self.slider.offset)
            self.slider.collision = True

        draw_rectangle_rec(self.scroll_rect, GRAY if self.slider.collision else fade(GRAY, 0.65))

        self.percent = (self.scroll_rect.y - 5) / (self.screen.screen_width - 70 - self.bar_size) if self.bar else 0
    
    def __draw_files(self)->None:
        '''This method draws the files'''
        for i in range(self.directory.NumberOfDirectories):
            rec = Rectangle(10, i * 50 + 10 - (((50 * self.directory.NumberOfDirectories + 10) - self.screen.screen_height + 60) * self.percent),
                            int(measure_text(self.directory.directories[i], 20) + 20), 30)
            over = check_collision_point_rec(get_mouse_position(), rec)
            if is_mouse_button_pressed(0) and over:
                board_temp = self.load_game(load_file_text(f"saved/{self.directory.directories[i]}"))
                if board_temp.initialized != 1:
                    self.screen.screen_to_show = screen_specs.GAME_SCREEN
                    self.destroy_directory()
                    return
                self.board = board_temp  # Modificación aquí
                self.screen.square_size = int(self.screen.screen_height / board_temp.size)
                self.screen.screen_to_show = screen_specs.GAME_SCREEN
            draw_rectangle_rec(rec, LIGHTGRAY if over else RAYWHITE)
            draw_text(self.directory.directories[i], 20, int(rec.y + 5), 20, BLACK)
    
    def __draw_cancel_button(self)->None:
        '''This method draws the cancel button'''	
        draw_rectangle(0, int(self.screen.screen_height - 70), self.screen.screen_width, 70, RAYWHITE)
        over = check_collision_point_rec(get_mouse_position(), self.cancel_rect)
        draw_rectangle_rec(self.cancel_rect, LIGHTGRAY if over else GRAY)
        if over and is_mouse_button_pressed(0):
            self.screen.screen_to_show = screen_specs.MAIN_SCREEN
        draw_text("CANCEL", int(self.screen.screen_width / 2 - measure_text("CANCEL", 30) / 2 + int(self.cancel_rect.x / 2)), int(self.cancel_rect.y + 10), 30, WHITE)
    
    def load_game(self, data,)->Board:
        '''This method loads the game'''	
        data_json = json.loads(data)
        self.size = data_json["board_size"]
        self.difficulty = screen_specs.Difficulty[data_json["game_difficulty"]]
        self.is_custom = data_json["custom"]
        
        # Crear una instancia de la clase Board sin parámetros
        board = Board()
        self.__initialize_game(True, Player(True), Player(True))

        if self.board.custom:
            initial_board = data_json["initial_board"]
            matrix_6x6 = [initial_board[i*self.size:(i+1)*self.size] for i in range(self.size)]
            for i in range(self.board.size):
                for j in range(self.board.size):
                    self.board.initialState[i][j].pieceType = matrix_6x6[i][j]["piece_type"]
            custom_b = self.board.set_custom_board_state()

        for move in data_json["movements"]:
            pieceType = move["piece_type"]
            x = move["x"]
            y = move["y"]
            m = Movement(pieceType, x, y)
            self.board.makeRealMove(m)

        return self.board

    def __initialize_game(self, custom: bool, player1: Player, player2: Player)->None:
        '''This method initializes the game'''
        self.board.initialized = 1
        self.board.difficulty = self.difficulty
        self.board.noOfMovesBack = 0
        self.board.historyBack = []
        self.board.noOfMovesFoward = 0
        self.board.historyForward = []
        self.board.size = self.size
        self.board.custom = custom
        self.board.player1 = player1
        self.board.player2 = player2
        self.board.initialize_board()
        return
    
        

    
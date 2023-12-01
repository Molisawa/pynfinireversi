import math
from pyray import *
from Menu import Menu
from board import Board
from piece import Piece
from player import Player
from screens.screen import Screen
import specs as screen_specs
import os

class ConfigScreenComponent():
    def __init__(self, screen: Screen, board: Board, custom_board_size: int, 
                 difficulty: screen_specs.Difficulty, clicked: bool, mouse: Vector2) -> None:
        self.screen = screen
        self.board = board
        self.custom_board_size = custom_board_size
        self.difficulty = difficulty    
        self.clicked = clicked
        self.mouse = mouse

    def display_screen(self)->None:
        '''This method displays the screen'''
        self.__draw()
    
    def __draw(self) -> int:
        '''This method draws the screen'''
        self.__draw_background_and_calculate()
        self.__draw_sliders_controllers()
        self.__draw_confirmation_buttons()
        self.__draw_difficulties()
        self.__click_handler()
        self.__check_confirmation_buttons()

    def __draw_background_and_calculate(self)->None:
        '''This method draws the background of the screen'''
        clear_background(RAYWHITE)

        draw_text("Chose your board size", int(self.screen.screen_width / 3 - measure_text("Chose your board size", 30) / 2), 
                  int(self.screen.screen_height / 2 - 300), 30, GRAY)
        self.margin = int((2 * (self.screen.screen_width / 3) - 2 * 130) / 3)
        self.sum_rect = Rectangle(self.margin, int(self.screen.screen_height / 2 - 30), 130, 130)
        self.subs_rect = Rectangle(self.margin + self.sum_rect.x + self.sum_rect.width, self.sum_rect.y, self.sum_rect.width, self.sum_rect.height)

        self.mouse = get_mouse_position()
        self.clicked = is_mouse_button_pressed(0)
        self.over_sum = check_collision_point_rec(self.mouse, self.sum_rect)
        self.over_subs = check_collision_point_rec(self.mouse, self.subs_rect)
    
    def __draw_sliders_controllers(self)->None:
        '''This method draws the sliders'''
        draw_rectangle_rec(self.sum_rect, LIGHTGRAY if self.over_sum else RAYWHITE)
        draw_text("+", int(self.sum_rect.x + self.sum_rect.width / 2 - measure_text("+", 70) / 2), int(self.sum_rect.y + self.sum_rect.height / 2 - 35), 70, BLACK)
        draw_rectangle_rec(self.subs_rect, LIGHTGRAY if self.over_subs else RAYWHITE)
        draw_text("-", int(self.subs_rect.x + self.subs_rect.width / 2 - measure_text("-", 70) / 2), int(self.subs_rect.y + self.subs_rect.height / 2 - 35), 70, BLACK)
    
    def __draw_confirmation_buttons(self)->None:
        '''This method draws the confirmation buttons'''
        self.accept_button = Rectangle(int(self.screen.screen_width / 2 - 100), int(self.screen.screen_height / 2 + 120), 200, 80)
        self.cancel_button = Rectangle(int(self.screen.screen_width / 2 - 100), int(self.accept_button.y + self.accept_button.height + 50), self.accept_button.width, self.accept_button.height)

        draw_rectangle_rec(self.accept_button, LIGHTGRAY)
        draw_rectangle_rec(self.cancel_button, LIGHTGRAY)

        draw_text("Accept", int(self.accept_button.x + self.accept_button.width / 2 - measure_text("Accept", 40) / 2), int(self.accept_button.y + self.accept_button.height / 2 - 20), 40, WHITE)
        draw_text("Cancel", int(self.cancel_button.x + self.cancel_button.width / 2 - measure_text("Cancel", 40) / 2), int(self.cancel_button.y + self.cancel_button.height / 2 - 20), 40, WHITE)
    
    def __draw_difficulties(self)->None:
        self.margin_difficulty = int((self.screen.screen_height - 340) / 2)

        self.easy_button = Rectangle(int(self.screen.screen_width * 3 / 4 - (self.screen.screen_width / 3 - 80) / 2), self.margin_difficulty, int(self.screen.screen_width / 3 - 80), 80)
        self.intermediate_button = Rectangle(self.easy_button.x, int(self.easy_button.y + self.easy_button.height + 50), self.easy_button.width, self.easy_button.height)
        self.hard_button = Rectangle(int(self.intermediate_button.x), int(self.intermediate_button.y + self.intermediate_button.height + 50), self.intermediate_button.width, self.intermediate_button.height)
        
        draw_rectangle_rec(self.easy_button, GRAY if self.difficulty == screen_specs.Difficulty.EASY else LIGHTGRAY)
        draw_rectangle_rec(self.intermediate_button, GRAY if self.difficulty == screen_specs.Difficulty.INTERMEDIATE else LIGHTGRAY)
        draw_rectangle_rec(self.hard_button, GRAY if self.difficulty == screen_specs.Difficulty.HARD else LIGHTGRAY)
    
        draw_text("EASY", int(self.easy_button.x + self.easy_button.width / 2 - measure_text("EASY", 20) / 2), int(self.easy_button.y + self.easy_button.height / 2 - 10), 20, WHITE)
        draw_text("INTERMEDIATE", int(self.intermediate_button.x + self.intermediate_button.width / 2 - measure_text("INTERMEDIATE", 20) / 2), int(self.intermediate_button.y + self.intermediate_button.height / 2 - 10), 20, WHITE)
        draw_text("HARD", int(self.hard_button.x + self.hard_button.width / 2 - measure_text("HARD", 20) / 2), int(self.hard_button.y + self.hard_button.height / 2 - 10), 20, WHITE)
    
    def  __click_handler(self)->None:
        '''This method handles the click'''
        self.over_easy = check_collision_point_rec(self.mouse, self.easy_button)
        self.over_intermediate = check_collision_point_rec(self.mouse, self.intermediate_button)
        self.over_hard = check_collision_point_rec(self.mouse, self.hard_button)

        if self.clicked and self.over_easy:
            self.difficulty = screen_specs.Difficulty.EASY
        if self.clicked and self.over_intermediate:
            self.difficulty = screen_specs.Difficulty.INTERMEDIATE
        if self.clicked and self.over_hard:
            self.difficulty = screen_specs.Difficulty.HARD

        if self.over_sum and self.clicked:
            self.custom_board_size += 1 
        if self.over_subs and self.clicked and self.custom_board_size > 0:
            self.custom_board_size -= 1 

        self.size =  6 + 2 * self.custom_board_size
        self.text = str(6 + 2 * self.custom_board_size)
        draw_text(self.text, int(self.screen.screen_width / 3 - measure_text(self.text, 100) / 2), int(self.screen.screen_height / 2 - 180), 100, BLACK)
    
    def __check_confirmation_buttons(self):
        if check_collision_point_rec(self.mouse, self.accept_button) and self.clicked:
            self.__initialize_game(True, Player(True), Player(False))
            self.difficulty = screen_specs.Difficulty.EASY
            self.screen.square_size = int(self.screen.screen_height / self.size)
            if self.screen.creating_new_board:
                self.screen.screen_to_show = screen_specs.EDITOR_SCREEN
            else:
                self.screen.screen_to_show = screen_specs.GAME_SCREEN
            self.screen.creating_new_board = False
        if check_collision_point_rec(self.mouse, self.cancel_button) and self.clicked:
            self.difficulty = screen_specs.Difficulty.EASY
            self.screen.screen_to_show = screen_specs.MAIN_SCREEN

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
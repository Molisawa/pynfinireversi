import math
from pyray import *
from Menu import Menu
from board import Board
from piece import Piece
from screens.screen import Screen
import specs as screen_specs
import os

class FileSaverScreenComponent():
    def __init__(self, screen: Screen, board: Board, menu: Menu, filename: str, frame_counter: int, num_of_chars: int) -> None:
        self.board = board
        self.filename = filename
        self.menu = menu
        self.screen = screen
        self.num_of_chars = num_of_chars
        self.frame_counter = frame_counter
        print(self.filename)

    def display_screen(self)->None:
        '''This method displays the screen'''
        self.__draw()
    
    def __draw(self):
        '''This method draws the screen'''	
        self.__draw_background_and_calculate()
        self.__create_action_rects()
        self.__draw_text_and_background_rectangles()
        self.__do_final_checks()
    
    def __draw_background_and_calculate(self)->None:
        '''This method draws the background of the screen'''
        clear_background(RAYWHITE)

        self.width = max(measure_text(self.screen.filename, 30), measure_text("XXXXXXXX", 30)) + 30

        self.save_width = measure_text("Save", 20) + 20
        self.cancel_width = measure_text("Cancel", 20) + 20
    
    def __create_action_rects(self)->None:
        '''This method creates the action rectangles'''	
        self.save_rect = Rectangle(
            int(self.screen.screen_width / 2 - (self.save_width + self.cancel_width + 40) / 2),
            int(self.screen.screen_height / 2 + 50),
            int(self.save_width),
            30
        )

        self.cancel_rect = Rectangle(
            int(self.save_rect.x + self.save_rect.width + 40),
            int(self.save_rect.y),
            int(self.cancel_width),
            30
        )
    
    def __draw_text_and_background_rectangles(self)->None:
        '''This method draws the text and background rectangles'''
        self.mouse = get_mouse_position()
        self.over_save = check_collision_point_rec(self.mouse, self.save_rect)
        self.over_cancel = check_collision_point_rec(self.mouse, self.cancel_rect)

        draw_rectangle_rec(self.save_rect, LIGHTGRAY if self.over_save else GRAY)
        draw_text("Save", int(self.save_rect.x + 10), int(self.save_rect.y + 5), 20, WHITE)
        draw_rectangle_rec(self.cancel_rect, LIGHTGRAY if self.over_cancel else GRAY)
        draw_text("Cancel", int(self.cancel_rect.x + 10), int(self.save_rect.y + 5), 20, WHITE)

        draw_rectangle_lines(int(screen_specs.SCREEN_WIDTH / 2 - self.width / 2), int(screen_specs.SCREEN_HEIGHT / 2 - 20), int(self.width), 40, BLACK)
        draw_text(self.screen.filename, int(screen_specs.SCREEN_WIDTH / 2 - self.width / 2 + 10), int(screen_specs.SCREEN_HEIGHT / 2 - 15), 30, BLACK)
    
    def __do_final_checks(self)->None:
        '''This method does the final checks'''	
        if (self.frame_counter // 20) % 2 == 0:
            draw_text("_", int(screen_specs.SCREEN_WIDTH / 2 - self.width / 2 + measure_text(self.screen.filename, 30) + 10), int(screen_specs.SCREEN_HEIGHT / 2 - 15), 30, BLACK)

        if is_mouse_button_pressed(0) and self.over_save:
            os.makedirs("../saved", exist_ok=True)
            save_file_text(f"saved/{self.screen.filename}.brd", self.board.save_game())
            self.screen.filename = ""
            self.num_of_chars = 0
            self.screen.screen_to_show = screen_specs.MAIN_SCREEN

        if is_mouse_button_pressed(0) and self.over_cancel:
            self.screen.filename = ""
            self.num_of_chars = 0
            self.screen.screen_to_show = screen_specs.MAIN_SCREEN

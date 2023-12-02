from pyray import *
from Menu import Menu
from board import Board
from screens.screen import Screen
import specs as screen_specs
import os

class LoadScreenComponent():
    ''''This class is an interface for the screen mediator'''
    def __init__(self, screen:Screen, board:Board, menu: Menu, slider: screen_specs.Slider) -> None:
        self.screen = screen
        self.board = board
        self.menu = menu
        self.slider = slider
        self.directory = None

    def __get_directories(self)->None:
        path = "saved/"
        dirs = []
        count = 0

        for file in os.listdir(path):
            if file.endswith(".brd"):
                count += 1
                dirs.append(file)
        
        return screen_specs.DirectoryEntry(dirs, count)

    def display_screen(self)->None:
        '''This method displays the screen'''
        self.__draw()
    
    def __draw(self)->None:
        '''This method draws the screen'''	
        self.__draw_background()

    def __draw_background(self)->None:
        '''This method draws the background'''
        clear_background(RAYWHITE)

    def get_buttons_dimensions(self)->None:
        '''This method gets the buttons dimensions'''
        self.directory = self.__get_directories()
        self.bar = (50 * self.NumberOfDirectories + 10) > (self.screen.screen_height - 80)
        self.bar_size = (
                (self.screen.screen_height - 80) / (50 * self.NumberOfDirectories + 10)) * (self.screen.screen_height - 70)

        self.cancel_rect = Rectangle(25, self.screen.screen_heightt - 60, self.screen.screen_width - 50, 50)

        self.scroll_rect = Rectangle(self.screen.screen_width - 20,
                                5 +
                                min(max(0, int(self.slider.offset + self.slider.difference)),
                                    self.screen.screen_height - 70 - self.bar_size),
                                15,
                                int(self.bar_size))
import math
from pyray import *
from Menu import Menu
from board import Board
from piece import Piece
from screens.screen import Screen
import specs as screen_specs
import os

class EditorScreenComponent():
    def __init__(self, screen: Screen, board: Board, piece: Piece) -> None:
        self.screen = screen
        self.board = board
        self.piece = piece
        self.is_black = piece.pieceType == screen_specs.PlayerType.BLACK_PLAYER.value

    def display_screen(self)->None:
        '''This method displays the screen'''
        self.__draw()
    
    def __draw(self):
        self.__draw_background()
        self.__calculate_measures()
        self.__draw_initial_pieces()
        self.__check_for_drawing()
        self.__draw_final_rectangles()
        self.__check_final_user_inputs()

    def __draw_background(self)->None:
        '''This method draws the background of the screen'''
        clear_background(DARKGREEN)
        self.__draw_board_grid()

    def __draw_board_grid(self)->None:
        '''This method draws the board grid'''
        # Horizontal lines
        for i in range(self.board.size + 1):
            draw_line_v((int(self.screen.square_size * i), 0), (int(self.screen.square_size * i), int(self.board.size * self.screen.square_size)), BLACK)

        # Vertical lines
        for i in range(self.board.size + 1):
            draw_line_v((0, int(self.screen.square_size * i)), (int(self.board.size * self.screen.square_size), int(self.screen.square_size * i)), BLACK)

        # Points and pieces selection
        draw_rectangle(int(self.board.size * self.screen.square_size) + 1, 0, int(self.screen.screen_width - 1), int(self.screen.screen_height), WHITE) # Right rectangles
        draw_rectangle(int(self.board.size * self.screen.square_size) + 1, 0, int(self.screen.screen_width - 1), int(self.screen.screen_height), fade(DARKGREEN, 0.5))
    
    def __calculate_measures(self)->None:
        self.margin = self.board.size * self.screen.square_size
        self.free_space = self.screen.screen_width- self.margin
        self.radius = self.free_space / 4
        self.black = Vector2(2 * self.radius + self.margin, 50 + self.radius)
        self.white = Vector2(self.black.x, 50 + self.black.y + 2 * self.radius)
    
    def __draw_initial_pieces(self)->None:
        '''This method draws the initial pieces'''
        draw_circle_v(self.black, self.radius, BLACK)
        draw_circle_v(self.white, self.radius, WHITE)
        is_black = self.piece.pieceType == screen_specs.PlayerType.BLACK_PLAYER.value
        draw_circle_v(self.black if is_black else self.white, self.radius // 10, RED)

        self.mouse = get_mouse_position()
        self.clicked = is_mouse_button_pressed(0)

        self.__update_drawing_state()
    
    def __update_drawing_state(self)->None:
        self.offset = int((self.screen.square_size / 2 - 5) * 0.25)

        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.state[i][j].pieceType == screen_specs.StateFlags.BLACK_PIECE.value: # Black piece drawing
                    self.__draw_black_pieces(i, j)
                elif self.board.state[i][j].pieceType == screen_specs.StateFlags.WHITE_PIECE.value: # White piece drawing
                    self.__draw_white_pieces(i, j)
                elif self.board.state[i][j].pieceType == screen_specs.StateFlags.HELPER.value: # Helper piece drawing
                    self.__draw_helper_pieces(i, j)
    
    def __draw_black_pieces(self, i: int, j: int)->None:
        '''This method draws the black pieces'''
        draw_circle(int(i * self.screen.square_size + self.screen.square_size / 2),
                int(j * self.screen.square_size + self.screen.square_size / 2),
                int(self.screen.square_size / 2 - 5), BLACK)
        draw_circle_gradient(int(i * self.screen.square_size + self.screen.square_size / 2 - self.offset),
                            int(j * self.screen.square_size + self.screen.square_size / 2 - self.offset),
                            int((self.screen.square_size / 2 - 5) * 0.5), fade(WHITE, 0.15), fade(WHITE, 0))
    
    def __draw_white_pieces(self, i: int, j: int)->None:
        '''This method draws the white pieces'''
        draw_circle(int(i * self.screen.square_size + self.screen.square_size / 2),
                int(j * self.screen.square_size + self.screen.square_size / 2),
                int(self.screen.square_size / 2 - 5), RAYWHITE)
        draw_circle_gradient(int(i * self.screen.square_size + self.screen.square_size / 2 - self.offset),
                            int(j * self.screen.square_size + self.screen.square_size / 2 - self.offset),
                            int((self.screen.square_size / 2 - 5) * 0.5), fade(BLACK, 0.15), fade(BLACK, 0))
    
    def __draw_helper_pieces(self, i: int, j: int)->None:
        '''This method draws the helper pieces'''
        draw_circle(int(i * self.screen.square_size + self.screen.square_size / 2),
                            int(j * self.screen.square_size + self.screen.square_size / 2),
                            int(self.screen.square_size / 2 - 5), DARKGRAY)
        draw_circle(int(i * self.screen.square_size + self.screen.square_size / 2),
                int(j * self.screen.square_size + self.screen.square_size / 2),
                int(self.screen.square_size / 2 - 7), DARKGREEN)
        
    
    def __check_for_drawing(self)->None:
        '''This method checks for drawing'''	
        if 0 <= self.mouse.x < self.margin and 0 <= self.mouse.x < self.screen.screen_height:
            self.__get_caulculated_data()
            draw_rectangle_rec(self.helper_rect, DARKGREEN)
            self.__draw_pieces()
            self.__draw_colliding_pieces()

    def __get_caulculated_data(self)->None:
        '''This method gets the calculated date'''	
        self.clicked = is_mouse_button_down(0)
        self.x = math.floor(self.mouse.x / self.screen.square_size)
        self.y = math.floor(self.mouse.y / self.screen.square_size)
        self.helper = Vector2(self.x * self.screen.square_size + self.radius, self.y * self.screen.square_size + self.radius)

        self.helper_rect = Rectangle(self.helper.x + 1 - self.radius, self.helper.y + 1 - self.radius, self.screen.square_size - 2, self.screen.square_size - 2)

        self.circle = Vector2(self.x * self.screen.square_size + self.screen.square_size / 2, self.y * self.screen.square_size + self.screen.square_size / 2)

    def __draw_pieces(self)->None:
        '''This method draws the pieces'''
        if self.piece == screen_specs.PlayerType.BLACK_PLAYER.value:
            draw_circle_v(self.circle, self.screen.square_size / 2 - 5, fade(BLACK, 0.5))
        elif self.piece == screen_specs.PlayerType.WHITE_PLAYER.value:
            draw_circle_v(self.circle, self.screen.square_size / 2 - 5, fade(WHITE, 0.5))

    def __draw_colliding_pieces(self)->None:
        '''This method draws the colliding pieces'''	
        if check_collision_point_rec(self.mouse, self.helper_rect) and self.clicked:
            self.board.state[self.x][self.y].piece = screen_specs.PlayerType.BLACK_PLAYER.value if self.is_black else screen_specs.PlayerType.WHITE_PLAYER.value
            self.board.initialState[self.x][self.y].piece = screen_specs.PlayerType.BLACK_PLAYER.value if self.is_black else screen_specs.PlayerType.WHITE_PLAYER.value

        if check_collision_point_rec(self.mouse, self.helper_rect) and (is_mouse_button_pressed(1) or is_mouse_button_down(1)):
            self.board.state[self.x][self.y].piece = screen_specs.StateFlags.VOID.value
            self.board.initialState[self.x][self.y].piece = screen_specs.StateFlags.VOID.value
    
    def __draw_final_rectangles(self)->None:
        self.exit_rect = Rectangle(int(self.margin + 30), int(self.screen.screen_height - 150), int((self.free_space - 60)), 100)
        draw_rectangle_rec(self.exit_rect, LIGHTGRAY)
        draw_text("Exit", int(self.exit_rect.x + self.exit_rect.width / 2 - measure_text("Exit", 30) / 2), int(self.exit_rect.y + self.exit_rect.height / 2 - 15), 30, WHITE)

        self.save_rect = Rectangle(int(self.margin + 30), int(self.exit_rect.y - self.exit_rect.height - 50), int((self.free_space - 60)), 100)
        draw_rectangle_rec(self.save_rect, LIGHTGRAY)
        draw_text("Save", int(self.save_rect.x + self.save_rect.width / 2 - measure_text("Save", 30) / 2), int(self.save_rect.y + self.save_rect.height / 2 - 15), 30, WHITE)
    
    def __check_final_user_inputs(self)->None:
        '''This method checks for the final user inputs'''
        if self.clicked and check_collision_point_circle(self.mouse, self.black, self.radius):
            self.piece.pieceType = screen_specs.PlayerType.BLACK_PLAYER.value
        if self.clicked and check_collision_point_circle(self.mouse, self.white, self.radius):
            self.piece.pieceType = screen_specs.PlayerType.WHITE_PLAYER.value

        if self.clicked and check_collision_point_rec(self.mouse, self.save_rect):
            #screen_list[0] = screen_specs.ScreenFlag.SAVE
            pass
        if self.clicked and check_collision_point_rec(self.mouse, self.exit_rect):
            del self.board
            self.screen.screen_to_show = screen_specs.MAIN_SCREEN
    
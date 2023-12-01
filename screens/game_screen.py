from pyray import *
from Menu import Menu
from board import Board
from movement import Movement
from screens.screen import Screen
import specs as screen_specs

class GameScreenComponent():
    def __init__(self, screen:Screen, board:Board, menu: Menu) -> None:
        self.screen = screen
        self.board = board
        self.menu = menu


    def display_screen(self)->None:
        '''This method displays the screen'''
        self.__draw()
    
    def __draw(self)->None:
        '''This method draws the screen'''	
        self.__draw_background()
        self.__handle_click()
        self.__draw_scores_text()
        self.check_piece_played()
        self.__check_game_over()
        self.__draw_exit_button()

    def __draw_background(self)->None:
        '''This method draws the background'''
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

        
    def __handle_click(self)->None:
        '''This method handles the click'''
        if self.screen.clicked:
            self.screen.mouse = get_mouse_position()
            self.__check_button_pressed()
        self.__update_drawing_state()
        if self.board.next_turn() == screen_specs.PlayerType.BLACK_PLAYER.value:
            self.board.set_helpers(screen_specs.PlayerType.BLACK_PLAYER.value)
            self.check_piece_played()
        elif self.board.next_turn() == screen_specs.PlayerType.WHITE_PLAYER.value:
            self.board.computer_move(screen_specs.PlayerType.WHITE_PLAYER.value)

    def __check_button_pressed(self)->None:
        '''This method checks if a button was pressed'''	
        if check_collision_point_rec(self.screen.mouse, self.menu.go_back_button):
            self.board.go_back() 
            self.board.go_back()
        elif check_collision_point_rec(self.screen.mouse, self.menu.go_forward_button):
            self.board.go_forward()
        elif check_collision_point_rec(self.screen.mouse, self.menu.save_game_button) and self.screen.clicked:
            self.screen.screen_to_show = screen_specs.SAVE_SCREEN

    def __update_drawing_state(self)->None:
        '''This method updates the drawing state'''	
        self.offset = int((self.screen.square_size / 2 - 5) * 0.25)
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.state[i][j].pieceType == screen_specs.StateFlags.VOID.value:
                    pass
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

    def __draw_scores_text(self)->None:
        draw_text("Your score:", int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 30), 20, WHITE) # Your score text
        val = self.board.get_score(screen_specs.PlayerType.BLACK_PLAYER.value)
        draw_text(str(val), int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 50), 20, WHITE)

        draw_text("CPU score:", int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 100), 20, WHITE) # CPU score text
        val = self.board.get_score(screen_specs.PlayerType.WHITE_PLAYER.value)
        draw_text(str(val), int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 120), 20, WHITE)
    
    def check_piece_played(self)->None:
        for i in range(self.board.size):
            for j in range(self.board.size):
                vector = None
                if self.board.state[i][j].pieceType == screen_specs.StateFlags.HELPER.value:
                    vector = (i * self.screen.square_size + self.screen.square_size / 2,
                            j * self.screen.square_size + self.screen.square_size / 2)
                    if check_collision_point_circle(self.screen.mouse, vector, self.screen.square_size / 2 - 5):
                        if not self.screen.clicked:
                            draw_rectangle(int(i * self.screen.square_size + 1), int(j * self.screen.square_size + 1),
                                        int(self.screen.square_size - 2), int(self.screen.square_size - 2), DARKGREEN)
                            draw_circle(int(i * self.screen.square_size + self.screen.square_size / 2),
                                        int(j * self.screen.square_size + self.screen.square_size / 2),
                                        int(self.screen.square_size / 2 - 5), fade(BLACK, 0.4))
                        else:
                            m = Movement(pieceType=screen_specs.PlayerType.BLACK_PLAYER.value, x=i, y=j)
                            self.board.make_real_move(m)
                            self.board.remove_history_forward()
                            self.__update_drawing_state()

    def __check_game_over(self)->None:
        if self.board.is_game_over():
            draw_text("Game Over", int((self.screen.square_size * self.board.size) / 2 - measure_text("Game Over", 80) / 2),
                    int(self.screen.screen_height / 2 - 40), 80, GRAY)
            text = ""
            color = GRAY
            winner = self.board.get_winner()
            if winner == screen_specs.Winners.WINNER.name:
                text = "You win!"
                color = GREEN
            elif winner == screen_specs.Winners.LOSER.name:
                text = "You lose!"
                color = RED
            elif winner == screen_specs.Winners.TIE.name:
                text = "It's a tie!"
            draw_text(text, int((self.screen.square_size * self.board.size) / 2 - measure_text(text, 60) / 2),
                    int(self.screen.screen_height / 2 - 30 + 80 + 10), 60, color)
    
    def __draw_exit_button(self)->None:
        margin = self.board.size * self.screen.square_size
        free_space = self.screen.screen_width - margin
        exit_rect = Rectangle(int(margin + 30), int(self.screen.screen_height - 150), int((free_space - 60)), 100)
        draw_rectangle_rec(exit_rect, WHITE)
        draw_text("Exit", int(exit_rect.x + exit_rect.width / 2 - measure_text("Exit", 30) / 2), int(exit_rect.y + exit_rect.height / 2 - 15), 30, BLACK)
        if self.screen.clicked and check_collision_point_rec(self.screen.mouse, exit_rect):
            self.screen.screen_to_show = screen_specs.MAIN_SCREEN
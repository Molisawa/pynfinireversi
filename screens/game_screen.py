from pyray import *
from Menu import Menu
from board import Board
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
        self.__draw_white_rectangles()
        self.__draw_text()
        self.__draw_scores_text()

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
    
    def __draw_white_rectangles(self)->None:
        '''This method draws the white rectangles'''	
        draw_rectangle(int(self.menu.go_back_button.x), int(self.menu.go_back_button.y), int(self.menu.go_back_button.width), int(self.menu.go_back_button.height), WHITE) # Go back base rectangle
        draw_rectangle(int(self.menu.go_forward_button.x), int(self.menu.go_forward_button.y), int(self.menu.go_forward_button.width), int(self.menu.go_forward_button.height), WHITE) # Go forward base rectangle
        draw_rectangle(int(self.menu.save_game_button.x), int(self.menu.save_game_button.y), int(self.menu.save_game_button.width), int(self.menu.save_game_button.height), WHITE) # Save game base rectangle
    
    def __draw_text(self)->None:
        draw_text("Go back", int(self.menu.go_back_button.x - measure_text("Go back", 30) / 2 + self.menu.go_back_button.width / 2),
              int(self.menu.go_back_button.y + self.menu.go_back_button.height / 2 - 15), 30, BLACK if self.board.can_go_back() else GRAY) # Go back text
        draw_text("Go foward", int(self.menu.go_forward_button.x - measure_text("Go foward", 30) / 2 + self.menu.go_forward_button.width / 2),
                int(self.menu.go_forward_button.y + self.menu.go_forward_button.height / 2 - 15), 30, BLACK if self.board.can_go_forward() else GRAY) # Go forward text
        draw_text("Save game", int(self.menu.save_game_button.x - measure_text("Save game", 30) / 2 + self.menu.save_game_button.width / 2),
                int(self.menu.save_game_button.y + self.menu.save_game_button.height / 2 - 15), 30, BLACK) # Save game text
        
    def __draw_scores_text(self)->None:
        draw_text("Your score:", int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 30), 20, WHITE) # Your score text
        val = self.board.get_score(screen_specs.PlayerType.BLACK_PLAYER.value)
        draw_text(str(val), int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 50), 20, WHITE)

        draw_text("CPU score:", int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 100), 20, WHITE) # CPU score text
        val = self.board.get_score(screen_specs.PlayerType.WHITE_PLAYER.value)
        draw_text(str(val), int(self.menu.save_game_button.x), int(self.menu.save_game_button.height + self.menu.save_game_button.y + 120), 20, WHITE)
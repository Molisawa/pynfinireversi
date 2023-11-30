from pyray import *
from screen import Screen
import specs as screen_specs

# Main screen component
class MainScreenComponent():
    '''
    This class is an interface for the screen mediator
    '''
    def __init__(self, screen:Screen) -> None:
        '''
        This constructor asks for the following:
        1. A screen to base the draw on
        '''
        self.screen = screen
    
    def display_screen(self)->None:
        '''This method displays the screen'''
        self.__draw()

    def __draw(self):
        '''This method draws the screen'''	
        self.__draw_background()
        self.__draw_buttons_shell()
        self.__draw_buttons_text()
        self.__draw_version_and_credits()
        self.__check_menu_button_pressed()
    
    def __draw_background(self)->None:
        '''
        This method draws the background of the screen
        '''
        clear_background(DARKGREEN)
        draw_text("INFINIREVERSI", 
              int(self.screen.screen_width // 2 - measure_text("INFINIREVERSI", 30) // 2),
              int(self.screen.screen_height // 2 - 375), 30, WHITE)
    
    def __draw_buttons_shell(self)->None:
        '''
        This method draws the buttons shell
        '''
        draw_rectangle_rec(self.screen.menu_options.start_game_button, LIGHTGRAY)
        draw_rectangle_rec(self.screen.menu_options.load_game_button, LIGHTGRAY)
        draw_rectangle_rec(self.screen.menu_options.editor_button, LIGHTGRAY)  

    def __draw_buttons_text(self)->None:
        ''''This method draws the buttons text'''	
        draw_text("Start",
              int(self.screen.menu_options.start_game_button.x + self.screen.menu_options.start_game_button.width // 2 - measure_text("Start", 30) // 2),
              int(self.screen.menu_options.start_game_button.y + self.screen.menu_options.start_game_button.height // 2 - 15), 30, WHITE)
        draw_text("Load game",
                int(self.screen.menu_options.load_game_button.x + self.screen.menu_options.load_game_button.width // 2 - measure_text("Load game", 30) // 2),
                int(self.screen.menu_options.load_game_button.y + self.screen.menu_options.load_game_button.height // 2 - 15), 30, WHITE)

        draw_text("Game editor",
                int(self.screen.menu_options.editor_button.x + self.screen.menu_options.editor_button.width // 2 - measure_text("Game editor", 30) // 2),
                int(self.screen.menu_options.editor_button.y + self.screen.menu_options.editor_button.height // 2 - 15), 30, WHITE) 

    def __draw_version_and_credits(self)->None:
        '''This method draws the version and credits'''
        draw_text("v1.0",
              int(self.screen.screen_width // 2 - measure_text("v1.0", 30) // 2),
              int(self.screen.screen_height // 2 + 375),
              15, WHITE)

        draw_text("Created by OSB",
                int(self.screen.screen_width - measure_text("Created by OSD", 30) // 2),
                int(self.screen.screen_height // 2 + 375),
                15, WHITE) 
    
    def __check_menu_button_pressed(self)->None:
        clicked = is_mouse_button_pressed(0)
        mouse = get_mouse_position()

        if clicked and check_collision_point_rec(mouse, self.screen.menu_options.start_game_button):
            self.screen.screen_to_show = screen_specs.GAME_SCREEN
        elif clicked and check_collision_point_rec(mouse, self.screen.menu_options.load_game_button):
            self.screen.screen_to_show = screen_specs.LOAD_SCREEN
        elif clicked and check_collision_point_rec(mouse, self.screen.menu_options.editor_button):
            self.screen.screen_to_show = screen_specs.EDITOR_SCREEN
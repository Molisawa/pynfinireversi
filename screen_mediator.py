from __future__ import annotations
from abc import ABC
from graphic_classes import ScreenFlag


DEFFAULT_VALUE = 0

class Mediator(ABC):
    '''
    This is the base interafce for the concrete mediators
    '''
    def notify(sender: any, event: int):
        '''
        It is assumed that an integer will be used in this notify method as the message identifier
        '''
        pass

class GraphicsMediator(Mediator):
    '''
    This mediator is used for the graphics rendering according to the case, which can be:
    MENU = 0
    GAME = 1
    SAVE = 2
    LOAD = 3
    EDITOR = 4
    CONFIG_GAME = 5
    '''
    def __init__(self) -> None:
        super().__init__()
        self.graphics_component = graphicsComponent(DEFFAULT_VALUE)

    def notify(self, flag: int) -> str:
        return self.graphics_component.get_action(flag)
        
class graphicsComponent():
    '''
    This component handles the graphics class
    '''
    def __init__(self, flag: int) -> None:
        self.flag = flag

    def get_action(self, new_flag: int) -> str:

        self.flag = new_flag

        if self.flag == ScreenFlag.MENU:
            return '''update_music_stream(music)
            MenuScreen(screen_features, frame_counter, menu_options, screen_list, board_container[0], next_screen_list)'''
        elif self.flag == ScreenFlag.GAME:
            return '''last_screen_list[0] = ScreenFlag.GAME
            PlayScreen(board_container[0], menu, screen_features, screen_list, mouse, clicked)'''
            draw_fps(10, 10)
        elif self.flag == ScreenFlag.SAVE:
            return '''last_screen_list[0] = ScreenFlag.MENU
            flag = ScreenFlag.SAVE
            ShowFileSaverScreen(board_container[0], screen_features, filename, frame_counter, mouse, screen_list, num_of_chars, last_screen_list[0])'''
        elif self.flag == ScreenFlag.LOAD:
            return '''LoadFileScreen(board_container, screen_features, screen_list, slider)'''
        elif self.flag == ScreenFlag.EDITOR:
            return '''last_screen_list[0] = ScreenFlag.EDITOR
            EditorScreen(screen_features, board_container[0], piece_selected, screen_list)'''
        elif self.flag == ScreenFlag.CONFIG_GAME:
            return '''[custom_board_size[0]] = ConfigGameScreen(screen_features, board_container[0], screen_list, [custom_board_size[0]], difficulty_list, next_screen_list)'''
    
from pyray import *
from board import Board
from screens.config_screen import *
from screens.editor_screen import *
from screens.load_file_screen import *
from screens.menu_screen import *
from screens.play_screen import *
from screens.show_file_screen import *

from graphic_utils.destroy_directory import *
from graphic_utils.get_directories import *
from graphic_utils.get_menu import *
from graphic_utils.get_menu_options import *
from graphic_utils.init_slider import *

# Definición de constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Función principal
def main():
    # Inicialización de la música y el tablero
    init_audio_device()
    music = load_music_stream("resources/background.mp3")
    play_music_stream(music)

    board_container = [Board()]  # Lista que contendrá el objeto board

    screen = init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Reversi")
    set_target_fps(60)

    screen_list = [ScreenFlag.MENU]
    next_screen_list = [ScreenFlag.MENU]
    last_screen_list = [ScreenFlag.MENU]

    filename = ""
    num_of_chars = 0
    frame_counter = 0
    difficulty_list = [Difficulty.EASY]
    custom_board_size = [0]

    piece_selected = Piece(StateFlags.BLACK_PIECE.value)
    
    slider = Slider(False, 0.0, 0.0)
    initSlider(slider)

    SQUARE_SIZE = SCREEN_HEIGHT / board_container[0].size

    screen_features = ScreenFeatures(SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE)

    menu = getMenu(board_container[0], screen_features)
    menu_options = getMenuOptions(screen_features)

    while not window_should_close():  
        frame_counter = (frame_counter + 1) % 60
        mouse = get_mouse_position()
        clicked = 0
        key = 0

        if is_mouse_button_pressed(0):
            clicked = 1

        if is_key_pressed(8):
            num_of_chars -= 1
            if num_of_chars < 0:
                num_of_chars = 0
            filename = filename[:-1]

        key = get_key_pressed()

        if key > 0 and 32 <= key <= 125 and num_of_chars < 10:
            num_of_chars += 1
            filename += chr(key)

        begin_drawing()

        if screen_list[0] == ScreenFlag.MENU:
            update_music_stream(music)
            MenuScreen(screen_features, frame_counter, menu_options, screen_list, board_container[0], next_screen_list)
        elif screen_list[0] == ScreenFlag.GAME:
            last_screen_list[0] = ScreenFlag.GAME
            PlayScreen(board_container[0], menu, screen_features, screen_list, mouse, clicked)
            draw_fps(10, 10)
        elif screen_list[0] == ScreenFlag.SAVE:
            last_screen_list[0] = ScreenFlag.MENU
            screen_list[0] = ScreenFlag.SAVE
            ShowFileSaverScreen(board_container[0], screen_features, filename, frame_counter, mouse, screen_list, num_of_chars, last_screen_list[0])
        elif screen_list[0] == ScreenFlag.LOAD:
            LoadFileScreen(board_container, screen_features, screen_list, slider)
        elif screen_list[0] == ScreenFlag.EDITOR:
            last_screen_list[0] = ScreenFlag.EDITOR
            EditorScreen(screen_features, board_container[0], piece_selected, screen_list)
        elif screen_list[0] == ScreenFlag.CONFIG_GAME:
            [custom_board_size[0]] = ConfigGameScreen(screen_features, board_container[0], screen_list, [custom_board_size[0]], difficulty_list, next_screen_list)
        
        end_drawing()

    unload_music_stream(music)
    close_audio_device()
    close_window()

if __name__ == "__main__":
    main()

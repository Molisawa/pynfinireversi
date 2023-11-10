from graphic import *
from pyray import *

# Definición de constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Función principal
def main():
    # Inicialización de la música y el tablero
    init_audio_device()
    music = load_music_stream("resources/background.mp3")
    play_music_stream(music)

    board = Board()  # Tamaño del tablero por defecto

    screen = init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Reversi")
    set_target_fps(60)

    screen_flag = ScreenFlag.MENU
    last_screen = ScreenFlag.MENU
    next_screen = ScreenFlag.MENU
    screen_list = [ScreenFlag.MENU]
    next_screen_list = [ScreenFlag.MENU]
    last_screen_list = [ScreenFlag.MENU]

    filename = ""
    num_of_chars = 0
    frame_counter = 0
    difficulty = Difficulty.EASY
    custom_board_size = 0

    piece_selected = Piece(StateFlags.BLACK_PIECE)

    SQUARE_SIZE = SCREEN_HEIGHT / board.size

    screen_features = ScreenFeatures(SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE)

    menu = getMenu(board, screen_features)
    menu_options = getMenuOptions(screen_features)

    while not window_should_close():  # Detectar botón de cierre de la ventana o tecla ESC
        frame_counter = (frame_counter + 1) % 60
        mouse = get_mouse_position()
        clicked = 0
        if is_mouse_button_pressed(0):
            clicked = 1

        key = get_key_pressed()

        while key > 0:
            if 32 <= key <= 125 and num_of_chars < 10:
                num_of_chars += 1
                filename += chr(key)
            key = get_key_pressed()

        if is_key_pressed(8):
            num_of_chars -= 1
            if num_of_chars < 0:
                num_of_chars = 0
            filename = filename[:-1]

        begin_drawing()
        if screen_list[0] == ScreenFlag.MENU:
            update_music_stream(music)
            MenuScreen(screen_features, frame_counter, menu_options, screen_list, board, next_screen_list)
        elif screen_list[0] == ScreenFlag.GAME:
            last_screen_list[0] = ScreenFlag.GAME
            PlayScreen(board, menu, screen_features, screen_list, mouse, clicked)
            draw_fps(10, 10)
        elif screen_list[0] == ScreenFlag.SAVE:
            screen_list[0], next_screen_list[0] = ShowFileSaverScreen(board, screen_features, filename, frame_counter, mouse, screen_list, num_of_chars, last_screen_list[0])
        elif screen_list[0] == ScreenFlag.LOAD:
            LoadFileScreen(board, screen_features, screen_list)
        elif screen_list[0] == ScreenFlag.EDITOR:
            last_screen_list[0] = ScreenFlag.EDITOR
            EditorScreen(screen_features, board, piece_selected, screen_list)
        elif screen_list[0] == ScreenFlag.CONFIG_GAME:
            ConfigGameScreen(screen_features, board, screen_list, custom_board_size, difficulty, next_screen_list)

        
        
        end_drawing()

    # ... (código adicional aquí)
    unload_music_stream(music)
    close_audio_device()
    close_window()

if __name__ == "__main__":
    main()

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
            print("Mouse clicked at: ", mouse)
            print("Mouse clicked at: ", clicked)

        key = get_key_pressed()
        print(key, "se presionó")

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
        if screen_flag == ScreenFlag.MENU:
            update_music_stream(music)
            MenuScreen(screen_features, frame_counter, menu_options, screen_flag, board, next_screen)
        elif screen_flag == ScreenFlag.GAME:
            last_screen = ScreenFlag.GAME
            PlayScreen(board, menu, screen_features, screen_flag, mouse, clicked)
            draw_fps(10, 10)
        elif screen_flag == ScreenFlag.SAVE:
            ShowFileSaverScreen(board, screen_features, filename, frame_counter, mouse, screen_flag, num_of_chars, last_screen)
        elif screen_flag == ScreenFlag.LOAD:
            LoadFileScreen(board, screen_features, screen_flag)
        elif screen_flag == ScreenFlag.EDITOR:
            last_screen = ScreenFlag.EDITOR
            EditorScreen(screen_features, board, piece_selected, screen_flag)
        elif screen_flag == ScreenFlag.CONFIG_GAME:
            ConfigGameScreen(screen_features, board, screen_flag, custom_board_size, difficulty, next_screen)

        end_drawing()

    # ... (código adicional aquí)
    unload_music_stream(music)
    close_audio_device()
    close_window()

if __name__ == "__main__":
    main()

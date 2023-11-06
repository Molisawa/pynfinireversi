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

    screen_flag = ScreenFlag.MENU
    lastScreen = ScreenFlag.MENU
    nextScreen = ScreenFlag.MENU

    filename = ""
    num_of_chars = 0
    frame_counter = 0
    difficulty = Difficulty.EASY
    custom_board_size = 0

    piece_selected = StateFlags.BLACK_PIECE

    SQUARE_SIZE = SCREEN_HEIGHT / board.size

    screenFeatures = ScreenFeatures(SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE)

    menu = getMenu(board, screenFeatures)
    menu_options = getMenuOptions(screenFeatures)

    while not window_should_close():  # Detect window close button or ESC key
        frame_counter = (frame_counter + 1) % 60
        mouse = get_mouse_position()
        clicked = 0
        if is_mouse_button_pressed(0):
            clicked = 1

        key = get_key_pressed()

        while key > 0:
            if (key >= 32) and (key <= 125) and num_of_chars < 10:
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
            MenuScreen(screenFeatures, frame_counter, menu_options, screen_flag, board, nextScreen)
        elif screen_flag == ScreenFlag.GAME:
            lastScreen = ScreenFlag.GAME
            PlayScreen(board, menu, screenFeatures, screen_flag, mouse, clicked)
            draw_fps(10, 10)
        elif screen_flag == ScreenFlag.SAVE:
            ShowFileSaverScreen(board, screenFeatures, filename, frame_counter, mouse, screen_flag, num_of_chars, lastScreen)
        elif screen_flag == ScreenFlag.LOAD:
            LoadFileScreen(board, screenFeatures, screen_flag)
        elif screen_flag == ScreenFlag.EDITOR:
            lastScreen = ScreenFlag.EDITOR
            EditorScreen(screenFeatures, board, piece_selected, screen_flag)
        elif screen_flag == ScreenFlag.CONFIG_GAME:
            ConfigGameScreen(screenFeatures, board, screen_flag, custom_board_size, difficulty, nextScreen)

        end_drawing()

    # ... (código adicional aquí)
    unload_texture(screen)
    unload_texture(lastScreen)
    unload_texture(nextScreen)
    unload_music_stream(music)
    close_audio_device()
    close_window()

if __name__ == "__main__":
    main()
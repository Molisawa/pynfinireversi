
from pyray import *
from engine import *
from graphic_classes import *
from graphic_utils.check_menu_button_pressed import *

def MenuScreen(ScreenFeatures, frame_count, MenuOptions: MenuOptions, screen_flag, board, nextScreen):
    clear_background(DARKGREEN)
    draw_text("INFINIREVERSI", 
              int(ScreenFeatures.screenWidth // 2 - measure_text("INFINIREVERSI", 30) // 2),
              int(ScreenFeatures.screenHeight // 2 - 375), 30, WHITE)

    # frame = math.floor(frame_count * 0.383)
    # put_zero = frame < 10
    # image_path = "resources/frames/frame_{}{}_delay-0.03s.gif".format("0" if put_zero else "", frame)
    # image = load_image(image_path.encode('utf-8'))
    # texture = load_texture_from_image(image)
    # draw_texture(texture, int(ScreenFeatures.screenWidth / 2 - image.width / 2), int(ScreenFeatures.screenHeight * 0.1), WHITE)
    draw_rectangle_rec(MenuOptions.startGameButton, LIGHTGRAY)
    draw_rectangle_rec(MenuOptions.loadGameButton, LIGHTGRAY)
    draw_rectangle_rec(MenuOptions.editorButton, LIGHTGRAY)

    draw_text("Start",
              int(MenuOptions.startGameButton.x + MenuOptions.startGameButton.width // 2 - measure_text("Start", 30) // 2),
              int(MenuOptions.startGameButton.y + MenuOptions.startGameButton.height // 2 - 15), 30, WHITE)
    draw_text("Load game",
              int(MenuOptions.loadGameButton.x + MenuOptions.loadGameButton.width // 2 - measure_text("Load game", 30) // 2),
              int(MenuOptions.loadGameButton.y + MenuOptions.loadGameButton.height // 2 - 15), 30, WHITE)

    draw_text("Game editor",
              int(MenuOptions.editorButton.x + MenuOptions.editorButton.width // 2 - measure_text("Game editor", 30) // 2),
              int(MenuOptions.editorButton.y + MenuOptions.editorButton.height // 2 - 15), 30, WHITE)

    draw_text("v1.0",
              int(ScreenFeatures.screenWidth // 2 - measure_text("v1.0", 30) // 2),
              int(ScreenFeatures.screenHeight // 2 + 375),
              15, WHITE)

    draw_text("Created by OSB",
              int(ScreenFeatures.screenWidth - measure_text("Created by OSD", 30) // 2),
              int(ScreenFeatures.screenHeight // 2 + 375),
              15, WHITE)

    CheckMenuButtonPressed(MenuOptions, screen_flag, board, nextScreen)

    # No descargues la textura y la imagen aquí
    # unload_texture(texture)
    # unload_image(image)

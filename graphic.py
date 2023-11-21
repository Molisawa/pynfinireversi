import math
from pyray import *
from engine import *
import os

from dataclasses import dataclass
from typing import List

@dataclass
class Menu:
    goBackButton: Rectangle
    goForwardButton: Rectangle
    saveGameButton: Rectangle

@dataclass
class MenuOptions:
    startGameButton: Rectangle
    loadGameButton: Rectangle
    editorButton: Rectangle

class ScreenFlag(Enum):
    MENU = 0
    GAME = 1
    SAVE = 2
    LOAD = 3
    EDITOR = 4
    CONFIG_GAME = 5

@dataclass
class DirectoryEntry:
    directories: List[str]
    NumberOfDirectories: int

@dataclass
class Slider:
    collision: bool
    difference: float
    offset: float

@dataclass
class ScreenFeatures:
    screenWidth: int
    screenHeight: int
    squareSize: float

def CheckButtonPressed(menu: Menu, board, screen_list, mouse):
    if check_collision_point_rec(mouse, menu.goBackButton):
        goBack(board)
    elif check_collision_point_rec(mouse, menu.goForwardButton):
        goForward(board)
    elif check_collision_point_rec(mouse, menu.saveGameButton):
        screen_list[0] = ScreenFlag.SAVE

def getDirectories():
    path = "saved/"
    dirs = []
    count = 0

    for file in os.listdir(path):
        if file.endswith(".brd"):
            count += 1
            dirs.append(file)
    
    return DirectoryEntry(dirs, count)

def DestroyDirectory(directory: DirectoryEntry):
    for dir in directory.directories:
        del dir
    del directory.directories

def CheckPiecePlayed(board: Board, screenFeatures: ScreenFeatures, clicked, mouse):
    for i in range(board.size):
        for j in range(board.size):
            vector = None
            if board.state[i][j].pieceType == StateFlags.HELPER.value:
                vector = (i * screenFeatures.squareSize + screenFeatures.squareSize / 2,
                          j * screenFeatures.squareSize + screenFeatures.squareSize / 2)
                if check_collision_point_circle(mouse, vector, screenFeatures.squareSize / 2 - 5):
                    if not clicked:
                        draw_rectangle(int(i * screenFeatures.squareSize + 1), int(j * screenFeatures.squareSize + 1),
                                       int(screenFeatures.squareSize - 2), int(screenFeatures.squareSize - 2), DARKGREEN)
                        draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                                    int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                                    int(screenFeatures.squareSize / 2 - 5), fade(BLACK, 0.4))
                    else:
                        m = Movement(pieceType=PlayerType.BLACK_PLAYER.value, x=i, y=j)
                        makeRealMove(board, m)
                        removeHistoryFoward(board)
                        UpdateDrawingState(board, screenFeatures)


def DrawBoardGrid(board: Board, screenFeatures: ScreenFeatures):
    for i in range(board.size + 1):
        draw_line_v((int(screenFeatures.squareSize * i), 0), (int(screenFeatures.squareSize * i), int(board.size * screenFeatures.squareSize)), BLACK)

    for i in range(board.size + 1):
        draw_line_v((0, int(screenFeatures.squareSize * i)), (int(board.size * screenFeatures.squareSize), int(screenFeatures.squareSize * i)), BLACK)

    draw_rectangle(int(board.size * screenFeatures.squareSize) + 1, 0, int(screenFeatures.screenWidth - 1), int(screenFeatures.screenHeight), WHITE)
    draw_rectangle(int(board.size * screenFeatures.squareSize) + 1, 0, int(screenFeatures.screenWidth - 1), int(screenFeatures.screenHeight), fade(DARKGREEN, 0.5))




def PlayScreen(board:Board, menu:Menu, ScreenFeatures:ScreenFeatures, screen_list, mouse, clicked):
    clear_background(DARKGREEN)
    DrawBoardGrid(board, ScreenFeatures)

    draw_rectangle(int(menu.goBackButton.x), int(menu.goBackButton.y), int(menu.goBackButton.width), int(menu.goBackButton.height), WHITE)
    draw_rectangle(int(menu.goForwardButton.x), int(menu.goForwardButton.y), int(menu.goForwardButton.width), int(menu.goForwardButton.height), WHITE)
    draw_rectangle(int(menu.saveGameButton.x), int(menu.saveGameButton.y), int(menu.saveGameButton.width), int(menu.saveGameButton.height), WHITE)

    draw_text("Go back", int(menu.goBackButton.x - measure_text("Go back", 30) / 2 + menu.goBackButton.width / 2),
              int(menu.goBackButton.y + menu.goBackButton.height / 2 - 15), 30, BLACK if canGoBack(board) else GRAY)
    draw_text("Go foward", int(menu.goForwardButton.x - measure_text("Go foward", 30) / 2 + menu.goForwardButton.width / 2),
              int(menu.goForwardButton.y + menu.goForwardButton.height / 2 - 15), 30, BLACK if canGoFoward(board) else GRAY)
    draw_text("Save game", int(menu.saveGameButton.x - measure_text("Save game", 30) / 2 + menu.saveGameButton.width / 2),
              int(menu.saveGameButton.y + menu.saveGameButton.height / 2 - 15), 30, BLACK)
    if clicked:
        CheckButtonPressed(menu, board, screen_list, mouse)
    UpdateDrawingState(board, ScreenFeatures)
    if nextTurn(board) == PlayerType.BLACK_PLAYER.value:
        SetHelpers(board, PlayerType.BLACK_PLAYER.value)
        CheckPiecePlayed(board, ScreenFeatures, clicked, mouse)
    elif nextTurn(board) == PlayerType.WHITE_PLAYER.value:
        computerMove(board, PlayerType.WHITE_PLAYER.value)

    draw_text("Your score:", int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 30), 20, WHITE)
    val = getScore(board, PlayerType.BLACK_PLAYER.value)
    draw_text(str(val), int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 50), 20, WHITE)

    draw_text("CPU score:", int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 100), 20, WHITE)
    val = getScore(board, PlayerType.WHITE_PLAYER.value)
    draw_text(str(val), int(menu.saveGameButton.x), int(menu.saveGameButton.height + menu.saveGameButton.y + 120), 20, WHITE)

    if isGameOver(board):
        draw_text("Game Over", int((ScreenFeatures.squareSize * board.size) / 2 - measure_text("Game Over", 80) / 2),
                  int(ScreenFeatures.screenHeight / 2 - 40), 80, GRAY)
        text = ""
        color = GRAY
        if getWinner(board) == Winners.WINNER.name:
            text = "You win!"
            color = GREEN
        elif getWinner(board) == Winners.LOSER.name:
            text = "You lose!"
            color = RED
        elif getWinner(board) == Winners.TIE.name:
            text = "It's a tie!"
        draw_text(text, int((ScreenFeatures.squareSize * board.size) / 2 - measure_text(text, 60) / 2),
                  int(ScreenFeatures.screenHeight / 2 - 30 + 80 + 10), 60, color)

    margin = board.size * ScreenFeatures.squareSize
    free_space = ScreenFeatures.screenWidth - margin
    exit_rect = Rectangle(int(margin + 30), int(ScreenFeatures.screenHeight - 150), int((free_space - 60)), 100)
    draw_rectangle_rec(exit_rect, WHITE)
    draw_text("Exit", int(exit_rect.x + exit_rect.width / 2 - measure_text("Exit", 30) / 2), int(exit_rect.y + exit_rect.height / 2 - 15), 30, BLACK)
    if clicked and check_collision_point_rec(mouse, exit_rect):
        destructBoard(board)
        screen_list[0] = ScreenFlag.MENU

def ShowFileSaverScreen(board, ScreenFeatures, filename, frame_counter, mouse, screen_list, num_of_chars, last_screen):
    clear_background(RAYWHITE)

    width = max(measure_text(filename, 30), measure_text("XXXXXXXX", 30)) + 30

    save_width = measure_text("Save", 20) + 20
    cancel_width = measure_text("Cancel", 20) + 20

    save_rect = Rectangle(
        int(ScreenFeatures.screenWidth / 2 - (save_width + cancel_width + 40) / 2),
        int(ScreenFeatures.screenHeight / 2 + 50),
        int(save_width),
        30
    )

    cancel_rect = Rectangle(
        int(save_rect.x + save_rect.width + 40),
        int(save_rect.y),
        int(cancel_width),
        30
    )


    over_save = check_collision_point_rec(mouse, save_rect)
    over_cancel = check_collision_point_rec(mouse, cancel_rect)

    draw_rectangle_rec(save_rect, LIGHTGRAY if over_save else GRAY)
    draw_text("Save", int(save_rect.x + 10), int(save_rect.y + 5), 20, WHITE)
    draw_rectangle_rec(cancel_rect, LIGHTGRAY if over_cancel else GRAY)
    draw_text("Cancel", int(cancel_rect.x + 10), int(save_rect.y + 5), 20, WHITE)

    draw_rectangle_lines(int(ScreenFeatures.screenWidth / 2 - width / 2), int(ScreenFeatures.screenHeight / 2 - 20), int(width), 40, BLACK)
    draw_text(filename, int(ScreenFeatures.screenWidth / 2 - width / 2 + 10), int(ScreenFeatures.screenHeight / 2 - 15), 30, BLACK)

    if (frame_counter // 20) % 2 == 0:
        draw_text("_", int(ScreenFeatures.screenWidth / 2 - width / 2 + measure_text(filename, 30) + 10), int(ScreenFeatures.screenHeight / 2 - 15), 30, BLACK)

    if is_mouse_button_pressed(0) and over_save:
        os.makedirs("saved", exist_ok=True)
        save_file_text(f"saved/{filename}.brd", saveGame(board))
        filename = ""
        num_of_chars = 0
        # return screen_list, last_screen  # Return a tuple here
        screen_list[0] = last_screen


    if is_mouse_button_pressed(0) and over_cancel:
        filename = ""
        num_of_chars = 0
        screen_list[0] = last_screen
        # return screen_list, last_screen  # Return a tuple here

    # return screen_list, last_screen

def LoadFileScreen(board: Board, ScreenFeatures: ScreenFeatures, screen_list, slider: Slider):
    directory = getDirectories()
    clear_background(RAYWHITE)
    bar = (50 * directory.NumberOfDirectories + 10) > (ScreenFeatures.screenHeight - 80)
    bar_size = (
            (ScreenFeatures.screenHeight - 80) / (50 * directory.NumberOfDirectories + 10)) * (ScreenFeatures.screenHeight - 70)

    cancel_rect = Rectangle(25, ScreenFeatures.screenHeight - 60, ScreenFeatures.screenWidth - 50, 50)

    scroll_rect = Rectangle(ScreenFeatures.screenWidth - 20,
                            5 +
                            min(max(0, int(slider.offset + slider.difference)),
                                ScreenFeatures.screenHeight - 70 - bar_size),
                            15,
                            int(bar_size))
    if bar:
        draw_rectangle(int(ScreenFeatures.screenWidth - 20), 5, 15, int(cancel_rect.y - 10), fade(LIGHTGRAY, 0.6))

        if slider.collision:
            slider.offset = int(get_mouse_position().y)
            if not is_mouse_button_down(0):
                slider.collision = False

        if check_collision_point_rec(get_mouse_position(), scroll_rect) and is_mouse_button_pressed(0):
            slider.offset = int(get_mouse_position().y)
            slider.difference = int(scroll_rect.y - slider.offset)
            slider.collision = True

        draw_rectangle_rec(scroll_rect, GRAY if slider.collision else fade(GRAY, 0.65))

    percent = (scroll_rect.y - 5) / (ScreenFeatures.screenHeight - 70 - bar_size) if bar else 0

    for i in range(directory.NumberOfDirectories):
        rec = Rectangle(10, i * 50 + 10 - (((50 * directory.NumberOfDirectories + 10) - ScreenFeatures.screenHeight + 60) * percent),
                        int(measure_text(directory.directories[i], 20) + 20), 30)
        over = check_collision_point_rec(get_mouse_position(), rec)
        if is_mouse_button_pressed(0) and over:
            board_temp = loadGame(load_file_text(f"saved/{directory.directories[i]}"))
            if board_temp.initialized != 1:
                screen_list[0] = ScreenFlag.GAME
                DestroyDirectory(directory)
                return
            board = board_temp
            ScreenFeatures.squareSize = int(ScreenFeatures.screenHeight / board.size)
            screen_list[0] = ScreenFlag.GAME
        draw_rectangle_rec(rec, LIGHTGRAY if over else RAYWHITE)
        draw_text(directory.directories[i], 20, int(rec.y + 5), 20, BLACK)

    draw_rectangle(0, int(ScreenFeatures.screenHeight - 70), ScreenFeatures.screenWidth, 70, RAYWHITE)
    over = check_collision_point_rec(get_mouse_position(), cancel_rect)
    draw_rectangle_rec(cancel_rect, LIGHTGRAY if over else GRAY)
    if over and is_mouse_button_pressed(0):
        screen_list[0] = ScreenFlag.MENU
    draw_text("CANCEL", int(ScreenFeatures.screenWidth / 2 - measure_text("CANCEL", 30) / 2 + int(cancel_rect.x / 2)), int(cancel_rect.y + 10), 30, WHITE)

def UpdateDrawingState(board:Board, screenFeatures: ScreenFeatures):

    offset = int((screenFeatures.squareSize / 2 - 5) * 0.25)
    for i in range(board.size):
        for j in range(board.size):
            if board.state[i][j].pieceType == StateFlags.VOID.value:
                pass
            elif board.state[i][j].pieceType == StateFlags.BLACK_PIECE.value:
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 5), BLACK)
                draw_circle_gradient(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int((screenFeatures.squareSize / 2 - 5) * 0.5), fade(WHITE, 0.15), fade(WHITE, 0))
            elif board.state[i][j].pieceType == StateFlags.WHITE_PIECE.value:
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 5), RAYWHITE)
                draw_circle_gradient(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2 - offset),
                                     int((screenFeatures.squareSize / 2 - 5) * 0.5), fade(BLACK, 0.15), fade(BLACK, 0))
            elif board.state[i][j].pieceType == StateFlags.HELPER.value:
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 5), DARKGRAY)
                draw_circle(int(i * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(j * screenFeatures.squareSize + screenFeatures.squareSize / 2),
                           int(screenFeatures.squareSize / 2 - 7), DARKGREEN)
def getMenu(board, ScreenFeatures: ScreenFeatures):
    goBackButton = Rectangle(board.size * ScreenFeatures.squareSize + 20, 30,
                               ScreenFeatures.screenWidth - board.size * ScreenFeatures.squareSize - 40, 75)

    goForwardButton = Rectangle(goBackButton.x, goBackButton.height + goBackButton.y + 10,
                                  ScreenFeatures.screenWidth - board.size * ScreenFeatures.squareSize - 40, 75)
    saveGameButton = Rectangle(goForwardButton.x, goForwardButton.height + goForwardButton.y + 10,
                                 ScreenFeatures.screenWidth - board.size * ScreenFeatures.squareSize - 40, 75)
    return Menu(goBackButton, goForwardButton, saveGameButton)
def getMenuOptions(ScreenFeatures: ScreenFeatures):
    bussy_screen = 400 + ScreenFeatures.screenHeight * 0.1
    free_screen = ScreenFeatures.screenHeight - bussy_screen
    number = (ScreenFeatures.screenWidth - (3 * 250)) / 4
    startGameButton = Rectangle(number, bussy_screen + 100, 250, free_screen - 200)
    loadGameButton = Rectangle(number + startGameButton.x + startGameButton.width, bussy_screen + 100, 250, free_screen - 200)
    editorButton = Rectangle(number + loadGameButton.x + loadGameButton.width, bussy_screen + 100, 250, free_screen - 200)

    return MenuOptions(startGameButton, loadGameButton, editorButton)

def initSlider(slider):
    slider.collision = False
    slider.offset = 0.0
    slider.difference = 0.0

def initScreenFeatures(features, screenWidth, screenHeight, squareSize):
    features.screenWidth = screenWidth
    features.screenHeight = screenHeight
    features.squareSize = squareSize

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

def EditorScreen(screenFeatures: ScreenFeatures, board: Board, piece: Piece, screen_list):
    clear_background(DARKGREEN)
    DrawBoardGrid(board, screenFeatures)
    margin = board.size * screenFeatures.squareSize
    free_space = screenFeatures.screenWidth - margin
    radius = free_space / 4
    black = Vector2(2 * radius + margin, 50 + radius)
    white = Vector2(black.x, 50 + black.y + 2 * radius)
    draw_circle_v(black, radius, BLACK)
    draw_circle_v(white, radius, WHITE)
    is_black = piece.pieceType == PlayerType.BLACK_PLAYER.value
    draw_circle_v(black if is_black else white, radius // 10, RED)

    mouse = get_mouse_position()
    clicked = is_mouse_button_pressed(0)

    UpdateDrawingState(board, screenFeatures)
    if 0 <= mouse.x < margin and 0 <= mouse.x < screenFeatures.screenHeight:
        clicked = is_mouse_button_down(0)
        x = math.floor(mouse.x / screenFeatures.squareSize)
        y = math.floor(mouse.y / screenFeatures.squareSize)
        helper = Vector2(x * screenFeatures.squareSize + radius, y * screenFeatures.squareSize + radius)

        helper_rect = Rectangle(helper.x + 1 - radius, helper.y + 1 - radius, screenFeatures.squareSize - 2, screenFeatures.squareSize - 2)
        draw_rectangle_rec(helper_rect, DARKGREEN)

        circle = Vector2(x * screenFeatures.squareSize + screenFeatures.squareSize / 2, y * screenFeatures.squareSize + screenFeatures.squareSize / 2)

        if piece.pieceType == PlayerType.BLACK_PLAYER.value:
            draw_circle_v(circle, screenFeatures.squareSize / 2 - 5, fade(BLACK, 0.5))
        elif piece.pieceType == PlayerType.WHITE_PLAYER.value:
            draw_circle_v(circle, screenFeatures.squareSize / 2 - 5, fade(WHITE, 0.5))

        if check_collision_point_rec(mouse, helper_rect) and clicked:
            board.state[x][y].pieceType = PlayerType.BLACK_PLAYER.value if is_black else PlayerType.WHITE_PLAYER.value
            board.initialState[x][y].pieceType = PlayerType.BLACK_PLAYER.value if is_black else PlayerType.WHITE_PLAYER.value

        if check_collision_point_rec(mouse, helper_rect) and (is_mouse_button_pressed(1) or is_mouse_button_down(1)):
            board.state[x][y].pieceType = StateFlags.VOID.value
            board.initialState[x][y].pieceType = StateFlags.VOID.value

    exit_rect = Rectangle(int(margin + 30), int(screenFeatures.screenHeight - 150), int((free_space - 60)), 100)
    draw_rectangle_rec(exit_rect, LIGHTGRAY)
    draw_text("Exit", int(exit_rect.x + exit_rect.width / 2 - measure_text("Exit", 30) / 2), int(exit_rect.y + exit_rect.height / 2 - 15), 30, WHITE)

    save_rect = Rectangle(int(margin + 30), int(exit_rect.y - exit_rect.height - 50), int((free_space - 60)), 100)
    draw_rectangle_rec(save_rect, LIGHTGRAY)
    draw_text("Save", int(save_rect.x + save_rect.width / 2 - measure_text("Save", 30) / 2), int(save_rect.y + save_rect.height / 2 - 15), 30, WHITE)

    if clicked and check_collision_point_circle(mouse, black, radius):
        piece.pieceType = PlayerType.BLACK_PLAYER.value
    if clicked and check_collision_point_circle(mouse, white, radius):
        piece.pieceType = PlayerType.WHITE_PLAYER.value

    if clicked and check_collision_point_rec(mouse, save_rect):
        screen_list[0] = ScreenFlag.SAVE

    if clicked and check_collision_point_rec(mouse, exit_rect):
        destructBoard(board)
        screen_list[0] = ScreenFlag.MENU

def CheckMenuButtonPressed(menuOptions: MenuOptions, screen_list, board:Board, next_screen_list):
    clicked = is_mouse_button_pressed(0)
    mouse = get_mouse_position()

    if clicked and check_collision_point_rec(mouse, menuOptions.startGameButton):
        screen_list[0] = ScreenFlag.CONFIG_GAME
        next_screen_list[0] = ScreenFlag.GAME

    if clicked and check_collision_point_rec(mouse, menuOptions.loadGameButton):
        screen_list[0] = ScreenFlag.LOAD

    if clicked and check_collision_point_rec(mouse, menuOptions.editorButton):
        screen_list[0] = ScreenFlag.CONFIG_GAME
        next_screen_list[0] = ScreenFlag.EDITOR
        board.custom = True

    return screen_list[0], next_screen_list[0]

def ConfigGameScreen(ScreenFeatures: ScreenFeatures, board, screen_list, customBoardSize_list, difficulty_list, next_screen_list):
    clear_background(RAYWHITE)

    draw_text("Chose your board size", int(ScreenFeatures.screenWidth / 3 - measure_text("Chose your board size", 30) / 2), int(ScreenFeatures.screenHeight / 2 - 300), 30, GRAY)
    margin = int((2 * (ScreenFeatures.screenWidth / 3) - 2 * 130) / 3)
    sum_rect = Rectangle(margin, int(ScreenFeatures.screenHeight / 2 - 30), 130, 130)
    subs_rect = Rectangle(margin + sum_rect.x + sum_rect.width, sum_rect.y, sum_rect.width, sum_rect.height)

    mouse = get_mouse_position()
    clicked = is_mouse_button_pressed(0)
    over_sum = check_collision_point_rec(mouse, sum_rect)
    over_subs = check_collision_point_rec(mouse, subs_rect)

    draw_rectangle_rec(sum_rect, LIGHTGRAY if over_sum else RAYWHITE)
    draw_text("+", int(sum_rect.x + sum_rect.width / 2 - measure_text("+", 70) / 2), int(sum_rect.y + sum_rect.height / 2 - 35), 70, BLACK)
    draw_rectangle_rec(subs_rect, LIGHTGRAY if over_subs else RAYWHITE)
    draw_text("-", int(subs_rect.x + subs_rect.width / 2 - measure_text("-", 70) / 2), int(subs_rect.y + subs_rect.height / 2 - 35), 70, BLACK)

    accept_button = Rectangle(int(ScreenFeatures.screenWidth / 2 - 100), int(ScreenFeatures.screenHeight / 2 + 120), 200, 80)
    cancel_button = Rectangle(int(ScreenFeatures.screenWidth / 2 - 100), int(accept_button.y + accept_button.height + 50), accept_button.width, accept_button.height)

    draw_rectangle_rec(accept_button, LIGHTGRAY)
    draw_rectangle_rec(cancel_button, LIGHTGRAY)

    draw_text("Accept", int(accept_button.x + accept_button.width / 2 - measure_text("Accept", 40) / 2), int(accept_button.y + accept_button.height / 2 - 20), 40, WHITE)
    draw_text("Cancel", int(cancel_button.x + cancel_button.width / 2 - measure_text("Cancel", 40) / 2), int(cancel_button.y + cancel_button.height / 2 - 20), 40, WHITE)

    margin_difficulty = int((ScreenFeatures.screenHeight - 340) / 2)

    easy_button = Rectangle(int(ScreenFeatures.screenWidth * 3 / 4 - (ScreenFeatures.screenWidth / 3 - 80) / 2), margin_difficulty, int(ScreenFeatures.screenWidth / 3 - 80), 80)
    intermediate_button = Rectangle(easy_button.x, int(easy_button.y + easy_button.height + 50), easy_button.width, easy_button.height)
    hard_button = Rectangle(int(intermediate_button.x), int(intermediate_button.y + intermediate_button.height + 50), intermediate_button.width, intermediate_button.height)

    draw_rectangle_rec(easy_button, GRAY if difficulty_list[0] == Difficulty.EASY else LIGHTGRAY)
    draw_rectangle_rec(intermediate_button, GRAY if difficulty_list[0] == Difficulty.INTERMEDIATE else LIGHTGRAY)
    draw_rectangle_rec(hard_button, GRAY if difficulty_list[0] == Difficulty.HARD else LIGHTGRAY)

    draw_text("EASY", int(easy_button.x + easy_button.width / 2 - measure_text("EASY", 20) / 2), int(easy_button.y + easy_button.height / 2 - 10), 20, WHITE)
    draw_text("INTERMEDIATE", int(intermediate_button.x + intermediate_button.width / 2 - measure_text("INTERMEDIATE", 20) / 2), int(intermediate_button.y + intermediate_button.height / 2 - 10), 20, WHITE)
    draw_text("HARD", int(hard_button.x + hard_button.width / 2 - measure_text("HARD", 20) / 2), int(hard_button.y + hard_button.height / 2 - 10), 20, WHITE)

    over_easy = check_collision_point_rec(mouse, easy_button)
    over_intermediate = check_collision_point_rec(mouse, intermediate_button)
    over_hard = check_collision_point_rec(mouse, hard_button)

    if clicked and over_easy:
        difficulty_list[0] = Difficulty.EASY
    if clicked and over_intermediate:
        difficulty_list[0] = Difficulty.INTERMEDIATE
    if clicked and over_hard:
        difficulty_list[0] = Difficulty.HARD

    if over_sum and clicked:
        customBoardSize_list[0] += 1 
    if over_subs and clicked and customBoardSize_list[0] > 0:
        customBoardSize_list[0] -= 1 

    size =  6 + 2 * customBoardSize_list[0]
    text = str(6 + 2 * customBoardSize_list[0])
    draw_text(text, int(ScreenFeatures.screenWidth / 3 - measure_text(text, 100) / 2), int(ScreenFeatures.screenHeight / 2 - 180), 100, BLACK)

    if check_collision_point_rec(mouse, accept_button) and clicked:
        initializeGame(board, size, difficulty_list[0], True, Player(True), Player(False))
        screen_list[0] = next_screen_list[0]
        difficulty_list[0] = Difficulty.EASY
        ScreenFeatures.squareSize = int(ScreenFeatures.screenHeight / size)
    if check_collision_point_rec(mouse, cancel_button) and clicked:
        screen_list[0] = ScreenFlag.MENU
        difficulty_list[0] = Difficulty.EASY

    return customBoardSize_list

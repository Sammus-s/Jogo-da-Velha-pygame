import pygame
from pygame import gfxdraw
import sys
import numpy as np

pygame.init()

WIDTH, HEIGHT = 600, 600
ICON = pygame.image.load('icon.png')
LINE_WIDTH = 15

RED = (255, 0, 0)
WHITE = (255, 255, 230)
GRAY = (66, 66, 66)
BG_COLOR = (28, 170, 156)  # Background color
LINE_COLOR = (23, 145, 135)

BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = 200
CIRCLE_RADIUS, CIRCLE_WIDTH = 60, 15
CROSS_WIDTH = 25
ESPACEMENT = 55

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
board = np.zeros((BOARD_ROWS, BOARD_COLS))
pygame.display.set_caption('JOGO DA VELHA')
pygame.display.set_icon(ICON)
WIN.fill(BG_COLOR)


def draw_lines():
    pygame.draw.line(WIN, LINE_COLOR, (0, SQUARE_SIZE), (HEIGHT, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(WIN, LINE_COLOR, (0, SQUARE_SIZE * 2), (HEIGHT, SQUARE_SIZE * 2), LINE_WIDTH)  # Vertical Lines

    pygame.draw.line(WIN, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, WIDTH), LINE_WIDTH)  # Horizontal Lines
    pygame.draw.line(WIN, LINE_COLOR, (SQUARE_SIZE * 2, 0), (SQUARE_SIZE * 2, WIDTH), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == -1:
                draw_circle(row, col)
            elif board[row][col] == 1:
                draw_cross(row, col)


def draw_circle(row, col):
    gfxdraw.aacircle(WIN, int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                     CIRCLE_RADIUS,
                     WHITE)
    gfxdraw.filled_circle(WIN, int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                          CIRCLE_RADIUS,
                          WHITE)
    gfxdraw.filled_circle(WIN, int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                          CIRCLE_RADIUS - CIRCLE_WIDTH,
                          BG_COLOR)
    gfxdraw.aacircle(WIN, int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                     int(row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS - CIRCLE_WIDTH,
                     BG_COLOR)


def draw_cross(row, col):
    pygame.draw.line(WIN, GRAY, (col * SQUARE_SIZE + ESPACEMENT, row * SQUARE_SIZE + SQUARE_SIZE - ESPACEMENT),
                     (col * SQUARE_SIZE + SQUARE_SIZE - ESPACEMENT, row * SQUARE_SIZE + ESPACEMENT), CROSS_WIDTH)
    pygame.draw.line(WIN, GRAY, (col * SQUARE_SIZE + ESPACEMENT, row * SQUARE_SIZE + ESPACEMENT),
                     (col * SQUARE_SIZE + SQUARE_SIZE - ESPACEMENT, row * SQUARE_SIZE + SQUARE_SIZE - ESPACEMENT),
                     CROSS_WIDTH)


def mark_square(row, column, player):
    board[row][column] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False

    return True


def check_win(player):
    # vertical
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # asc diagonal
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        draw_asc_winning_line(player)
        return True

    # desc diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_winning_line(player)
        return True

    return False


def draw_vertical_winning_line(col, player):
    pos_x = col * SQUARE_SIZE + SQUARE_SIZE // 2

    if player == 1:
        color = GRAY
    else:
        color = WHITE

    pygame.draw.line(WIN, color, (pos_x, 15), (pos_x, HEIGHT - 15), LINE_WIDTH)


def draw_horizontal_winning_line(row, player):
    pos_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

    if player == 1:
        color = GRAY
    else:
        color = WHITE

    pygame.draw.line(WIN, color, (15, pos_y), (WIDTH - 15, pos_y), LINE_WIDTH)


def draw_asc_winning_line(player):
    if player == 1:
        color = GRAY
    else:
        color = WHITE

    pygame.draw.line(WIN, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)


def draw_desc_winning_line(player):
    if player == 1:
        color = GRAY
    else:
        color = WHITE

    pygame.draw.line(WIN, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)


def restart():
    WIN.fill(BG_COLOR)
    pygame.display.set_caption('JOGO DA VELHA')
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


draw_lines()
player = 1
game_over = False

while True:  # Main Loop
    if game_over or is_board_full():
        pygame.display.set_caption('PRESSIONE "R" PARA RECOMEÇAR')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x = event.pos[0] - 1
            mouse_y = event.pos[1] - 1

            clicked_row = int(mouse_y // SQUARE_SIZE)
            clicked_col = int(mouse_x // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()
                game_over = check_win(player)
                player *= -1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart()
            player = 1
            game_over = False

    pygame.display.update()

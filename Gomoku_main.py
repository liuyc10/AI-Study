import copy
import turtle
from random import choice
from Gomoku import Gomoku, GameState
from Search import alphabeta_cutoff_search, monte_carlo_tree_search
from utils import extend_moves, compute_utility

is_calculating = False
is_finished = False
tl = turtle.Turtle()
screen = turtle.Screen()
delta = 40
h = v = 15
height = h * delta
width = v * delta

ttt = Gomoku()
p_pos = []
c_pos = []
state = copy.deepcopy(ttt.initial)
step_count = 0
'''
def initialize():
    col = row = 15
'''


def get_real_coordinate(a, b):
    x = (a - 1) * delta - width / 2
    y = (b - 1) * delta - height / 2
    return x, y


def get_relative_coordinate(x, y):
    a = int(round((x + width / 2) / delta)) + 1
    b = int(round((y + height / 2) / delta)) + 1
    return a, b


def draw_game_board():
    screen.screensize(height, width)
    screen.bgcolor('gold')
    screen.tracer(50000)
    tl.penup()

    for i in range(1, h + 1):
        tl.setposition(get_real_coordinate(i, 1))
        tl.pendown()
        tl.setposition(get_real_coordinate(i, h))
        tl.penup()
        tl.setposition(get_real_coordinate(1, i))
        tl.pendown()
        tl.setposition(get_real_coordinate(v, i))
        tl.penup()

    x, y = get_real_coordinate(8, 8)
    tl.setposition(x, y - 3)
    tl.pendown()
    tl.begin_fill()
    tl.color('black')
    tl.circle(3)
    tl.end_fill()
    tl.penup()


def draw_stone(a, b, color):
    x, y = get_real_coordinate(a, b)
    tl.setposition(x, y - 17)
    tl.pendown()
    tl.begin_fill()
    tl.color(color)
    tl.circle(17)
    tl.end_fill()
    tl.penup()
    screen.update()


def update_state(move):
    global state
    board = state.board.copy()
    board[move] = state.to_move
    moves = state.moves.copy()
    del moves[move]
    moves = extend_moves(move, moves, True)
    return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                     utility=compute_utility(board, move, state.to_move),
                     board=board, moves=moves)


def print_coor(x, y):
    global is_calculating, ttt, state, step_count, is_finished
    if not is_calculating and not is_finished:
        # print((x, y))
        a, b = get_relative_coordinate(x, y)
        print((a, b))
        if 0 < a < 16 and 0 < b < 16:
            draw_stone(a, b, 'black')
            step_count += 1
            state = update_state((a, b))
            is_finished = ttt.terminal_test(state)
            is_calculating = True
            if step_count < 3:
                (r_a, r_b) = choice(ttt.actions(state))
            else:
                (r_a, r_b) = monte_carlo_tree_search(state, ttt)
            state = update_state((r_a, r_b))
            print(state.board)
            print(state.utility)
            is_finished = ttt.terminal_test(state)
            draw_stone(r_a, r_b, 'white')
            step_count += 1
            is_calculating = False


tl.hideturtle()
draw_game_board()
screen.onscreenclick(print_coor)

turtle.done()

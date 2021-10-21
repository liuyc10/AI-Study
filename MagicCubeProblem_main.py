import random
import turtle
from copy import deepcopy
from datetime import datetime

import numpy as np

from MagicCubeProblem import MagicCubeProblem
from Search import *
from utils import move_reverse

color = ['blue', 'yellow', 'red', 'gray', 'green', 'orange']
delta = 40
h = v = 3
height = 3 * h * delta + 60
width = 4 * v * delta + 40
tl = turtle.Turtle()
screen = turtle.Screen()
tl.hideturtle()
screen.screensize(height, width)
screen.tracer(50000)
tl.penup()


def get_coor_set_l(x, y):
    coor_set = []
    for i in range(3):
        for j in range(3):
            coor_set.append([x - j * 40, y - i * 40])

    return coor_set


def get_coor_set_f(x, y):
    coor_set = []
    for i in range(3):
        for j in range(3):
            coor_set.append([x + j * 40, y - i * 40])

    return coor_set


def get_coor_set_t(x, y):
    coor_set = []
    for i in range(3):
        for j in range(3):
            coor_set.append([x + j * 40, y + i * 40])

    return coor_set


def get_all_coor_set():
    coor_set = []
    coor_set.append(get_coor_set_l(-180, 20))
    coor_set.append(get_coor_set_t(-130, 70))
    coor_set.append(get_coor_set_f(-130, 20))
    coor_set.append(get_coor_set_f(-130, -110))
    coor_set.append(get_coor_set_f(0, 20))
    coor_set.append(get_coor_set_l(210, 20))
    coor = np.array(coor_set).reshape((6, 3, 3, 2))
    print(coor)

    return coor


def squares():
    for i in range(4):  # For each edge of the shape
        tl.forward(40)  # Move forward 40 units
        tl.left(90)  # Turn ready for the next edge


def draw(x, y, color):
    tl.setposition(x, y)
    tl.pendown()
    tl.begin_fill()
    tl.color(color)  # 'black'
    squares()
    tl.end_fill()
    tl.penup()
    screen.update()
    # sleep(0.1)


def draw_num(x, y, cell_num):
    tl.setposition(x + 15, y + 15)
    tl.color('black')  # 'black'
    tl.write(cell_num)
    tl.penup()
    screen.update()


def draw_state(state, coor):
    for surface in range(6):
        for cell_x in range(3):
            for cell_y in range(3):
                cell_num = state[surface, cell_y, cell_x]
                color_index = int(cell_num / 9)
                # color_index = int(cell_num)
                x, y = coor[surface, cell_y, cell_x]
                draw(x, y, color[color_index])
                draw_num(x, y, cell_num)


def print_results(results):
    bi_path = []
    if results is not None:
        path_forward = results[0].solution()
        path_backward = results[1].solution()

        '''print('forward')
        print(path_forward)

        print('backward')
        print(path_backward)
'''
        bi_path.extend(path_forward)
        bi_path.extend(revers_dist[x] for x in reversed(path_backward))
        print('step count:' + str(len(bi_path)))
        print(bi_path)

        print([revers_dist[x] for x in reversed(action_list)])
        print(action_list)


if __name__ == "__main__":
    goal = np.arange(54)

    cor = get_all_coor_set()

    actions = ['ru', 'rd', 'lu', 'ld', 'ff', 'fb', 'bf', 'bb', 'tr', 'tl', 'br', 'bl']
    revers_dist = {'ru': 'rd',
                   'rd': 'ru',
                   'lu': 'ld',
                   'ld': 'lu',
                   'ff': 'fb',
                   'fb': 'ff',
                   'bf': 'bb',
                   'bb': 'bf',
                   'tr': 'tl',
                   'tl': 'tr',
                   'br': 'bl',
                   'bl': 'br'
                   }
    # scramble = []
    i = 15
    for _ in range(4):
        state = np.arange(54)
        initial = MagicCubeProblem(state, goal)
        action_list = []
        for _ in range(i):
            action = random.choice(actions)
            action_list.append(action)
            state = initial.result(state, action)

        initial_state = np.array(state).reshape((6, 3, 3))
        draw_state(initial_state, cor)

        puzzle = MagicCubeProblem(tuple(initial_state.flat), tuple(goal))

        start = datetime.datetime.now()
        result = bidirectional_bread_first_graph_search(puzzle)
        end = datetime.datetime.now()
        print('time cost(' + str(i) + '): ' + str(end - start))
        print('move: ' + str(puzzle.time_cost_move))
        print_results(result)
    # print(results.solution())

'''
    bi_path = []
    if results is not None:
        path_forward = results[0].solution()
        path_backward = results[1].solution()

        print('forward')
        print(path_forward)

        print('backward')
        print(path_backward)

        bi_path.extend(path_forward)
        bi_path.extend(revers_dist[x] for x in reversed(path_backward))
        print(bi_path)
        print(len(bi_path))
        print([revers_dist[x] for x in reversed(action_list)])
        print(action_list)


    turtle.done()

    # draw_state(result.solution())
'''

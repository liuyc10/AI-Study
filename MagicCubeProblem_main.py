import random
import turtle
from copy import deepcopy
from datetime import datetime
from time import sleep

import numpy as np

from MagicCubeProblem import MagicCubeProblem
from MagicCubeProblem_ForDisplay import MagicCubeProblemForDisplay
from Search import *

back = 0
left = 1
front = 2
right = 3
top = 4
bottom = 5

color = ['orange', 'blue', 'red', 'green', 'yellow', 'gray']
delta = 40
h = v = 3
height = (3 * h * delta + 60) * 2
width = (4 * v * delta + 40) * 2
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
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40, y - row * 40])
    return coordinate_list


def get_coordinate_FB(x, y):
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40, y - row * 40])
    return coordinate_list


def get_coordinate_LR(x, y):
    angle = np.pi / 3
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40 * np.sin(angle), y - row * 40 + col * 40 * np.cos(angle)])
    return coordinate_list


def get_coordinate_TB(x, y):
    angle = np.pi / 6
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40 + row * 40 * np.cos(angle), y + row * 40 * np.sin(angle)])
    return coordinate_list


def get_all_coor_set(delta_y):
    coor_set = [get_coordinate_FB(120, 180 + delta_y),
                get_coordinate_LR(-240, 60 + delta_y),
                get_coordinate_FB(-120, 60 + delta_y),
                get_coordinate_LR(0, 60 + delta_y),
                get_coordinate_TB(-120, 60 + delta_y),
                get_coordinate_TB(-120, -130 + delta_y)]
    # coor_set.append(get_coor_set_f(0, -110 + delta_y))
    # coor =
    # print(coor)

    return np.array(coor_set).reshape((6, 3, 3, 2))


def squares(side):
    angle = 60
    if side == front or side == back:
        tl.seth(0)
        for _ in range(4):  # For each edge of the shape
            tl.forward(40)  # Move forward 40 units
            tl.right(90)
    elif side == left or side == right:
        tl.seth(-90)
        a = 180 - angle
        for _ in range(4):
            tl.forward(40)
            tl.left(a)
            a = 180 - a
    elif side == top or side == bottom:
        tl.seth(0)
        a = angle/2
        for _ in range(4):
            tl.forward(40)
            tl.left(a)
            a = 180 - a


def draw(surface, x, y, color):
    tl.setposition(x, y)
    tl.pendown()
    tl.begin_fill()
    tl.color(color)  # 'black'
    squares(surface)
    tl.end_fill()
    tl.penup()
    screen.update()
    # sleep(0.1)


def draw_num(side, x, y, cell_num):

    if side == front or side == back:
        tl.setposition(x + 20, y - 30)
    elif side == left or side == right:
        tl.setposition(x + 15, y - 15)
    elif side == top or side == bottom:
        tl.setposition(x + 30, y + 1)
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
                draw(surface, x, y, color[color_index])
                draw_num(surface, x, y, cell_num)


def get_results(results):
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
        print('steps: ' + str(bi_path))

        print('action_list' + str([revers_dist[x] for x in reversed(action_list)]))
        # print('action_list' + str(action_list))
        return bi_path


if __name__ == "__main__":
    goal = tuple(np.array([
        [[415, 105, 125],
         [410, 100, 120],
         [416, 106, 126]],
        [[125, 205, 235],
         [120, 200, 230],
         [126, 206, 236]],
        [[235, 305, 345],
         [230, 300, 340],
         [236, 306, 346]],
        [[345, 405, 415],
         [340, 400, 410],
         [346, 406, 416]]
    ]).flat)

    cor_u = get_all_coor_set(130)
    cor_d = get_all_coor_set(-130)

    actions = ['rc', 'ra', 'lc', 'la', 'fc', 'fa', 'bc', 'ba', 'tr', 'tl', 'br', 'bl']
    revers_dist = {'rc': 'ra',
                   'ra': 'rc',
                   'lc': 'la',
                   'la': 'lc',
                   'fc': 'fa',
                   'fa': 'fc',
                   'bc': 'ba',
                   'ba': 'bc',
                   'tr': 'tl',
                   'tl': 'tr',
                   'br': 'bl',
                   'bl': 'br'
                   }
    # scramble = []
    i = 10
    for _ in range(1):
        state = deepcopy(goal)
        initial = MagicCubeProblem(state, goal)
        state_display = tuple(np.arange(54))
        initial_forDisplay = MagicCubeProblemForDisplay(state_display)


        # turtle.done()

        action_list = []

        '''        for action in actions:
                    state = initial.result(state, action)
                    state_display = initial_forDisplay.result(state_display, action)
                    if pos:
                        draw_state(np.array(list(state_display)).reshape((6, 3, 3)), cor_u)
                        pos = not pos
                    else:
                        draw_state(np.array(list(state_display)).reshape((6, 3, 3)), cor_d)
                        pos = not pos
        '''
        for _ in range(i):
            action = random.choice(actions)
            action_list.append(action)
            state = initial.result(state, action)
            state_display = initial_forDisplay.result(state_display, action)

        initial_state = np.array(state).reshape((4, 3, 3))
        # draw_state(initial_state, cor)
        pos = False
        draw_state(np.array(list(state_display)).reshape((6, 3, 3)), cor_u)

        puzzle = MagicCubeProblem(tuple(initial_state.flat), goal)

        start = datetime.datetime.now()
        result = bidirectional_bread_first_graph_search(puzzle)
        end = datetime.datetime.now()
        print('time cost(' + str(i) + '): ' + str(end - start))
        print('move: ' + str(puzzle.time_cost_move))
        steps = get_results(result)

        puzzle = MagicCubeProblem(tuple(initial_state.flat), goal)
        initial_forDisplay = MagicCubeProblemForDisplay(state_display)

        for action in steps:
            state = initial.result(state, action)
            state_display = initial_forDisplay.result(state_display, action)
            if pos:
                draw_state(np.array(list(state_display)).reshape((6, 3, 3)), cor_u)
                pos = not pos
            else:
                draw_state(np.array(list(state_display)).reshape((6, 3, 3)), cor_d)
                pos = not pos
            sleep(1)

turtle.done()
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

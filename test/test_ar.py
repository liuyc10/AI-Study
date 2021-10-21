import copy
from time import sleep

import numpy as np
from copy import deepcopy
import turtle

left = 0
top = 1
front = 2
bottom = 3
right = 4
back = 5

# color = ['blue', 'yellow', 'red', 'gray', 'green', 'orange']
color = ['blue', 'yellow', 'red', 'gray', 'green', 'orange', 'pink', 'black',
         'brown', 'aquamarine', 'tomato', 'firebrick', 'cyan', 'salmon', 'magenta', 'orchid',
         'crimson', 'chocolate', 'purple', 'linen']

'''org_state = np.array([np.linspace(0, 0, 9).reshape([3, 3]),
                  np.linspace(1, 1, 9).reshape([3, 3]),
                  np.linspace(2, 2, 9).reshape([3, 3]),
                  np.linspace(3, 3, 9).reshape([3, 3]),
                  np.linspace(4, 4, 9).reshape([3, 3]),
                  np.linspace(5, 5, 9).reshape([3, 3])])
'''
org_state = np.arange(54).reshape(6, 3, 3)
'''org_state = np.array([[[0, 8, 19],
                       [4, 0, 15],
                       [2, 9, 17]],
                      [[0, 5, 1],
                       [8, 1, 11],
                       [19, 13, 16]],
                      [[0, 5, 1],
                       [4, 2, 7],
                       [2, 6, 3]],
                      [[2, 6, 3],
                       [9, 3, 10],
                       [17, 14, 18]],
                      [[1, 11, 16],
                       [7, 4, 12],
                       [3, 10, 18]],
                      [[19, 13, 16],
                       [15, 5, 12],
                       [17, 14, 18]]])
                       '''
print(org_state)


def ru(state):
    state[right] = state[right][::-1].T
    org = state[..., 2]
    new_state = deepcopy(org)
    org[top] = new_state[front][::-1]
    org[front] = new_state[bottom]
    org[bottom] = new_state[back][::-1]
    org[back] = new_state[top]
    return state


def rd(state):
    state[right] = state[right][:, ::-1].T
    org = state[..., 2]
    new_state = deepcopy(org)
    org[front] = new_state[top][::-1]
    org[top] = new_state[back]
    org[back] = new_state[bottom][::-1]
    org[bottom] = new_state[front]
    return state


def lu(state):
    state[left] = state[left][::-1].T
    org = state[..., 0]
    new_state = deepcopy(org)
    org[top] = new_state[front][::-1]
    org[front] = new_state[bottom]
    org[bottom] = new_state[back][::-1]
    org[back] = new_state[top]
    return state


def ld(state):
    state[left] = state[left][:, ::-1].T
    org = state[..., 0]
    new_state = deepcopy(org)
    org[front] = new_state[top][::-1]
    org[top] = new_state[back]
    org[back] = new_state[bottom][::-1]
    org[bottom] = new_state[front]
    return state


def ur(state):
    state[top] = state[top][::-1].T
    org = state[:, 0, ...]
    new_state = deepcopy(org)
    org[front] = new_state[left][::-1]
    org[right] = new_state[front]
    org[back] = new_state[right][::-1]
    org[left] = new_state[back]
    return state


def ul(state):
    state[top] = state[top][:, ::-1].T
    org = state[:, 0, ...]
    new_state = deepcopy(org)
    org[right] = new_state[back][::-1]
    org[front] = new_state[right]
    org[left] = new_state[front][::-1]
    org[back] = new_state[left]
    return state


def bl(state):
    state[bottom] = state[bottom][:, ::-1].T
    org = state[:, 2, ...]
    new_state = deepcopy(org)
    org[right] = new_state[back][::-1]
    org[front] = new_state[right]
    org[left] = new_state[front][::-1]
    org[back] = new_state[left]

    return state


def br(state):
    state[bottom] = state[bottom][::-1].T
    org = state[:, 2, ...]
    new_state = deepcopy(org)
    org[front] = new_state[left][::-1]
    org[right] = new_state[front]
    org[back] = new_state[right][::-1]
    org[left] = new_state[back]
    return state


def ff(state):
    state[front] = state[front][::-1].T
    new_state = deepcopy(state)
    state[top][0, ...] = new_state[left][..., 0][::-1]
    state[right][..., 0] = new_state[top][0, ...]
    state[bottom][0, ...] = new_state[right][..., 0][::-1]
    state[left][..., 0] = new_state[bottom][0, ...]
    return state


def fb(state):
    state[front] = state[front][:, ::-1].T
    new_state = deepcopy(state)
    state[top][0, ...] = new_state[right][..., 0]
    state[right][..., 0] = new_state[bottom][0, ...][::-1]
    state[bottom][0, ...] = new_state[left][..., 0]
    state[left][..., 0] = new_state[top][0, ...][::-1]
    return state


def bf(state):
    state[back] = state[back][::-1].T
    new_state = deepcopy(state)
    state[top][2, ...] = new_state[left][..., 2][::-1]
    state[right][..., 2] = new_state[top][2, ...]
    state[bottom][2, ...] = new_state[right][..., 2][::-1]
    state[left][..., 2] = new_state[bottom][2, ...]
    return state


def bb(state):
    state[back] = state[back][:, ::-1].T
    new_state = deepcopy(state)
    state[top][2, ...] = new_state[right][..., 2]
    state[right][..., 2] = new_state[bottom][2, ...][::-1]
    state[bottom][2, ...] = new_state[left][..., 2]
    state[left][..., 2] = new_state[top][2, ...][::-1]
    return state


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

cor = get_all_coor_set()

draw_state(org_state, cor)

org_state = ff(org_state)
draw_state(org_state, cor)
org_state = fb(org_state)
draw_state(org_state, cor)
org_state = bf(org_state)
draw_state(org_state, cor)
org_state = bb(org_state)
draw_state(org_state, cor)
org_state = ru(org_state)
draw_state(org_state, cor)
org_state = rd(org_state)
draw_state(org_state, cor)
org_state = lu(org_state)
draw_state(org_state, cor)
org_state = ld(org_state)
draw_state(org_state, cor)
org_state = ur(org_state)
draw_state(org_state, cor)
org_state = ul(org_state)
draw_state(org_state, cor)
org_state = br(org_state)
draw_state(org_state, cor)
org_state = bl(org_state)
draw_state(org_state, cor)
print(org_state)
turtle.done()

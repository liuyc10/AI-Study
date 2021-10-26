import turtle
from time import sleep

import numpy as np

back = 0
left = 1
front = 2
right = 3
top = 4
bottom = 5

delta = 40
surface = 6
h = v = 3
height = 3 * h * delta + 60
width = 4 * v * delta + 40
tl = turtle.Turtle()
screen = turtle.Screen()
# tl.hideturtle()
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
    print(coor_set)
    # coor = np.array(coor_set).reshape((6, 3, 3, 2))
    # print(coor)
    return coor_set


def squares():
    for i in range(4):  # For each edge of the shape
        tl.forward(40)  # Move forward 40 units
        tl.left(90)  # Turn ready for the next edge


def squares(side):
    angle = 60
    if side == front or side == back:
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
        a = 180 - angle
        for _ in range(4):
            tl.forward(40)
            tl.left(a)
            a = 180 - a


def get_coordinate_LR(x, y):
    angle = np.pi / 3
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40 * np.sin(angle), y - row * 40 + col * 40 * np.cos(angle)])
    return coordinate_list


def draw():
    coor = get_all_coor_set()

    for a in coor:
        for [x, y] in a:
            tl.setposition(x, y)
            tl.pendown()
            tl.begin_fill()
            tl.color('black')
            squares()
            tl.end_fill()
            tl.penup()
            screen.update()
            sleep(0.1)


def get_coordinate_FB(x, y):
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40, y - row * 40])
    return coordinate_list


def get_coordinate_TB(x, y):
    angle = np.pi / 3
    coordinate_list = []
    for row in range(3):
        for col in range(3):
            coordinate_list.append([x + col * 40 + row * 40 * np.cos(angle), y + row * 40 * np.sin(angle)])
    return coordinate_list


a = get_coordinate_TB(0, 0)
for x, y in a:
    tl.setposition(x, y)
    tl.pendown()
    tl.begin_fill()
    tl.color('black')
    squares(top)
    tl.end_fill()
    tl.penup()
    screen.update()
    sleep(1)

turtle.done()
'''
get_all_coor_set()
draw()
turtle.done()
'''

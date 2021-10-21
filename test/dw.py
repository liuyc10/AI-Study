import turtle
from time import sleep

import numpy as np

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



get_all_coor_set()
draw()
turtle.done()

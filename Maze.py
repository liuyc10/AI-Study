import random
from datetime import datetime

from GraphProblem import GraphProblem
from RomaniaMap import undirectedGraph
from Search import astar_search
import turtle


class Individual:

    def __init__(self, num, row, col, row_count, col_count):
        self.num = num
        self.group = num
        self.row = row
        self.col = col
        self.row_count = row_count
        self.col_count = col_count
        self.root = num
        self.parent = None
        self.child = []
        self.connected_nodes = []
        self.connected_directions = []

    def get_possible_connections(self):
        possible_connection = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if self.row == 0:
            possible_connection.remove('UP')
        if self.row == self.row_count - 1:
            possible_connection.remove('DOWN')
        if self.col == 0:
            possible_connection.remove('LEFT')
        if self.col == self.col_count - 1:
            possible_connection.remove('RIGHT')
        return possible_connection

    def get_neighbor(self, action):
        delta = {'UP': -self.col_count,
                 'DOWN': self.col_count,
                 'LEFT': -1,
                 'RIGHT': 1}
        return self.num + delta[action]

    def set_root_node_parent(self, new_parent_node):
        node = self
        # node.root = new_parent_node.root
        while node.parent:
            node = node.parent
            # node.root = new_parent_node.root

        node.root = new_parent_node.root
        node.parent = new_parent_node
        new_parent_node.child = node

        while node.child:
            node = node.child
            node.root = new_parent_node.root


def initial(size, row_count, col_count):
    initial_set = []
    for i in range(size):
        initial_set.append(Individual(i, int(i / col_count), int(i % col_count), row_count, col_count))
    return initial_set


def search(idv):
    if idv.parent:
        return search(idv.parent)
    else:
        return idv


def union(idv, neighbor):
    root_idv = search(idv)
    root_neighbor = search(neighbor)
    if root_idv.num > root_neighbor.num:
        root_idv.root = neighbor.root
        update_root(root_idv)
        root_idv.parent = neighbor
        neighbor.child.append(root_idv)
    else:
        root_neighbor.root = idv.root
        update_root(root_neighbor)
        root_neighbor.parent = idv
        idv.child.append(root_neighbor)


def update_root(idv):
    children = []
    if idv.child:
        children.extend(idv.child)
        while children:
            node = children.pop()
            node.root = idv.root
            update_root(node)


def reverse_directions(direction):
    if direction == 'UP':
        return 'DOWN'
    if direction == 'DOWN':
        return 'UP'
    if direction == 'LEFT':
        return 'RIGHT'
    if direction == 'RIGHT':
        return 'LEFT'


def print_format(tree, row_count, col_count):
    formatted = []
    for row_index in range(row_count):
        row = []
        for col_index in range(col_count):
            row.append(tree[row_index * col_count + col_index].root)
        formatted.append(row)
    return formatted


def great_new_maze(size, col, row):
    start = 0
    end = size - 1
    tree = initial(size, row, col)

    while tree[start].num != search(tree[end]).num:
        idv_num = random.randint(0, size - 1)
        idv = tree[idv_num]

        action = random.choice(idv.get_possible_connections())
        neighbor_num = idv.get_neighbor(action)
        neighbor = tree[neighbor_num]

        if search(idv).num == search(neighbor).num:
            continue
        else:
            idv.connected_nodes.append(neighbor)
            neighbor.connected_nodes.append(idv)
            idv.connected_directions.append(action)
            neighbor.connected_directions.append(reverse_directions(action))
            union(idv, neighbor)

    for idv in tree:
        if idv.root != 0:
            action = random.choice(idv.get_possible_connections())
            neighbor_num = idv.get_neighbor(action)
            neighbor = tree[neighbor_num]

            if search(idv).num == search(neighbor).num:
                continue
            else:
                idv.connected_nodes.append(neighbor)
                neighbor.connected_nodes.append(idv)
                idv.connected_directions.append(action)
                neighbor.connected_directions.append(reverse_directions(action))
                union(idv, neighbor)
    return tree


def solution(tree):
    node = tree[-1]
    solution_list = [node]
    while node.parent:
        solution_list.append(node.parent)
        node = node.parent

    return solution_list


def draw(tree, col_count, row_count, t, height, width):
    x_0 = -col_count * width / 2
    y_0 = row_count * height / 2
    x_1 = col_count * width / 2
    y_1 = -row_count * height / 2
    t.speed(0)
    t.penup()
    t.goto(x_0, y_0)
    t.pendown()
    t.goto(x_1, y_0)

    t.goto(x_1, y_1 + height)
    t.penup()

    for n in tree:
        t.setposition(x_0 + n.col * width, y_0 - n.row * height)
        if 'LEFT' not in n.connected_directions:
            t.pendown()
            if n.num == 0:
                t.penup()
        t.setposition(x_0 + n.col * width, y_0 - n.row * height - height)

        t.penup()
        if 'DOWN' not in n.connected_directions:
            t.pendown()
            t.setposition(x_0 + n.col * width + width, y_0 - n.row * height - height)
        t.penup()

    return x_0, y_0


row = col = 100
size = row * col
start = datetime.now()
maze = great_new_maze(size, row, col)
end = datetime.now()
print('create time cost: ' + str(end - start))

maze_graph = dict()

for node in maze:
    c = dict()
    for connected_node in node.connected_nodes:
        c[str(connected_node.num)] = 1
    maze_graph[str(node.num)] = c
undirectedGraph_maze = undirectedGraph(maze_graph)
undirectedGraph_maze.locations = dict()
for node in maze:
    undirectedGraph_maze.locations[str(node.num)] = (node.col, node.row)

Maze_problem = GraphProblem('0', str(maze[-1].num), undirectedGraph_maze)

start = datetime.now()
search_result = astar_search(Maze_problem)
end = datetime.now()
print('search time cost: ' + str(end - start))
solution = search_result.solution()
h = w = 6
tl = turtle.Turtle()
screen = turtle.Screen()
screen.screensize(col * w, row * h)
screen.tracer(50000)
tl.hideturtle()
x0, y0 = draw(maze, row, col, tl, h, w)

tl.setposition(x0 + w / 2, y0 - h / 2)
tl.pencolor('red')
tl.pensize(2)
tl.pendown()
screen.tracer(1)
tl.speed(5)
for i in range(len(solution) - 1):
    next_node = maze[int(solution[i])]
    tl.setposition(x0 + next_node.col * w + w / 2, y0 - next_node.row * h - h / 2)
final_node = maze[-1]
tl.setposition(x0 + final_node.col * w + w / 2, y0 - final_node.row * h - h / 2)
tl.penup()
turtle.done()

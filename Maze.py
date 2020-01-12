import random

import matplotlib.pyplot as plt


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


def print_format(tree, row_count, col_count):
    formatted = []
    for row_index in range(row_count):
        row = []
        for col_index in range(col_count):
            row.append(tree[row_index * col_count + col_index].root)
        formatted.append(row)
    return formatted


def great_new_maze():
    size = 100
    col = 10
    row = 10
    start = 0
    end = size - 1
    tree = initial(size, row, col)
    print(print_format(tree, row, col))

    count = 0
    while tree[start].num != search(tree[end]).num:
        idv_num = random.randint(0, size - 1)
        idv = tree[idv_num]
        print(idv_num)
        action = random.choice(idv.get_possible_connections())
        neighbor_num = idv.get_neighbor(action)
        neighbor = tree[neighbor_num]
        print(neighbor_num)
        count += 1
        print('count:' + str(count))
        if search(idv).num == search(neighbor).num:
            continue
        else:
            idv.connected_nodes.append(neighbor)
            neighbor.connected_nodes.append(idv)
            union(idv, neighbor)
        print(print_format(tree, row, col))
    print(print_format(tree, row, col))
    return tree


def draw(tree):
    for node in tree:
        if node.connected_nodes:
            for con_node in node.connected_nodes:
                plt.plot()
        else:
            plt.plot


maze = great_new_maze()

from collections import deque

from Node import Node
from utils import memoize, PriorityQueue


def breadth_first_tree_search(problem):
    node = Node(problem.initial)
    frontier = deque()
    frontier.append(node)
    while frontier:
        node = frontier.popleft()
        print(node.state)
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None


def depth_first_tree_search(problem):
    node = Node(problem.initial)
    frontier = [node]

    while frontier:
        node = frontier.pop()
        print(node.state)
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None


def breadth_first_graph_search(problem):
    node = Node(problem.initial)
    frontier = deque()
    frontier.append(node)

    explored = set()

    while frontier:
        node = frontier.popleft()
        print(node.state)
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return None


def depth_first_graph_search(problem):
    node = Node(problem.initial)
    frontier = [node]

    explored = set()

    while frontier:
        node = frontier.pop()
        print(node.state)
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)

    return None


def bidirectional_bread_first_graph_search(problem):
    node_forward = Node(problem.initial)
    node_backward = Node(problem.goal)
    frontier_forward = deque()
    frontier_backward = deque()
    frontier_forward.append(node_forward)
    frontier_backward.append(node_backward)
    explored = set()

    while frontier_forward and frontier_backward:
        node_forward = frontier_forward.popleft()
        # print(node_forward.state)
        if problem.goal_test_forward(node_forward.state):
            print('[f]meet point:')
            print(node_forward.state)
            while True:
                node_backward = frontier_backward.popleft()
                if node_backward.state == node_forward.state:
                    break
            return [node_forward, node_backward]
        explored.add(node_forward.state)

        for child in node_forward.expand(problem):
            if child.state not in explored and child not in frontier_forward:
                frontier_forward.append(child)
                problem.backward_goal.append(child.state)
        problem.backward_goal.remove(node_forward.state)

        node_backward = frontier_backward.popleft()
        # print(node_backward.state)
        if problem.goal_test_backward(node_backward.state):
            print('[b]meet point:')
            print(node_backward.state)
            while True:
                node_forward = frontier_forward.popleft()
                if node_backward.state == node_forward.state:
                    break
            return [node_forward, node_backward]
        explored.add(node_backward.state)
        # problem.backward_goal = [problem.initial]
        for child in node_backward.expand(problem):
            if child.state not in explored and child not in frontier_backward:
                frontier_backward.append(child)
                problem.forward_goal.append(child.state)
        problem.forward_goal.remove(node_backward.state)

    return None


def best_first_graph_search(problem, f):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def uniform_search(problem):
    return best_first_graph_search(problem, lambda x: x.path_cost)


def astar_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda x: x.path_cost + h(x))

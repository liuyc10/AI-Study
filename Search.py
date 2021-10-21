import datetime
import random
from collections import deque

from numpy import ndarray

from MCT_Node import MCT_Node
from Node import Node
from utils import memoize, PriorityQueue, inf, ucb


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
        # print(node.state)
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        if len(explored) % 1000 == 0:
            print(len(explored))
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
    frontier_forward_set = set()
    frontier_backward_set = set()
    frontier_forward.append(node_forward)
    frontier_backward.append(node_backward)
    frontier_forward_set.add(node_forward)
    frontier_backward_set.add(node_backward)
    explored = set()

    time_cost_filter_explore = datetime.timedelta(0)
    time_cost_filter_frontier = datetime.timedelta(0)
    time_cost_goal_test = datetime.timedelta(0)

    while frontier_forward and frontier_backward:
        node_forward = frontier_forward.popleft()
        # print(node_forward.state)
        start = datetime.datetime.now()
        if problem.goal_test_forward(node_forward.state):

            # print('[f]meet point:')
            # print(node_forward.state)
            while True:
                node_backward = frontier_backward.popleft()
                if node_backward.state == node_forward.state:
                    break
            print('count:' + str(len(explored)))
            print('time_cost_filter_explore:' + str(time_cost_filter_explore))
            print('time_cost_filter_frontier:' + str(time_cost_filter_frontier))
            print('time_cost_goal_test:' + str(time_cost_goal_test))
            return [node_forward, node_backward]
        end = datetime.datetime.now()
        time_cost_goal_test += (end - start)
        explored.add(node_forward.state)

        for child in node_forward.expand(problem):
            start = datetime.datetime.now()
            if child.state not in explored:  # and child not in frontier_forward:
                end = datetime.datetime.now()
                time_cost_filter_explore += (end - start)
                start = datetime.datetime.now()
                # if child not in frontier_forward:
                if child not in frontier_forward_set:
                    end = datetime.datetime.now()
                    time_cost_filter_frontier += (end - start)
                    frontier_forward.append(child)
                    frontier_forward_set.add(child)
                    problem.backward_goal.append(child.state)
                    problem.backward_goal_set.add(child.state)  # 可删除
        problem.backward_goal.remove(node_forward.state)

        node_backward = frontier_backward.popleft()
        # print(node_backward.state)
        start = datetime.datetime.now()
        if problem.goal_test_backward(node_backward.state):
            # print('[b]meet point:')
            # print(node_backward.state)
            while True:
                node_forward = frontier_forward.popleft()
                if node_backward.state == node_forward.state:
                    break
            print('count:' + str(len(explored)))
            print('time_cost_filter_explore:' + str(time_cost_filter_explore))
            print('time_cost_filter_frontier:' + str(time_cost_filter_frontier))
            print('time_cost_goal_test:' + str(time_cost_goal_test))
            return [node_forward, node_backward]
        end = datetime.datetime.now()
        time_cost_goal_test += (end - start)
        explored.add(node_backward.state)
        # problem.backward_goal = [problem.initial]
        for child in node_backward.expand(problem):
            start = datetime.datetime.now()
            if child.state not in explored:  # and child not in frontier_backward:
                end = datetime.datetime.now()
                time_cost_filter_explore += (end - start)
                start = datetime.datetime.now()
                # if child not in frontier_backward:
                if child not in frontier_backward_set:
                    end = datetime.datetime.now()
                    time_cost_filter_frontier += (end - start)
                    frontier_backward.append(child)
                    frontier_backward_set.add(child)
                    problem.forward_goal.append(child.state)
                    problem.forward_goal_set.add(child.state)  # 可删除
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


def bidirectional_best_first_graph_search(problem, h=None, h_reverse=None):
    h = memoize(h or problem.h, 'h')
    h_reverse = memoize(h_reverse or problem.h_reverse, 'h_reverse')
    node_forward = Node(problem.initial)
    node_backward = Node(problem.goal)
    frontier_forward = PriorityQueue('min', h)
    frontier_backward = PriorityQueue('min', h_reverse)
    frontier_forward.append(node_forward)
    frontier_backward.append(node_backward)
    explored = set()

    while frontier_forward and frontier_backward:
        node_forward = frontier_forward.pop()
        # print(node_forward.state)
        if problem.goal_test_forward(node_forward.state):
            print('[f]meet point:')
            print(node_forward.state)
            while True:
                node_backward = frontier_backward.pop()
                if node_backward.state == node_forward.state:
                    break
            return [node_forward, node_backward]
        explored.add(node_forward.state)

        for child in node_forward.expand(problem):
            if child.state not in explored and child not in frontier_forward:
                frontier_forward.append(child)
                problem.backward_goal.append(child.state)
        problem.backward_goal.remove(node_forward.state)

        node_backward = frontier_backward.pop()
        # print(node_backward.state)
        if problem.goal_test_backward(node_backward.state):
            print('[b]meet point:')
            print(node_backward.state)
            while True:
                node_forward = frontier_forward.pop()
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


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            ev = eval_fn(state)
            # print(ev)
            return ev
        v = -inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            ev = eval_fn(state)
            # print(ev)
            return ev
        v = inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -inf
    beta = inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def monte_carlo_tree_search(state, game, N=2000):
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.terminal_test(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """simulate the utility of current state by random picking a step"""
        player = game.to_move(state)
        while not game.terminal_test(state):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

    root = MCT_Node(state=state)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)

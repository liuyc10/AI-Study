import datetime
from copy import deepcopy
import numpy as np

from Problem import Problem

left = 0
top = 1
front = 2
bottom = 3
right = 4
back = 5


class MagicCubeProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        self.forward_goal_set = set(goal)
        self.backward_goal_set = set(initial)
        # self.count = len(goal)
        # self.size = int(self.count ** 0.5)
        self.time_cost_move = datetime.timedelta(0)

    def goal_test_forward(self, state):
        return state in self.forward_goal_set

    def goal_test_backward(self, state):
        return state in self.backward_goal_set

    def actions(self, state):
        possible_action = ['ru', 'rd', 'lu', 'ld', 'ff', 'fb', 'bf', 'bb', 'tr', 'tl', 'br', 'bl']
        return possible_action

    def result(self, state, action):
        start = datetime.datetime.now()
        reshape_state = np.array(list(state)).reshape((6, 3, 3))
        new_state = tuple(self.get_move(reshape_state, action).flat)
        finish = datetime.datetime.now()
        self.time_cost_move += (finish - start)
        return new_state

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h_reverse(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.initial))

    def value(self, state):
        pass

    def ru(self, state):
        state[right] = state[right][::-1].T
        org = state[..., 2]
        new_state = deepcopy(org)
        org[top] = new_state[front][::-1]
        org[front] = new_state[bottom]
        org[bottom] = new_state[back][::-1]
        org[back] = new_state[top]
        return state

    def rd(self, state):
        state[right] = state[right][:, ::-1].T
        org = state[..., 2]
        new_state = deepcopy(org)
        org[front] = new_state[top][::-1]
        org[top] = new_state[back]
        org[back] = new_state[bottom][::-1]
        org[bottom] = new_state[front]
        return state

    def lu(self, state):
        state[left] = state[left][::-1].T
        org = state[..., 0]
        new_state = deepcopy(org)
        org[top] = new_state[front][::-1]
        org[front] = new_state[bottom]
        org[bottom] = new_state[back][::-1]
        org[back] = new_state[top]
        return state

    def ld(self, state):
        state[left] = state[left][:, ::-1].T
        org = state[..., 0]
        new_state = deepcopy(org)
        org[front] = new_state[top][::-1]
        org[top] = new_state[back]
        org[back] = new_state[bottom][::-1]
        org[bottom] = new_state[front]
        return state

    def tr(self, state):
        state[top] = state[top][::-1].T
        org = state[:, 0, ...]
        new_state = deepcopy(org)
        org[front] = new_state[left][::-1]
        org[right] = new_state[front]
        org[back] = new_state[right][::-1]
        org[left] = new_state[back]
        return state

    def tl(self, state):
        state[top] = state[top][:, ::-1].T
        org = state[:, 0, ...]
        new_state = deepcopy(org)
        org[right] = new_state[back][::-1]
        org[front] = new_state[right]
        org[left] = new_state[front][::-1]
        org[back] = new_state[left]
        return state

    def bl(self, state):
        state[bottom] = state[bottom][:, ::-1].T
        org = state[:, 2, ...]
        new_state = deepcopy(org)
        org[right] = new_state[back][::-1]
        org[front] = new_state[right]
        org[left] = new_state[front][::-1]
        org[back] = new_state[left]

        return state

    def br(self, state):
        state[bottom] = state[bottom][::-1].T
        org = state[:, 2, ...]
        new_state = deepcopy(org)
        org[front] = new_state[left][::-1]
        org[right] = new_state[front]
        org[back] = new_state[right][::-1]
        org[left] = new_state[back]
        return state

    def ff(self, state):
        state[front] = state[front][::-1].T
        new_state = deepcopy(state)
        state[top][0, ...] = new_state[left][..., 0][::-1]
        state[right][..., 0] = new_state[top][0, ...]
        state[bottom][0, ...] = new_state[right][..., 0][::-1]
        state[left][..., 0] = new_state[bottom][0, ...]
        return state

    def fb(self, state):
        state[front] = state[front][:, ::-1].T
        new_state = deepcopy(state)
        state[top][0, ...] = new_state[right][..., 0]
        state[right][..., 0] = new_state[bottom][0, ...][::-1]
        state[bottom][0, ...] = new_state[left][..., 0]
        state[left][..., 0] = new_state[top][0, ...][::-1]
        return state

    def bf(self, state):
        state[back] = state[back][::-1].T
        new_state = deepcopy(state)
        state[top][2, ...] = new_state[left][..., 2][::-1]
        state[right][..., 2] = new_state[top][2, ...]
        state[bottom][2, ...] = new_state[right][..., 2][::-1]
        state[left][..., 2] = new_state[bottom][2, ...]
        return state

    def bb(self, state):
        state[back] = state[back][:, ::-1].T
        new_state = deepcopy(state)
        state[top][2, ...] = new_state[right][..., 2]
        state[right][..., 2] = new_state[bottom][2, ...][::-1]
        state[bottom][2, ...] = new_state[left][..., 2]
        state[left][..., 2] = new_state[top][2, ...][::-1]
        return state

    def get_move(self, state, action):
        method = getattr(self, action)
        return method(state)

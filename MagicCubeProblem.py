import datetime
import numpy as np
from Problem import Problem

back = 0
left = 1
front = 2
right = 3


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
        possible_action = ['rc', 'ra', 'lc', 'la', 'fc', 'fa', 'bc', 'ba', 'tr', 'tl', 'br', 'bl']
        return possible_action

    def result(self, state, action):
        start = datetime.datetime.now()
        reshape_state = np.array(list(state)).reshape((4, 3, 3))
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

    def rc(self, state):
        state[right] = state[right][::-1].T
        state[back][..., 0] = state[right][..., 2]
        state[front][..., 2] = state[right][..., 0]
        return state

    def ra(self, state):
        state[right] = state[right][:, ::-1].T
        state[back][..., 0] = state[right][..., 2]
        state[front][..., 2] = state[right][..., 0]
        return state

    def lc(self, state):
        state[left] = state[left][::-1].T
        state[back][..., 2] = state[left][..., 0]
        state[front][..., 0] = state[left][..., 2]
        return state

    def la(self, state):
        state[left] = state[left][:, ::-1].T
        state[back][..., 2] = state[left][..., 0]
        state[front][..., 0] = state[left][..., 2]
        return state

    def fc(self, state):
        state[front] = state[front][::-1].T
        state[left][..., 2] = state[front][..., 0]
        state[right][..., 0] = state[front][..., 2]
        return state

    def fa(self, state):
        state[front] = state[front][:, ::-1].T
        state[left][..., 2] = state[front][..., 0]
        state[right][..., 0] = state[front][..., 2]
        return state

    def bc(self, state):
        state[back] = state[back][::-1].T
        state[right][..., 2] = state[back][..., 0]
        state[left][..., 0] = state[back][..., 2]
        return state

    def ba(self, state):
        state[back] = state[back][:, ::-1].T
        state[right][..., 2] = state[back][..., 0]
        state[left][..., 0] = state[back][..., 2]
        return state

    def tr(self, state):
        state[:, 0, ...] = np.vstack((state[:, 0, ...][-1], state[:, 0, ...][:-1]))
        return state

    def tl(self, state):
        state[:, 0, ...] = np.vstack((state[:, 0, ...][1:], state[:, 0, ...][0]))
        return state

    def br(self, state):
        state[:, 2, ...] = np.vstack((state[:, 2, ...][-1], state[:, 2, ...][:-1]))
        return state

    def bl(self, state):
        state[:, 2, ...] = np.vstack((state[:, 2, ...][1:], state[:, 2, ...][0]))
        return state

    def get_move(self, state, action):
        method = getattr(self, action)
        return method(state)

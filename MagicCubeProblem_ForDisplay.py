import datetime
from copy import deepcopy
import numpy as np

from MagicCubeProblem import MagicCubeProblem

'''
left = 0
top = 1
front = 2
bottom = 3
right = 4
back = 5
'''
back = 0
left = 1
front = 2
right = 3
top = 4
bottom = 5


class MagicCubeProblemForDisplay(MagicCubeProblem):
    def __init__(self, initial):
        super().__init__(initial, initial)

    def result(self, state, action):
        reshape_state = np.array(list(state)).reshape((6, 3, 3))
        new_state = tuple(self.get_move(reshape_state, action).flat)
        return new_state

    def rc(self, state):
        state[right] = state[right][::-1].T
        org = state[..., 2]
        new_state = deepcopy(org)
        org[top] = new_state[front][::-1]
        org[front] = new_state[bottom]
        org[bottom] = new_state[back][::-1]
        org[back] = new_state[top]
        return state

    def ra(self, state):
        state[right] = state[right][:, ::-1].T
        org = state[..., 2]
        new_state = deepcopy(org)
        org[front] = new_state[top][::-1]
        org[top] = new_state[back]
        org[back] = new_state[bottom][::-1]
        org[bottom] = new_state[front]
        return state

    def la(self, state):
        state[left] = state[left][::-1].T
        org = state[..., 0]
        new_state = deepcopy(org)
        org[top] = new_state[front][::-1]
        org[front] = new_state[bottom]
        org[bottom] = new_state[back][::-1]
        org[back] = new_state[top]
        return state

    def lc(self, state):
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

    def fc(self, state):
        state[front] = state[front][::-1].T
        new_state = deepcopy(state)
        state[top][0, ...] = new_state[left][..., 0][::-1]
        state[right][..., 0] = new_state[top][0, ...]
        state[bottom][0, ...] = new_state[right][..., 0][::-1]
        state[left][..., 0] = new_state[bottom][0, ...]
        return state

    def fa(self, state):
        state[front] = state[front][:, ::-1].T
        new_state = deepcopy(state)
        state[top][0, ...] = new_state[right][..., 0]
        state[right][..., 0] = new_state[bottom][0, ...][::-1]
        state[bottom][0, ...] = new_state[left][..., 0]
        state[left][..., 0] = new_state[top][0, ...][::-1]
        return state

    def ba(self, state):
        state[back] = state[back][::-1].T
        new_state = deepcopy(state)
        state[top][2, ...] = new_state[left][..., 2][::-1]
        state[right][..., 2] = new_state[top][2, ...]
        state[bottom][2, ...] = new_state[right][..., 2][::-1]
        state[left][..., 2] = new_state[bottom][2, ...]
        return state

    def bc(self, state):
        state[back] = state[back][:, ::-1].T
        new_state = deepcopy(state)
        state[top][2, ...] = new_state[right][..., 2]
        state[right][..., 2] = new_state[bottom][2, ...][::-1]
        state[bottom][2, ...] = new_state[left][..., 2]
        state[left][..., 2] = new_state[top][2, ...][::-1]
        return state


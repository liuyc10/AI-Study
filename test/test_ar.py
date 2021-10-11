import copy

import numpy as np
from copy import deepcopy

left = 0
top = 1
front = 2
bottom = 3
right = 4
back = 5

state = np.array([np.linspace(0, 0, 9).reshape([3, 3]),
                  np.linspace(1, 1, 9).reshape([3, 3]),
                  np.linspace(2, 2, 9).reshape([3, 3]),
                  np.linspace(3, 3, 9).reshape([3, 3]),
                  np.linspace(4, 4, 9).reshape([3, 3]),
                  np.linspace(5, 5, 9).reshape([3, 3])])

state = np.arange(54).reshape(6,3,3)
print(state)


def rc(state):
    state[right] = state[right][::-1].T
    org = state[..., 2]
    new_state = deepcopy(org)
    org[top] = new_state[front][::-1]
    org[front] = new_state[bottom]
    org[bottom] = new_state[back][::-1]
    org[back] = new_state[top]
    return state


def rac(state):
    state[right] = state[right][:, ::-1].T
    org = state[..., 2]
    new_state = deepcopy(org)
    org[front] = new_state[top][::-1]
    org[top] = new_state[back]
    org[back] = new_state[bottom][::-1]
    org[bottom] = new_state[front]
    return state


state = rc(state)
print(state)
state = rac(state)
print(state)

import random
from copy import deepcopy
from datetime import datetime

from Search import best_first_graph_search, astar_search, bidirectional_bread_first_graph_search, \
    bidirectional_best_first_graph_search

from SquareMovePuzzleProblem import SquareMovePuzzleProblem
from utils import move_reverse

state = []
goal = []

for i in range(24):
    state.append(i + 1)
    goal.append(i + 1)
state.append(0)
goal.append(0)

puzzle = SquareMovePuzzleProblem(tuple(state), tuple(goal))

actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
scramble = []
count = 0
for _ in range(60):
    scramble.append(random.choice(actions))
moves = []
for move in scramble:
    if move in puzzle.actions(state):
        state = list(puzzle.result(state, move, False, False))
        puzzle = SquareMovePuzzleProblem(tuple(state), tuple(goal))
        moves.append(move)
        count += 1

puzzle1 = deepcopy(puzzle)
puzzle2 = deepcopy(puzzle)
print('scramble =' + str(count))
initial = puzzle.initial
# print(moves)
print(puzzle.print_format(puzzle.initial))

start = datetime.now()
# results = bidirectional_bread_first_graph_search(puzzle)
end = datetime.now()
print('time cost: ' + str(end - start))
bi_path = []
'''
if results is not None:
    path_forward = results[0].solution()
    path_backward = results[1].solution()

    print('forward')
    print(path_forward)

    print('backward')
    print(path_backward)

    bi_path.extend(path_forward)
    bi_path.extend(move_reverse(path_backward))
    print(bi_path)
    print(len(bi_path))

'''
start = datetime.now()
results = astar_search(puzzle1)
end = datetime.now()
print('time cost: ' + str(end - start))

as_path = results.solution()

print(as_path)
print(len(as_path))


results_move_bi = bi_path
results_move_as = as_path

state1 = initial
print(initial)


print('bi')
for move_bi in results_move_bi:
    state1 = list(puzzle1.result(state1, move_bi, False, False))
    puzzle2 = SquareMovePuzzleProblem(tuple(state1), tuple(goal))
    print(move_bi)
    print(state1)

print(bi_path == as_path)

"""

for move_bi, move_as in zip(results_move_bi, results_move_as):
    state1 = list(puzzle1.result(state1, move_bi, False, False))
    puzzle1 = SquareMovePuzzleProblem(tuple(state1), tuple(goal))
    print(state1)
    state2 = list(puzzle2.result(state2, move_as, False, False))
    puzzle2 = SquareMovePuzzleProblem(tuple(state2), tuple(goal))
    print(state2)"""
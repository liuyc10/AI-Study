from collections import namedtuple

from Game import Game
from utils import get_score, k_in_row, compute_utility, extend_moves

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


class Gomoku(Game):

    def __init__(self, h=15, v=15, k=5):
        super().__init__()
        self.h = h
        self.v = v
        self.k = k
        moves_list = [(x, y) for x in range(1, h + 1) for y in range(1, v + 1)]
        moves = dict()
        for move in moves_list:
            moves[move] = 0
        moves[(8, 8)] = 1
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        moves = []
        for move in state.moves.keys():
            if state.moves[move] == 1:
                moves.append(move)
        return moves

    def result(self, state, move):
        if move not in state.moves:
            return state
        board = state.board.copy()
        board[move] = state.to_move
        moves = state.moves.copy()
        del moves[move]
        moves = extend_moves(move, moves, True)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        return 220 <= abs(state.utility) or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

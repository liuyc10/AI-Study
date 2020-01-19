from Game import Game
from TicTacToe import TicTacToe


class FiveInARow(TicTacToe):

    def __init__(self, h=15, v=15, k=3):
        super().__init__(h, v, k)

    def utility(self, state, player):
        return state.utility != 0 or len(state.moves) == 0

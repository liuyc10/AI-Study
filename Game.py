class Game:
    def __init__(self):
        self.initial = None

    def action(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def terminal_test(self, state):
        return not self.action(state)

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))



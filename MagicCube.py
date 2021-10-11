from Problem import Problem


class MagicCube(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        self.count = len(goal)
        self.size = int(self.count ** 0.5)

    def actions(self, state):
        pass

    def result(self, state, action):
        pass

    def value(self, state):
        pass

    def left(self, state):
        return state

from Problem import Problem


def check_solvability(state):

    inversion = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                inversion += 1

    return inversion % 2 == 0


class SquareMovePuzzleProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        self.count = len(goal)
        self.size = int(self.count ** 0.5)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % self.size == 0:
            possible_actions.remove('LEFT')
        if index_blank_square % self.size == self.size - 1:
            possible_actions.remove('RIGHT')
        if index_blank_square < self.size:
            possible_actions.remove('UP')
        if index_blank_square >= self.count - self.size:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action, check=False, display=False):
        blank = self.find_blank_square(state)
        new_state = list(state)
        delta = {'UP': -self.size,
                 'DOWN': self.size,
                 'LEFT': -1,
                 'RIGHT': 1}
        neighbor = blank + delta[action]
        try:
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        except IndexError:
            print(blank + neighbor)
        if check:
            if check_solvability(new_state):
                print(new_state)
                return tuple(new_state)
        else:
            if display:
                print(new_state)
            return tuple(new_state)

        return None

    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h_reverse(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.initial))

    def print_format(self, input_list):
        formated = []
        for row_index in range(self.size):
            row = []
            for col_index in range(self.size):
                row.append(input_list[row_index * self.size + col_index])
            formated.append(row)
        return formated

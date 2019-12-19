class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal
        self.forward_goal = [goal]
        self.backward_goal = [initial]

    def actions(self, action):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return any(state is x for x in self.goal)
            # return is_in(state, self.goal)
        else:
            return state == self.goal

    def goal_test_forward(self, state):
        if isinstance(self.forward_goal, list):
            re = []
            for x in self.forward_goal:
                re.append(state == x)
            return any(re)
            # return any(state is x for x in self.forward_goal)
            # return is_in(state, self.goal)
        else:
            return state == self.forward_goal

    def goal_test_backward(self, state):
        if isinstance(self.backward_goal, list):
            re = []
            for x in self.backward_goal:
                re.append(state == x)
            return any(re)

            # return any(state is x for x in self.backward_goal)
            # return is_in(state, self.goal)
        else:
            return state == self.backward_goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

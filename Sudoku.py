from copy import deepcopy

from Problem import Problem
from Node import Node
import CSP


class SudokuProblem(Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.num_assign = 0

    def assign(self, variable, value, assignment):
        assignment[variable] = value
        self.num_assign += 1

    def resign(self, variable, assignment):
        if variable in assignment:
            del assignment[variable]

    def num_conflicts(self, variable, value, assignment):
        count = 0
        for v in self.neighbors[variable]:
            if v in assignment and not self.constraints(variable, value, v, assignment[v]):
                count += 1

        def conflict(variable2):
            return variable2 in assignment and not self.constraints(variable, value, variable2, assignment[variable2])

        return count

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, variable, value):
        self.support_pruning()
        removals = [(variable, a) for a in self.curr_domains[variable] if a != value]
        self.curr_domains[variable] = [value]
        return removals

    def prune(self, variable, value, removals):
        """Rule out var=value."""
        self.curr_domains[variable].remove(value)
        if removals is not None:
            removals.append((variable, value))

    def choices(self, variable):
        return (self.curr_domains or self.domains)[variable]

    def actions(self, state):
        for (x, y) in self.domains:
            if (x, y) not in state:
                return list({(x, y): var} for var in domains_org[(x, y)])
        return None

    def result(self, state, action):

        return state.update(action)

    def scope_check(self, state, action):
        return None

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}


group_num = [[0, 0, 0, 1, 1, 1, 2, 2, 2],
             [0, 0, 0, 1, 1, 1, 2, 2, 2],
             [0, 0, 0, 1, 1, 1, 2, 2, 2],
             [3, 3, 3, 4, 4, 4, 5, 5, 5],
             [3, 3, 3, 4, 4, 4, 5, 5, 5],
             [3, 3, 3, 4, 4, 4, 5, 5, 5],
             [6, 6, 6, 7, 7, 7, 8, 8, 8],
             [6, 6, 6, 7, 7, 7, 8, 8, 8],
             [6, 6, 6, 7, 7, 7, 8, 8, 8]]

pro_o = [[0, 0, 0, 2, 0, 9, 3, 0, 7],
         [0, 5, 0, 0, 0, 0, 2, 0, 1],
         [4, 2, 0, 7, 0, 0, 0, 0, 5],
         [0, 0, 7, 0, 4, 0, 6, 3, 0],
         [0, 0, 0, 6, 0, 5, 0, 0, 0],
         [0, 3, 6, 0, 9, 0, 5, 0, 0],
         [3, 0, 0, 0, 0, 1, 0, 2, 8],
         [8, 0, 4, 0, 0, 0, 0, 9, 0],
         [1, 0, 2, 4, 0, 3, 0, 0, 0]]

pro = [[0, 0, 0, 2, 0, 9, 3, 0, 7],
       [0, 5, 0, 0, 0, 0, 2, 0, 1],
       [4, 0, 0, 7, 0, 0, 0, 0, 5],
       [0, 0, 7, 0, 4, 0, 6, 3, 0],
       [0, 0, 0, 6, 0, 5, 0, 0, 0],
       [0, 3, 6, 0, 9, 0, 5, 0, 0],
       [3, 0, 0, 0, 0, 1, 0, 2, 8],
       [8, 0, 4, 0, 0, 0, 0, 9, 0],
       [1, 0, 2, 4, 0, 3, 0, 0, 0]]


groups = [[] for _ in range(9)]
domains_org = {}
neighbors_org = {}

# for i in range(9):
#     groups.append([])

for x in range(9):
    for y in range(9):
        if pro[x][y] == 0:
            domains_org[(x, y)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            domains_org[(x, y)] = [pro[x][y]]

        groups[group_num[x][y]].append((x, y))


for x in range(9):
    for y in range(9):
        temp = []
        temp.extend(groups[group_num[x][y]])
        temp.extend((row, y) for row in range(9) if (row, y) not in temp)
        temp.extend((x, col) for col in range(9) if (x, col) not in temp)
        temp.remove((x, y))
        neighbors_org[(x, y)] = temp

su = SudokuProblem(variables=None, domains=domains_org, neighbors=neighbors_org, constraints=CSP.different_values_constraint)
re, ch = CSP.AC3(su)


def goal_test(state):
    return len(state) == len(pro)


print()

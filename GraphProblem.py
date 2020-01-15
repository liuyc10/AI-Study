from Problem import Problem
import utils


class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, a):
        return list(self.graph.get(a).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost_so_far, a, action, b):
        return cost_so_far + (self.graph.get(a, b) or utils.inf)

    def find_min_edge(self):
        """Find minimum value of edges."""
        m = utils.inf
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)
        return m

    def h(self, node):
        """h function is straight-line distance from a node's state to goal."""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(utils.distance(locs[node], locs[self.goal]))
            return int(utils.distance(locs[node.state], locs[self.goal]))
        else:
            return utils.inf

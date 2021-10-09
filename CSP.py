from operator import neg

from sortedcontainers import SortedSet


def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)


def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def no_inference(csp, var, value, assignment, removals):
    return True


def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def dom_j_up(csp, queue):
    """sorted by neighbor's values count"""
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))


def revise(csp, variable, neighbor, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[variable][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[neighbor]:
            if csp.constraints(variable, x, neighbor, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(variable, x, removals)
            revised = True
    return revised, checks


def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(variable, neighbor) for variable in csp.variables for neighbor in csp.neighbors[variable]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (variable, neighbor) = queue.pop()
        revised, checks = revise(csp, variable, neighbor, removals, checks)
        if revised:
            if not csp.curr_domains[variable]:
                return False, checks  # CSP is inconsistent
            for other_neighbors in csp.neighbors[variable]:
                if other_neighbors != neighbor:
                    queue.add((other_neighbors, variable))
    return True, checks  # CSP is satisfiable


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

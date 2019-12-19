from GraphProblem import GraphProblem
from RomaniaMap import romania_map
from Search import best_first_graph_search

"""romania_problem = GraphProblem('Arad', 'Neamt', romania_map)

print('Breadth-first Tree search')
result_node = breadth_first_tree_search(romania_problem)
if result_node is not None:
    final_path = result_node.solution()
    print(final_path)
else:
    print('failed')"""

initial = 'Arad'
goal = 'Bucharest'

"""romania_problem = GraphProblem(initial, goal, romania_map)

print('bidirectional_bread_first_graph_search')
result_node = bidirectional_bread_first_graph_search(romania_problem)
if result_node is not None:
    path_forward = result_node[0].solution()
    path_backward = result_node[1].solution()
    path_backward.reverse()
    final_path = [initial]
    final_path.extend(path_forward)
    final_path.extend(path_backward)
    final_path.extend([goal])
    print(final_path)
else:
    print('failed')"""

print('Uniform_search')
romania_problem = GraphProblem(initial, goal, romania_map)
result_node = best_first_graph_search(romania_problem, lambda x: x.path_cost)
if result_node is not None:
    final_path = result_node.solution()
    print(final_path)
else:
    print('failed')


print('AStar_search')
romania_problem = GraphProblem(initial, goal, romania_map)
result_node = best_first_graph_search(romania_problem, lambda x: x.path_cost + romania_problem.h(x))
if result_node is not None:
    final_path = result_node.solution()
    print(final_path)
else:
    print('failed')

"""romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)
print('depth_first_tree_search')
result_node = depth_first_tree_search(romania_problem)
if result_node is not None:
    final_path = result_node.solution()
    print(final_path)
else:
    print('failed')

romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)
print('depth_first_graph_search')
result_node = depth_first_graph_search(romania_problem)
if result_node is not None:
    final_path = result_node.solution()
    print(final_path)
else:
    print('failed')

romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)
print('breadth_first_graph_search')
result_node = breadth_first_graph_search(romania_problem)
if result_node is not None:
    final_path = result_node.solution()
    print(final_path)
else:
    print('failed')"""

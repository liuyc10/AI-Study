from GeneticAlgorithm import *


rd = [0, 2, 4, 7, 4, 8, 5, 5, 2]


def test_fitness():
    score = fitness_fn(rd)
    assert score == 24

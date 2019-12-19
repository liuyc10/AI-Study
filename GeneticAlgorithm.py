import copy
import random
from datetime import datetime

from utils import random_selection, reproduce, mutation


def fitness_fn(ind, score=0):
    for n in range(1, len(ind)):
        for y in range(n + 1, len(ind)):
            if ind[n] == ind[y]:
                score += 1
            elif abs(ind[n] - ind[y]) == (n - y):
                score += 1
    return score


def generate_new_population(population, weights, size, mutation_rate=0.1):
    dna_set = [1, 2, 3, 4, 5, 6, 7, 8]
    new_population = []
    for _ in range(size):
        ind_x = random_selection(population, weights)
        ind_y = random_selection(population, weights)
        xy = reproduce(ind_x, ind_y)
        mutated_xy = mutation(xy, dna_set, mutation_rate)
        # mutated_xy[0] = fitness_fn(mutated_xy)
        new_population.append(mutated_xy)
    return new_population


def weight(population, target_score):
    fitness_score = []
    for idv in population:
        fitness_score.append(fitness_fn(idv, target_score))
    weights = []
    sums = sum(fitness_score)
    for score in fitness_score:
        if score == 0:
            weights.append(-1)
        else:
            weights.append(1 - score / sums)
    return weights


def GeneticAlgorithm(population, mutation_rate, generation_limit=None, target_score=0):
    population_size = len(population)
    if generation_limit:
        for gen in range(generation_limit):
            weights = weight(population, target_score)
            for i, w in zip(population, weights):
                if w == -1:
                    return gen, i
            population = generate_new_population(population, weights, population_size, mutation_rate)
    else:
        gen = 0
        while True:
            weights = weight(population)
            for i, w in zip(population, weights):
                if w == -1:
                    return gen, i
            population = generate_new_population(population, weights, population_size, mutation_rate)
            gen += 1
    return -1, -1


dna = [1, 2, 3, 4, 5, 6, 7, 8]
initial_population = []

for _ in range(100):
    individual = []
    for x in range(len(dna) + 1):
        individual.append(random.choice(dna))
    initial_population.append(individual)
print(initial_population)

results = set()
result_list = []
count = 0

total_start = datetime.now()
for test_round in range(500):
    start = datetime.now()
    gene, result = GeneticAlgorithm(copy.deepcopy(initial_population), 0.2, 100000)
    end = datetime.now()
    re = str(test_round) + '\t\t' + str(end - start) + '\t\t' + str(gene) + '  \t\t' + str(result[1:])

    result_list.append(re)
    if gene == -1:
        print(str(test_round) + '  \t' + 'No result')
        continue
    str_result = ''.join([str(i) for i in result[1:]])
    if str_result in results:
        print(re + '\t\t' + 'duplicated')
    else:
        print(re + '\t\t' + str(count))
        results.add(str_result)
        count += 1
        if count == 92:
            break


print(str(datetime.now()-total_start) + '\t' + str(count))
print(results)

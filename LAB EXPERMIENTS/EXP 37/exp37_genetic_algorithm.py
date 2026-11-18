import random

# Genetic algorithm that maximizes f(x) = x^2 for x in [0, 31]
POPULATION_SIZE = 20
GENES = 5
GENERATIONS = 30
MUTATION_RATE = 0.1


def fitness(chromosome):
    x = int("".join(str(gene) for gene in chromosome), 2)
    return x ** 2


def generate_population():
    return [[random.randint(0, 1) for _ in range(GENES)]
            for _ in range(POPULATION_SIZE)]


def tournament_selection(population, tournament_size=3):
    candidates = random.sample(population, tournament_size)
    return max(candidates, key=fitness)


def crossover(parent1, parent2):
    point = random.randint(1, GENES - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]


def mutate(chromosome):
    chromosome = chromosome.copy()
    for index in range(GENES):
        if random.random() < MUTATION_RATE:
            chromosome[index] = 1 - chromosome[index]
    return chromosome


random.seed(42)
population = generate_population()

for generation in range(GENERATIONS):
    population = sorted(population, key=fitness, reverse=True)
    next_population = population[:2]

    while len(next_population) < POPULATION_SIZE:
        parent1 = tournament_selection(population)
        parent2 = tournament_selection(population)
        child1, child2 = crossover(parent1, parent2)
        next_population.append(mutate(child1))
        if len(next_population) < POPULATION_SIZE:
            next_population.append(mutate(child2))

    population = next_population

population = sorted(population, key=fitness, reverse=True)
best_chromosome = population[0]
best_x = int("".join(str(gene) for gene in best_chromosome), 2)
print(f"Best solution found: x = {best_x}")
print(f"Maximum fitness f(x) = x^2 = {fitness(best_chromosome)}")

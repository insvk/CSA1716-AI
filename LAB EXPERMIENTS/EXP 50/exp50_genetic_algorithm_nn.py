import random

import numpy as np

# Evolve a small neural-network population for the XOR problem.
INPUTS = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
TARGETS = np.array([[0], [1], [1], [0]], dtype=float)

INPUT_SIZE = 2
HIDDEN_SIZE = 4
OUTPUT_SIZE = 1
CHROMOSOME_SIZE = INPUT_SIZE * HIDDEN_SIZE + HIDDEN_SIZE + HIDDEN_SIZE * OUTPUT_SIZE + OUTPUT_SIZE

POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.10
MUTATION_SCALE = 0.20
ELITE_COUNT = 10
rng = np.random.default_rng(42)


def sigmoid(value):
    return 1.0 / (1.0 + np.exp(-np.clip(value, -500.0, 500.0)))


def decode(chromosome):
    start = 0
    end = INPUT_SIZE * HIDDEN_SIZE
    w1 = chromosome[start:end].reshape(INPUT_SIZE, HIDDEN_SIZE)

    start, end = end, end + HIDDEN_SIZE
    b1 = chromosome[start:end]

    start, end = end, end + HIDDEN_SIZE * OUTPUT_SIZE
    w2 = chromosome[start:end].reshape(HIDDEN_SIZE, OUTPUT_SIZE)

    b2 = chromosome[end:end + OUTPUT_SIZE]
    return w1, b1, w2, b2


def predict(chromosome, inputs):
    w1, b1, w2, b2 = decode(chromosome)
    hidden = sigmoid(inputs @ w1 + b1)
    return sigmoid(hidden @ w2 + b2)


def fitness(chromosome):
    predictions = predict(chromosome, INPUTS)
    mse = np.mean((predictions - TARGETS) ** 2)
    return -mse


def crossover(parent1, parent2):
    point = int(rng.integers(1, CHROMOSOME_SIZE))
    return np.concatenate((parent1[:point], parent2[point:]))


def mutate(chromosome):
    child = chromosome.copy()
    for index in range(CHROMOSOME_SIZE):
        if rng.random() < MUTATION_RATE:
            child[index] += rng.normal(0.0, MUTATION_SCALE)
    return child


population = [rng.normal(0.0, 0.5, CHROMOSOME_SIZE) for _ in range(POPULATION_SIZE)]

for generation in range(GENERATIONS):
    ranked = sorted(population, key=fitness, reverse=True)
    best_fitness = fitness(ranked[0])

    if best_fitness >= -0.01:
        print(f"Solved in generation {generation}: MSE={-best_fitness:.6f}")
        break

    new_population = ranked[:ELITE_COUNT]
    while len(new_population) < POPULATION_SIZE:
        parent1 = random.choice(ranked[:POPULATION_SIZE // 2])
        parent2 = random.choice(ranked[:POPULATION_SIZE // 2])
        new_population.append(mutate(crossover(parent1, parent2)))

    population = new_population

best = max(population, key=fitness)
predictions = predict(best, INPUTS)
print("Best network predictions:")
for input_row, prediction in zip(INPUTS, predictions):
    print(f"Input: {input_row.astype(int).tolist()} -> Output: {prediction[0]:.4f}")
print(f"Best MSE: {-fitness(best):.6f}")

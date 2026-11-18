import numpy as np

# Genetic Algorithm to evolve weights of a tiny Neural Network
# Problem: Evolve a network to solve the AND logic gate
inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
targets = np.array([0, 0, 0, 1])

POPULATION_SIZE = 20
GENERATIONS = 100

# Initialize population (chromosome = 2 weights and 1 bias)
population = [np.random.randn(3) for _ in range(POPULATION_SIZE)]

def activate(x, weights):
    # Linear combination + step activation function
    return 1 if (np.dot(x, weights[:2]) + weights[2]) > 0 else 0

def fitness(weights):
    # Fitness is the number of correct predictions (max 4)
    score = sum([1 for x, y in zip(inputs, targets) if activate(x, weights) == y])
    return score

print("Starting Evolution...")
for gen in range(GENERATIONS):
    population.sort(key=fitness, reverse=True)
    if fitness(population[0]) == 4:
        print(f"Solved in generation {gen}!")
        break
    
    # Crossover and Mutate to evolve next generation
    next_gen = population[:2] # Elitism (keep top 2)
    while len(next_gen) < POPULATION_SIZE:
        p1, p2 = population[0], population[1]
        child = (p1 + p2) / 2.0 + (np.random.randn(3) * 0.2) # Avg + Mutation
        next_gen.append(child)
    population = next_gen

best_weights = max(population, key=fitness)
print("\nBest Weights found:", best_weights)
print("Testing Evolved Neural Network:")
for x in inputs:
    print(f"Input: {x} -> Output: {activate(x, best_weights)}")

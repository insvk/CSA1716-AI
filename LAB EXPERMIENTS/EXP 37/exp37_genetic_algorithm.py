import random

# Simple GA to optimize f(x) = x^2 where x is between 0 and 31 (5-bit string)
POPULATION_SIZE = 10
GENES = 5
GENERATIONS = 20

def fitness(chromosome):
    # Convert binary list to integer and square it
    x = int("".join(str(gene) for gene in chromosome), 2)
    return x ** 2

def generate_population():
    return [[random.randint(0, 1) for _ in range(GENES)] for _ in range(POPULATION_SIZE)]

population = generate_population()

for generation in range(GENERATIONS):
    # Sort population by fitness
    population = sorted(population, key=fitness, reverse=True)
    
    # Crossover and Mutate to create next generation
    next_gen = population[:2] # Elitism (keep top 2)
    while len(next_gen) < POPULATION_SIZE:
        p1, p2 = random.choices(population[:5], k=2)
        crossover_point = random.randint(1, GENES-1)
        child = p1[:crossover_point] + p2[crossover_point:]
        
        # Mutation
        if random.random() < 0.1:
            mutate_point = random.randint(0, GENES-1)
            child[mutate_point] = 1 - child[mutate_point]
            
        next_gen.append(child)
    population = next_gen

best_solution = sorted(population, key=fitness, reverse=True)[0]
best_x = int("".join(str(g) for g in best_solution), 2)
print(f"Best solution found: x = {best_x}, f(x) = {fitness(best_solution)}")
import random

# Define the function to optimize
def fitness(x):
    return 2 * (x ** 2) - 1

# Binary encoding and decoding
def encode(x):
    return format(x, '06b')

def decode(binary_str):
    return int(binary_str, 2)

# Generate initial population
def initialize_population(size):
    return [encode(random.randint(0, 31)) for _ in range(size)]

# Tournament selection
def tournament_selection(population, k=3):
    selected = random.sample(population, k)
    return max(selected, key=lambda ind: fitness(decode(ind)))

# Uniform crossover
def uniform_crossover(parent1, parent2):
    child = ''.join(p1 if random.random() < 0.5 else p2 for p1, p2 in zip(parent1, parent2))
    return child

# Adaptive mutation
def mutate(individual, gen, max_gens):
    mutation_rate = max(0.1, 0.5 * (1 - gen / max_gens))  # Higher at start, reduces over time
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = '1' if individual[i] == '0' else '0'
    return ''.join(individual)

# Genetic Algorithm
def genetic_algorithm(pop_size=10, max_gens=50):
    population = initialize_population(pop_size)
    best_individual = max(population, key=lambda ind: fitness(decode(ind)))
    
    for gen in range(max_gens):
        new_population = []
        for _ in range(pop_size // 2):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1 = uniform_crossover(parent1, parent2)
            child2 = uniform_crossover(parent2, parent1)
            child1 = mutate(child1, gen, max_gens)
            child2 = mutate(child2, gen, max_gens)
            new_population.extend([child1, child2])
        
        population = new_population
        current_best = max(population, key=lambda ind: fitness(decode(ind)))
        if fitness(decode(current_best)) > fitness(decode(best_individual)):
            best_individual = current_best
    
    return decode(best_individual), fitness(decode(best_individual))

# Run the algorithm
best_x, best_fitness = genetic_algorithm()
print(f"Best x: {best_x}, Best fitness: {best_fitness}")

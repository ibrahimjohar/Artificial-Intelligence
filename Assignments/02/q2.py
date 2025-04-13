#q2

import random

# Task definitions: (task id: time required in hours)
tasks = {
    0: 5,  # Task 1
    1: 8,  # Task 2
    2: 4,  # Task 3
    3: 7,  # Task 4
    4: 6,  # Task 5
    5: 3,  # Task 6
    6: 9   # Task 7
}

# Facility capacities (in hours per day)
capacities = {
    0: 24,  # Facility 1
    1: 30,  # Facility 2
    2: 28   # Facility 3
}

# Cost matrix: cost per hour for each task at each facility.
# Indexed as cost_matrix[task][facility]
cost_matrix = {
    0: [10, 12, 9],  # Task 1
    1: [15, 14, 16], # Task 2
    2: [8, 9, 7],    # Task 3
    3: [12, 10, 13], # Task 4
    4: [14, 13, 12], # Task 5
    5: [9, 8, 10],   # Task 6
    6: [11, 12, 13]  # Task 7
}

# GA parameters
POPULATION_SIZE = 6
GENERATIONS = 50
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2

def random_chromosome():
    """Generate a random assignment of tasks to facilities (chromosome)."""
    # Each gene is an integer 0, 1, or 2 (three facilities)
    return [random.randint(0, 2) for _ in tasks]

def evaluate(chromosome):
    """
    Calculate the total cost of a chromosome.
    Also checks capacity constraints – if exceeded, adds a penalty.
    Lower cost is better.
    """
    facility_time = {0: 0, 1: 0, 2: 0}
    total_cost = 0
    for task, facility in enumerate(chromosome):
        time = tasks[task]
        cost_rate = cost_matrix[task][facility]
        total_cost += time * cost_rate
        facility_time[facility] += time

    # Check capacity constraints; if any facility is over-capacity add heavy penalty
    penalty = 0
    for facility, used_time in facility_time.items():
        if used_time > capacities[facility]:
            penalty += (used_time - capacities[facility]) * 100  # arbitrary high penalty

    return total_cost + penalty

def roulette_wheel_selection(population, fitnesses):
    """Select one chromosome from the population using roulette wheel selection."""
    # In our case, lower fitness is better so we need to invert the fitness for probabilities.
    # Adding a constant to avoid division by zero.
    max_fit = max(fitnesses)
    # For minimization, we can compute scores as: score = (max_fit - fitness + 1)
    scores = [max_fit - f + 1 for f in fitnesses]
    total_score = sum(scores)
    pick = random.uniform(0, total_score)
    current = 0
    for i, score in enumerate(scores):
        current += score
        if current > pick:
            return population[i]

def one_point_crossover(parent1, parent2):
    """Perform one-point crossover between two parents."""
    point = random.randint(1, len(parent1)-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def swap_mutation(chromosome):
    """Perform swap mutation: swap the allocation of two random tasks."""
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

def genetic_algorithm():
    # Initialize population
    population = [random_chromosome() for _ in range(POPULATION_SIZE)]
    best_solution = None
    best_fitness = float('inf')
    
    for gen in range(GENERATIONS):
        # Evaluate population
        fitnesses = [evaluate(individual) for individual in population]
        
        # Track best solution
        for i in range(POPULATION_SIZE):
            if fitnesses[i] < best_fitness:
                best_fitness = fitnesses[i]
                best_solution = population[i]
        
        # Create new population
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            # Selection: choose two parents
            parent1 = roulette_wheel_selection(population, fitnesses)
            parent2 = roulette_wheel_selection(population, fitnesses)
            
            # Crossover
            if random.random() < CROSSOVER_RATE:
                child1, child2 = one_point_crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            
            # Mutation
            if random.random() < MUTATION_RATE:
                child1 = swap_mutation(child1)
            if random.random() < MUTATION_RATE:
                child2 = swap_mutation(child2)
            
            new_population.extend([child1, child2])
        
        # Make sure our new population has exactly POPULATION_SIZE individuals
        population = new_population[:POPULATION_SIZE]
        print(f"Generation {gen+1}: Best Fitness = {best_fitness}")
    
    return best_solution, best_fitness

best_assignment, best_cost = genetic_algorithm()
print("\nBest Task Assignment (Facility indices for Tasks 1-7):")
print(best_assignment)
print("Total cost (including penalties if any):", best_cost)

#Evolutionary Search Algorithms:
# Start with a Population
# Evaluate Fitness
# Select the best
# Combine Traits(crossover)
# Introduce Random Changes(mutation)
# Repeat over generations

#Types Of Evolutionary Search Algorithms:
# Genetic Algorithms (GAs): The most well-known evolutionary search method,relies heavily on crossover and mutation.
# Genetic Programming (GP): Extends GAs to evolve computer programs or mathematical expressions.
# Evolution Strategies (ES): Focuses on continuous optimization problems, emphasizes mutation and self-adaptation of parameters.
# Differential Evolution (DE): A variant of GAs designed for continuous optimization, uses a difference vector to create new candidate solutions.
# Particle Swarm Optimization (PSO): Inspired by the social behavior of birds and fish, individuals (particles) move through the search space based on their own experience and the experience of the group.

#Genetic Algorithm:
# Population 
# Fitness function
# Selection
# Crossover
# Mutation
# Generations

import random
import math

#Traveling Salesman Problem(TSP):

#locations w (x,y) coordinates
locations = [(0,0), (1,5), (2,3), (5,2), (6,6)]

#fitness function: calc the total dist of a route
def calculate_distance(route):
    total_distance = 0
    for i in range(len(route) - 1): #loop over all locations
        x1, y1 = locations[route[i]]        #coordinates at i
        x2, y2 = locations[route[i + 1]]    #coordinates at j
        
        #dist between the above two cities
        total_distance += math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    return total_distance

#INITIALIZE A POPULATION
#generate a random route
#10 rand routes generated
def create_random_route():
    route = list(range(len(locations)))
    random.shuffle(route)
    return route

population_size = 10
population = [create_random_route() for _ in range(population_size)]
print("initial population: ", population)


#FITNESS SCORE EVAL
fitness_scores = [calculate_distance(route) for route in population]
print("fitness scores: ", fitness_scores)

#SELECTION
#select best routes (parents) based on fitness
def select_parents(population, fitness_scores):
    #select top 50% of population
    sorted_population = [route for _, route in sorted(zip(fitness_scores, population))]
    return sorted_population[:len(population)//2]

parents = select_parents(population, fitness_scores)
print("selected parents: ", parents)

#CROSSOVER
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = parent1[start:end]
    
    for gene in parent2:
        if gene not in child:
            child.append(gene)
    return child


#create new population using crossover
new_population = []
for i in range(population_size):
    parent1, parent2 = random.sample(parents, 2)
    child = crossover(parent1, parent2)
    new_population.append(child)
print("new population after crossover: ", new_population)

#MUTATION
#rand swap 2 locations in a route
def mutate(route):
    idx1, idx2 = random.sample(range(len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

mutation_rate = 0.1
for i in range(len(new_population)):
    if random.random() < mutation_rate:
        new_population[i] = mutate(new_population[i])
print("population after mutation: ", new_population)

#CONVERGENCE CHECK
# Convergence criteria: Stop if no improvement for 10 generations
best_fitness = min(fitness_scores)
no_improvement_count = 0
max_generations = 100
generation = 0

while generation < max_generations and no_improvement_count < 10:
    #eval fitness of new population in each gen
    fitness_scores = [calculate_distance(route) for route in new_population]
    current_best_fitness = min(fitness_scores)
    
    #update best_fitness if a better route is found
    if current_best_fitness < best_fitness:
        best_fitness = current_best_fitness
        no_improvement_count = 0
    else:
        no_improvement_count += 1
        
    #selects parents from curr population based on fitness
    parents = select_parents(new_population, fitness_scores)
    
    #generates new population using crossover
    new_population = [crossover(random.choice(parents), random.choice(parents))
                      for _ in range(population_size)]
    
    #applies mutataion to the new population with a small probablity 
    for i in range(len(new_population)):
        if random.random() < mutation_rate:
            new_population[i] = mutate(new_population[i])
            
    #proceed to next generation
    generation += 1
    
print("best route: ", new_population[fitness_scores.index(min(fitness_scores))])
print("best distance: ", min(fitness_scores))

#output:
# initial population:  [[3, 0, 4, 1, 2], [2, 4, 3, 0, 1], [1, 3, 2, 0, 4], [4, 0, 3, 2, 1], [4, 3, 2, 1, 0], [2, 3, 4, 0, 1], [0, 2, 1, 4, 3], [2, 4, 3, 1, 0], [1, 0, 2, 3, 4], [1, 3, 0, 2, 4]]
# fitness scores:  [21.205533672465645, 19.60728994634495, 20.25311030987094, 19.26879181904124, 14.620470776878614, 20.869684173617394, 15.063744392174225, 19.222125139210448, 15.989954074842814, 18.990716082598496]
# selected parents:  [[4, 3, 2, 1, 0], [0, 2, 1, 4, 3], [1, 0, 2, 3, 4], [1, 3, 0, 2, 4], [2, 4, 3, 1, 0]]
# new population after crossover:  [[0, 2, 4, 3, 1], [4, 3, 2, 1, 0], [3, 0, 4, 2, 1], [1, 3, 0, 2, 4], [3, 0, 2, 4, 1], [4, 3, 2, 1, 0], [2, 1, 0, 3, 4], [1, 0, 2, 4, 3], [2, 1, 4, 0, 3], [1, 3, 2, 4, 0]]
# population after mutation:  [[0, 2, 4, 3, 1], [4, 3, 2, 1, 0], [3, 0, 4, 2, 1], [1, 3, 0, 2, 4], [3, 0, 2, 4, 1], [4, 3, 2, 1, 0], [2, 1, 0, 3, 4], [1, 0, 2, 4, 3], [2, 1, 4, 0, 3], [1, 3, 2, 4, 0]]
# best route:  [3, 1, 2, 4, 0]
# best distance:  14.620470776878614
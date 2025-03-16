import numpy as np
import random

num_cities = 10
population_size = 100
mutation_rate = 0.1
generations = 500

#generate random cities (x,y coordinates)
cities = np.random.rand(num_cities, 2) * 100

def distance(city1, city2):
    return np.linalg.norm(city1 - city2)

def total_distance(path):
    return sum(distance(cities[path[i]], cities[path[i + 1]]) for i in range(num_cities - 1)) + distance(cities[path[-1]], cities[path[0]])

def create_individual():
    return random.sample(range(num_cities), num_cities)

def create_population():
    return [create_individual() for _ in range(population_size)]

def select_parents(population):
    tournament = random.sample(population, 5)
    return min(tournament, key=total_distance)

def ordered_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(num_cities), 2))
    child = [-1] * num_cities
    child[start:end] = parent1[start:end]
    fill_values = [city for city in parent2 if city not in child]
    idx = 0
    for i in range(num_cities):
        if child[i] == -1:
            child[i] = fill_values[idx]
            idx += 1
    return child

def mutate(individual):
    if random.random() < mutation_rate:
        i, j = random.sample(range(num_cities), 2)
        individual[i], individual[j] = individual[j], individual[i]
        
def genetic_algorithm():
    population = create_population()
    
    for generation in range(generations):
        population = sorted(population, key=total_distance)
        new_population = [population[0]]
        
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population), select_parents(population)
            child = ordered_crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)
            
        population = new_population
        
        if generation % 50 == 0:
            print(f"generation {generation}: best distance = {total_distance(population[0]):.2f}")
            
    best_path = population[0]
    print(f"Best Path Found: {best_path}")
    print(f"Best Distance: {total_distance(best_path):.2f}")
    
    return best_path

best_path = genetic_algorithm()
        
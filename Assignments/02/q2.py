import random

#parameters for GA
populationSize = 6
generations = 5 #num of iterations
crossoverRate = 0.8
mutationRate = 0.2

#data
#task durations(hours)
task_times = [5, 8, 4, 7, 6, 3, 9]
#facility capacities
facility_capacities = {
    1: 24,
    2: 30,
    3: 28
}
#cost matrix [task][facility]
cost_matrix = {
    1: [10, 12, 9],
    2: [15, 14, 16],
    3: [8, 9, 7],
    4: [12, 10, 13],
    5: [14, 13, 12],
    6: [9, 8, 10],
    7: [11, 12, 13],
}

def calculate_cost(chromosome):
    facility_load = {1: 0, 2: 0, 3: 0}
    total_cost = 0
    
    for i, facility in enumerate(chromosome):
        task = i + 1
        time = task_times[i]
        cost = cost_matrix[task][facility - 1]
        facility_load[facility] += time
        total_cost += time * cost

    penalty = 0
    for f in facility_load:
        if facility_load[f] > facility_capacities[f]:
            penalty += (facility_load[f] - facility_capacities[f]) * 100
    return total_cost + penalty

def fitness(cost):
    return 1 / cost

def roulette_selection(pop, fits):
    total_fit = sum(fits)
    r = random.uniform(0, total_fit)
    accum = 0
    
    for ind, f in zip(pop, fits):
        accum += f
        if accum >= r:
            return ind
    return pop[-1]

def one_point_crossover(p1, p2):
    point = random.randint(1, len(p1)-2)
    return p1[:point]+p2[point:], p2[:point]+p1[point:]

def swap_mutation(chrom):
    i, j = random.sample(range(len(chrom)), 2)
    chrom[i], chrom[j] = chrom[j], chrom[i]
    return chrom

def genetic_algorithm():
    population = [
        [2, 1, 1, 3, 2, 2, 1],
        [1, 2, 3, 1, 2, 3, 3],
        [3, 3, 2, 2, 1, 1, 2],
        [2, 2, 1, 1, 3, 3, 3],
        [1, 3, 2, 3, 1, 2, 1],
        [3, 1, 3, 2, 2, 1, 2],
    ]

    best_cost = float('inf')
    best_chrom = None

    for gen in range(generations):
        costs = [calculate_cost(ch) for ch in population]
        fits = [fitness(c) for c in costs]

        print(f"\ngeneration {gen+1}")
        for i in range(len(population)):
            print(f"{i+1}. {population[i]} - cost: {costs[i]}")

        for i in range(populationSize):
            if costs[i] < best_cost:
                best_cost = costs[i]
                best_chrom = population[i]

        new_pop = []
        while len(new_pop) < populationSize:
            p1 = roulette_selection(population, fits)
            p2 = roulette_selection(population, fits)
            
            if random.random() < crossoverRate:
                c1, c2 = one_point_crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]
            
            if random.random() < mutationRate:
                c1 = swap_mutation(c1)
            
            if random.random() < mutationRate:
                c2 = swap_mutation(c2)
            new_pop.extend([c1, c2])

        population = new_pop[:populationSize]

    print("\nbest assignment:")
    print("chromosome:", best_chrom)
    print("min cost:", best_cost)


genetic_algorithm()

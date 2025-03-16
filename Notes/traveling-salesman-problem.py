from collections import deque
from itertools import permutations

# Example graph representing distances between cities (adjacency matrix)
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

num_cities = len(graph)

def bfs_tsp(graph, start=0):
    queue = deque()
    queue.append((start, 1 << start, 0, [start]))  # (current_city, visited_mask, cost, path)
    min_cost = float("inf")
    best_path = []
    
    while queue:
        city, visited, cost, path = queue.popleft()
        
        # If all cities are visited, return to start
        if visited == (1 << num_cities) - 1:
            total_cost = cost + graph[city][start]  # Complete the cycle
            if total_cost < min_cost:
                min_cost = total_cost
                best_path = path + [start]
            continue
        
        # Explore neighbors
        for next_city in range(num_cities):
            if not (visited & (1 << next_city)):  # If not visited
                new_visited = visited | (1 << next_city)
                new_cost = cost + graph[city][next_city]
                queue.append((next_city, new_visited, new_cost, path + [next_city]))
    
    return min_cost, best_path

# Running BFS-based TSP
optimal_cost, optimal_path = bfs_tsp(graph)
print("Optimal Cost:", optimal_cost)
print("Optimal Path:", optimal_path)

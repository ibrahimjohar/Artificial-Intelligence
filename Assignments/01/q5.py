#Ibrahim Johar Farooqi - 23K-0074 - BAI-4A - AI Assignment 01
import heapq

#romania map graph (adjacency list), where the graph is initialized as a dictionary, each key is a city & the value is a list of tuples (neighbor, cost)
romania_map = {
    'Arad': [('Zerind', 75), ('Timisoara', 118), ('Sibiu', 140)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Pitesti', 97), ('Craiova', 146)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Bucharest', 101), ('Craiova', 138)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Pitesti', 138), ('Rimnicu Vilcea', 146)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Vaslui', 142), ('Hirsova', 98)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

#heuristics (straight line distances to bucharest)  
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

#breadth-first search (BFS) -> explores nodes level by level & does not consider costs & might not always yield optimal path
def bfs(graph, start, goal):
    queue = [(start, [start], 0)]  #(current node, path, total cost)
    while queue:
        current, path, cost = queue.pop(0)
        if current == goal:
            return path, cost
        for neighbor, distance in graph[current]:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor], cost + distance))
    return None, float('inf')

#uniform cost search (UCS) -> uses priority queue to always expand the least-cost city first, uses costs & ensures shortest/optimal path
def ucs(graph, start, goal):
    pq = [(0, start, [start])]  #(cost, current node, path)
    visited = set()
    
    while pq:
        cost, current, path = heapq.heappop(pq)  #lowest-cost node extracted
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            return path, cost
        for neighbor, distance in graph[current]:
            if neighbor not in visited:
                heapq.heappush(pq, (cost + distance, neighbor, path + [neighbor]))
    return None, float('inf')

#greedy best-first search (GBFS) -> uses heuristics & picks cities that seem closer to the goal city & gurantees optimal path  
def gbfs(graph, start, goal):
    pq = [(heuristic[start], start, [start])]  #(heuristic cost, current node, path)
    visited = set()
    
    while pq:
        _, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            cost = sum(next(dist for nbr, dist in graph[path[i]] if nbr == path[i + 1]) for i in range(len(path) - 1))
            return path, cost
        for neighbor, _ in graph[current]:
            if neighbor not in visited:
                heapq.heappush(pq, (heuristic[neighbor], neighbor, path + [neighbor]))
    return None, float('inf')

#depth-limited search (DLS) used in IDDFS -> 
def dls(graph, current, goal, depth, path):
    if depth == 0 and current == goal:
        return path
    if depth > 0:
        for neighbor, _ in graph[current]:
            if neighbor not in path:
                new_path = dls(graph, neighbor, goal, depth - 1, path + [neighbor])
                if new_path:
                    return new_path
    return None

#iterative deepening depth-first search (IDDFS) -> performs depth limited DFS, increasing depth incremently, & is optimal for uniform cost graphs
def iddfs(graph, start, goal, max_depth=10):
    for depth in range(max_depth):
        result = dls(graph, start, goal, depth, [start])
        if result:
            cost = sum(next(dist for nbr, dist in graph[result[i]] if nbr == result[i + 1]) for i in range(len(result) - 1))
            return result, cost
    return None, float('inf')


#running all algorithms and print results
start, goal = 'Arad', 'Bucharest'

bfs_path, bfs_cost = bfs(romania_map, start, goal)
ucs_path, ucs_cost = ucs(romania_map, start, goal)
gbfs_path, gbfs_cost = gbfs(romania_map, start, goal)
iddfs_path, iddfs_cost = iddfs(romania_map, start, goal)

print("Ibrahim Johar Farooqi - 23K-0074 - BAI-4A - AI Assignment 01\n")
print("running all search algorithms-")

def print_result(name, path, cost):
    if path:
        print(f"{name}: Path = {path}, Cost = {cost}")
    else:
        print(f"{name}: No path found.")

print_result("BFS", bfs_path, bfs_cost)
print_result("UCS", ucs_path, ucs_cost)
print_result("GBFS", gbfs_path, gbfs_cost)
print_result("IDDFS", iddfs_path, iddfs_cost)

#the results show that uniform cost search (ucs) to perform 
#the best, when 'ARAD' is start city & 'Bucharest' is the goal city
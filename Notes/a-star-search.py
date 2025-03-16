#a* evaluation function =>    f(n) = g(n) + h(n)

#g(n) -> cost so far to reach n
#h(n) -> estimated cost from n to goal
#f(n) -> estimated total cost of path through n to goal

graph = {
    'A': {'B': 2, 'C': 1},
    'B': {'D': 4, 'E': 3},
    'C': {'F': 1, 'G': 5},
    'D': {'H': 2},
    'E': {},
    'F': {'I': 6},
    'G': {},
    'H': {},
    'I': {}
}

#heuristic function (estimated cost to reach goal 'I')
heuristic = {
    'A': 7,
    'B': 6,
    'C': 5,
    'D': 4,
    'E': 7,
    'F': 3,
    'G': 6,
    'H': 2,
    'I': 0 # Goal node
}

#a* search function
def a_star(graph, start, goal):
    frontier = [(start, 0 + heuristic[start])] #list based priority queue(manually sorted)
    
    visited = set()
    g_costs = {start:0} #cost to reach each node from start
    came_from = {start: None} #path reconstruction
    
    while frontier:
        #sort frontier by f(n) = g(n) + h(n)
        frontier.sort(key=lambda x:x[1])
        current_node, current_f = frontier.pop(0) #get node w/ lowest f(n)
        
        if current_node in visited:
            continue
        
        print(current_node, end=" ") #print visited node
        visited.add(current_node)
        
        #if goal reached, reconstruct path
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"\ngoal found with A*. Path: {path}")
            return
        
        #explore neighbours
        for neighbour, cost in graph[current_node].items():
            new_g_cost = g_costs[current_node] + cost #path cost from start to neighbour
            f_cost = new_g_cost + heuristic[neighbour] #f(n) = g(n) + h(n)
            
            if neighbour not in g_costs or new_g_cost < g_costs[neighbour]:
                g_costs[neighbour] = new_g_cost
                came_from[neighbour] = current_node
                frontier.append((neighbour, f_cost))
    print("\ngoal not found")
    
#run 
print("\n A* search below:\n")
a_star(graph, 'A', 'F')
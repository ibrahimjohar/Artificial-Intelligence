from queue import PriorityQueue

# Example graph represented as an adjacency list with heuristic values included
graph = {
    'A': [('B', 5, 9), ('C', 8, 5)], # (neighbor, cost, heuristic)
    'B': [('D', 10, 4)], # (neighbor, cost, heuristic)
    'C': [('E', 3, 7)], # (neighbor, cost, heuristic)
    'D': [('F', 7, 5)], # (neighbor, cost, heuristic)
    'E': [('F', 2, 1)], # (neighbor, cost, heuristic)
    'F': [] # (neighbor, cost, heuristic)
}

def astar_search(graph, start, goal):
    visited = set() # Set to keep track of visited nodes
    
    pq = PriorityQueue() # Priority queue to prioritize nodes based on f-value (cost + heuristic)
    pq.put((0, start)) # Enqueue the start node with priority 0
    
    while not pq.empty():
        cost, node = pq.get() # Dequeue the node with the lowest priority
        if node not in visited:
            print(node, end=' ') # Print the current node
            visited.add(node) # Mark the current node as visited
            if node == goal: # Check if the goal node is reached
                print("\nGoal reached!")
                return True
            for neighbor, edge_cost, heuristic in graph[node]: # Explore neighbors of the current node
                if neighbor not in visited:
                    # Calculate f-value for the neighbor (cost + heuristic)
                    f_value = cost + edge_cost + heuristic
                    pq.put((f_value, neighbor)) # Enqueue neighbor with priority based on f-value
    print("\nGoal not reachable!")
    return False

# Example usage:
print("A* Search Path:")
astar_search(graph, 'A', 'F')
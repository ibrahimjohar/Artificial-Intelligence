from queue import PriorityQueue

graph = {
    'A': [('B', 5), ('C', 8)],
    'B': [('D', 10)],
    'C': [('E', 3)],
    'D': [('F', 7)],
    'E': [('F', 2)],
    'F': []
}

def best_first_search(graph, start, goal):
    visited = set()
    pq = PriorityQueue()
    
    pq.put((0,start)) #priority queue w/ priority as the heuristic value
    
    while not pq.empty():
        cost, node = pq.get() #get elements(always removes lowest priority value first)
        
        if node not in visited:
            print(node, end=' ')
            visited.add(node)
            if node == goal:
                print("\ngoal reached!")
                return True
            
            for neighbour, weight in graph[node]:
                if neighbour not in visited:
                    pq.put((weight, neighbour))
    print("\ngoal not reachable!")
    return False

print("best first search path:")
best_first_search(graph, 'A', 'F')    
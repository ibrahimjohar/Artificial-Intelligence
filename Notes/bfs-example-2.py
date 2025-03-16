graph = {
    0: [1, 3],
    1: [0, 3],
    2: [4,5],
    3: [0, 1, 6, 4],
    4: [3, 2, 5],
    5: [4, 2, 6],
    6: [3, 5]  
}

def bfs(graph, start, goal):
    visited = []
    queue = []
    
    visited.append(start)
    queue.append(start)
    
    while queue:
        node = queue.pop(0)
        print(node, end=" ")
        
        if node == goal:
            print("\ngoal found!")
            break
        
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
                
start_node = 0
goal_node = 5

print("\nFollowing is the Breadth-First Search (BFS):")
bfs(graph, start_node, goal_node)
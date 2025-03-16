tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

#bfs function
def bfs(tree, start, goal):
    visited = []
    queue = [] 
    
    visited.append(start)
    queue.append(start)
    
    while queue:
        node = queue.pop(0) #dequeue from front
        print(node, end=" ")
        
        if node == goal:
            print("\ngoal found!")
            break
        
        for neighbor in tree[node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                
start_node = 'A'
goal_node = 'I'

print("\nFollowing is the Breadth-First Search (BFS):")

bfs(tree, start_node, goal_node)
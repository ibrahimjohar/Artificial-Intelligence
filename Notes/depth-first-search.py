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

def dfs(graph, start, goal):
    visited = []
    stack = []
    
    visited.append(start)
    stack.append(start)
    
    while stack:
        node = stack.pop() #pop from top (LIFO)
        print(node, end=" ")
        
        if node == goal:
            print("\ngoal found!")
            break
        
        for neighbour in reversed(graph[node]): #reverse to maintain correct order
            if neighbour not in visited:
                visited.append(neighbour)
                stack.append(neighbour)
                
start_node = 'A'
goal_node = 'I'

print("\nFollowing is the Depth-First Search (DFS):")
dfs(tree, start_node, goal_node)
        
        
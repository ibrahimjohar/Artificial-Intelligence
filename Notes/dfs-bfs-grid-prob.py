from collections import deque

grid = [
    ['O', 'O', 'X', 'O', 'T'],
    ['O', 'X', 'O', 'O', 'X'],
    ['P', 'O', 'O', 'X', 'O'],
    ['X', 'X', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'X', 'O']
]

directions = [(0,1), (1,0), (0,-1), (-1,0)] #right, down, left, right

def find_positions(symbol):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == symbol:
                return (i,j)
    return None

def bfs(start, goal):
    queue = deque([(start, [])])
    visited = set()
    
    while queue:
        (x,y), path = queue.popleft()
        if(x,y) in visited:
            continue
        visited.add((x,y))
        path = path + [(x,y)]
        
        if (x,y) == goal:
            return path
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 'X':
                queue.append(((nx,ny), path))
    return None

def dfs(start, goal):
    stack = [(start, [])]
    visited = set()
    
    while stack:
        (x,y), path = stack.pop()
        if (x,y) in visited:
            continue
        visited.add((x,y))
        path = path + [(x,y)]
        
        if (x,y) == goal:
            return path
        
        for dx, dy in reversed(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 'X':
                stack.append(((nx,ny), path))
    return None

start = find_positions('P')
goal = find_positions('T')

bfs_path = bfs(start, goal)
dfs_path = dfs(start, goal)

print("bfs path: ", bfs_path)
print("dfs path: ", dfs_path)
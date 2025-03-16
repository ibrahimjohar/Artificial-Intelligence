"""
A courier robot needs to deliver a package from the top-left corner (0,0) to the bottom-right
corner (N-1, M-1) of an N x M weighted grid. The grid contains different terrain costs
represented by positive integers. Some cells are impassable and marked as &#39;#&#39;.
Implement the A search algorithm to find the optimal path from (0,0) to (N-1,M-1).
1 2 3 # 4
1 # 1 2 2
2 3 1 # 1
# # 2 1 1
1 1 2 2 1
"""

import heapq

#define the grid
grid = [
    [1, 2, 3, None, 4],
    [1, None, 1, 2, 2],
    [2, 3, 1, None, 1],
    [None, 4, 2, 1, 1],
    [1, 1, 2, 2, 1]
]

directions = [(0,1), (1,0), (0,-1), (-1,0)]

def heuristic(a,b):
    """manhattan distance heuristic formula"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid):
    rows, cols = len(grid), len(grid[0])
    start, goal = (0,0), (rows-1, cols-1)
    
    #minheap priority queue
    pq = [(0 + heuristic(start, goal), 0, start, [])]   # (f, g, (x,y), path)
    visited = set()
    
    while pq:
        f, g, (x,y), path = heapq.heappop(pq)
        
        if(x,y) in visited:
            continue
        
        visited.add((x,y))
        
        #add to path
        path = path + [(x, y)]
        
        #goal check
        if (x,y) == goal:
            return path     #return optimal path
        
        #explore neigbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] is not None:
                new_g = g + grid[nx][ny]    #cost so far
                new_f = new_g + heuristic((nx,ny), goal)    #f = g + h
                heapq.heappush(pq, (new_f, new_g, (nx, ny), path))
                
    return None     #no path found

#run A* search
optimal_path = a_star_search(grid)
print("optimal path: ", optimal_path)
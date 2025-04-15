#q3
import time
from collections import deque
from ortools.sat.python import cp_model

def read_puzzle_file(path):
    #reads a file cont. sudoku puzzles (one per line) & returns a list of puzzle strings.
    with open(path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def grid_from_line(line):
    # Converts an 81-character string into a 9x9 grid (list of lists) of integers, where dots are interpreted as zeros.
    line = line.strip().replace('.', '0')
    grid = []
    
    for i in range(9):
        row = [int(line[i * 9 + j]) for j in range(9)]
        grid.append(row)
    return grid

#GPT
def show_grid(board):
    #prints the 9x9 Sudoku board. empty cells(0) are printed as dots.
    for r in range(9):
        row_str = ""
        for c in range(9):
            val = board[r][c]
            row_str += str(val) if val != 0 else '.'
            if c == 2 or c == 5:
                row_str += " | "
            else:
                row_str += " "
        print(row_str)
        if r == 2 or r == 5:
            print("-" * 21)
    print()

#method 1: custom Solver using AC-3 + backtracking
#function implements a custom sudoku solver using a combination of constraint propagation (similar to AC-3) and implements backtracking search.
#custom approach with forward checking (AC-3 inspired) and recursion for backtracking.
def solve_custom(board):
    #tracking numbers used in rows, cols & boxes
    rows_used = [[False] * 10 for _ in range(9)] 
    cols_used = [[False] * 10 for _ in range(9)]
    boxes_used = [[False] * 10 for _ in range(9)]
    
    domains = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)} #domain set for AC-3
    
    def assign_value(r, c, v):
        #give value 'v' to cell (r, c) & mark this val as used for the corr. row, column, & box.
        board[r][c] = v
        rows_used[r][v] = True
        cols_used[c][v] = True
        box_index = (r // 3) * 3 + (c // 3)
        boxes_used[box_index][v] = True
        domains[(r, c)] = {v}
    
    def unassign_value(r, c, v):
        #removes/unassigns a value from cell (r, c) & resets flags.
        board[r][c] = 0
        rows_used[r][v] = False
        cols_used[c][v] = False
        box_index = (r // 3) * 3 + (c // 3)
        boxes_used[box_index][v] = False
        valid = {num for num in range(1, 10)
                 if not rows_used[r][num] and not cols_used[c][num] and not boxes_used[box_index][num]}
        domains[(r, c)] = valid
    
    def enforce_forward_check():
        #implements forward checking similar to AC-3: as for every empty cell, filters thru the possible vals(domain) based on current row, column, & box constraints.
        queue = deque((r, c) for r in range(9) for c in range(9) if board[r][c] == 0)
        
        while queue:
            r, c = queue.popleft()
            bi = (r // 3) * 3 + (c // 3) #bi: box index
            
            valid = {num for num in domains[(r, c)]
                     if not rows_used[r][num] and not cols_used[c][num] and not boxes_used[bi][num]}
            if not valid:
                return False
            domains[(r, c)] = valid
            
            if len(valid) == 1 and valid != domains[(r, c)]:
                single_val = next(iter(valid))
                assign_value(r, c, single_val)
                
                #append all the cells in the same row, column, or box to the 'queue'
                for i in range(9):
                    if board[r][i] == 0 and (r, i) != (r, c):
                        queue.append((r, i))
                    if board[i][c] == 0 and (i, c) != (r, c):
                        queue.append((i, c))
                        
                box_row, box_col = (r // 3) * 3, (c // 3) * 3
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        if board[i][j] == 0 and (i, j) != (r, c):
                            queue.append((i, j))
            domains[(r, c)] = valid
        return True

    #using recursive backtracking to fill in the sudoku board.
    def backtrack_search():
        empty_spots = [(r, c) for r in range(9) for c in range(9) if board[r][c] == 0]
        if not empty_spots:
            return True
        r,c = min(empty_spots, key=lambda cell: len(domains[cell]))  #MRV heuristic for better pruning
        
        for num in domains[(r, c)].copy():
            bi = (r // 3) * 3 + (c // 3)
            if rows_used[r][num] or cols_used[c][num] or boxes_used[bi][num]:
                continue
            assign_value(r, c, num)
            
            if enforce_forward_check() and backtrack_search():  #apply forward check again during recursion
                return True
            unassign_value(r, c, num)
        return False

    #initializing the board w/ given values, marking flags as need be.
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                v = board[i][j]
                box = (i // 3) * 3 + (j // 3)
                if rows_used[i][v] or cols_used[j][v] or boxes_used[box][v]:
                    return None
                assign_value(i, j, v)
    
    if enforce_forward_check() and backtrack_search():
        return board
    return None

#method 2: OR-tools solver
#function uses google OR-Tools' CP-SAT solver to solve the sudoku puzzle by modeling it as a CSP.
def solve_or_tools(puzzle):
    model = cp_model.CpModel()
    cell_vars = [[model.NewIntVar(1, 9, "cell_{}_{}".format(i, j)) for j in range(9)] for i in range(9)]
    
    #setting up the constraints
    
    #row constraints: all vals in a row must be diff.
    for i in range(9):
        model.AddAllDifferent(cell_vars[i])
    
    #column constraints: all vals in a col must be diff.
    for j in range(9):
        model.AddAllDifferent([cell_vars[i][j] for i in range(9)])
    
    #subgrid constraints: all vals in each 3x3 block must be diff.
    for bi in range(3):
        for bj in range(3):
            block = [cell_vars[r][c] for r in range(bi * 3, bi * 3 + 3)
                     for c in range(bj * 3, bj * 3 + 3)]
            model.AddAllDifferent(block)

    #fix the cells that are already set in the puzzle.
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                model.Add(cell_vars[i][j] == puzzle[i][j])
    solver = cp_model.CpSolver()
    start_t = time.time()
    result = solver.Solve(model)
    elapsed = time.time() - start_t
    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [[solver.Value(cell_vars[i][j]) for j in range(9)] for i in range(9)]
        return sol, elapsed
    return None, elapsed

#method 3 (chat-GPT inspired): heuristic solver (AC-3 inspired + recursice search)
#class implements a sudoku solver that uses a heuristic, inspired by AC-3 for domain reduction combined w/ recursive search guided by
#min remain. vals & least-conflict ordering.

class HeuristicSolver:
    def __init__(self, initial_board):
        self.size = 9
        self.box_dim = 3
        self.board = [row[:] for row in initial_board]
        self.domains = {(r, c): list(range(1, 10)) for r in range(9) for c in range(9)}
        self.initialize_domains()

    #initialising domains based on the filled cells in the board.
    def initialize_domains(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] != 0:
                    self.domains[(r, c)] = [self.board[r][c]]

    #returns a list of cells that are in the same row, col, or even the 3x3 block. as cell (r, c)
    def related_cells(self, r, c):
        related = set()
        
        for i in range(self.size):
            related.add((r, i))
            related.add((i, c))
        br, bc = (r // 3) * 3, (c // 3) * 3        #br: box row, bc: box column
        
        for i in range(br, br + self.box_dim):
            for j in range(bc, bc + self.box_dim):
                related.add((i, j))
        related.remove((r, c))
        return list(related)

    #implements the AC-3 algo to enforce arc consistency among the cell domains.
    def ac3(self):
        queue = deque(((i, j), neighbor)
                      for i in range(9)
                      for j in range(9)
                      for neighbor in self.related_cells(i, j))
        while queue:
            (r1, c1), (r2, c2) = queue.popleft()
            if self.revise((r1, c1), (r2, c2)):
                if not self.domains[(r1, c1)]:
                    return False
                
                for other in self.related_cells(r1, c1):
                    if other != (r2, c2):
                        queue.append((other, (r1, c1)))
        return True

    #removing vals from cell1's domain if cell2 has a singleton domain with the same val.
    def revise(self, cell1, cell2):
        revised = False
        
        for value in self.domains[cell1][:]:
            if self.domains[cell2] == [value]:
                self.domains[cell1].remove(value)
                revised = True
        return revised

    #selects empty cell (has board val 0) that has the smallest domain (min remaining values heuristic).
    def select_unassigned(self):
        empty = [(r, c) for r in range(9) for c in range(9) if self.board[r][c] == 0]
        return min(empty, key=lambda cell: len(self.domains[cell]))

    #orders possible vals for a cell by how less conflicts they create in their related cells.
    def order_by_least_conflict(self, cell):
        vals = self.domains[cell][:]
        related = self.related_cells(cell[0], cell[1])
        return sorted(vals, key=lambda v: sum(v in self.domains[rel] for rel in related))
    
    #checks whether placing a val in the given cell violates the constraints in the related cells.
    def is_assignment_valid(self, cell, value):
        for r, c in self.related_cells(cell[0], cell[1]):
            if self.board[r][c] == value:
                return False
        return True

    #performs recursive backtracking search w/ AC-3 enforced to complete the board.
    def search(self):
        if all(self.board[r][c] != 0 for r in range(9) for c in range(9)):
            return [self.board[r][:] for r in range(9)]
        cell = self.select_unassigned()
        for val in self.order_by_least_conflict(cell):
            if self.is_assignment_valid(cell, val):
                orig_domain = self.domains[cell][:]
                self.board[cell[0]][cell[1]] = val
                self.domains[cell] = [val]
                if self.ac3():
                    result = self.search()
                    if result is not None:
                        return result
                self.board[cell[0]][cell[1]] = 0
                self.domains[cell] = orig_domain
        return None

def solve_heuristic(board):
    #instance created that attempts to solve the board.
    solver_obj = HeuristicSolver(board)
    return solver_obj.search()

#timing-helper func
def compute_average_runtime(func, board_input, iterations=10):
    #calc avg runtime of a solver function over several iterations.
    total = 0.0
    for _ in range(iterations):
        start = time.time()
        func([row[:] for row in board_input])
        total += time.time() - start
    return total / iterations

#main implementation below

puzzle_lines = read_puzzle_file(r"C:\Ibrahim\Personal\University Stuff\Artificial Intelligence\Assignments\02\q3sudoko.txt")
sample_line = puzzle_lines[0]
puzzle_board = grid_from_line(sample_line)

print("original puzzle:")
show_grid(puzzle_board)

#solving using custom method
board_copy = [row[:] for row in puzzle_board]
start_time = time.time()
custom_solution = solve_custom(board_copy)
custom_elapsed = time.time() - start_time

print("custom method output:")
if custom_solution:
    show_grid(custom_solution)
else:
    print("no sol found w/ custom method.")
print("custom method time: {:.3f} secs\n".format(custom_elapsed))

#solving using OR-Tools solver
board_copy2 = [row[:] for row in puzzle_board]
ort_solution, ort_time = solve_or_tools(board_copy2)

print("OR-Tools solver output:")
if ort_solution:
    show_grid(ort_solution)
else:
    print("no sol found w/ OR-Tools solver.")
print("OR-Tools solver time: {:.3f} secs\n".format(ort_time))

#solving using heuristic method
board_copy3 = [row[:] for row in puzzle_board]
start_time = time.time()
heuristic_solution = solve_heuristic(board_copy3)
heuristic_time = time.time() - start_time

print("heuristic method output:")
if heuristic_solution:
    show_grid(heuristic_solution)
else:
    print("no sol found w/ heuristic method.")
print("heuristic method time: {:.3f} secs\n".format(heuristic_time))

#avg runtime comparison over multiple iterations
avg_custom = compute_average_runtime(solve_custom, puzzle_board, 10)
avg_ort = compute_average_runtime(lambda b: solve_or_tools(b)[0], puzzle_board, 10)
avg_heuristic = compute_average_runtime(solve_heuristic, puzzle_board, 10)

print("average runtime over 10 iterations:")
print("custom method: {:.3f} sec".format(avg_custom))
print("OR-Tools Solver: {:.3f} sec".format(avg_ort))
print("heuristic method: {:.3f} sec".format(avg_heuristic))

#q3

import time

def parse_puzzle(puzzle_str):
    """
    Convert an 81-character string into a dictionary mapping cell coordinates to their value.
    Empty cells are denoted by '0' or '.'.
    """
    assert len(puzzle_str) == 81, "Puzzle must be 81 characters long."
    grid = {}
    for i, ch in enumerate(puzzle_str):
        row, col = divmod(i, 9)
        grid[(row, col)] = ch if ch in '123456789' else '0'
    return grid

def display(grid):
    """Display the Sudoku grid."""
    for i in range(9):
        row = ''
        for j in range(9):
            row += grid[(i, j)] + ' '
            if j in [2, 5]:
                row += '| '
        print(row)
        if i in [2, 5]:
            print("-" * 21)
    print()

def possible_values(grid, row, col):
    """
    Returns the possible digits for a given cell (row, col) based on current grid state.
    """
    if grid[(row, col)] != '0':
        return set()
    used = set()
    # Row and column constraints
    for j in range(9):
        used.add(grid[(row, j)])
    for i in range(9):
        used.add(grid[(i, col)])
    # Block constraint (3x3)
    r0, c0 = 3 * (row // 3), 3 * (col // 3)
    for i in range(r0, r0 + 3):
        for j in range(c0, c0 + 3):
            used.add(grid[(i, j)])
    return set('123456789') - used

def find_unassigned(grid):
    """Return the coordinates of an unassigned cell or None if complete."""
    for i in range(9):
        for j in range(9):
            if grid[(i, j)] == '0':
                return (i, j)
    return None

def backtracking_solve(grid):
    """
    Solve the Sudoku using backtracking with constraint propagation.
    """
    cell = find_unassigned(grid)
    if not cell:
        return grid  # Solved
    
    row, col = cell
    for value in possible_values(grid, row, col):
        grid[(row, col)] = value
        # Optionally, we could incorporate AC-3 here for more propagation.
        result = backtracking_solve(grid)
        if result:
            return result
        grid[(row, col)] = '0'
    return None

def solve_sudoku_custom(puzzle_str):
    grid = parse_puzzle(puzzle_str)
    start_time = time.time()
    solution = backtracking_solve(grid)
    end_time = time.time()
    elapsed = end_time - start_time
    return solution, elapsed

# Example puzzle (0 denotes an empty cell)
puzzle_str = (
    "530070000"
    "600195000"
    "098000060"
    "800060003"
    "400803001"
    "700020006"
    "060000280"
    "000419005"
    "000080079"
)

if __name__ == "__main__":
    solution, elapsed_custom = solve_sudoku_custom(puzzle_str)
    print("Custom Backtracking Solver Solution:")
    display(solution)
    print("Time taken: {:.6f} seconds\n".format(elapsed_custom))

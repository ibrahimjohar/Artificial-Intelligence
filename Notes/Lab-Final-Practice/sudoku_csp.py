from ortools.sat.python import cp_model

def solve_sudoku():
    model = cp_model.CpModel()
    cell_size = 3
    line_size = cell_size * cell_size

    # Define variables
    grid = [[model.NewIntVar(1, line_size, f'cell_{i}_{j}') for j in range(line_size)] for i in range(line_size)]

    # Rows and columns must have all different values
    for i in range(line_size):
        model.AddAllDifferent([grid[i][j] for j in range(line_size)])
        model.AddAllDifferent([grid[j][i] for j in range(line_size)])

    # 3x3 blocks must have all different values
    for i in range(0, line_size, cell_size):
        for j in range(0, line_size, cell_size):
            block = [grid[i + di][j + dj] for di in range(cell_size) for dj in range(cell_size)]
            model.AddAllDifferent(block)

    # Example Sudoku puzzle
    puzzle = [
        [0, 0, 0, 0, 9, 4, 0, 3, 0],
        [0, 0, 0, 5, 1, 0, 0, 0, 7],
        [0, 8, 9, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 8],
        [0, 6, 0, 2, 0, 1, 0, 5, 0],
        [1, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 5, 2, 0],
        [9, 0, 0, 0, 6, 5, 0, 0, 0],
        [0, 4, 0, 9, 7, 0, 0, 0, 0]
    ]

    for i in range(line_size):
        for j in range(line_size):
            if puzzle[i][j] != 0:
                model.Add(grid[i][j] == puzzle[i][j])

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        for i in range(line_size):
            print([solver.Value(grid[i][j]) for j in range(line_size)])
    else:
        print("No solution found.")

solve_sudoku()

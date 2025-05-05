from ortools.sat.python import cp_model

model = cp_model.CpModel()
n = 3
cells = [[model.NewIntVar(1, 9, f'cell_{i}_{j}') for j in range(n)] for i in range(n)]
flat = [cell for row in cells for cell in row]

model.AddAllDifferent(flat)

# All rows, cols, and diagonals sum to the same value
target_sum = 15
for i in range(n):
    model.Add(sum(cells[i]) == target_sum)  # rows
    model.Add(sum(cells[j][i] for j in range(n)) == target_sum)  # columns

model.Add(sum(cells[i][i] for i in range(n)) == target_sum)  # diag
model.Add(sum(cells[i][n - i - 1] for i in range(n)) == target_sum)  # anti-diag

solver = cp_model.CpSolver()
if solver.Solve(model) == cp_model.FEASIBLE:
    for row in cells:
        print([solver.Value(c) for c in row])

from ortools.sat.python import cp_model

model = cp_model.CpModel()
N = 8
queens = [model.NewIntVar(0, N - 1, f"Q{i}") for i in range(N)]

model.AddAllDifferent(queens)
model.AddAllDifferent([queens[i] + i for i in range(N)])
model.AddAllDifferent([queens[i] - i for i in range(N)])

solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.FEASIBLE:
    for i in range(N):
        print(' '.join('Q' if solver.Value(queens[i]) == j else '.' for j in range(N)))

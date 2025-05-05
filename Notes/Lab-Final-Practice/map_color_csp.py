from ortools.sat.python import cp_model

model = cp_model.CpModel()
colors = ['Red', 'Green', 'Blue']
regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
region_vars = {region: model.NewIntVar(0, 2, region) for region in regions}
adjacent = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),('NSW','V')]

for r1, r2 in adjacent:
    model.Add(region_vars[r1] != region_vars[r2])

solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.FEASIBLE:
    for r in regions:
        print(f"{r}: {colors[solver.Value(region_vars[r])]}")

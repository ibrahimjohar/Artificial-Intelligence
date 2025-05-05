from ortools.sat.python import cp_model

model = cp_model.CpModel()
letters = 'SENDMORY'
digits = range(10)
vars = {l: model.NewIntVar(0, 9, l) for l in letters}

# All letters must have different digits
model.AddAllDifferent(vars.values())

# Leading letters can't be zero
model.Add(vars['S'] != 0)
model.Add(vars['M'] != 0)

# SEND + MORE = MONEY as an equation
send = vars['S']*1000 + vars['E']*100 + vars['N']*10 + vars['D']
more = vars['M']*1000 + vars['O']*100 + vars['R']*10 + vars['E']
money = vars['M']*10000 + vars['O']*1000 + vars['N']*100 + vars['E']*10 + vars['Y']

model.Add(send + more == money)

solver = cp_model.CpSolver()
if solver.Solve(model) == cp_model.FEASIBLE:
    for l in letters:
        print(f"{l} = {solver.Value(vars[l])}")
    print(f"SEND + MORE = MONEY --> {solver.Value(send)} + {solver.Value(more)} = {solver.Value(money)}")

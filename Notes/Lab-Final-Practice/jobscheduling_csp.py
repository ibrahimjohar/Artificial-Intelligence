from ortools.sat.python import cp_model

model = cp_model.CpModel()
horizon = 10

# Jobs: (duration, machine)
jobs = [
    [(3, 0), (2, 1)],
    [(2, 1), (4, 0)]
]

all_tasks = {}
machine_to_intervals = {0: [], 1: []}

for j, job in enumerate(jobs):
    for t, (dur, machine) in enumerate(job):
        start = model.NewIntVar(0, horizon, f'start_{j}_{t}')
        end = model.NewIntVar(0, horizon, f'end_{j}_{t}')
        interval = model.NewIntervalVar(start, dur, end, f'interval_{j}_{t}')
        all_tasks[(j, t)] = (start, end, interval)
        machine_to_intervals[machine].append(interval)

# No overlapping tasks on machines
for intervals in machine_to_intervals.values():
    model.AddNoOverlap(intervals)

# Job task order
for j in range(len(jobs)):
    model.Add(all_tasks[(j, 0)][1] <= all_tasks[(j, 1)][0])

solver = cp_model.CpSolver()
if solver.Solve(model) == cp_model.OPTIMAL:
    for key, (s, e, _) in all_tasks.items():
        print(f"Job {key[0]}, Task {key[1]}: Start at {solver.Value(s)}, End at {solver.Value(e)}")

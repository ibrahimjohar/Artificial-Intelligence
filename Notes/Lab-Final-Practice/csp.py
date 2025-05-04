#csp
#x - set of variables
#d - set of domains
#c - set of constraints

#constraint vals can be rep. as a pair{scope, relation}
#scope - tuple of variables in a constraint
#relation - set of allowed values of variables

#Consistent (Legal) Assignment:

#Variables: {Player_1, Player_2, Player_3, Player_4}
#Domains: {Red, Blue, Green, Yellow}
#Constraints: Player_1 ≠ Player_2, Player_2 ≠ Player_3, Player_1 ≠ Player_3

#Complete Assignment:

#each and every variable assigns a value and the solution is to satisfy the constraints.
#For example: Sudoku Game in which a complete assignment assigns each row and column a unique value containing values to all variables.
#Variables: Each cell in the grid.
#Domains: Possible values {1,2,3,4} (or {1-9} for a 9x9 Sudoku).
#Constraints: Uniqueness in rows, columns, and sub-grids.
#Goal: Find a complete and valid assignment satisfying all constraints.

#Partial Assignment:

#Those assignments who assign values to some variables are known as partial assignments.
#For example: In Sudoku Game Partial Assignment assigns values to some variables not all.

#domains: Domains are used by the variables

#discrete domain:
#domain is infinite where multiple variables can be mapped to one state 
#For Example: Multiple Variables can use start state infinite times.

#finite domain:
#A finite domain containing one domain for one variable can be a specific variable in a form of continuous states.

#Constraints in CSP:
# 1. Unary Constraints:
# It is the simplest type of constraint that restricts the value of a single variable.

# 2. Binary Constraints:
# Binary means “two” variables lies in this constraint where the value of one
# variable contains the set of variables values that shows the relationship between
# two variables for example: if x2​​ is constrained by x1 and x3​, it means that the possible values of 
# x2 are influenced by or lie within a set defined by x1 and x3​.

# 3. Global Constraints: The variables are arbitrary in this constraint and have no relationship or connection or pattern between them.

# 4. Linear Constraints: The variables in this constraint contain integer values in linear form.

# 5. Non-linear Constraints: The variables in this constraint contain integer values in a non-linear form.

# 6. Constraint propagation in CSP: It is a special type of inference that helps in reducing the legal number of values
# for the variables and makes the propagation local consistent in the form of nodes. 
# We solve the constraint satisfaction problem with this inference.

# 7. Node Consistency:
# A variable is considered node consistent if every value in its domain satisfies the
# unary constraints imposed on it.

# 8. Arc Consistency:
# A variable is arc consistent if each value in its domain satisfies the binary
# constraints with respect to the related variables.

# 9. Path Consistency:
# When the evaluation of a pair of variables concerning a third variable can be
# extended to another variable while satisfying all binary constraints, it is similar to arc consistency.

# 10. k-consistency: This type of consistency is used to establish stronger forms of propagation.

#google ortools library - for csp problem
import ortools
from ortools.sat.python import cp_model

#declare model and bind with cp-model which is alr present in ortools library
model = cp_model.CpModel()

#declaring set of variables for csp
n_vals = 3
x = model.new_int_var(0, n_vals - 1, "x")
y = model.new_int_var(0, n_vals - 1, "y")
z = model.new_int_var(0, n_vals - 1, "z")

#add example constraints
model.Add(x != y)
model.Add(y != z)
model.Add(x != z)

#solve
solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"x = {solver.value(x)}")
    print(f"y = {solver.value(y)}")
    print(f"z = {solver.value(z)}")
else:
    print("no solution found.")
    
#output:
# x = 1
# y = 2
# z = 0

from ortools.sat.python import cp_model

def simple_sat_program():
    """minimal CP_SAT example to showcase calling the solver"""
    #create the model
    model = cp_model.CpModel()
    
    #create the variables
    num_vals = 3
    x = model.new_int_var(0, num_vals - 1, "x")
    y = model.new_int_var(0, num_vals - 1, "y")
    z = model.new_int_var(0, num_vals - 1, "z")
    
    #create the constraints
    model.add(x != y)
    
    #create a solver & the solver solves the model
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("no solution found.")
        
simple_sat_program()

# output:
# x = 1
# y = 0
# z = 0

import ortools
from ortools.sat.python import cp_model
#declare model and bind with cp-model which is alr present in ortools library
model = cp_model.CpModel()

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """print intermediate solutions."""
    
    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
    
    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v} = {self.value(v)}", end=" ")
        print()
        
    @property
    def solution_count(self) -> int:
        return self.__solution_count
    
solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter([x,y,z])

#enumerate all solutions
solver.parameters.enumerate_all_solutions = True

#solve 
status = solver.solve(model, solution_printer)

print(f"status = {solver.status_name(status)}")
print(f"number of sols found: {solution_printer.solution_count}")

# output:
# x = 0 y = 0 z = 0 
# status = OPTIMAL
# number of sols found: 1

from ortools.sat.python import cp_model

def main() -> None:
    """minimal cp-sat example to showcase calling the solver"""
    #create the model
    model = cp_model.CpModel()
    
    #create the variables
    var_upper_bound = max(50, 45, 37)
    x = model.new_int_var(0, var_upper_bound, "x")
    y = model.new_int_var(0, var_upper_bound, "y")
    z = model.new_int_var(0, var_upper_bound, "z")
    
    #create constraints
    
    # Three linear inequalities constraining (x, y, z):
    # 1. 2x + 7y + 3z ≤ 50
    # 2. 3x − 5y + 7z ≤ 45
    # 3. 5x + 2y − 6z ≤ 37
    
    model.add(2 * x + 7 * y + 3 * z <= 50)
    model.add(3 * x - 5 * y + 7 * z <= 45)
    model.add(5 * x + 2 * y - 6 * z <= 37)
    
    #objective function
    #Tells the solver to maximize the linear expression 2x+2y+3z over all integer points 
    #(x,y,z) that satisfy the constraints.
    model.maximize(2 * x + 2 * y + 3 * z) 
    
    #create a solver & solves the model
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    
    #OPTIMAL means the best possible value was proven.
    #FEASIBLE means a valid solution was found, but optimality wasn’t proven (rare in pure CP-SAT with a linear objective).
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"maximum of objective function: {solver.objective_value}\n")
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("no solution found.")
        
    #On success, prints:
    # 1. Objective value (the maximized 2x+2y+3z)
    # 2. The chosen values of x, y, and z.
    
    #statistics
    print("\nstatistics:")
    print(f"    status   : {solver.status_name(status)}")
    print(f"    conflicts: {solver.num_conflicts}")
    print(f"    branches : {solver.num_branches}")
    print(f"    wall time: {solver.wall_time}")
    
    #conflicts: how many times the solver hit a dead‐end and backtracked
    #branches: num of branching decisions
    #wall time: total runtime (secs)
    
main()

#Objective of the Code: 
# This is a minimal demonstration of a CP-SAT workflow:
# Define integer variables (x, y, z).
# Impose linear constraints to carve out the feasible set.
# Specify a linear objective to maximize.
# Solve and inspect both the solution and some performance stats.
# You could view it as a tiny instance of a resource-allocation or budgeting problem: find nonnegative integer amounts 
# x,y,z satisfying three capacity constraints, so as to maximize a profit function 2x+2y+3z.

#output:
# maximum of objective function: 35.0

# x = 7
# y = 3
# z = 5

# statistics:
#     status   : OPTIMAL
#     conflicts: 0
#     branches : 0
#     wall time: 0.0426288
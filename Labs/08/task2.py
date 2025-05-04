from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Nodes:
# ● Intelligence (I) — {High, Low}
# ● StudyHours (S) — {Sufficient, Insufficient}
# ● Difficulty (D) — {Hard, Easy}
# ● Grade (G) — {A, B, C}
# ● Pass (P) — {Yes, No}

# Dependencies:
# Intelligence(I), StudyHours(S), and Difficulty(D) directly affect Grade(G).
# Grade(G) directly affects Pass(P).

# Prior Probabilities:
# ● P(Intelligence = High) = 0.7, P(Intelligence = Low) = 0.3
# ● P(StudyHours = Sufficient) = 0.6, P(StudyHours = Insufficient) = 0.4
# ● P(Difficulty = Hard) = 0.4, P(Difficulty = Easy) = 0.6

# Conditional Probabilities (examples):
# P(Grade | Intelligence, StudyHours, Difficulty):
# (Assume your own valid values, e.g., students with High intelligence, Sufficient study
# hours, and Easy difficulty are most likely to get A)

# ● P(Pass | Grade):
# ● P(Pass = Yes | Grade = A) = 0.95
# ● P(Pass = Yes | Grade = B) = 0.80
# ● P(Pass = Yes | Grade = C) = 0.50

# Tasks to do
# ● Construct the Bayesian Network structure diagram showing all dependencies.
# ● Define the complete Conditional Probability Tables (CPTs) for all nodes.
# ● Implement the Bayesian Network using Python (pgmpy or equivalent).
# ● Perform inference using Variable Elimination to answer:
# ● What is the probability that the student passes the exam, given:
#       StudyHours = Sufficient,
#       Difficulty = Hard
# ● What is the probability that the student has High Intelligence, given:
#       Pass = Yes

#dependencies:

# I       S       D
#  \      |      /
#         G
#         |
#         P

#step 1 -> define the structure of the bayesian network
model = DiscreteBayesianNetwork([
    ('Intelligence', 'Grade'),
    ('StudyHours', 'Grade'),
    ('Difficulty','Grade'),
    ('Grade', 'Pass')
])

#step 2 -> define the CPDs (conditional probability distributions)
#P(Intelligence)
cpd_intelligence = TabularCPD(variable='Intelligence', variable_card=2, values=[[0.7],[0.3]], state_names={'Intelligence': ['High', 'Low']})

#P(StudyHours)
cpd_studyhrs = TabularCPD(variable='StudyHours', variable_card=2, values=[[0.6],[0.4]], state_names={'StudyHours': ['Sufficient', 'Insufficient']})

#P(Difficulty)
cpd_difficulty = TabularCPD(variable='Difficulty', variable_card=2, values=[[0.4],[0.6]], state_names={'Difficulty': ['Hard', 'Easy']})

#P(Grade | Intelligence, StudyHours, Difficulty)
cpd_grade = TabularCPD(variable='Grade', variable_card=3, 
                       values=[
                                # High Int, Sufficient Study, Easy Difficulty -> most likely A
                                [0.80, 0.7, 0.60, 0.5, 0.4, 0.3, 0.2, 0.1],  # A
                                [0.15, 0.2, 0.25, 0.3, 0.3, 0.4, 0.4, 0.5],  # B
                                [0.05, 0.1, 0.15, 0.2, 0.3, 0.3, 0.4, 0.4]   # C
                           ],
                       evidence=['Intelligence', 'StudyHours', 'Difficulty'],
                       evidence_card=[2,2,2],
                       state_names={
                           'Grade': ['A','B','C'],
                           'Intelligence': ['High', 'Low'],
                           'StudyHours': ['Sufficient', 'Insufficient'],
                           'Difficulty': ['Hard', 'Easy']
                       })

#P(Pass | Grade)
cpd_pass = TabularCPD(variable='Pass', variable_card=2, 
                      values=[
                          [0.05, 0.2, 0.5], # Pass = No
                          [0.95, 0.8, 0.5]  # Pass = Yes
                      ],
                      evidence=['Grade'],
                      evidence_card=[3],
                      state_names={
                          'Pass': ['No', 'Yes'],
                          'Grade': ['A', 'B', 'C']
                      })

#step 3 -> add CPDs to the model
model.add_cpds(cpd_intelligence, cpd_studyhrs, cpd_difficulty, cpd_grade, cpd_pass)

#step 4 -> verify the model
assert model.check_model(), "model is incorrect"

#step 5 -> perform inference
inference = VariableElimination(model) 

#query 1: probability of PASSING given StudyHours = Sufficient, Difficulty = Hard
result1 = inference.query(variables=['Pass'], evidence={'StudyHours': 'Sufficient', 'Difficulty': 'Hard'})
print("\nprobability of passing given sufficient study hours and hard difficulty: ")
print(result1)

#query 2: probability of High Intelligence, given Pass = Yes
result2 = inference.query(variables=['Intelligence'], evidence={'Pass': 'Yes'})
print("\nprobability of high intelligence given pass: ")
print(result2)  

#output:
# probability of passing given sufficient study hours and hard difficulty: 
# +-----------+-------------+
# | Pass      |   phi(Pass) |
# +===========+=============+
# | Pass(No)  |      0.1355 |
# +-----------+-------------+
# | Pass(Yes) |      0.8645 |
# +-----------+-------------+

# probability of high intelligence given pass: 
# +--------------------+---------------------+
# | Intelligence       |   phi(Intelligence) |
# +====================+=====================+
# | Intelligence(High) |              0.7321 |
# +--------------------+---------------------+
# | Intelligence(Low)  |              0.2679 |
# +--------------------+---------------------+

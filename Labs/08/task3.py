#task 3 - lab 08

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

#         D 
#     /  / \  \
#   Fe  Co Fa  Ch  

#step 1 -> define the structure of the bayesian network
model = DiscreteBayesianNetwork([
    ('Disease', 'Fever'),
    ('Disease', 'Cough'),
    ('Disease', 'Fatigue'),
    ('Disease', 'Chills')
])

#step 2 -> define the CPDs (conditional probability distributions)
#P(Disease)
cpd_disease = TabularCPD( variable='Disease', variable_card=2, values=[[0.3], [0.7]], state_names={'Disease': ['Flu', 'Cold']})

#P(Fever | Disease)
cpd_fever = TabularCPD(variable='Fever', variable_card=2,
    values=[
        [0.1, 0.5],  #Fever = No
        [0.9, 0.5]   #Fever = Yes
    ],
    evidence=['Disease'],
    evidence_card=[2],
    state_names={
        'Fever': ['No', 'Yes'],
        'Disease': ['Flu', 'Cold']
    }
)

#P(Cough | Disease)
cpd_cough = TabularCPD(variable='Cough', variable_card=2,
    values=[
        [0.2, 0.4],  #Cough = No
        [0.8, 0.6]   #Cough = Yes
    ],
    evidence=['Disease'],
    evidence_card=[2],
    state_names={
        'Cough': ['No', 'Yes'],
        'Disease': ['Flu', 'Cold']
    }
)

#P(Fatigue | Disease)
cpd_fatigue = TabularCPD(variable='Fatigue', variable_card=2,
    values=[
        [0.3, 0.7],  #Fatigue = No
        [0.7, 0.3]   #Fatigue = Yes
    ],
    evidence=['Disease'],
    evidence_card=[2],
    state_names={
        'Fatigue': ['No', 'Yes'],
        'Disease': ['Flu', 'Cold']
    }
)

#P(Chills | Disease)
cpd_chills = TabularCPD(variable='Chills', variable_card=2,
    values=[
        [0.4, 0.6],  #Chills = No
        [0.6, 0.4]   #Chills = Yes
    ],
    evidence=['Disease'],
    evidence_card=[2],
    state_names={
        'Chills': ['No', 'Yes'],
        'Disease': ['Flu', 'Cold']
    }
)

#step 3 -> add CPDs to the model
model.add_cpds(cpd_disease, cpd_fever, cpd_cough, cpd_fatigue, cpd_chills)

#step 4 -> verify the model
assert model.check_model()

#step 5 -> perform inference
inference = VariableElimination(model)

#inference task 1 -> P(Disease | Fever=Yes, Cough=Yes)
result1 = inference.query(variables=['Disease'], evidence={'Fever': 'Yes', 'Cough': 'Yes'})
print("\nprobability of disease given fever and cough:")
print(result1)

#inference task 2 -> P(Disease | Fever=Yes, Cough=Yes, Chills=Yes)
result2 = inference.query(variables=['Disease'], evidence={'Fever': 'Yes', 'Cough': 'Yes', 'Chills': 'Yes'})
print("\nprobability of disease given fever, cough, and chills:")
print(result2)

#inference task 3 -> P(Fatigue=Yes | Disease=Flu)
result3 = inference.query(variables=['Fatigue'], evidence={'Disease': 'Flu'})
print("\nprobability of fatigue given flu:")
print(result3)

#output:
# probability of disease given fever and cough:
# +---------------+----------------+
# | Disease       |   phi(Disease) |
# +===============+================+
# | Disease(Flu)  |         0.5070 |
# +---------------+----------------+
# | Disease(Cold) |         0.4930 |
# +---------------+----------------+

# probability of disease given fever, cough, and chills:
# +---------------+----------------+
# | Disease       |   phi(Disease) |
# +===============+================+
# | Disease(Flu)  |         0.6067 |
# +---------------+----------------+
# | Disease(Cold) |         0.3933 |
# +---------------+----------------+

# probability of fatigue given flu:
# +--------------+----------------+
# | Fatigue      |   phi(Fatigue) |
# +==============+================+
# | Fatigue(No)  |         0.3000 |
# +--------------+----------------+
# | Fatigue(Yes) |         0.7000 |
# +--------------+----------------+

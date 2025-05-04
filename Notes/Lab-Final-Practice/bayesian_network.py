#bayesian-network
# probabilistic graphical model that rep(s) a set of variables & their conditional
# dependencies thru a directed acyclic graph (DAG).
# also known as a Bayes Network
# these are built from probability distributions & leverage probability theory for tasks
# such as prediction, anomaly detection, diagnostics, & decision making under uncertainty

#bayesian networks help model probabilistic relationships between multiplpe events
# useful in:
# prediction, anomaly detection, diagnostic systems, automated reasoning & insight generation
# time series prediction, decision-making under uncertainty
# components of a bayesian network

#bayesian network consists of 2 main components:
## 1. directed acyclic graph (DAG): represents structure of dependencies b/w variables
## 2. conditional probability tables (CPTs): specify the quantitative strength of those dependencies

#elements of a bayesian network:
## 1. nodes -> rep random variables in the domain that is being modeled (can be observable or hidden)
## 2. edges -> directed links b/w nodes that rep probabilistic dependencies
##              edge from node A -> B implies: B is conditionally dependent on A
## 3. CPTs -> each non-root node is associated w/ a CPT that def. the probability distribution of that variable given its parent nodes
## 4. parent nodes -> nodes that hv edges pointing to a specific node, node's val depends on its parent node
## 5. root nodes -> nodes w/ no incoming edges, independent variables or inputs to system
## 6. leaf nodes -> nodes w/ no outgoing edges, often rep outputs or final observed variables
## 7. network structure -> overall connection pattern among nodes, determines the conditional independencies & supports efficient probabilistic inference


#burglary alarm problem - using bayesian network

#home alarm system that can be triggered by a burglary or an earthquake.

#two neighbors, John and Mary, may call to report the alarm if they hear it.

#Bayesian Network for this problem includes the following five Boolean variables:
## Burglary (B) – Whether a burglary has occurred.
## Earthquake (E) – Whether an earthquake has occurred.
## Alarm (A) – Whether the alarm has gone off.
## JohnCalls (J) – Whether John calls to report the alarm.
## MaryCalls (M) – Whether Mary calls to report the alarm.

#network structure
## Alarm(A) is DIRECTLY INFLUENCED by Burglary(B) & Earthquake(E)
## JohnCalls(J) & MaryCalls(M) depend on Alarm(A)

#  B      E 
#   \    /
#      A
#    /   \
#   J     M

#conditional probability tables (CPTs)
## P(B) -> probability of a burglary occuring
## P(E) -> probability of an earthquake occuring
## P(A | B, E) -> probability of the ALARM going OFF, given BURGLARY & EARTHQUAKE
## P(J | A) -> probability of JOHN CALLING, given ALARM 
## P(M | A) -> probability of MARY CALLING, given ALARM

#Given that both John and Mary have called, what is the probability that a burglary has actually occurred?

#pip install pgmpy

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

#step 1 -> define the structure of the bayesian network
model = DiscreteBayesianNetwork([
    ('Burglary', 'Alarm'),
    ('Earthquake', 'Alarm'),
    ('Alarm', 'JohnCalls'),
    ('Alarm', 'MaryCalls')
])

#step 2 -> define the CPDs (conditional probability distributions)
#P(Burglary)
cpd_burglary = TabularCPD(variable='Burglary', variable_card=2, values=[[0.999], [0.001]])

#P(Earthquake)
cpd_earthquake = TabularCPD(variable='Earthquake', variable_card=2, values=[[0.998],[0.002]])

#P(Alarm | Burglary, Earthquake)
cpd_alarm = TabularCPD(variable='Alarm', variable_card=2, 
                       values=[
                           [0.999, 0.71, 0.06, 0.05],   #Alarm = False
                           [0.001, 0.29, 0.94, 0.95]    #Alarm = True
                       ],
                       evidence=['Burglary', 'Earthquake'],
                       evidence_card=[2,2])

#P(JohnCalls | Alarm)
cpd_john = TabularCPD(variable='JohnCalls', variable_card=2,
                      values=[
                          [0.3, 0.9],   #JohnCalls = False
                          [0.7, 0.1]    #JohnCalls = True
                      ],
                      evidence=['Alarm'],
                      evidence_card=[2])

#P(MarryCalls | Alarm)
cpd_mary = TabularCPD(variable='MaryCalls', variable_card=2,
                      values=[
                          [0.2, 0.99],  #MaryCalls = False
                          [0.8, 0.01]   #MaryCalls = True
                      ],
                      evidence=['Alarm'],
                      evidence_card=[2])

#step 3 -> add CPDs to the model
model.add_cpds(cpd_burglary, cpd_earthquake, cpd_alarm, cpd_john, cpd_mary)

#step 4 -> verify the model
assert model.check_model(), "model is incorrect"

#step 5 -> perform inference
inference = VariableElimination(model)

#query: what is the probability of a burglary given that both John and Mary called?
result = inference.query(variables=['Burglary'], evidence={'JohnCalls': 1, 'MaryCalls': 1})

print(result)

#P(Grade | Intelligence, StudyHours, Difficulty)
cpd_grade = TabularCPD(variable='Grade', variable_card=3, 
                       values=[
                                # High Int, Sufficient Study, Easy Difficulty -> most likely A
                                #COLS -> corr. to every combination of its parent's states (2**3=8)
                                [0.80, 0.7, 0.60, 0.5, 0.4, 0.3, 0.2, 0.1],  # A
                                [0.15, 0.2, 0.25, 0.3, 0.3, 0.4, 0.4, 0.5],  # B
                                [0.05, 0.1, 0.15, 0.2, 0.3, 0.3, 0.4, 0.4]   # C
                           ], #ROWS -> corr. to child variable's possible state in the order you declare them
                       evidence=['Intelligence', 'StudyHours', 'Difficulty'],
                       evidence_card=[2,2,2],
                       state_names={
                           'Grade': ['A','B','C'],
                           'Intelligence': ['High', 'Low'],
                           'StudyHours': ['Sufficient', 'Insufficient'],
                           'Difficulty': ['Hard', 'Easy']
                       })


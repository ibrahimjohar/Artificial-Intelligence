class environment:
    def __init__(self, initial_state):
        self.initial_state = initial_state
    #initial state could be fixed or random
        
    #initial condition of the environment
    #that would be perceived by the environment
    def get_percept(self):
        pass
    
class SimpleReflexAgent:
    def __init__(self):
        pass
    
    def act(self, percept):
        #determine action based on the initial percept
        pass
    
    
def run_agent(agent, environment):
    #agent reacts to the initial percept
    percept = environment.get_percept()
    
    #action based on the percept we will get from the environment
    action = agent.act(percept)
    
    print(f"percept: {percept}, action: {action}")


agent = SimpleReflexAgent()

e1 = environment(initial_state=0)
# Start with any initial condition (high/low , 1/0, True/False , 
# high/med/low etc, based on scenario)

#run the agent in the environment (only once)
run_agent(agent, e1)
    
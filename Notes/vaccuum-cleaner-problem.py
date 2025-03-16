class Environment:
    def __init__(self, state="Dirty"):
        self.state = state
        
    def get_percept(self):
        return self.state
    
    def clean_room(self):
        self.state = "Clean"
        
class SimpleReflexAgent:
    def __init__(self):
        pass
    
    def act(self, percept):
        if percept == "Dirty":
            return 'please clean the room'
        else:
            return 'room is already clean. good job.'
        

def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        print(f"step {step + 1}: percept - {percept}, action - {action}")
        
        if percept == "Dirty":
            environment.clean_room()
            

agent = SimpleReflexAgent()
environment = Environment()

run_agent(agent, environment, 5)
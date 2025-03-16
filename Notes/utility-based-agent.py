class UtilityBasedAgent:
    def __init__(self):
        self.utility = {'dirty': -10, 'clean': 10}
        
    def calculate_utility(self, percept):
        return self.utility[percept]
    
    def select_action(self, percept):
        if percept == 'dirty':
            return 'clean the room'
        else:
            return 'no action needed'
        
    def act(self, percept):
        action = self.select_action(percept)
        return action 
    
class Environment:
    def __init__(self, state='dirty'):
        self.state = state
        
    def get_percept(self):
        return self.state
    
    def clean_room(self):
        self.state = 'clean'
        
def run_agent(agent, environment, steps):
    total_utility = 0
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        utility = agent.calculate_utility(percept)
        
        print(f"step {step+1}: Percept - {percept}, Action - {action}, Utility - {utility}")
        total_utility += utility 
        
        if percept == 'dirty':
            environment.clean_room()
            
    print('total utility: ', total_utility)
    

agent = UtilityBasedAgent()
environment = Environment()

run_agent(agent, environment, 5)
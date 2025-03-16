class GoalBasedAgent:
    def __init__(self):
        self.goal = 'clean'
        
    def formulate_goal(self, percept):
        if percept == 'dirty':
            self.goal = 'clean'
        else:
            self.goal = 'no action needed'
    
    def act(self, percept):
        self.formulate_goal(percept)
        if self.goal == 'clean':
            return 'clean the room'
        else:
            return 'room is clean'
        
class Environment:
    def __init__(self, state='dirty'):
        self.state = state
        
    def get_percept(self):
        return self.state
    
    def clean_room(self):
        self.state = 'clean'
        
def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        print(f"Step {step+1}: Percept - {percept}, Action - {action}")
        
        if percept == 'dirty':
            environment.clean_room()
            

agent = GoalBasedAgent()
environment = Environment()

run_agent(agent, environment, 5)
        
        
class Environment:
    def __init__(self):
        self.grid = ['clean', 'dirty', 'clean', 
                     'clean', 'dirty', 'dirty',
                     'clean', 'clean', 'clean']
        
    def get_percept(self, position):
        return self.grid[position]
    
    def clean_room(self, position):
        self.grid[position] = "clean"
        
    def display_grid(self, agent_position):
        print("\ncurrent-grid-state:")
        grid_with_agent = self.grid[:] #copy the grid
        grid_with_agent[agent_position] = "👽" #place agent at the curr pos
        
        for i in range(0, 9, 3):
            print(" | ".join(grid_with_agent[i:i + 3]))
        print()
        
        
class SimpleReflexAgent:
    def __init__(self):
        self.position = 0
        pass
    
    def act(self, percept, grid):
        if percept == 'dirty':
            grid[self.position] = 'clean'
            return 'clean the room'
        else:
            return 'room is clean'
        
    def move(self):
        #move to the next position in the grid
        if self.position < 8:
            self.position += 1
        return self.position
    
def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept(agent.position)
        action = agent.act(percept, environment.grid)
        print(f"Step {step + 1}: Position {agent.position} -> Percept - {percept}, Action - {action}")
        environment.display_grid(agent.position)
        
        if percept == 'dirty':
            environment.clean_room(agent.position)
            
        agent.move()
        
agent = SimpleReflexAgent()
environment = Environment()

run_agent(agent, environment, 9)
            
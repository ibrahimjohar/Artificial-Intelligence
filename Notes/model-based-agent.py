class Environment:
    def __init__(self, rain='no', windows_open='open'):
        self.rain = rain
        self.windows_open = windows_open
        
    def get_percept(self):
        #returns the current percept(rain status & window status)
        return {'rain': self.rain, 'windows_open': self.windows_open}
    
    def close_windows(self):
        #closes the windows if they are open
        if self.windows_open == 'open':
            self.windows_open = 'closed'
            
class ModelBasedAgent:
    def __init__(self):
        self.model = {'rain': 'no', 'windows_open': 'open'}
        
    #agent uses a model to keep track of its past experiences w/ rain & window states.
    
    def act(self, percept):
        #decides action based on the model and current percept
        
        #update the model w/ current percept
        self.model.update(percept)          #dict.update() used here
        
        
        #check model to decide action
        if self.model['rain'] == 'yes' and self.model['windows_open'] == 'open':
            return 'close the windows'
        else:
            return 'no action needed'
        
def run_agent(agent, environment, steps):
    for step in range(steps):
        #get current percepts from environment
        percept = environment.get_percept()
        
        #agent makes a decision based on current percept
        action = agent.act(percept)
        
        #print the current percept & the agent's action
        print(f"Step {step+1}: Percept - {percept}, Action - {action}")
        
        #if agent decided to close the windows, update the environment
        if action == 'close the windows':
            environment.close_windows()


agent = ModelBasedAgent()
environment = Environment(rain='yes', windows_open='open')

run_agent(agent, environment, 5)


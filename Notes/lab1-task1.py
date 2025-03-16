import random

class Environment:
    def __init__(self):
        self.components = ["A","B","C","D","F","G","H","I"]
        self.state = {component: random.choice(["safe", "vulnerable"]) for component in self.components}
        
    def get_state(self):
        return self.state
    
class Agent:
    def __init__(self):
        self.patching_list = []
        
    def scan(self, environment):
        state = environment.get_state()
        
        for component, status in state.items():
            if status == "vulnerable":
                self.patching_list.append(component)
                print(f"Warning: Component {component} is vulnerable.")
            elif status == "safe":
                print(f"Success: Component {component} is safe.")
                
    def patching_vulnerabilities(self, environment):
        state = environment.get_state()
        for component in self.patching_list:
            state[component] = "safe"
            print(f"Success: Component {component} has been patched and is now marked as safe")
        environment.state = state
        
    def get_patching_list(self):
        return self.patching_list
    
def run_agent(agent, environment):
    print("scanning:\n")
    agent.scan(environment)
    print("\npatching vulnerabilities...\n")
    agent.patching_vulnerabilities(environment)
    print("\nfinal system state:\n")
    print(environment.get_state())


environment = Environment()
agent = Agent()

run_agent(agent, environment)        
    
        
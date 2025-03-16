import random

class Env:
    def __init__(self):
        self.components = ["A","B","C","D","F","G","H","I"]
        self.state = {component: random.choice(["safe","low risk","high risk"]) for component in self.components}
    
    def get_component(self):
        return self.components
    
    def get_state(self):
        return self.state
    
class Agent:
    def __init__(self):
        self.risks = []
    
    def scan(self, environment):
        state = environment.get_state()
        
        for component, risk in state.items():
            if risk == "low risk":
                self.risks.append(component)
                print(f"component {component} has a low risk vulnerability.")
            elif risk == "high risk":
                self.risks.append(component)
                print(f"component {component} has a high risk vulnerability.")
            elif risk == "safe":
                print(f"component {component} is safe.") 
        
    def patching_vulnerabilities(self, environment):
        state = environment.get_state()
        
        for component, risk in state.items():
            if risk == "low risk":
                state[component] = "safe"
                print(f"success: component {component} has been patched and is now marked as safe")
            elif risk == "high risk":
                print(f"warning: component {component} has a high risk vulnerability and requires premium patching.")
        
        environment.state = state
        return environment.state
    
def run_agent(agent, environment):
    print("initial State:\n")
    print(environment.get_state())
    print("\nscanning...\n")
    agent.scan(environment)
    print("\npatching vulnerabilities...\n")
    agent.patching_vulnerabilities(environment)
    print("\nfinal system state:\n")
    print(environment.get_state())
  
agent = Agent()
env = Env()

run_agent(agent, env)
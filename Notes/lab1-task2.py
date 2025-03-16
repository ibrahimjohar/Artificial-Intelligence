import random

class Environment:
    def __init__(self):
        self.servers = [1,2,3,4,5]    
        self.state = {server: random.choice(["underloaded", "balanced", "overloaded"]) for server in self.servers}
        
    def get_state(self):
        return self.state
    
    def update_state(self, new_state):
        self.state = new_state
        
    def get_servers(self):
        return self.servers
        
class Agent:
    def __init__(self):
        self.overloaded_servers = []
        self.underloaded_servers = []
    
    def scan(self, environment):
        state = environment.get_state()
        self.overloaded_servers = [server for server in state if state[server] == "overloaded"]
        self.underloaded_servers = [server for server in state if state[server] == "underloaded"]
        
        for server in self.overloaded_servers:
            print(f"server {server} is overloaded.")
        for server in self.underloaded_servers:
            print(f"server {server} is underloaded.")
            
    def load_balancing(self, environment):
        state = environment.get_state()
        
        while self.overloaded_servers and self.underloaded_servers:
            overloaded_server = self.overloaded_servers.pop()
            underloaded_server = self.underloaded_servers.pop()
            
            state[overloaded_server] = "balanced"
            state[underloaded_server] = "balanced"
            
            print(f"balanced: server {overloaded_server} offloaded tasks to server {underloaded_server}.")
        
        environment.update_state(state)
    
def run_agent():
    environment = Environment()
    agent = Agent()
    
    print("initial state:\n")
    print(environment.get_state())
    
    print("\nscanning...\n")
    agent.scan(environment)
    
    print("\nload balancing...\n")
    agent.load_balancing(environment)
    
    print("\nfinal system state:\n")
    print(environment.get_state())
    
run_agent()
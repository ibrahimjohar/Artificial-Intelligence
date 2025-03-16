import random

class Environment:
    def __init__(self):
        self.tasks = [1,2,3,4,5]
        self.state = {task: random.choice(["completed", "failed"]) for task in self.tasks}
        
    def get_state(self):
        return self.state
    
    def get_tasks(self):
        return self.tasks
    
class Agent:
    def __init__(self):
        self.failed_tasks = []
        
    def scan(self, environment):
        state = environment.get_state()
        
        for task in state:
            if state[task] == "failed":
                self.failed_tasks.append(task)
                print(f"backup task {task} is failed.")
        
        return self.failed_tasks
    
    def retry_failed_tasks(self, environment):
        state = environment.get_state()
        
        for task in self.failed_tasks:
            state[task] = "completed"
            print(f"backup task {task} has now been retried and comepleted")
        
        environment.state = state
        return environment.state
    
def run_agent(agent, environment):
    print("initial state:\n")
    print(environment.get_state())
    
    print("\nscanning...\n")
    agent.scan(environment)
    
    print("\nretrying failed tasks...\n")
    agent.retry_failed_tasks(environment)
    
    print("\nfinal system state:\n")
    print(environment.get_state())
    
    
agent = Agent()
e1 = Environment()

run_agent(agent, e1)
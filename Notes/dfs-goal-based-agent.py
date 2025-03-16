class GoalBasedAgent:
    def __init__(self, goal):
        self.goal = goal
        
    def formulate_goal(self, percept):
        if percept == self.goal:
            return "goal reached"
        return "searching"
    
    def act(self, percept, environment):
        goal_status = self.formulate_goal(percept)
        if goal_status == "goal reached":
            return f"gaol {self.goal} found!"
        else:
            return environment.dfs_search(percept, self.goal)
        
class Environment:
    def __init__(self, graph):
        self.graph = graph
    
    def get_percept(self, node):
        return node
    
    def dfs_search(self, start, goal):
        visited = []
        stack = []
        
        visited.append(start)
        stack.append(start)
        
        while stack:
            node = stack.pop()
            print(f"visiting: {node}")
            
            if node == goal:
                return f"goal {goal} found!"
            
            for neighbour in reversed(self.graph.get(node, [])):
                if neighbour not in visited:
                    visited.append(neighbour)
                    stack.append(neighbour)
                    
        return "goal not found"
    
    
def run_agent(agent, environment, start_node):
    percept = environment.get_percept(start_node)
    action = agent.act(percept, environment)
    print(action)
    
    
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

start_node = 'A'
goal_node = 'I'

agent = GoalBasedAgent(goal_node)
environment = Environment(tree)

run_agent(agent, environment, start_node)
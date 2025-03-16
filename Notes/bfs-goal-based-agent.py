#bfs goal based agent
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
            return f"goal {self.goal} found!"
        else:
            return environment.bfs_search(percept, self.goal)
        
class Environment:
    def __init__(self, graph):
        self.graph = graph
        
    def get_percept(self, node):
        return node
    
    def bfs_search(self, start, goal):
        visited = []
        queue = []
        
        visited.append(start)
        queue.append(start)
        
        while queue:
            node = queue.pop(0)
            print(f"visiting: {node}")
            
            if node == goal:
                return f"goal {goal} found!"
            
            
            for neighbour in self.graph.get(node, []):
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        
        return "goal not found."
    
    
def run_agent(agent, environment, start_node):
    percept = environment.get_percept(start_node)
    action = agent.act(percept, environment)
    print(action)
    
    
# Tree Representation
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

# Define Start and Goal Nodes
start_node = 'A'
goal_node = 'I'

# Create instances of agent and environment
agent = GoalBasedAgent(goal_node)
environment = Environment(tree)

run_agent(agent, environment, start_node)
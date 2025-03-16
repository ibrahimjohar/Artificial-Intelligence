class Env:
    def __init__(self):
        self.grid = {
            'a': 'safe', 'b': 'safe', 'c': 'fire',
            'd': 'safe', 'e': 'fire', 'f': 'safe',
            'g': 'safe', 'h': 'safe', 'j': 'fire'
        }
        
    def get_status(self):
        return self.grid
    
    def update_status(self, room, status):
        self.grid[room] = status 
        
    def display(self):
        rows = [
            ['a','b','c'],
            ['d','e','f'],
            ['g','h','j']
        ]
        
        symbol = lambda status: "🔥" if status == 'fire' else " "
        
        print("current environment:")
        
        for row in rows:
            print(" | ".join(symbol(self.grid[room]) for room in row))
        print()
        
class Robot:
    def __init__(self):
        self.path = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j']
        self.position = self.path[0]
        
    def move(self, environment):
        for room in self.path:
            self.position = room
            print(f"robot is moving to room '{self.position}'...")
            
            if environment.grid[room] == 'fire':
                print(f"Fire detected in room '{self.position}'. Extinguishing fire...")
                environment.update_status(room, 'safe')
            else:
                print(f"room {self.position} is already safe")
            
            environment.display()
            
def run_agent(agent, environment):
    state = environment.get_status()
    print("initial state\n")
    print(state)
    print("\nexecuting delivery tasks...\n")
    agent.move(environment)
    print("\nfinal state:\n")
    print(environment.get_status())        


agent = Robot()
environment = Env()

run_agent(agent, environment)
#alpha-beta pruning

# major drawback of the Minimax strategy is that it explores every node in the game tree, which can be time-consuming and computationally expensive. 
# Alpha-Beta Pruning addresses this issue by reducing the number of nodes explored in the search tree.

#key idea behind alpha-beta pruning is to "prune" or eliminate branches of the tree that do not affect the final decision.

#Alpha-Beta Pruning works based on two threshold values:

# alpha(-∞):
#    best value that the max player can gurantee at any pt. acts as the lowerbound (-ve infinity initially)
#    α = -∞ (worst case for Max)

# beta(+∞):
#   best value that the min player can gurantee at any pt. acts as the upperbound (+ve infinity initially)
#   β = +∞ (worst case for Min)

#pruning mechanism ensures that branches that cant influence the outcome are skipped
#making the algo faster & efficient w/o compromising accuracy

# function minimax(node, depth, alpha, beta, maximizingPlayer) is
#     if depth == 0 or node is a terminal node then
#         return static evaluation of node 
    
#     if MaximizingPlayer then // for Maximizer Player
#         maxEva = -infinity
#         for each child of node do 
#             eva = minimax(child, depth - 1, false)
#             maxEva = max(maxEva, eva) //gives the maximum value
#             alpha = max(aplha, maxEva)
#             if beta <= alpha then
#                   break
#         return maxEva 
#     else // for Minimizer Player 
#         minEva = +infinity
#         for each child of node do 
#             eva = minimax(child, depth - 1, true)
#             minEva = min(minEva, eva) //gives the minimum value 
#             beta = min(beta, eva)
#             if beta <= alpha then 
#                   break 
#         return minEva

import math

class node:
    def __init__(self, value=None):
        self.value = value
        self.children = []
        self.minimax_value = None
        
class MinimaxAgent:
    def __init__(self, depth):
        self.depth = depth
        
    def formulate_goal(self, node):
        return "goal reached" if node.minimax_value is not None else "searching"
    
    def act(self, node, environment):
        goal_status = self.formulate_goal(node)
        if goal_status == "goal reached":
            return f"minimax value for root node: {node.minimax_value}"
        else:
            return environment.alpha_beta_search(node, self.depth, -math.inf, math.inf, True)
        
        
class Environment:
    def __init__(self, tree):
        self.tree = tree
        self.computed_nodes = []
        
    def get_percept(self, node):
        return node
    
    def alpha_beta_search(self, node, depth, alpha, beta, maximizingPlayer=True):
        self.computed_nodes.append(node.value)
        if depth == 0 or not node.children:
            return node.value
        
        if maximizingPlayer:
            value = -math.inf
            for child in node.children:
                value = max(value, self.alpha_beta_search(child, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    print("pruned node: ", child.value)
                    break
            node.minimax_value = value
            return value
        else:
            value = math.inf
            for child in node.children:
                value = min(value, self.alpha_beta_search(child, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    print("pruned node: ", child.value)
                    break
            node.minimax_value = value
            return value 
            
def run_agent(agent, environment, start_node):
    percept = environment.get_percept(start_node)
    agent.act(percept, environment)
    
# constructing the tree
root = node('A')
n1 = node('B')
n2 = node('C')
root.children = [n1, n2]
n3 = node('D')
n4 = node('E')
n5 = node('F')
n6 = node('G')
n1.children = [n3, n4]
n2.children = [n5, n6]
n7 = node(2)
n8 = node(3)
n9 = node(5)
n10 = node(9)
n3.children = [n7, n8]
n4.children = [n9, n10]
n11 = node(0)
n12 = node(1)
n13 = node(7)
n14 = node(5)
n5.children = [n11, n12]
n6.children = [n13, n14]

#define the depth for alpha-beta pruning 
depth = 3

agent = MinimaxAgent(depth)
environment = Environment(root)

run_agent(agent, environment, root)

print("Computed Nodes:", environment.computed_nodes)
print("Minimax values:")
print(f"A: {root.minimax_value}")
print(f"B: {n1.minimax_value}")
print(f"C: {n2.minimax_value}")
print(f"D: {n3.minimax_value}")
print(f"E: {n4.minimax_value}")
print(f"F: {n5.minimax_value}")
print(f"G: {n6.minimax_value}")


#output:
# pruned node:  5
# pruned node:  F
# Computed Nodes: ['A', 'B', 'D', 2, 3, 'E', 5, 'C', 'F', 0, 1]
# Minimax values:
# A: 3
# B: 3
# C: 1
# D: 3
# E: 5
# F: 1
# G: None

#task 2

import math

class CardNode:
    def __init__(self, cards, turn_max, max_score=0, min_score=0):
        self.cards = cards            #remaining cards
        self.turn_max = turn_max      #true if max's turn, false if min's
        self.max_score = max_score    #accumulated max score
        self.min_score = min_score    #accumulated min score
        self.children = []            #child CardNode states
        self.minimax_value = None     #store evaluated max_score at root

class MinimaxAgent:
    def __init__(self, depth):
        self.depth = depth

    def formulate_goal(self, node):
        return "goal reached" if node.minimax_value is not None else "searching"

    def act(self, node, environment):
        status = self.formulate_goal(node)
        if status == "goal reached":
            return node.minimax_value
        return environment.compute_minimax(node, self.depth)

class Environment:
    def __init__(self):
        self.computed_states = []

    def compute_minimax(self, node, depth):
        if depth == 0 or not node.cards:
            node.minimax_value = node.max_score
            self.computed_states.append(node.cards)
            return node.max_score
        
        if node.turn_max:
            best = -math.inf
            for pick_idx in (0, -1):  #left or right
                pick = node.cards[pick_idx]
                rem = node.cards[1:] if pick_idx == 0 else node.cards[:-1]
                child = CardNode(rem,
                                 turn_max=False,
                                 max_score=node.max_score + pick,
                                 min_score=node.min_score)
                node.children.append(child)
                val = self.compute_minimax(child, depth - 1)
                best = max(best, val)
                if best >= math.inf: break
            
            node.minimax_value = best
            self.computed_states.append(node.cards)
            return best
        else:
            #min's greedy turn: pick smaller end
            left, right = node.cards[0], node.cards[-1]
            if left <= right:
                pick_idx = 0
            else:
                pick_idx = -1
            
            pick = node.cards[pick_idx]
            rem = node.cards[1:] if pick_idx == 0 else node.cards[:-1]
            child = CardNode(rem,
                             turn_max=True,
                             max_score=node.max_score,
                             min_score=node.min_score + pick)
            node.children.append(child)
            val = self.compute_minimax(child, depth - 1)
            node.minimax_value = val
            self.computed_states.append(node.cards)
            return val

def play_card_game(cards, depth=10):
    env = Environment()
    agent = MinimaxAgent(depth)
    root = CardNode(tuple(cards), turn_max=True)
    
    #run minimax
    best_score = agent.act(root, env)
    
    #play moves sequentially following the tree
    node = root
    max_score = 0
    min_score = 0
    print(f"initial cards: {list(node.cards)}\n")
    
    while node.cards:
        if node.turn_max:
            #pick child with node.minimax_value
            for child in node.children:
                if child.minimax_value == root.minimax_value:
                    pick = list(set(node.cards) - set(child.cards))[0]
                    max_score += pick
                    print(f"max picks {pick}, remaining cards: {list(child.cards)}")
                    node = child
                    break
        else:
            #single child in greedy
            child = node.children[0]
            pick = list(set(node.cards) - set(child.cards))[0]
            min_score += pick
            print(f"min picks {pick}, remaining cards: {list(child.cards)}")
            node = child
        root = node
    
    print(f"\nfinal scores - max: {max_score}, min: {min_score}")
    winner = "Max" if max_score > min_score else "Min" if min_score > max_score else "Draw"
    print(f"winner: {winner}")

#simulation example
play_card_game([4, 10, 6, 2, 9, 5], depth=10)

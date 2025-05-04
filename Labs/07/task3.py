#task3

import random
import string

#constants
grid_size = 10
ship_lengths = [5, 4, 3, 3, 2]

def coord_to_index(coord):
    row = int(coord[1:]) - 1
    col = string.ascii_uppercase.index(coord[0].upper())
    return row, col

def index_to_coord(r, c):
    return f"{string.ascii_uppercase[c]}{r+1}"

def print_grid(grid, show_ships=False):
    header = "  " + " ".join(str(i + 1) for i in range(grid_size))
    print(header)
    for r in range(grid_size):
        line = []
        for c in range(grid_size):
            cell = grid[r][c]
            if cell == 'O':
                char = 'O' if show_ships else '~'
            elif cell == 'X':
                char = 'X'
            elif cell == 'M':
                char = 'M'
            else:
                char = '~'
            line.append(char)
        print(f"{string.ascii_uppercase[r]} " + " ".join(line))
    print()

class Board:
    def __init__(self):
        self.grid = [['~'] * grid_size for _ in range(grid_size)]
        self.ships = []

    def place_random_ships(self):
        for length in ship_lengths:
            placed = False
            while not placed:
                orient = random.choice(['H', 'V'])
                r = random.randint(0, grid_size - 1)
                c = random.randint(0, grid_size - 1)
                coords = [(r + (i if orient == 'V' else 0), c + (i if orient == 'H' else 0)) for i in range(length)]
                if all(0 <= rr < grid_size and 0 <= cc < grid_size and self.grid[rr][cc] == '~' for rr, cc in coords):
                    for rr, cc in coords:
                        self.grid[rr][cc] = 'O'
                    self.ships.append(set(coords))
                    placed = True

    def receive_attack(self, r, c):
        if self.grid[r][c] == 'O':
            self.grid[r][c] = 'X'
            for ship in self.ships:
                if (r, c) in ship:
                    ship.remove((r, c))
                    return 'sunk' if not ship else 'hit'
        elif self.grid[r][c] == '~':
            self.grid[r][c] = 'M'
            return 'miss'
        return 'already'

    def all_sunk(self):
        return all(not ship for ship in self.ships)

class BattleshipAI:
    def __init__(self):
        self.heatmap = [[0] * grid_size for _ in range(grid_size)]
        self.known_hits = []
        self.guessed = set()

    def update_heatmap(self, board):
        self.heatmap = [[0] * grid_size for _ in range(grid_size)]
        for length in ship_lengths:
            #horizontal
            for r in range(grid_size):
                for c in range(grid_size - length + 1):
                    if all(board.grid[r][c + i] in ('~', 'O') for i in range(length)):
                        for i in range(length):
                            self.heatmap[r][c + i] += 1
            #vertical
            for r in range(grid_size - length + 1):
                for c in range(grid_size):
                    if all(board.grid[r + i][c] in ('~', 'O') for i in range(length)):
                        for i in range(length):
                            self.heatmap[r + i][c] += 1

    def pick_move(self, board):
        if self.known_hits:
            r, c = self.known_hits[-1]
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < grid_size and 0 <= nc < grid_size and (nr, nc) not in self.guessed:
                    self.guessed.add((nr, nc))
                    return nr, nc

        self.update_heatmap(board)
        best_val = -1
        best = []
        for r in range(grid_size):
            for c in range(grid_size):
                if (r, c) not in self.guessed:
                    if self.heatmap[r][c] > best_val:
                        best = [(r, c)]
                        best_val = self.heatmap[r][c]
                    elif self.heatmap[r][c] == best_val:
                        best.append((r, c))
        choice = random.choice(best)
        self.guessed.add(choice)
        return choice

#setup
grid_player = Board()
grid_ai = Board()
grid_player.place_random_ships()
grid_ai.place_random_ships()
ai = BattleshipAI()

#game-loop
def game_loop():
    print("welcome to battleship!\nyour grid is hidden, just enter coordinates to attack (e.g., B4)")
    while True:
        print("your turn:")
        print_grid(grid_ai.grid, show_ships=False)
        move = input("enter coordinate to attack (e.g., B4):").strip().upper()
        try:
            r, c = coord_to_index(move)
        except:
            print("invalid")
            continue
        res = grid_ai.receive_attack(r, c)
        print(f"player attacks: {move} → {res}")
        if res in ('hit', 'sunk'):
            ai.known_hits.append((r, c))
        if grid_ai.all_sunk():
            print("you win!")
            break

        print("AI's turn:")
        ar, ac = ai.pick_move(grid_player)
        pos = index_to_coord(ar, ac)
        res = grid_player.receive_attack(ar, ac)
        print(f"AI attacks: {pos} → {res}")
        if res in ('hit', 'sunk'):
            ai.known_hits.append((ar, ac))

        print("your board:")
        print_grid(grid_player.grid, show_ships=True)
        if grid_player.all_sunk():
            print("AI wins!")
            break

if __name__ == '__main__':
    game_loop()

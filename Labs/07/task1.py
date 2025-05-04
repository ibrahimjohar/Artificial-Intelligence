#task1
import copy
import math

#constants
EMPTY = '.'
WHITE = 'W'
WHITE_KING = 'WK'
BLACK = 'B'
BLACK_KING = 'BK'
ROWS, COLS = 8, 8

#dir: (dr, dc)
DIRECTIONS = {
    WHITE: [(-1, -1), (-1, 1)],
    BLACK: [(1, -1), (1, 1)],
    WHITE_KING: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    BLACK_KING: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
}

class Move:
    def __init__(self, path, captures=None):
        self.path = path          #list of positions [(r,c), ..]
        self.src = path[0]
        self.dest = path[-1]
        self.captures = captures or []  #list of positions captured
    def __repr__(self):
        cap = f" captures {self.captures}" if self.captures else ""
        return f"move({self.src}->{self.dest}{cap})"

class CheckersGame:
    def __init__(self, depth=4):
        self.board = self._init_board()
        self.depth = depth
        self.turn = WHITE

    def _init_board(self):
        b = [[EMPTY]*COLS for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if (r + c) % 2:
                    if r < 3:
                        b[r][c] = BLACK
                    elif r > 4:
                        b[r][c] = WHITE
        return b

    def print_board(self):
        print("  " + " ".join(map(str, range(COLS))))
        for r, row in enumerate(self.board):
            print(r, " ".join(cell.rjust(2) for cell in row))
        print()

    def inside(self, r, c):
        return 0 <= r < ROWS and 0 <= c < COLS

    def get_moves(self, player):
        #mandatory captures
        caps = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] in (player, player+'K'):
                    caps += self._captures_from(r, c, self.board, [])
        if caps:
            return caps
        #simple moves
        moves = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] in (player, player+'K'):
                    moves += self._simple_moves_from(r, c)
        return moves

    def _simple_moves_from(self, r, c):
        piece = self.board[r][c]
        dirs = DIRECTIONS[piece]
        out = []
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if self.inside(nr, nc) and self.board[nr][nc] == EMPTY:
                out.append(Move([(r, c), (nr, nc)]))
        return out

    def _captures_from(self, r, c, board, visited):
        piece = board[r][c]
        dirs = DIRECTIONS[piece]
        moves = []
        any_capture = False
        for dr, dc in dirs:
            mr, mc = r+dr, c+dc
            er, ec = r+2*dr, c+2*dc
            if self.inside(er, ec) and board[er][ec] == EMPTY:
                target = board[mr][mc]
                if target != EMPTY and target[0] != piece[0] and (mr,mc) not in visited:
                    any_capture = True
                    nb = copy.deepcopy(board)
                    nb[r][c] = EMPTY
                    nb[mr][mc] = EMPTY
                    nb[er][ec] = piece
                    #promote
                    if piece == WHITE and er == 0: nb[er][ec] = WHITE_KING
                    if piece == BLACK and er == 7: nb[er][ec] = BLACK_KING
                    next_moves = self._captures_from(er, ec, nb, visited+[(mr,mc)])
                    if next_moves:
                        for m in next_moves:
                            moves.append(Move([(r,c)]+m.path, [(mr,mc)]+m.captures))
                    else:
                        moves.append(Move([(r,c),(er,ec)], [(mr,mc)]))
        return moves

    def apply_move(self, move):
        b = self.board
        src, dst = move.src, move.dest
        piece = b[src[0]][src[1]]
        b[src[0]][src[1]] = EMPTY
        b[dst[0]][dst[1]] = piece
        for mr, mc in move.captures:
            b[mr][mc] = EMPTY
        #promote
        if piece == WHITE and dst[0] == 0:
            b[dst[0]][dst[1]] = WHITE_KING
        if piece == BLACK and dst[0] == 7:
            b[dst[0]][dst[1]] = BLACK_KING
        self.turn = BLACK if self.turn == WHITE else WHITE

    def evaluate(self):
        score = 0
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p == WHITE: score += 1+(7-r)*0.1
                if p == WHITE_KING: score += 2
                if p == BLACK: score -= 1+r*0.1
                if p == BLACK_KING: score -= 2
        return score

    def minimax(self, board_state, depth, alpha, beta, maximizing):
        if depth == 0 or not self.get_moves(self.turn if maximizing else self.turn):
            return self.evaluate(), None
        best_move = None
        if maximizing:
            value = -math.inf
            for m in self.get_moves(self.turn):
                saved = copy.deepcopy(self.board)
                saved_turn = self.turn
                self.apply_move(m)
                val, _ = self.minimax(self.board, depth-1, alpha, beta, False)
                if val > value:
                    value, best_move = val, m
                alpha = max(alpha, value)
                self.board, self.turn = saved, saved_turn
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = math.inf
            for m in self.get_moves(self.turn):
                saved = copy.deepcopy(self.board)
                saved_turn = self.turn
                self.apply_move(m)
                val, _ = self.minimax(self.board, depth-1, alpha, beta, True)
                if val < value:
                    value, best_move = val, m
                beta = min(beta, value)
                self.board, self.turn = saved, saved_turn
                if alpha >= beta:
                    break
            return value, best_move

    def ai_move(self):
        _, m = self.minimax(self.board, self.depth, -math.inf, math.inf, True)
        return m

    def is_over(self):
        return not self.get_moves(WHITE) or not self.get_moves(BLACK)

if __name__ == '__main__':
    game = CheckersGame()
    while not game.is_over():
        game.print_board()
        if game.turn == WHITE:
            moves = game.get_moves(WHITE)
            for i, m in enumerate(moves):
                print(f"{i}: {m}")
            try:
                idx = int(input("choose your move: "))
                if 0 <= idx < len(moves):
                    game.apply_move(moves[idx])
                else:
                    print("invalid move num.")
            except ValueError:
                print("please enter a valid num.")
        else:
            print("AI (BLACK) is thinking right now...")
            move = game.ai_move()
            if move:
                print(f"AI chose: {move}")
                game.apply_move(move)
            else:
                print("AI has no moves.")
    print("game over.")
    game.print_board()

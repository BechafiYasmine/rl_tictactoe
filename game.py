# game.py
# Tic-Tac-Toe Game Logic

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        # 0 = empty, 1 = human, -1 = AI
        self.board = [0] * 9
        self.current_player = 1
        return self.board

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, position, player):
        if self.board[position] == 0:
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]

        for a, b, c in wins:
            s = self.board[a] + self.board[b] + self.board[c]
            if s == 3:
                return 1      # Human wins
            if s == -3:
                return -1     # AI wins

        if 0 not in self.board:
            return 0          # Draw

        return None           # Game not finished

    def get_state(self):
        return tuple(self.board)

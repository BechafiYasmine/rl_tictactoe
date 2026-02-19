import numpy as np

class TicTacToeGame:
    """The game environment - manages board state and rules"""
    
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.done = False
        self.winner = None
    
    def reset(self):
        """Start a new game"""
        self.board = [' '] * 9
        self.current_player = 'X'
        self.done = False
        self.winner = None
        return self.get_state()
    
    def get_state(self):
        """Convert board to tuple for memory key"""
        return tuple(self.board)
    
    def get_valid_moves(self):
        """Return list of empty squares"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def is_winner(self, player):
        """Check if player has won"""
        win_patterns = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # columns
            [0,4,8], [2,4,6]             # diagonals
        ]
        for pattern in win_patterns:
            if all(self.board[i] == player for i in pattern):
                return True
        return False
    
    def is_draw(self):
        """Check if game is a draw"""
        return ' ' not in self.board and not self.is_winner('X') and not self.is_winner('O')
    
    def make_move(self, position):
        """
        Make a move at the specified position
        Returns: (new_state, reward, done, winner)
        """
        # Check if game already over
        if self.done:
            return self.get_state(), 0, True, None
        
        # Check if move is valid
        if self.board[position] != ' ':
            return self.get_state(), -10, True, None
        
        # Place the piece
        self.board[position] = self.current_player
        
        # Check win
        if self.is_winner(self.current_player):
            self.done = True
            self.winner = self.current_player
            reward = 1
        # Check draw
        elif self.is_draw():
            self.done = True
            self.winner = None
            reward = 0
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            reward = -0.01
        
        return self.get_state(), reward, self.done, self.winner
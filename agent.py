import numpy as np
import random 
from collections import defaultdict

class QLearningAgent:
    """The agent that learns to play tic-tac-toe"""
    
    def __init__(self, player='X'):
        self.player = player
        self.memory = defaultdict(lambda: np.zeros(9))  # Q-table
        self.curiosity = 1.0        # Exploration rate (epsilon)
        self.learning_speed = 0.1    # Learning rate (alpha)
        self.future_optimism = 0.9   # Discount factor (gamma)
        self.min_curiosity = 0.01
    
    def get_state_key(self, board):
        """Convert board list to string key"""
        return ''.join(board)
    
    def choose_move(self, board, valid_moves):
        """
        Choose a move using epsilon-greedy policy
        """
        state_key = self.get_state_key(board)
        
        # Exploration: random move
        if random.random() < self.curiosity:
            return random.choice(valid_moves)
        
        # Exploitation: best move from memory
        values = self.memory[state_key]
        
        best_move = valid_moves[0]
        best_value = values[best_move]
        
        for move in valid_moves:
            if values[move] > best_value:
                best_value = values[move]
                best_move = move
        
        return best_move
    
    def learn(self, board_before, move, reward, board_after, game_over):
        """
        Update Q-table using Q-learning formula
        """
        state_key = self.get_state_key(board_before)
        next_key = self.get_state_key(board_after)
        
        # Old value
        old_value = self.memory[state_key][move]
        
        # Calculate reality
        if game_over:
            reality = reward
        else:
            best_future = max(self.memory[next_key])
            reality = reward + self.future_optimism * best_future
        
        # Update
        error = reality - old_value
        new_value = old_value + self.learning_speed * error
        self.memory[state_key][move] = new_value
    
    def become_less_curious(self):
        """Reduce exploration over time"""
        self.curiosity *= 0.995
        if self.curiosity < self.min_curiosity:
            self.curiosity = self.min_curiosity
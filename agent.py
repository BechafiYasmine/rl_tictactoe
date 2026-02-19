# agent.py
import random

class RandomAgent:
    def __init__(self, player=-1):
        self.player = player  # -1 = AI

    def choose_move(self, available_moves):
        # Just pick a random empty spot
        return random.choice(available_moves)

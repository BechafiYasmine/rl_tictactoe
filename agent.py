# agent.py
# Simple Random Agent

import random


class RandomAgent:
    def __init__(self, player=-1):
        self.player = player  # -1 = AI

    def choose_move(self, game):
        """
        Choose a random move from available moves
        """
        moves = game.available_moves()

        if len(moves) == 0:
            return None

        return random.choice(moves)

# agent.py
import random
import pickle
import os


class QLearningAgent:

    def __init__(self, player=-1, alpha=0.5, gamma=0.9, epsilon=0.1):

        self.player = player
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.q_table = {}

    # -------------------------
    # Q TABLE
    # -------------------------

    def get_q(self, state, action):

        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in range(9)}

        return self.q_table[state][action]

    # -------------------------
    # SMART MOVE
    # -------------------------

    def choose_move(self, state, available_moves):

        board = list(state)

        # 1️⃣ Try to WIN
        for move in available_moves:

            board[move] = self.player

            if self._is_winner(board, self.player):
                board[move] = 0
                return move

            board[move] = 0

        # 2️⃣ Try to BLOCK human
        for move in available_moves:

            board[move] = -self.player

            if self._is_winner(board, -self.player):
                board[move] = 0
                return move

            board[move] = 0

        # 3️⃣ Explore
        if random.random() < self.epsilon:
            return random.choice(available_moves)

        # 4️⃣ Exploit Q-table
        q_vals = {a: self.get_q(state, a) for a in available_moves}

        max_q = max(q_vals.values())

        best_moves = [a for a, v in q_vals.items() if v == max_q]

        return random.choice(best_moves)

    # -------------------------
    # LEARNING
    # -------------------------

    def update_q(self, state, action, reward, next_state, next_moves):

        max_future = 0

        if next_moves:
            max_future = max(
                [self.get_q(next_state, a) for a in next_moves]
            )

        old_q = self.get_q(state, action)

        new_q = old_q + self.alpha * (
            reward + self.gamma * max_future - old_q
        )

        self.q_table[state][action] = new_q

    # -------------------------
    # SAVE / LOAD
    # -------------------------

    def save_q(self, file="q_table.pkl"):

        with open(file, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q(self, file="q_table.pkl"):

        if os.path.exists(file):

            with open(file, "rb") as f:
                self.q_table = pickle.load(f)

    # -------------------------
    # CHECK WIN
    # -------------------------

    def _is_winner(self, board, player):

        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]

        for a,b,c in wins:

            if board[a] == board[b] == board[c] == player:
                return True

        return False
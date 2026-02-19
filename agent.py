# agent.py
import random
import pickle

class QLearningAgent:
    def __init__(self, player=-1, alpha=0.5, gamma=0.9, epsilon=0.2):
        self.player = player
        self.q_table = {}  # state: {action: value}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {a:0 for a in range(9)}
        return self.q_table[state][action]

    def choose_move(self, state, available_moves):
        # Exploration
        if random.random() < self.epsilon:
            return random.choice(available_moves)

        # Exploitation
        q_values = {a:self.get_q(state,a) for a in available_moves}
        max_q = max(q_values.values())
        best_moves = [a for a,v in q_values.items() if v==max_q]
        return random.choice(best_moves)

    def update_q(self, state, action, reward, next_state, next_available):
        max_future = 0
        if next_available:
            max_future = max([self.get_q(next_state,a) for a in next_available])
        old_q = self.get_q(state,action)
        self.q_table[state][action] = old_q + self.alpha * (reward + self.gamma*max_future - old_q)

    def save_q(self, filename="q_table.pkl"):
        with open(filename,"wb") as f:
            pickle.dump(self.q_table,f)

    def load_q(self, filename="q_table.pkl"):
        with open(filename,"rb") as f:
            self.q_table = pickle.load(f)

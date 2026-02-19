from game import TicTacToe
from agent import QLearningAgent
import random

ai = QLearningAgent()
episodes = 50000

for _ in range(episodes):
    game = TicTacToe()
    state = game.get_state()
    while True:
        moves = game.available_moves()
        if not moves:
            break

        # Random human for training
        human_move = random.choice(moves)
        game.make_move(human_move, 1)
        winner = game.check_winner()
        if winner is not None:
            reward = -1 if winner==-1 else 1 if winner==1 else 0
            break

        # AI turn
        moves = game.available_moves()
        action = ai.choose_move(state, moves)
        game.make_move(action, -1)
        next_state = game.get_state()
        next_moves = game.available_moves()
        winner = game.check_winner()
        reward = 1 if winner==-1 else -1 if winner==1 else 0
        ai.update_q(state, action, reward, next_state, next_moves)
        state = next_state

ai.save_q()
print("Training completed and Q-table saved.")

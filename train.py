# train.py
from game import TicTacToe
from agent import QLearningAgent
import random


ai = QLearningAgent()
ai.load_q()

episodes = 300000


for i in range(episodes):

    game = TicTacToe()
    state = game.get_state()

    while True:

        # Random human
        moves = game.available_moves()

        if not moves:
            break

        human = random.choice(moves)
        game.make_move(human, 1)

        winner = game.check_winner()

        if winner is not None:
            break

        # AI turn
        moves = game.available_moves()

        action = ai.choose_move(state, moves)

        game.make_move(action, -1)

        next_state = game.get_state()
        next_moves = game.available_moves()

        winner = game.check_winner()

        reward = 0

        if winner == -1:
            reward = 1
        elif winner == 1:
            reward = -1

        ai.update_q(
            state,
            action,
            reward,
            next_state,
            next_moves
        )

        state = next_state

    if i % 20000 == 0:
        print("Training:", i)


ai.save_q()

print("Training finished.")

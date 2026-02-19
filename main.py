import random

from game import TicTacToe
from agent import RandomAgent

game = TicTacToe()
ai = RandomAgent()

# Simple test loop
while True:
    print("Board:", game.board)
    moves = game.available_moves()
    if not moves:
        break

    # Human (simulated random for now)
    human_move = random.choice(moves)
    game.make_move(human_move, 1)

    winner = game.check_winner()
    if winner is not None:
        print("Winner:", winner)
        break

    # AI move
    moves = game.available_moves()
    ai_move = ai.choose_move(moves)
    game.make_move(ai_move, -1)

    winner = game.check_winner()
    if winner is not None:
        print("Winner:", winner)
        break

# main.py
from game import TicTacToe

game = TicTacToe()

print("Initial board:", game.board)

game.make_move(0, 1)
game.make_move(4, -1)
game.make_move(1, 1)

print("Board now:", game.board)
print("Winner:", game.check_winner())

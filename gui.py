# gui.py
import tkinter as tk
from tkinter import messagebox

from game import TicTacToe
from agent import QLearningAgent


class TicTacToeGUI:

    def __init__(self):

        self.game = TicTacToe()
        self.ai = QLearningAgent()

        self.ai.load_q()

        self.last_state = None
        self.last_action = None

        self.root = tk.Tk()
        self.root.title("Tic Tac Toe AI")

        self.buttons = []
        self.create_buttons()

        self.root.mainloop()

    def create_buttons(self):

        for i in range(9):

            btn = tk.Button(
                self.root,
                text="",
                width=10,
                height=5,
                font=("Arial", 20),
                command=lambda i=i: self.click(i)
            )

            btn.grid(row=i // 3, column=i % 3)

            self.buttons.append(btn)

    def click(self, pos):

        # Human move
        if self.game.board[pos] != 0:
            return

        self.game.make_move(pos, 1)
        self.update_buttons()

        if self.check_end():
            return

        # AI move
        state = self.game.get_state()
        moves = self.game.available_moves()

        ai_move = self.ai.choose_move(state, moves)

        self.last_state = state
        self.last_action = ai_move

        self.game.make_move(ai_move, -1)
        self.update_buttons()

        self.check_end()

    def update_buttons(self):

        for i in range(9):

            if self.game.board[i] == 1:
                self.buttons[i]["text"] = "X"

            elif self.game.board[i] == -1:
                self.buttons[i]["text"] = "O"

            else:
                self.buttons[i]["text"] = ""

    def check_end(self):

        winner = self.game.check_winner()

        if winner is not None:

            if winner == -1:
                reward = 1
                msg = "AI Wins!"

            elif winner == 1:
                reward = -1
                msg = "You Win!"

            else:
                reward = 0
                msg = "Draw!"

            # Learn from game
            if self.last_state is not None:

                self.ai.update_q(
                    self.last_state,
                    self.last_action,
                    reward,
                    self.game.get_state(),
                    self.game.available_moves()
                )

                self.ai.save_q()

            messagebox.showinfo("Game Over", msg)

            self.game.reset()
            self.update_buttons()

            return True

        return False


if __name__ == "__main__":

    TicTacToeGUI()

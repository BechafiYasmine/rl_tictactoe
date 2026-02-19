import tkinter as tk
from game import TicTacToe
from agent import QLearningAgent

class TicTacToeGUI:
    def __init__(self):
        self.game = TicTacToe()
        self.ai = QLearningAgent()
        self.ai.load_q()
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe AI")
        self.buttons = []
        self.create_buttons()
        self.window.mainloop()

    def create_buttons(self):
        for i in range(9):
            btn = tk.Button(self.window, text="", width=10, height=5,
                            command=lambda i=i: self.click(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def click(self, pos):
        if self.game.board[pos] != 0:
            return
        self.game.make_move(pos, 1)
        self.update_buttons()
        if self.check_end(): return

        # AI move
        state = self.game.get_state()
        moves = self.game.available_moves()
        ai_move = self.ai.choose_move(state, moves)
        self.game.make_move(ai_move, -1)
        self.update_buttons()
        self.check_end()

    def update_buttons(self):
        for i in range(9):
            if self.game.board[i]==1:
                self.buttons[i]["text"] = "X"
            elif self.game.board[i]==-1:
                self.buttons[i]["text"] = "O"
            else:
                self.buttons[i]["text"] = ""

    def check_end(self):
        winner = self.game.check_winner()
        if winner is not None:
            if winner==1: msg="You Win!"
            elif winner==-1: msg="AI Wins!"
            else: msg="Draw!"
            tk.messagebox.showinfo("Game Over", msg)
            self.game.reset()
            self.update_buttons()
            return True
        return False

# Run GUI
if __name__=="__main__":
    TicTacToeGUI()

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
        self.root.geometry("500x550")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)

        # Title
        title_label = tk.Label(
            self.root,
            text="Tic Tac Toe vs AI",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Your turn (X)",
            font=("Arial", 14),
            bg='#2c3e50',
            fg='#3498db'
        )
        self.status_label.pack(pady=10)

        # Frame for game board
        board_frame = tk.Frame(self.root, bg='#34495e', padx=20, pady=20)
        board_frame.pack(expand=True)

        self.buttons = []
        self.create_buttons(board_frame)

        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=30)

        # Reset button
        reset_btn = tk.Button(
            control_frame,
            text="New Game",
            command=self.reset_game,
            font=("Arial", 12),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            bd=0,
            cursor='hand2'
        )
        reset_btn.pack(side=tk.LEFT, padx=10)

        # Quit button
        quit_btn = tk.Button(
            control_frame,
            text="Quit",
            command=self.root.quit,
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            bd=0,
            cursor='hand2'
        )
        quit_btn.pack(side=tk.LEFT, padx=10)

        self.root.mainloop()

    def create_buttons(self, parent):

        colors = {
            1: {'bg': '#2ecc71', 'fg': 'white', 'text': 'X'},
            -1: {'bg': '#e74c3c', 'fg': 'white', 'text': 'O'},
            0: {'bg': '#ecf0f1', 'fg': '#2c3e50', 'text': ''}
        }

        for i in range(9):
            btn = tk.Button(
                parent,
                text="",
                width=4,
                height=2,
                font=("Arial", 24, "bold"),
                bg=colors[0]['bg'],
                fg=colors[0]['fg'],
                bd=2,
                relief='raised',
                cursor='hand2',
                command=lambda i=i: self.click(i)
            )

            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

    def click(self, pos):

        # Human move
        if self.game.board[pos] != 0:
            return

        self.game.make_move(pos, 1)
        self.update_buttons()
        self.status_label.config(text="AI thinking...", fg='#f39c12')

        if self.check_end():
            return

        # Schedule AI move after a short delay for better UX
        self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        # AI move
        state = self.game.get_state()
        moves = self.game.available_moves()

        ai_move = self.ai.choose_move(state, moves)

        self.last_state = state
        self.last_action = ai_move

        self.game.make_move(ai_move, -1)
        self.update_buttons()
        self.status_label.config(text="Your turn (X)", fg='#3498db')

        self.check_end()

    def update_buttons(self):

        colors = {
            1: {'bg': '#2ecc71', 'fg': 'white', 'text': 'X'},
            -1: {'bg': '#e74c3c', 'fg': 'white', 'text': 'O'},
            0: {'bg': '#ecf0f1', 'fg': '#2c3e50', 'text': ''}
        }

        for i in range(9):
            btn = self.buttons[i]
            value = self.game.board[i]
            btn.config(
                text=colors[value]['text'],
                bg=colors[value]['bg'],
                fg=colors[value]['fg']
            )

    def check_end(self):

        winner = self.game.check_winner()

        if winner is not None:

            if winner == -1:
                reward = 1
                msg = "AI Wins!"
                color = '#e74c3c'

            elif winner == 1:
                reward = -1
                msg = "You Win!"
                color = '#2ecc71'

            else:
                reward = 0
                msg = "Draw!"
                color = '#f39c12'

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

            self.status_label.config(text=msg, fg=color)
            messagebox.showinfo("Game Over", msg)

            self.game.reset()
            self.update_buttons()
            self.status_label.config(text="Your turn (X)", fg='#3498db')

            return True

        return False

    def reset_game(self):
        self.game.reset()
        self.last_state = None
        self.last_action = None
        self.update_buttons()
        self.status_label.config(text="Your turn (X)", fg='#3498db')


if __name__ == "__main__":

    TicTacToeGUI()
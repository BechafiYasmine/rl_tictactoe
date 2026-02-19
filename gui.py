import tkinter as tk
from tkinter import messagebox
import time

class TicTacToeGUI:
    """Graphical window for Tic-Tac-Toe using tkinter"""
    
    def __init__(self, agent):
        self.agent = agent
        self.game = None
        self.human_player = 'O'
        self.ai_player = 'X'
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe vs AI")
        self.window.geometry("450x650")
        self.window.resizable(False, False)
        self.window.configure(bg='#2c3e50')
        
        # Game variables
        self.buttons = []
        self.game_active = False
        self.ai_thinking = False  # Prevent multiple AI moves
        
        # Create UI elements
        self.create_title()
        self.create_board()
        self.create_status_bar()
        self.create_control_buttons()
        
    def create_title(self):
        """Create title label"""
        title_frame = tk.Frame(self.window, bg='#2c3e50')
        title_frame.pack(pady=10)
        
        title = tk.Label(
            title_frame,
            text="Tic-Tac-Toe vs AI",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="You are O • AI is X",
            font=('Arial', 12),
            fg='#3498db',
            bg='#2c3e50'
        )
        subtitle.pack()
    
    def create_board(self):
        """Create the 3x3 game board"""
        board_frame = tk.Frame(self.window, bg='#2c3e50')
        board_frame.pack(pady=20)
        
        # Create 3x3 grid of buttons
        for i in range(9):
            row = i // 3
            col = i % 3
            
            button = tk.Button(
                board_frame,
                text=' ',
                font=('Arial', 24, 'bold'),
                width=4,
                height=2,
                bg='#34495e',
                fg='white',
                activebackground='#3498db',
                relief='raised',
                bd=3,
                command=lambda idx=i: self.square_clicked(idx)
            )
            button.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(button)
    
    def create_status_bar(self):
        """Create status bar to show game state"""
        self.status_frame = tk.Frame(self.window, bg='#2c3e50')
        self.status_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Click NEW GAME to start!",
            font=('Arial', 14, 'bold'),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.status_label.pack()
    
    def create_control_buttons(self):
        """Create control buttons"""
        control_frame = tk.Frame(self.window, bg='#2c3e50')
        control_frame.pack(side=tk.BOTTOM, pady=20)
        
        # New Game button
        new_game_btn = tk.Button(
            control_frame,
            text="🎮 NEW GAME",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            width=12,
            height=2,
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(
            control_frame,
            text="🚪 QUIT",
            font=('Arial', 14, 'bold'),
            bg='#c0392b',
            fg='white',
            width=12,
            height=2,
            command=self.quit_game
        )
        quit_btn.pack(side=tk.LEFT, padx=10)
    
    def update_status_display(self):
        """Update the status label based on actual game state"""
        if not self.game_active or not self.game:
            self.status_label.config(text="Click NEW GAME to start!", fg='#f39c12')
            return
        
        if self.game.done:
            return
        
        # Check actual game.current_player
        if self.game.current_player == self.human_player:
            self.status_label.config(
                text="🔵 YOUR TURN (O) - Click any empty square!",
                fg='#f39c12'
            )
            print(f"DEBUG: Human's turn - current_player = {self.game.current_player}")
        else:
            self.status_label.config(
                text="🤖 AI is thinking...",
                fg='#3498db'
            )
            print(f"DEBUG: AI's turn - current_player = {self.game.current_player}")
    
    def square_clicked(self, position):
        """Called when a square is clicked"""
        print(f"\n--- Square {position} clicked ---")
        print(f"Game active: {self.game_active}")
        print(f"AI thinking: {self.ai_thinking}")
        
        if not self.game_active or not self.game:
            messagebox.showinfo("Game not started", "Click NEW GAME first!")
            return
        
        if self.game.done:
            messagebox.showinfo("Game over", "Game is already over! Click NEW GAME to play again.")
            return
        
        if self.ai_thinking:
            messagebox.showinfo("Please wait", "AI is thinking... Wait a moment!")
            return
        
        # Check whose turn it REALLY is
        print(f"Current player in game: {self.game.current_player}")
        print(f"Human player should be: {self.human_player}")
        
        if self.game.current_player != self.human_player:
            messagebox.showinfo("Not your turn", f"It's AI's turn (X). Please wait!")
            return
        
        # Check if square is empty
        if self.game.board[position] != ' ':
            messagebox.showinfo("Invalid move", "This square is already taken!")
            return
        
        # Valid human move!
        print(f"✅ Valid human move at {position}")
        self.make_human_move(position)
    
    def make_human_move(self, position):
        """Process human move"""
        # Make the move in the game
        _, _, done, winner = self.game.make_move(position)
        print(f"Move made. Game done: {done}, Winner: {winner}")
        
        # Update the button
        self.buttons[position].config(
            text='O',
            fg='#e74c3c',
            state='disabled'
        )
        
        if done:
            self.game_active = False
            self.show_game_result(winner)
        else:
            # Update status to show AI's turn
            self.update_status_display()
            
            # Make AI move after delay
            print("Scheduling AI move...")
            self.ai_thinking = True
            self.window.after(800, self.make_ai_move)
    
    def make_ai_move(self):
        """Process AI move"""
        print("\n--- AI making move ---")
        
        if not self.game_active or not self.game:
            print("Game not active, cancelling AI move")
            self.ai_thinking = False
            return
        
        if self.game.done:
            print("Game is done, cancelling AI move")
            self.ai_thinking = False
            return
        
        # Verify it's actually AI's turn
        if self.game.current_player != self.ai_player:
            print(f"ERROR: It's {self.game.current_player}'s turn, not AI's!")
            self.ai_thinking = False
            self.update_status_display()
            return
        
        # Get valid moves
        valid_moves = self.game.get_valid_moves()
        if not valid_moves:
            print("No valid moves available")
            self.ai_thinking = False
            return
        
        # AI chooses move
        move = self.agent.choose_move(self.game.board, valid_moves)
        print(f"AI chooses position {move}")
        
        # Make the move
        _, _, done, winner = self.game.make_move(move)
        print(f"AI move made. Game done: {done}, Winner: {winner}")
        
        # Update the button
        self.buttons[move].config(
            text='X',
            fg='#3498db',
            state='disabled'
        )
        
        self.ai_thinking = False
        
        if done:
            self.game_active = False
            self.show_game_result(winner)
        else:
            # Update status to show human's turn
            self.update_status_display()
            print("AI done, now human's turn")
    
    def show_game_result(self, winner):
        """Show game result"""
        if winner == self.human_player:
            message = "🎉 YOU WIN! 🎉"
            color = '#27ae60'
        elif winner == self.ai_player:
            message = "🤖 AI WINS! 🤖"
            color = '#c0392b'
        else:
            message = "🤝 DRAW! 🤝"
            color = '#f39c12'
        
        self.status_label.config(text=message, fg=color)
        self.ai_thinking = False
        
        # Show popup
        messagebox.showinfo("Game Over", f"{message}\n\nClick NEW GAME to play again!")
    
    def new_game(self):
        """Start a new game"""
        from game import TicTacToeGame
        
        print("\n=== STARTING NEW GAME ===")
        
        # Create new game
        self.game = TicTacToeGame()
        self.game_active = True
        self.ai_thinking = False
        
        # IMPORTANT: In TicTacToeGame, X always starts
        # So current_player should be 'X' (AI) at the beginning
        print(f"Initial current_player: {self.game.current_player}")
        
        # Reset all buttons
        for button in self.buttons:
            button.config(
                text=' ',
                state='normal',
                bg='#34495e',
                fg='white'
            )
        
        # Update status
        self.update_status_display()
        
        # If AI starts (X), make AI move automatically
        if self.game.current_player == self.ai_player:
            print("AI starts first - scheduling AI move")
            self.window.after(500, self.make_ai_move)
    
    def quit_game(self):
        """Quit the game"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.window.quit()
            self.window.destroy()
    
    def run(self):
        """Start the GUI"""
        self.window.protocol("WM_DELETE_WINDOW", self.quit_game)
        
        # Start with a new game
        self.new_game()
        
        self.window.mainloop()
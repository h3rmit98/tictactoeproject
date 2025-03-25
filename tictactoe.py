import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        
        # Game variables
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.against_ai = False
        
        # Store default button color
        self.default_bg = self.root.cget('bg')
        
        # Create menu
        self.create_menu()
        
        # Create game board
        self.create_board()
        
    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)
        
        self.player_mode_var = tk.StringVar(value="2 Players")
        
        tk.Label(menu_frame, text="Game Mode:").pack(side=tk.LEFT, padx=5)
        modes = ["2 Players", "Against AI"]
        mode_menu = tk.OptionMenu(menu_frame, self.player_mode_var, *modes, command=self.change_mode)
        mode_menu.pack(side=tk.LEFT, padx=5)
        
        # Fix: Make sure the reset button is properly configured
        reset_button = tk.Button(menu_frame, text="Reset Game", command=self.reset_game)
        reset_button.pack(side=tk.LEFT, padx=5)
        
    def change_mode(self, _):
        self.against_ai = self.player_mode_var.get() == "Against AI"
        self.reset_game()
        
    def create_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        
        self.buttons = []
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                button = tk.Button(
                    self.board_frame, 
                    text="", 
                    font=("Helvetica", 24, "bold"), 
                    width=5, 
                    height=2,
                    command=lambda idx=index: self.make_move(idx)
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(button)
        
        # Status label
        self.status_label = tk.Label(
            self.root, 
            text=f"Player {self.current_player}'s turn", 
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=10)
        
    def make_move(self, index):
        if self.game_over or self.board[index] != "":
            return
            
        # Update board and button
        self.board[index] = self.current_player
        self.buttons[index].config(
            text=self.current_player,
            fg="blue" if self.current_player == "X" else "red"
        )
        
        # Check for win or draw
        if self.check_winner():
            self.game_over = True
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.status_label.config(text=f"Player {self.current_player} wins!")
            return
            
        if "" not in self.board:
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            self.status_label.config(text="It's a draw!")
            return
            
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s turn")
        
        # AI move if applicable
        if self.against_ai and self.current_player == "O" and not self.game_over:
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        # Simple AI: First try to win, then block, then random move
        
        # Try to win
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner(False):
                    self.buttons[i].config(text="O", fg="red")
                    self.game_over = True
                    messagebox.showinfo("Game Over", "AI wins!")
                    self.status_label.config(text="AI wins!")
                    return
                self.board[i] = ""
        
        # Try to block
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner(False):
                    self.board[i] = "O"
                    self.buttons[i].config(text="O", fg="red")
                    self.current_player = "X"
                    self.status_label.config(text="Player X's turn")
                    return
                self.board[i] = ""
        
        # Random move
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.board[move] = "O"
            self.buttons[move].config(text="O", fg="red")
            
            # Check for win or draw after AI move
            if self.check_winner():
                self.game_over = True
                messagebox.showinfo("Game Over", "AI wins!")
                self.status_label.config(text="AI wins!")
                return
                
            if "" not in self.board:
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a draw!")
                self.status_label.config(text="It's a draw!")
                return
                
            self.current_player = "X"
            self.status_label.config(text="Player X's turn")
            
    def check_winner(self, update_buttons=True):
        # Define winning combinations
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] != "" and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                
                if update_buttons:
                    # Highlight winning combination
                    for pos in combo:
                        self.buttons[pos].config(bg="light green")
                        
                return True
                
        return False
        
    def reset_game(self):
        # Reset all game variables
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        
        # Fix: Use the stored default background color instead of SystemButtonFace
        for button in self.buttons:
            button.config(text="", bg=self.default_bg, fg="black")
            
        self.status_label.config(text=f"Player {self.current_player}'s turn")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

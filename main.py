import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os

#Initialize sound system
pygame.mixer.init()

def play_sound(name):
    try:
        pygame.mixer.Sound(f"{name}.wav").play()
    except:
        pass  #skip if sound file not found

#Centering the window
def center_window(win, width=300, height=450):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe - Player vs Bot")
        self.current_player = "X"
        self.board = [""] * 9
        self.difficulty = "Medium"
        self.player_score = 0
        self.ai_score = 0
        self.score_file = "scores.txt"
        self.load_scores()
        self.create_widgets()

    def create_widgets(self):
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.master, text="", font=("Arial", 20), width=5, height=2,
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.status_label = tk.Label(self.master, text="Your Turn (X)", font=("Arial", 12))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.score_label = tk.Label(self.master, text=f"Player: {self.player_score}  |  Bot: {self.ai_score}", font=("Arial", 12))
        self.score_label.grid(row=4, column=0, columnspan=3, pady=5)

        self.reset_button = tk.Button(self.master, text="Reset Board", command=self.reset_board)
        self.reset_button.grid(row=5, column=0, columnspan=1, pady=10)

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        self.difficulty_menu = tk.OptionMenu(self.master, self.difficulty_var, "Easy", "Medium", "Hard", command=self.set_difficulty)
        self.difficulty_menu.grid(row=5, column=1)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=5, column=2)

    def set_difficulty(self, level):
        self.difficulty = level
        self.status_label.config(text=f"Difficulty set to: {level}")

    def player_move(self, index):
        if self.board[index] == "" and self.current_player == "X":
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            play_sound("click")
            if self.check_winner("X"):
                self.player_score += 1
                play_sound("win")
                messagebox.showinfo("Game Over", "🎉 You win!")
                self.reset_board()
            elif "" not in self.board:
                play_sound("draw")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "O"
                self.status_label.config(text="Bot's Turn (O)")
                self.master.after(500, self.ai_move)

    def ai_move(self):
        index = self.find_best_move()
        if index is not None:
            self.board[index] = "O"
            self.buttons[index].config(text="O")
            play_sound("click")
            if self.check_winner("O"):
                self.ai_score += 1
                play_sound("win")
                messagebox.showinfo("Game Over", "😈 Bot wins!")
                self.reset_board()
            elif "" not in self.board:
                play_sound("draw")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "X"
                self.status_label.config(text="Your Turn (X)")

    def find_best_move(self):
        empty = [i for i in range(9) if self.board[i] == ""]

        if self.difficulty == "Easy":
            return random.choice(empty)

        elif self.difficulty == "Medium":
            # Try to win or block
            for mark in ["O", "X"]:
                for i in empty:
                    self.board[i] = mark
                    if self.check_winner(mark):
                        self.board[i] = ""
                        return i
                    self.board[i] = ""
            return random.choice(empty)

        elif self.difficulty == "Hard":
            return self.minimax(True)[1]

    def minimax(self, is_max):
        winner = self.get_winner()
        if winner == "O":
            return 1, None
        elif winner == "X":
            return -1, None
        elif "" not in self.board:
            return 0, None

        moves = []
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O" if is_max else "X"
                score, _ = self.minimax(not is_max)
                moves.append((score, i))
                self.board[i] = ""

        return max(moves) if is_max else min(moves)

    def get_winner(self):
        for a, b, c in [(0,1,2), (3,4,5), (6,7,8),
                        (0,3,6), (1,4,7), (2,5,8),
                        (0,4,8), (2,4,6)]:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a]
        return None

    def check_winner(self, player):
        wins = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
        return any(self.board[a] == self.board[b] == self.board[c] == player for a,b,c in wins)

    def reset_board(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="")
        self.current_player = "X"
        self.status_label.config(text="Your Turn (X)")
        self.score_label.config(text=f"Player: {self.player_score}  |  Bot: {self.ai_score}")
        self.save_scores()

    def save_scores(self):
        with open(self.score_file, "w") as f:
            f.write(f"{self.player_score},{self.ai_score}")

    def load_scores(self):
        if os.path.exists(self.score_file):
            with open(self.score_file, "r") as f:
                scores = f.read().strip().split(",")
                if len(scores) == 2:
                    self.player_score = int(scores[0])
                    self.ai_score = int(scores[1])

# ▶️ Run Game
if __name__ == "__main__":
    root = tk.Tk()
    center_window(root)
    game = TicTacToe(root)
    root.mainloop()
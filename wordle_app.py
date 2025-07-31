import tkinter as tk
from tkinter import messagebox
from wordle_functionality import Wordle, load_word_bank

class WordleGUI:
    def __init__(self, word_bank_file="words.txt"):
        self.root = tk.Tk()
        self.root.title("Wordle")
        self.root.geometry("400x600") # size window
        self.root.configure(bg="#121213") # set background color 
        self.root.resizable(False, False)
        
        # load word bank and initialize game
        try:
            self.word_bank = load_word_bank(word_bank_file)
            self.game = Wordle(self.word_bank)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {word_bank_file}")
            return
        
        # initial game state
        self.current_row = 0
        self.current_col = 0
        self.current_guess = ""
        
        # set colors 
        self.colors = {
            "green": "#6aaa64",
            "yellow": "#c9b458", 
            "gray": "#787c7e",
            "empty": "#121213",
            "border": "#3a3a3c",
            "text": "#ffffff"
        }
        
        self.setup_ui()
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()
        
    def setup_ui(self):
        """ sets UI display """
        # set up title 
        title_label = tk.Label(
            self.root, 
            text="WORDLE", 
            font=("Arial", 24, "bold"),
            fg=self.colors["text"],
            bg="#121213"
        )
        title_label.pack(pady=20)
        
        # set up grid 
        self.grid_frame = tk.Frame(self.root, bg="#121213")
        self.grid_frame.pack(pady=20)
        
        # create 6x5 grid of labels
        self.grid = []
        for row in range(6):
            grid_row = []
            for col in range(5):
                cell = tk.Label(
                    self.grid_frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Arial", 18, "bold"),
                    fg=self.colors["text"],
                    bg=self.colors["empty"],
                    relief="solid",
                    borderwidth=2,
                    bd=2,
                    highlightbackground=self.colors["border"]
                )
                cell.grid(row=row, column=col, padx=2, pady=2)
                grid_row.append(cell)
            self.grid.append(grid_row)
        
        # input frame
        input_frame = tk.Frame(self.root, bg="#121213")
        input_frame.pack(pady=20)
        
        # current guess display
        self.guess_label = tk.Label(
            input_frame,
            text="Type your guess:",
            font=("Arial", 12),
            fg=self.colors["text"],
            bg="#121213"
        )
        self.guess_label.pack()
        
        self.current_guess_label = tk.Label(
            input_frame,
            text="",
            font=("Arial", 16, "bold"),
            fg=self.colors["text"],
            bg="#121213",
            height=2
        )
        self.current_guess_label.pack()
        
        # submit button
        self.submit_btn = tk.Button(
            input_frame,
            text="SUBMIT GUESS",
            font=("Arial", 12, "bold"),
            bg="#6aaa64",
            fg="white",
            width=15,
            height=2,
            command=self.submit_guess,
            relief="flat"
        )
        self.submit_btn.pack(pady=10)
        
        # instructions
        instructions = tk.Label(
            self.root,
            text="Type letters and press ENTER to submit\nBACKSPACE to delete",
            font=("Arial", 10),
            fg="#787c7e",
            bg="#121213"
        )
        instructions.pack(pady=10)
        
        # new game button
        self.new_game_btn = tk.Button(
            self.root,
            text="NEW GAME",
            font=("Arial", 10),
            bg="#787c7e",
            fg="white",
            command=self.new_game,
            relief="flat"
        )
        self.new_game_btn.pack(pady=5)
        
    def on_key_press(self, event):
        key = event.keysym.lower()
        
        if key == 'return':
            self.submit_guess()
        elif key == 'backspace':
            self.delete_letter()
        elif key.isalpha() and len(key) == 1:
            self.add_letter(key.upper())
    

    def add_letter(self, letter):
        if len(self.current_guess) < 5 and self.current_row < 6:
            self.current_guess += letter
            self.grid[self.current_row][len(self.current_guess)-1].config(
                text=letter,
                bg=self.colors["border"]
            )
            self.update_current_guess_display()
    
    # backspace functionality 
    def delete_letter(self):
        if len(self.current_guess) > 0:
            self.grid[self.current_row][len(self.current_guess)-1].config(
                text="",
                bg=self.colors["empty"]
            )
            self.current_guess = self.current_guess[:-1]
            self.update_current_guess_display()
    
    def update_current_guess_display(self):
        self.current_guess_label.config(text=self.current_guess)
    
    def submit_guess(self):
        if len(self.current_guess) != 5:
            messagebox.showwarning("Invalid Guess", "Please enter a 5-letter word.")
            return
        
        guess_lower = self.current_guess.lower()
        
        # check if word is valid
        if not self.game.is_valid(guess_lower):
            messagebox.showwarning("Invalid Word", "Word not in word list.")
            return
        
        # check if word is unique
        if not self.game.is_unique(guess_lower):
            messagebox.showwarning("Duplicate Guess", "You already guessed this word.")
            return
        
        # submit guess to game
        result = self.game.check_word(guess_lower)
        
        # update grid with colors
        for i, (letter, color) in enumerate(result):
            self.grid[self.current_row][i].config(
                text=letter.upper(),
                bg=self.colors[color],
                fg="white" if color != "empty" else self.colors["text"]
            )
        
        # check win condition
        if self.game.is_won():
            self.show_end_game_dialog("Congratulations!", 
                                    f"You won in {self.game.attempts} attempts!\nThe word was: {self.game.target.upper()}")
            return
        
        # move to next row
        self.current_row += 1
        self.current_guess = ""
        self.update_current_guess_display()
        
        # check lose condition
        if self.game.is_lost():
            self.show_end_game_dialog("Game Over", 
                                    f"You ran out of attempts.\nThe word was: {self.game.target.upper()}")
    
    def show_end_game_dialog(self, title, message):
        result = messagebox.askyesno(title, f"{message}\n\nWould you like to play again?")
        if result:
            self.new_game()
        else:
            self.root.quit()
    
    def new_game(self):
        # reset game
        self.game = Wordle(self.word_bank)
        self.current_row = 0
        self.current_col = 0
        self.current_guess = ""
        
        # clear grid
        for row in range(6):
            for col in range(5):
                self.grid[row][col].config(
                    text="",
                    bg=self.colors["empty"],
                    fg=self.colors["text"]
                )
        
        self.update_current_guess_display()
        self.root.focus_set()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WordleGUI("words.txt") 
    app.run()
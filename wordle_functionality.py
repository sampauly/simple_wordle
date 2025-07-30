import random

def load_word_bank(filename):
    with open(filename, "r") as file:
        return [line.strip().lower() for line in file]

class Wordle:

    def __init__(self, word_bank, max_attempts=6):
        self.word_bank = word_bank                          # will hold word bank
        self.target = random.choice(word_bank)              # target word
        self.guesses = []                                   # holds past user guesses
        self.max_attempts = max_attempts                    # max attempts
        self.attempts = 0                                   # current number of attempts
        self.checked_user_input = []                        # populate with result of word check (greens, yellows, grays)
        self.target_counts = {}                             # empty dict, holds num of occurences for each letter in target 
        self.counts_initialized = False                      # set to True once target word has been counted 

    def is_won(self):
        """ true if user has won. checks if a valid guess has been made, then checks if all colors are green for that guess """
        if self.checked_user_input:
            return all(color == "green" for (_, color) in self.checked_user_input) 
        else: 
            return False

    def is_lost(self):
        """ returns true if user is out of attempts """
        if self.attempts < self.max_attempts:
            return False
        else: 
            return True
        
    def get_target_counts(self):
        """ counts number of occurences of each letter """
        for char in self.target:
            if char in self.target_counts:
                self.target_counts[char] += 1
            else:
                self.target_counts[char] = 1

        self.counts_initialized = True

    def is_valid(self, user_input):
        """ returns True if users input is a valid 5 letter word """
        return user_input in self.word_bank and len(user_input) == 5
        
    def is_unique(self, user_input):
        """ returns true if user input a new guess """
        return user_input not in self.guesses

    def check_word(self, user_input):
        """
            What it does:
            1. clears prior guesses checked_user_input
            3. checks if target has been counted yet, and counts char occurences if needed
            4. assigns green, yellow, or gray to chars based on their level of correctness 
            5. adds the users guess to a list 
            6. returns the checked word as a tuple of (char, color)
        """
        self.checked_user_input = [] # reset checked user input 
        user_input = user_input.lower()

        # call get_target_counts once
        if self.counts_initialized == False:
            self.get_target_counts()

        # make a copy of target_counts, essentially resetting the counts each time a new check is called 
        temp_target_counts = self.target_counts.copy()

        # mark greens, yellows, and grays using a loop 
        for i in range(0,5):
            if user_input[i] == self.target[i]:
                self.checked_user_input.append((user_input[i], "green"))
                temp_target_counts[user_input[i]] -= 1
            elif user_input[i] not in self.target or temp_target_counts[user_input[i]] < 1:
                self.checked_user_input.append((user_input[i], "gray"))
            else:
                self.checked_user_input.append((user_input[i], "yellow"))
                temp_target_counts[user_input[i]] -= 1 

        # add guess to list
        self.guesses.append(user_input)

        # increment attempts
        self.attempts += 1 

        return self.checked_user_input

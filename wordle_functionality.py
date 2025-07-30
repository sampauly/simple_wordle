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
        # true if user has won. checks if every 
        return all(color == "green" for (_, color) in self.checked_user_input)

    def is_lost(self):
        # returns true if user is out of attempts
        if self.attempts > self.max_attempts:
            return True
        else: 
            return False
        
    def get_target_counts(self):
        """ counts number of occurences of each letter """
        for char in self.target:
            if char in self.target_counts:
                self.target_counts[char] += 1
            else:
                self.target_counts[char] = 1

        self.counts_initialized = True

    def is_valid(self, user_input):
        """
        checks that users input is valid and hasnt been guessed already 
            if valid -> attempt used, return True
            if not valid -> try again, return False
        """
        if user_input in self.word_bank and user_input not in self.guesses:
            self.attempts += 1  # mark an attempt
            return True
        else:
            return False

    def check_word(self, user_input):
        """
            Goal:
            * if character is not in the word, its gray 
            * if character is in word, but out of place, its yellow
            * if character is in its correct spot in the word, its green

            Calls:
            * is_valid to check if user input is in the word bank
            * get_target_counts to count the occurences of each letter in the target word, necessary for assigning colors 

            Takes: 5 letter word provided by user
            Returns: list holding tuples (char, color) for complete word 
        """
        self.checked_user_input = [] # reset checked user input 
        user_input = user_input.lower()

        # call is_valid to check if attempt is valid 
        if self.is_valid(user_input):

            # call get_target_counts once
            if self.counts_initialized == False:
                self.get_target_counts()

            # mark greens, yellows, and grays using a loop 
            for i in range(0,5):
                if user_input[i] == self.target[i]:
                    self.checked_user_input.append((user_input[i], "green"))
                    self.target_counts[user_input[i]] -= 1
                elif user_input[i] not in self.target or self.target_counts[user_input[i]] < 1:
                    self.checked_user_input.append((user_input[i], "gray"))
                else:
                    self.checked_user_input.append((user_input[i], "yellow"))
                    self.target_counts[user_input[i]] -= 1 

            # add guess to list
            self.guesses.append(user_input)

        else:
            # word is not valid 
            print(f"Sorry, {user_input} is an invalid word, try again.")

        return self.checked_user_input

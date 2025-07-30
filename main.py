""" CLI driver for Wordle testing """

from wordle_functionality import Wordle, load_word_bank

def main():
    # build word bank
    word_bank = load_word_bank("words.txt")

    # create game instance 
    game = Wordle(word_bank)

    # greet user
    print(""" 
Welcome to Wordle!
          
You have 6 attempts to correctly guess a 5 letter word.
          
Gray - Letter is not in the word
Yellow - Letter is in the word, but in the wrong spot
Green - Letter is in its correct place 
    """)

    # loop game until is won or user is out of attempts
    while not game.is_won() and not game.is_lost():

        # get user input
        user_input = input(f"\nAttempt {game.attempts + 1}: ").strip().lower()

        # fheck if user input is invalid 
        if not game.is_valid(user_input):
            print(f"Sorry, '{user_input}' is an invalid word, try again.")

        # check if user input is repeated
        elif not game.is_unique(user_input):
            print(f"Sorry, you have already guessed '{user_input}', try again.")

        # user input is valid, so check word 
        else:
            result = game.check_word(user_input)
            # print result 
            print("Result:", " ".join(f"{char.upper()}({color})" for char, color in result))

    # now check if game is won
    if game.is_won():
        print(f"Congratulations! '{game.target}' is correct!")
    else:
        print(f"Sorry, you are out of lives. The correct word was '{game.target}'")


        
if __name__ == "__main__":
    main()




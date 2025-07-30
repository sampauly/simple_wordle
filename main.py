""" CLI driver for Wordle testing """

import wordle_functionality as wordle

# build word bank
word_bank = wordle.load_word_bank("words.txt")

# create game instance 
w = wordle.Wordle(word_bank)

print(word_bank[:10])




# 218final

## This is a 20 questions sort of game except you get infinite questions because why not.
The app will query the language model to pick a random word and your goal is to guess the word with only yes or no questions  
  
to run: `python3 main.py` 

commands:  
- `quit`/`exit`: exits the game
- `give up`: reveals the word and asks the user if they want to play again
  - `yes` picks a new word and continues the game
  - `no` exits the game
- `new word`: picks a new random word
- [any yes or no question]: asks the language model a yes or no question about the word
  - the language model will respond with `yes`, `no`, or `unsure`
  - if the use types in anything other than a yes or no question they will be reminded the rules of the game


# video
[video](https://youtu.be/2pAEoTAh6rI)

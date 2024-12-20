from app.groq_calls import ask_yes_no_question, request_word

# Main console application
def console_chat():
    # game start
    the_word = request_word()
    print("I'm thinking of a word. Can you guess it? \n"+
          "If you would like to give up and know the word, type 'give up'.\n"+
          "If you would like to get a new word type 'new word'.\n")
    while True:
        # prompt user
        prompt = input("You: ")
        # check if user wants to exit
        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        # check if user wants to give up
        elif prompt.lower() == "give up":
            print(f"The word was {the_word}.")
            print("Would you like to play again?")
            answer = input("You: ").lower()
            # validate user input
            while(answer not in "yesno"):
                print("Invalid input. Please type 'yes' or 'no'.")
                answer = input("You: ")
            # check if user wants to play again    
            if answer == "yes":
                the_word = request_word()
                print("Now ask yes or no questions to try and guess the word.")
            else:
                print("Goodbye!")
                break
        # check if user wants a new word
        elif "new word" in prompt.lower():
                request_word()
                print("Now ask yes or no questions to try and guess the word")
        # check if user wants to ask a yes or no question
        elif prompt:
            result = ask_yes_no_question(prompt, the_word)
            print(result)
        else:
            print("No function call was made or an error occurred.")

if __name__ == "__main__":
    console_chat()
from app.groq_calls import ask_yes_no_question, request_word
from app.auth import register_user, authenticate_user

def auth_menu():
    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user_id = authenticate_user(username, password)
            if user_id:
                print("Login successful!")
                return user_id
            print("Invalid credentials!")
            
        elif choice == "2":
            username = input("Choose username: ")
            password = input("Choose password: ")
            if register_user(username, password):
                print("Registration successful! Please login.")
            else:
                print("Username already exists!")
                
        elif choice == "3":
            exit()

# Main console application

user_id = auth_menu()
# game loop
def console_chat(user_id):
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
    user_id = auth_menu()
    console_chat(user_id)
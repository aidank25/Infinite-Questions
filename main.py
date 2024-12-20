from app.groq_calls import ask_yes_no_question, request_word
from app.auth import register_user, authenticate_user
from app.database.operations import create_game_record, get_user_games
from app.database import Base, engine

def setup_database():
    Base.metadata.create_all(engine)

def display_game_history(user_id):
    games = get_user_games(user_id)
    if not games:
        print("\nNo games found!")
        return
    
    print("\n=== Game History ===")
    print("Word\t\tQuestions\tResult\t\tDate")
    print("-" * 50)
    
    for game in games:
        result = "Won" if game.win else "Gave up"
        date = game.created_at.strftime("%Y-%m-%d %H:%M")
        print(f"{game.word:<12}\t{game.numQuestions:<10}\t{result:<8}\t{date}")
    print("-" * 50)

# authorization menu
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

def console_chat(user_id):
    while True:
        print("\n1. Play Game\n2. View History\n3. Logout")
        choice = input("Choose an option: ")
        
        if choice == "1":
            play_game(user_id)
        elif choice == "2":
            display_game_history(user_id)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

def play_game(user_id):
    numGuesses = 0
    the_word = request_word()
    print("I'm thinking of a word. Can you guess it? \n"+
          "If you would like to give up and know the word, type 'give up'.\n"+
          "If you would like to get a new word type 'new word'.\n")
    
    while True:
        # prompt user
        prompt = input("You: ")
        # check if user wants to exit
        if prompt.lower() in ["exit", "quit"]:
            create_game_record(user_id, the_word, numGuesses, False)
            print("Goodbye!")
            break
        # check if user wants to give up
        elif prompt.lower() == "give up":
            print(f"The word was {the_word}.")
            create_game_record(user_id, the_word, numGuesses, False)
            print("Would you like to play again?")
            answer = input("You: ").lower()
            # validate user input
            while(answer not in "yesno"):
                print("Invalid input. Please type 'yes' or 'no'.")
                answer = input("You: ")
            # check if user wants to play again    
            if answer == "yes":
                numGuesses = 0
                the_word = request_word()
                print("Now ask yes or no questions to try and guess the word.")
            else:
                print("Goodbye!")
                break
        # check if user wants a new word
        elif "new word" in prompt.lower():
                numGuesses = 0
                request_word()
                print("Now ask yes or no questions to try and guess the word")
        # check if user wants to ask a yes or no question
        elif prompt:
            result = ask_yes_no_question(prompt, the_word)
            numGuesses += 1
            if result == "You did it!":
                create_game_record(user_id, the_word, numGuesses, True)
            print(result)
        else:
            print("No function call was made or an error occurred.")

if __name__ == "__main__":
    setup_database()
    user_id = auth_menu()
    console_chat(user_id)
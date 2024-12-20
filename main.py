import sys
import os

# Add the lib folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

#from dot_env import load_dotenv # type: ignore
import requests
# Add the lib folder to the Python path

# Load environment variables from .env file
#load_dotenv()


# API Endpoint and API Key
API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY="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" #API_KEY = os.getenv("API_KEY")  # Ensure your .env file contains API_KEY

# Function to call the Groq API and expect a yes or no response
def ask_groq(messages, model="llama-3.1-70b-versatile"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
         "messages": messages,
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Extract the response content
        answer = data["choices"][0]["message"]["content"].strip().lower()
        
        return answer

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "error"

def request_word():
    return ask_groq([{
            "role": "user",
            "content": "Give me a random word, just the word"
        }])

def ask_yes_no_question(question, the_word):
    return ask_groq([
        {
            "role": "system",
            "content": f"The word is {the_word}. If the user guesses the word, tell them \"You did it!\", otherwise, only answer yes, no, or unsure. The user is only allowed to ask yes or no questions, if they ask the wrong type of question, remind them that they are only allowed to ask yes or no questions. Do not answer the question if it is not a yes or no question. "
        },
        {
            "role": "user",
            "content": question
        }
    ])


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
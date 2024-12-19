import sys
import os

# Add the lib folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

#from dot_env import load_dotenv # type: ignore
import requests
import json
# Add the lib folder to the Python path

# Load environment variables from .env file
#load_dotenv()


# API Endpoint and API Key
API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY="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" #API_KEY = os.getenv("API_KEY")  # Ensure your .env file contains API_KEY

# Define functions for arithmetic operations
def request_word():
    return "zebra"

# Function to call the Groq API and expect a yes or no response
def ask_yes_no_question(question, model="llama3-8b-8192"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "functions": [],
        "function_call": "auto",
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract the response content
        answer = data["choices"][0]["message"]["content"].strip().lower()

        # Determine if the response is yes or no
        if "yes" in answer:
            return "yes"
        elif "no" in answer:
            return "no"
        else:
            return "unclear"

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "error"
# Function to call the Groq API
def call_groq_function(prompt, functions, model="llama3-8b-8192"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "functions": functions,
        "function_call": "auto",
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Check if the model called a function
        if "function_call" in data["choices"][0]["message"]:
            function_name = data["choices"][0]["message"]["function_call"]["name"]
            arguments = json.loads(data["choices"][0]["message"]["function_call"]["arguments"])
            return function_name, arguments

        return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

# Main console application
def console_chat():
    print("Welcome to the Groq Function Chat!")
    print("You can ask the system to perform addition, subtraction, multiplication, or division.")

    functions = [
        {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number."},
                    "b": {"type": "number", "description": "The second number."}
                },
                "required": ["a", "b"]
            },
        },
        {

            "name": "request_word",
            "description": "Request a word from the system.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
            "required": []
        },
        {
            "name": "ask_yes_no_question",
            "description": "Ask a yes or no question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The yes or no question to ask."}
                },
                "required": ["question"]
            },
        }
    ]

    while True:
        prompt = input("You: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        function_name, arguments = call_groq_function(prompt, functions)

        if function_name and arguments:
            if function_name == "request word":
                result = request_word()
            elif function_name == "ask":
                result = ask_yes_no_question(arguments["a"])
            else:
                result = "Error: Unknown function called"

            print(f"Result: {result}")
        else:
            print("No function call was made or an error occurred.")

if __name__ == "__main__":
    console_chat()
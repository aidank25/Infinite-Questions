import pytest
from unittest.mock import patch
from app.groq_calls import request_word, ask_yes_no_question

@pytest.fixture
def mock_ask_groq():
    with patch('app.groq_calls.ask_groq') as mock:
        yield mock

def test_request_word(mock_ask_groq):
    # Arrange
    mock_ask_groq.return_value = "test"
    
    # Act
    result = request_word()
    
    # Assert
    assert isinstance(result, str)
    assert result == "test"
    mock_ask_groq.assert_called_once()

def test_ask_yes_no_question_valid(mock_ask_groq):
    # Arrange
    mock_ask_groq.return_value = "yes"
    test_word = "apple"
    test_question = "Is it a fruit?"
    
    # Act
    result = ask_yes_no_question(test_question, test_word)
    
    # Assert
    assert result in ["yes", "no", "unsure"]
    assert result == "yes"
    mock_ask_groq.assert_called_once()

def test_ask_yes_no_question_correct_guess(mock_ask_groq):
    # Arrange
    mock_ask_groq.return_value = "You did it!"
    test_word = "apple"
    test_question = "Is it apple?"
    
    # Act
    result = ask_yes_no_question(test_question, test_word)
    
    # Assert
    assert result == "You did it!"
    mock_ask_groq.assert_called_once()

def test_ask_yes_no_question_invalid_response(mock_ask_groq):
    # Arrange
    mock_ask_groq.return_value = "error"
    test_word = "apple"
    test_question = "What is the word?"
    
    # Act
    result = ask_yes_no_question(test_question, test_word)
    
    # Assert
    assert result == "error"
    mock_ask_groq.assert_called_once()


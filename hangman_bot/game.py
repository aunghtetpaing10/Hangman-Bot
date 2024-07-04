import random
from words import words
from utils import game_message
import string

LIVES = 7 # Number of lives

def get_random_word(words):
    """Get a random word from the words list."""
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()

def start_new_game(chat_id, context):
    """Start a new game for the chat"""
    word = get_random_word(words)
    context.user_data[chat_id] = {
        "word": word,
        "word_letters": set(word),
        "guessed_letters": set(),
        "lives": LIVES
    }
    return f"Let's play Hangman! You have 7 lives. Guess a letter by typing it in."

def process_guess(chat_id, user_guess, context):
    """Process a user guess"""
    game = context.user_data.get(chat_id)
    if game == None:
        return "Start a new game by typing /start"

    alphabet = set(string.ascii_uppercase)

    if user_guess not in alphabet or len(user_guess) != 1:
        return "This is not a valid letter. Please guess a single letter"
    
    if user_guess in game["guessed_letters"]:
        return "You have already guessed that letter. Try again."

    game["guessed_letters"].add(user_guess)

    if user_guess in game["word_letters"]:
        game["word_letters"].remove(user_guess)
        if not game["word_letters"]:
            del context.user_data[chat_id]
            return f"You won! The word is {game['word']}. Start a new game with /start."
        return game_message(game, True)
    else:
        game["lives"] -= 1
        if game["lives"] == 0:
            del context.user_data[chat_id]
            return f"Game Over. The word is {game['word']}. Start a new game with /start"
        return game_message(game, False)
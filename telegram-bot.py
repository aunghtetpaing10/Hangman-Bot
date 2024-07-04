import random
from words import words
from hangman_visual import lives_visual_dict
import string
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ContextTypes, filters, Application
import logging
from config import *


games = {}

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def get_random_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    word = get_random_word(words)
    games[chat_id] = {
        "word": word,
        "word_letters": set(word),
        "guessed_letters": set(),
        "lives": LIVES
    }
    await update.message.reply_text(f"Let's play Hangman! You have 7 lives. Guess a letter by typing it in.")


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alphabet = string.ascii_uppercase

    chat_id = update.message.chat_id
    if chat_id not in games:
        await update.message.reply_text("Start a new game by typing /start")
        return
    
    game = games[chat_id]
    user_guess = update.message.text.upper()

    if user_guess in alphabet and len(user_guess) == 1:
        if user_guess in game['guessed_letters']:
            await update.message.reply_text("You have already guessed that letter. Try again.")
        else:
            game['guessed_letters'].add(user_guess)
            if user_guess in game['word_letters']:
                game['word_letters'].remove(user_guess)
                await update.message.reply_text("Your guess is correct!")
                if not game['word_letters']:
                    await update.message.reply_text(f"You won! The word was {game['word']}. Start a new game with /start")
                    del games[chat_id]
                    return
            else:
                game['lives'] -= 1
                await update.message.reply_text("Your guess is wrong!")
                if game['lives'] == 0:
                    await update.message.reply_text(f"Game Over. The correct word was {game['word']}. Start a new game with /start")
                    del games[chat_id]
                    return
    
            display_word = ' '.join([letter if letter in game['guessed_letters'] else '_' for letter in game['word']])
            message = (f"{lives_visual_dict[game['lives']]}\n"
                       f"Current word: {display_word}\n"
                       f"You have {game['lives']} lives left and have guessed these letters: {' '.join(game['guessed_letters'])}")
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("That is not a valid letter. Please guess a single letter.")

def main():
    try:
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess ))

        app.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
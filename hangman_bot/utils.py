from hangman_visual import lives_visual_dict

async def send_message(update, message):
    """Send a message to the user."""
    await update.message.reply_text(message)

def game_message(game, is_correct):
    """Format the game message after a guess."""
    if is_correct:
        feedback = "Your guess is correct!"
    else:
        feedback = "Your guess is wrong!"

    display_word = ' '.join([letter if letter in game['guessed_letters'] else '_' for letter in game['word']])
    message = (f"{feedback}\n"
            f"{lives_visual_dict[game['lives']]}\n"
            f"Current word: {display_word}\n"
            f"You have {game['lives']} lives left and have guessed these letters: {' '.join(game['guessed_letters'])}")

    return message
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import logging
from game import start_new_game, process_guess
from utils import send_message

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a new game"""
    try:
        chat_id = update.message.chat_id
        response = start_new_game(chat_id, context)
        await send_message(update, response)
        return "GUESS"
    except Exception as e:
        logger.error(f"An error occurred in start function: {e}")
        await send_message(update, "An error occurred while starting the game. Please try again.")
        return ConversationHandler.END


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user guess"""
    try:
        chat_id = update.message.chat_id
        user_guess = update.message.text.upper()
        response = process_guess(chat_id, user_guess, context)
        await send_message(update, response)
        if response.startswith("You won!") or response.startswith("Game Over"):
            return ConversationHandler.END
        return "GUESS"
    except KeyError as e:
        logger.error(f"Key error: {e}")
        await send_message(update, "An error occurred during the game. Please try again.")
        return ConversationHandler.End
    except Exception as e:
        logger.error(f"An error occurred in guess function: {e}")
        await send_message(update, "An error occurred during the game. Please try again.")
        return ConversationHandler.End

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """End the current conversation."""
    await send_message(update, "Game ended. Start a new game with /start.")
    return ConversationHandler.End

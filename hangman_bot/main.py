import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import *
from bot_handlers import start, guess

# Config logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def main():
    # Start the bot
    try:
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess ))

        app.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
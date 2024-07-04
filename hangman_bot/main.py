import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config import *
from bot_handlers import start, guess, end

# Config logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def main():
    # Start the bot
    try:
        app = Application.builder().token(TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states= {
                "GUESS": [MessageHandler(filters.TEXT & ~filters.COMMAND, guess )]
            },
            fallbacks=[CommandHandler("end", end)],
        )
        
        app.add_handler(conv_handler)

        app.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
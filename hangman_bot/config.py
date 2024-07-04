import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('Bot_Token')
if not TOKEN:
    raise ValueError("Bot token not found")

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
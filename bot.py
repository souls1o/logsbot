import os
from db import test_connection, create_or_update_user
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from keep_alive import keep_alive

keep_alive()
test_connection()

parse_mode = "MarkdownV2"

def main() -> None:
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    
    application.add_handler(start.get_handler())
    
    app.run_polling()

if __name__ == '__main__':
    main()

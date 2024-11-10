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

# MAIN COMMANDS #
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = get_chat_id(update)
    

# MAIN FUNCTIONS #
def get_chat_id(update: Update) -> int:
    return update.message.chat_id if update.message else update.callback_query.message.chat_id

def filter_text(text: str):
    return text.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.').replace('!', '\\!').replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace('=', '\\=').replace('<', '\\<').replace('>', '\\>')

def main() -> None:
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(poll_interval=5)

if __name__ == '__main__':
    main()

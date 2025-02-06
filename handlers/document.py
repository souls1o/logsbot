from telegram import Update
from telegram.ext import MessageHandler, CallbackContext, filters
from db import get_log, update_log
from helpers import escape_markdown

async def handle_document(update: Update, context: CallbackContext) -> None:
    if context.bot_data.get("awaiting_file") is not True:
        return

    document = update.message.document
    if document:
        file = await document.get_file()
        file_path = await file.download_as_bytearray()
        logs = file_path.decode("utf-8").strip().split("\n")

        log = get_log(context.bot_data["log_id"])
        log["logs"].extend(logs)
        update_log(context.bot_data["log_id"],
log)

        product = log["product"]
        name = log["name"]
        stock = len(log["logs"])

        text = escape_markdown(f"*{product} | {name}* stock has been updated.\n\nStock: _{stock}_")
        chat_id = -1002487007307
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode="MarkdownV2")

        context.bot_data["awaiting_file"] = False
        await update.message.reply_text("Successfully updated stock")

def get_handler():
    return MessageHandler(filters.Document, handle_document)
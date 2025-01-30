import os
from db import test_connection
from telegram.ext import Application
from handlers import start, menu, adminstats
from keep_alive import keep_alive

keep_alive()
test_connection()

parse_mode = "MarkdownV2"

def main() -> None:
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    
    app.add_handler(start.get_handler())
    app.add_handler(adminstats.get_handler())
    app.add_handler(menu.get_handler())
    
    app.run_polling()

if __name__ == '__main__':
    main()

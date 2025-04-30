# from telegram_bot.telegram_main import start, button, handle_file, dialog_handler
# from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
# from credentials import credentialss
# import threading
# from flask import Flask
# import os
#
#
# def start_web_server():
#     app = Flask(__name__)
#
#     @app.route('/')
#     def home():
#         return 'Bot is running (polling)...'
#
#     port = int(os.environ.get('PORT', 10000))
#     app.run(host='0.0.0.0', port=port)
#
#
# if __name__ == '__main__':
#     threading.Thread(target=start_web_server).start()
#
#     application = ApplicationBuilder().token(credentialss('BOT_TOKEN')).build()
#     application.add_handler(CommandHandler('start', start))
#     application.add_handler(CallbackQueryHandler(button))
#     application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dialog_handler))
#     application.run_polling()
#
#     threading.Event().wait()

from telegram_bot.telegram_main import start, button, handle_file, dialog_handler
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from credentials import credentialss
from flask import Flask
import threading
import os

# Flask-сервер для Render (чтобы был открыт порт)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# Запуск Telegram-бота
def run_bot():
    application = ApplicationBuilder().token(credentialss('BOT_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dialog_handler))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()  # стартуем Flask в фоне
    run_bot()  # запускаем polling в основном потоке

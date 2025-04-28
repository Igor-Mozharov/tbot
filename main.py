from telegram_bot.telegram_main import start, button, done, handle_file, telegram_credentials
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_credentials()).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)
    file_handler = MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file)
    application.add_handler(file_handler)
    application.run_polling()
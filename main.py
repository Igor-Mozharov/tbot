from telegram_bot.telegram_main import start, button, handle_file, dialog_handler
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from credentials import credentialss


if __name__ == '__main__':
    application = ApplicationBuilder().token(credentialss('BOT_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dialog_handler))
    application.run_polling()
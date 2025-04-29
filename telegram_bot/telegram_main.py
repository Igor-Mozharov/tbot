import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from mindee_api.mindee_main import mindee_mock


UPLOAD_DIR = 'uploaded_files'
os.makedirs(UPLOAD_DIR, exist_ok=True)


def messages():
    with open('telegram_bot/messages.json') as file:
        res = json.load(file)
        return res


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    introduction = messages()['intro']

    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Сost calculation', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=introduction, reply_markup=markup)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_us = messages()['about']
    buttons = [
        [InlineKeyboardButton('Сost calculation', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=about_us, reply_markup=markup)


async def cost_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cost_message = messages()['instructions']
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Please, confirm file uploading!', callback_data='done')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=cost_message, reply_markup=markup)
    context.user_data['awaiting'] = 'passport'


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file_info = None
    if message.document:
        file_info = await message.document.get_file()
        file_name = message.document.file_name
    elif message.photo:
        photo = message.photo[-1]
        file_info = await photo.get_file()
        file_name = f"{photo.file_id}.jpg"
    else:
        await message.reply_text('Please send a document or a photo.')
        return

    if file_info:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        await file_info.download_to_drive(file_path)

        result = mindee_mock()
        await message.reply_text(f"Please check if all info is ok!\n{result}")

        if 'files' not in context.user_data:
            context.user_data['files'] = []
        context.user_data['files'].append({'file_id': file_info.file_id, 'file_name': file_name})
        # await message.reply_text(f"File received and saved: {file_name}")
        for f in os.listdir(UPLOAD_DIR):
            temp = os.path.join(UPLOAD_DIR, f)
            os.remove(temp)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if 'files' not in context.user_data or not context.user_data['files']:
        await query.message.reply_text("There are no uploaded files!")
        return

    file_list = '\n'.join(f['file_name'] for f in context.user_data['files'])

    await query.message.reply_text(
        f"Uploaded files:\n{file_list}\nSaved successfully!"
    )
    context.user_data['files'] = []


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'about_us':
        await about(update, context)
    elif query.data == 'cost_calculation':
        await cost_calc(update, context)
    elif query.data == 'done':
        await done(update, context)
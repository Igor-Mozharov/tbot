import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from mindee_api.mindee_main import mindee_mock
from openai_api.openai_main import gemini_speaker


UPLOAD_DIR = 'uploaded_files'
os.makedirs(UPLOAD_DIR, exist_ok=True)


def messages():
    """
    Loads predefined messages from the JSON configuration file.
    Returns: dict: A dictionary containing message texts for the bot.
    """
    with open('telegram_bot/messages.json') as file:
        res = json.load(file)
        return res


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    The /start command. Greetings from bot
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    introduction = messages()['intro']
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Сost calculation', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=introduction, reply_markup=markup)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    About page. Insurance company introduction
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    about_us = messages()['about']
    buttons = [
        [InlineKeyboardButton('Сost calculation', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=about_us, reply_markup=markup)


async def cost_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Page for insurance cost calculation. Instruction for user.
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    cost_message = messages()['instructions']
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Please, confirm file uploading!', callback_data='done')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=cost_message, reply_markup=markup)
    context.user_data['awaiting'] = 'passport'


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles uploaded file or photo, extracts information using Mindee, and shows extracted data for confirmation
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
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
        context.user_data['mindee_result'] = result
        buttons = [
            [InlineKeyboardButton('Accept', callback_data='accept_data')],
            [InlineKeyboardButton('Reject', callback_data='reject_data')]
        ]
        b_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(f"Please check if all info is ok:\n\n{result}", reply_markup=b_markup)
        if 'files' not in context.user_data:
            context.user_data['files'] = []
        context.user_data['files'].append({'file_id': file_info.file_id, 'file_name': file_name})
        for f in os.listdir(UPLOAD_DIR):
            temp = os.path.join(UPLOAD_DIR, f)
            os.remove(temp)


async def dialog_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generate text message for user-bot dialog
    :param update: Incoming update from the user
    :param context:Context object with user data
    """
    message = update.message.text
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Сost calculation', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    gemini_response = gemini_speaker(messages()['gemini_instruction'] + '\n' + message)
    await update.message.reply_text(gemini_response, reply_markup=markup)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Function for confirmation of uploaded files
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    query = update.callback_query
    if 'files' not in context.user_data or not context.user_data['files']:
        await query.message.reply_text("There are no uploaded files!")
        return
    file_list = '\n'.join(f['file_name'] for f in context.user_data['files'])
    await query.message.reply_text(
        f"Uploaded files:\n{file_list}\nSaved successfully!"
    )
    context.user_data['files'] = []


async def accept_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Function for confirmation of mindee returned response (after document upload)
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    query = update.callback_query
    buttons = [
        [InlineKeyboardButton('Accept and pay for it !', callback_data='pay')],
        [InlineKeyboardButton('Decline', callback_data='not_pay')]
    ]
    choise_mark = InlineKeyboardMarkup(buttons)
    await query.edit_message_text('Thank you! Your cost is 100$', reply_markup=choise_mark)


async def reject_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Function for rejection of mindee returned response (after document upload)
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    query = update.callback_query
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
    ]
    markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text('Try to upload documents again!', reply_markup=markup)
    context.user_data.pop('files', None)


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Function for confirming of mindee response / buy polis (generate insurance polis after that)
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    query = update.callback_query
    await query.answer()
    mindee_result = context.user_data.get('mindee_result', 'No data found')
    prompt = (
        f"Please generate a short Ukrainian insurance policy document based on the following extracted information:\n"
        f"{mindee_result}\n"
        f"Only generate the fields of the policy, keep it formal."
    )
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Сost calculation', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(gemini_speaker(prompt), reply_markup=markup)


async def not_pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Function for declining of mindee response / not buy polis
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    query = update.callback_query
    await query.answer()
    buttons = [
        [InlineKeyboardButton('About us', callback_data='about_us')],
        [InlineKeyboardButton('Calculate again', callback_data='cost_calculation')]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text('My appologize, sir! But your insurance is 100$, and it can"t be lower!',
                                  reply_markup=markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Inline buttons callbacks function
    :param update: Incoming update from the user
    :param context:Context object with user data

    """
    query = update.callback_query
    callback = query.data

    commands_list = {
        'about_us': about,
        'cost_calculation': cost_calc,
        'done': done,
        'accept_data': accept_data,
        'reject_data': reject_data,
        'pay': pay,
        'not_pay': not_pay
    }
    result = commands_list.get(callback)
    if result:
        await result(update, context)


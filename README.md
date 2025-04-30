
# Telegram Insurance Bot

https://t.me/InsuranceBestCarBot

note: This sample bot was deployed at https://render.com. There is some 'sleep timeout' issue. If you wand to check bot functionality - please press this link to activate this bot:

https://tbot-1o9m.onrender.com  - BOT ACTIVATION LINK

This is a simple Telegram bot that assists users in purchasing car insurance by processing user-submitted documents, interacting through AI-driven communications, and confirming transaction details

# Dependencies

- python 3.12 +
- python-telegram-bot
- mindee
- google-generativeai

# Setup instruction

1. Copy project folder from git repository:
git clone https://github.com/Igor-Mozharov/tbot

2. Dependencies installation:
pip install -r requirements.txt

3. Get your own Telegram Token (with @Botfather), Mindee Token, Gemini Token(google-generativeai).

4. Replace config.ini with your Tokens.

5. Run Bot

6. You can deploy it on some cloud platforms (heroku, render) - OPTIONAL

# Detailed description of the bot workflow

This Telegram bot performs several key tasks and interacts with the user through commands and messages. Here's how the workflow of the bot works:

#### first run
When the user starts interacting with the bot, they send the `/start` command. This triggers the bot to send a welcome message and offer the user to start interacting with it.

#### Handling text messages
The bot processes all text messages that are not commands and responds to them based on predefined algorithms. For instance, if the user sends a regular text, the bot may process it and return a response(AI POWERED).

#### Handling files
The bot supports file uploads, such as images or documents. When the user sends a file, the bot processes it or confirms successful upload. Generate insurance polis at the end.

#### Interaction via buttons
The bot can generate buttons for user interaction. When the user clicks a button, the bot processes the request and performs the corresponding action associated with the selected option.

# Examples of interaction flows with the bot.

### Starting the bot
<USER> /start

<BOT> Hello!
My name is InsuranceBestCarBot!
I can help you with buying your car insurance!
Just need to upload your passport and vehicle identification document to know the actual price!

(Bot display buttons 'about us', 'cost calculation')

<USER> pressing the button 'About us'

<BOT> The insurance company "K.V.I.G." is a reliable national-scale insurance company that has been continuously developing and operating in the Ukrainian insurance market since 1997. Since 2009, it has been a part of the powerful European financial structure, V.I.G.

### Uploading a Files

<USER> Uploading the files (passport)

<BOT> Mindee api is transform this documents to text and show it to user for confirmation

(Bot display buttons 'Accept', 'Reject')

<USER> press the 'Accept' button

<BOT> text to user: Thank you! Your cost is 100$

(bot display buttons 'Accept and pay for it', 'Decline')

<USER> press the Accept button

<BOT> send Insurance polis to user

# License

This project is licensed under the MIT License

# Authors:
- Igor Mozharov - https://github.com/Igor-Mozharov?tab=repositories

# Feedback

If you have any feedback, please reach out to us at r5@ukr.net



# Glory to Ukraine !




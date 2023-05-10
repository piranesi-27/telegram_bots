import os
import telegram
from telegram import Update
import io
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import re

TOKEN = '******'

# Define the function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a word counter bot. Please upload a .txt file to count the number of words in it.")

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Send me a .txt file to count the words in it.")
# Define help function
def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('''
    You can use the following commands:
    /start - Start the bot
    /help - Get help on how to use the bot
    /count_words - Count the number of words in a .txt file
    /choose_source - Choose the source language
    /choose_target - Choose the target language
    ''')
def count_words(update, context):
    file = context.bot.get_file(update.message.document.file_id)
    file_name, file_ext = os.path.splitext(update.message.document.file_name)
    if file_ext != '.txt':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload a .txt file.")
        return
    words_count = 0
    with io.BytesIO() as output:
        file.download(out=output)
        text = output.getvalue().decode('utf-8')
        words = text.split()
        words_count = len(words)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The file '{file_name}{file_ext}' contains {words_count} words.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document, count_words))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

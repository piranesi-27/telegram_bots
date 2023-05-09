import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import docx2txt
from telegram import Bot


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a command handler for /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! Send me a .txt or .docx file and I will count the words in it.')

# Define a message handler for text messages
def text_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please send a .txt or .docx file.')

# Define a message handler for document messages
def document_message(update, context):
    document = update.message.document
    if document.mime_type == 'text/plain' or document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        file_id = document.file_id
        file = context.bot.get_file(file_id)
        file_path = file.file_path
        if document.mime_type == 'text/plain':
            with context.bot.download_file(file_path) as f:
                content = f.read().decode('utf-8')
            word_count = len(content.split())
        elif document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            with context.bot.download_file(file_path) as f:
                content = docx2txt.process(f)
            word_count = len(content.split())
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'The file contains {word_count} words.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please send a .txt or .docx file.')

# Define a message handler for unsupported messages
def unsupported_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I cannot process this message. Please send a .txt or .docx file.')

def main():
    # Create the Updater and pass in the bot token

    #myBot = Bot('5826936170:AAFRs8vd3PXbCKTjIi1ge2xpoGs83Wlci5Q')
    #updater = Updater(myBot)
    updater = Updater(token='*********', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Register message handlers
    dispatcher.add_handler(MessageHandler(Filters.text, text_message))
    dispatcher.add_handler(MessageHandler(Filters.document, document_message))
    dispatcher.add_handler(MessageHandler(~Filters.text & ~Filters.document, unsupported_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()

import telebot
from telebot import types

bot = telebot.TeleBot('*******')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello! Please enter the number of words in your text.')

@bot.message_handler(func=lambda message: True)
def get_number_of_words(message):
    try:
        num_words = int(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton('Russian'), types.KeyboardButton('English'))
        bot.send_message(message.chat.id, 'Please select the source language of your text:', reply_markup=markup)
        bot.register_next_step_handler(message, get_source_language, num_words)
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter a valid number.')

def get_source_language(message, num_words):
    source_language = message.text.lower()
    if source_language == 'russian' or source_language == 'english':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton('Romanian'), types.KeyboardButton('Spanish'), types.KeyboardButton('German'))
        bot.send_message(message.chat.id, 'Please select the target language of the translation:', reply_markup=markup)
        bot.register_next_step_handler(message, get_target_language, num_words, source_language)
    else:
        bot.send_message(message.chat.id, 'Invalid input. Please select either "Russian" or "English" from the dropdown menu.')
        bot.register_next_step_handler(message, get_source_language, num_words)

def get_target_language(message, num_words, source_language):
    target_language = message.text.lower()
    if target_language == 'romanian' or target_language == 'spanish' or target_language == 'german':
        price = num_words * 0.06
        bot.send_message(message.chat.id, f'The cost of translating your text from {source_language} to {target_language} is {price} USD.')
    else:
        bot.send_message(message.chat.id, 'Invalid input. Please select either "Romanian", "Spanish", or "German" from the dropdown menu.')
        bot.register_next_step_handler(message, get_target_language, num_words, source_language)

bot.polling()

import telebot
from keyboa import Keyboa #Keyboa

import config
import make_beat

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    inline_markup = Keyboa(items=config.menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Здарова, бот', reply_markup=inline_markup())

# Клавиатура меню
@bot.callback_query_handler(func=lambda call: call.data in config.menu_buttons)
def menu(call):
    try:
        if call.message:
            if call.data == 'Заказать бит':
                styles_markup = Keyboa(items=config.styles_markup, items_in_row=2)
                bot.send_message(call.message.chat.id, 'Выбери стиль бита:', reply_markup=styles_markup())
            elif call.data == 'Баланс':
                balance_markup = Keyboa(items=config.balance_buttons, items_in_row=2)
                bot.send_message(call.message.chat.id, 'Баланс: нищий.', reply_markup=balance_markup())
            elif call.data == 'О нас':
                navigation_markup = Keyboa(items=config.navigation_buttons, items_in_row=2)
                bot.send_message(call.message.chat.id, 'О нас много не скажешь.')
    except Exception as e:
        print(repr(e))

# Клавиатура битов
@bot.callback_query_handler(func=lambda call: call.data in config.styles_markup)
def menu(call):
    try:
        if call.message:
            if call.data == 'Jersey Club':   
                bot.send_message(call.message.chat.id, 'Тут типо делается бит')
                make_beat.jersey_club()
            elif call.data == 'Plug':
                bot.send_message(call.message.chat.id, 'Тут типо делается бит')
                make_beat.plug()
    except Exception as e:
        print(repr(e))

bot.infinity_polling()
import telebot
from keyboa import Keyboa #Keyboa
import os
import config
import make_beat

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    inline_markup = Keyboa(items=config.menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Здарова, бот', reply_markup=inline_markup())

@bot.message_handler(commands=['menu'])
def welcome(message):
    inline_markup = Keyboa(items=config.menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Меню:', reply_markup=inline_markup())

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

# user_id: call.data(style)
user_chosen_style = {}

@bot.callback_query_handler(func=lambda call: call.data in config.styles_markup)
def menu(call):
    try:
        if call.message:
            user_chosen_style[call.message.chat.id] = call.data

            bpm_markup = Keyboa(items=config.bpm_buttons, items_in_row=3)
            bot.send_message(call.message.chat.id, f'{call.data} - отличный выбор! Теперь выбери темп:', reply_markup=bpm_markup()) 

    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: call.data in config.bpm_buttons)
def menu(call):
    try:
        if call.message:
           if user_chosen_style[call.message.chat.id] == 'Jersey Club':
                del user_chosen_style[call.message.chat.id]
                msg = bot.send_message(call.message.chat.id, 'Тут типо делается бит')
                # Сделать бит
                make_beat.jersey_club(call.message.chat.id, call.data)
                # Удалить предыдущее сообщение
                bot.delete_message(call.message.chat.id, msg.message_id)
                # Отправить бит
                beat = open(f'output_beats/{call.message.chat.id}.wav', 'rb')
                bot.send_message(call.message.chat.id, 'Лови бит')
                bot.send_document(call.message.chat.id, beat, timeout=20000) 
                beat.close()
                os.remove(f'output_beats/{call.message.chat.id}.wav')
                

    except Exception as e:
        print(repr(e))

bot.infinity_polling()
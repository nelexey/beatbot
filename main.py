import telebot
from keyboa import Keyboa #Keyboa
import os
import config
import make_beat
import db_handler

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    inline_markup = Keyboa(items=config.menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Здарова, бот', reply_markup=inline_markup())

    db_handler.add_user(message.chat.username, message.chat.id, config.start_balance)

@bot.message_handler(commands=['menu'])
def welcome(message):
    inline_markup = Keyboa(items=config.menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Меню:', reply_markup=inline_markup())

# Клавиатура меню
@bot.callback_query_handler(func=lambda call: call.data in config.menu_buttons)
def menu(call):
    global msg
    try:
        if call.message:
            if call.data == f'Заказать бит - {config.beat_price}₽':
                styles_markup = Keyboa(items=config.styles_markup, items_in_row=2)
                msg = bot.send_message(call.message.chat.id, 'Выбери стиль бита:', reply_markup=styles_markup())
            elif call.data == 'Баланс':
                balance_markup = Keyboa(items=config.balance_buttons, items_in_row=3)
                balance = db_handler.get_balance(call.message.chat.id)
                if balance == 0:
                    msg = bot.send_message(call.message.chat.id, f'На твоем балансе {balance}₽\n\n⚠️Зачисленные деньги будут лежать на балансе сколько угодно, на них в любой момент можно купить бит!', reply_markup=balance_markup())
                else:
                    msg = bot.send_message(call.message.chat.id, f'На твоем балансе {balance}руб', reply_markup=balance_markup())
            elif call.data == 'О нас':
                navigation_markup = Keyboa(items=config.navigation_buttons, items_in_row=2)
                bot.send_message(call.message.chat.id, 'О нас много не скажешь.')
    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: call.data in config.balance_buttons)
def balance(call):
    global msg
    try:
        if call.message:
            if call.data == 'Своя сумма':
                bot.delete_message(call.message.chat.id, msg.message_id)
                msg = bot.send_message(call.message.chat.id, f'⚠️Эта функция пока не доступна⚠️') 
            else:
                bot.delete_message(call.message.chat.id, msg.message_id)
                db_handler.top_balance(call.message.chat.id, call.data.split('₽')[0])
                msg = bot.send_message(call.message.chat.id, f'Твой баланс пополнен на {call.data}') 

    except Exception as e:
        print(repr(e))

# user_id: call.data(style)
user_chosen_style = {}

@bot.callback_query_handler(func=lambda call: call.data in config.styles_markup)
def temp(call):
    global msg
    try:
        if call.message:
            bot.delete_message(call.message.chat.id, msg.message_id)
            bpm_markup = Keyboa(items=config.bpm_buttons, items_in_row=3)
            msg = bot.send_message(call.message.chat.id, f'{call.data} - отличный выбор! Теперь выбери темп:', reply_markup=bpm_markup()) 
            user_chosen_style[call.message.chat.id] = call.data

    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: call.data in config.bpm_buttons)
def style(call):
    global msg
    try:
        if call.message:

            bot.delete_message(call.message.chat.id, msg.message_id)

            if db_handler.get_balance(call.message.chat.id) >= config.beat_price:
                msg = bot.send_message(call.message.chat.id, 'Делаю бит...')

                # Сделать бит
                if user_chosen_style[call.message.chat.id] == 'Jersey Club':
                    make_beat.jersey_club(call.message.chat.id, call.data)

                elif user_chosen_style[call.message.chat.id] == 'Trap':
                    make_beat.trap(call.message.chat.id, call.data)

                elif user_chosen_style[call.message.chat.id] == 'Drill':
                    make_beat.drill(call.message.chat.id, call.data)

                elif user_chosen_style[call.message.chat.id] == 'Plug':
                    make_beat.plug(call.message.chat.id, call.data)

                # Удалить предыдущее сообщение
                bot.delete_message(call.message.chat.id, msg.message_id)

                # Отправить бит
                msg = bot.send_message(call.message.chat.id, f'Забирай свой бит\nв стиле: {user_chosen_style[call.message.chat.id]}\nс темпом: {call.data}\n\nС твоего баланса снято {config.beat_price}₽\n\nБит будет тут 👇')
                del user_chosen_style[call.message.chat.id]

                # Открыть файл
                beat = open(f'output_beats/{call.message.chat.id}.wav', 'rb')

                # Скинуть файл
                bot.send_audio(call.message.chat.id, beat) 

                db_handler.pay(call.message.chat.id, config.beat_price)

                # Закрыть файл
                beat.close()

                # Удалить файл
                os.remove(f'output_beats/{call.message.chat.id}.wav')

            else:    
                inline_markup = Keyboa(items=config.menu_buttons[0], items_in_row=1)
                bot.send_message(call.message.chat.id, f'Тебе не хватает денег на балансе, пополни баланс чтобы купить бит.', reply_markup=inline_markup())
    except Exception as e:
        print(repr(e))
        bot.delete_message(call.message.chat.id, msg.message_id)
        bot.send_message(call.message.chat.id, 'Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.')

bot.infinity_polling()
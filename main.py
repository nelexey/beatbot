import telebot
from keyboa import Keyboa
from os import listdir, remove
import config
import make_beat
import db_handler
from pydub import AudioSegment

# Подключение бота
bot = telebot.TeleBot(config.TOKEN)

# # Создаем объект YandexCheckout
# yandex_checkout = YandexCheckout('506751')

styles = []
for dir in listdir():
    if dir.split('_')[0] == 'style':
        styles.append(dir)

# Ключи - названия стилей на кнопках, значения - названия папок style_*
aliases = {
    'Jersey Club': 'JC',
    'Trap': 'Trap',
}
styles_buttons = []
for key in aliases.keys():
    styles_buttons.append(key)

beat_price = 45

# кнопки
menu_buttons = ['Баланс', 'О нас', f'Заказать бит - {beat_price}₽']
balance_buttons = ['45₽', '90₽', '135₽']
navigation_buttons = ['<<Назад']
bpm_buttons = ['110bpm', '130bpm', '145bpm']
beats_buttons = ['1', '2', '3', 'Никакой']

# начальный баланс пользователя при добавлении в БД
start_balance = 0

@bot.message_handler(commands=['start'])
def welcome(message):
    inline_markup = Keyboa(items=menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Здарова, бот', reply_markup=inline_markup())

    db_handler.add_user(message.chat.username, message.chat.id, start_balance)

@bot.message_handler(commands=['menu'])
def welcome(message):
    inline_markup = Keyboa(items=menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Меню:', reply_markup=inline_markup())

# Переменная показывет, в процессе ли обработки пользователь
processing = {}

# Клавиатура меню
@bot.callback_query_handler(func=lambda call: call.data in menu_buttons)
def menu(call):
    global msg
    try:
        if call.message:
            if call.data == f'Заказать бит - {beat_price}₽':
                styles_markup = Keyboa(items=styles_buttons, items_in_row=2)
                msg = bot.send_message(call.message.chat.id, 'Выбери стиль бита:', reply_markup=styles_markup())
            elif call.data == 'Баланс':
                balance_markup = Keyboa(items=balance_buttons, items_in_row=3)
                balance = db_handler.get_balance(call.message.chat.id)
                if balance == 0:
                    msg = bot.send_message(call.message.chat.id, f'На твоем балансе {balance}₽\n\n⚠️Зачисленные деньги будут лежать на балансе сколько угодно, на них в любой момент можно купить бит!', reply_markup=balance_markup())
                else:
                    msg = bot.send_message(call.message.chat.id, f'На твоем балансе {balance}руб', reply_markup=balance_markup())
            elif call.data == 'О нас':
                navigation_markup = Keyboa(items=navigation_buttons, items_in_row=2)
                bot.send_message(call.message.chat.id, 'О нас много не скажешь.')
    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: call.data in balance_buttons)
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

@bot.callback_query_handler(func=lambda call: call.data in styles_buttons)
def temp(call):
    global msg
    try:
        if call.message:
            bot.delete_message(call.message.chat.id, msg.message_id)
            bpm_markup = Keyboa(items=bpm_buttons, items_in_row=3)
            msg = bot.send_message(call.message.chat.id, f'{call.data} - отличный выбор! Теперь выбери темп:', reply_markup=bpm_markup()) 
            user_chosen_style[call.message.chat.id] = call.data

    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: call.data in bpm_buttons)
def style(call):
    global msg
    try:
        if call.message:

            bot.delete_message(call.message.chat.id, msg.message_id)

            if db_handler.get_balance(call.message.chat.id) >= beat_price:
                msg = bot.send_message(call.message.chat.id, 'Создаю...')

                # style - стиль бита, count - сколько битов сделать
                def generate_beats(style, count):
                    if style == 'Jersey Club':
                        for i in range(1, count+1):
                            make_beat.jersey_club(call.message.chat.id, call.data, i)
                    elif style == 'Trap':
                        for i in range(1, count+1):
                            make_beat.trap(call.message.chat.id, call.data, i)
                    elif style == 'Drill':
                        for i in range(1, count+1):
                            make_beat.drill(call.message.chat.id, call.data, i)
                    elif style == 'Plug':
                        for i in range(1, count+1):
                            make_beat.plug(call.message.chat.id, call.data, i)
                
                # Сделать бит
                generate_beats(user_chosen_style[call.message.chat.id], 3)

                # Удалить предыдущее сообщение
                bot.delete_message(call.message.chat.id, msg.message_id)

                # Отправить бит
                msg = bot.send_message(call.message.chat.id, f'Вот 3 демо версии битов на твой вкус:')
                del user_chosen_style[call.message.chat.id]

                # Открыть файл
                beat1 = AudioSegment.from_wav(f'output_beats/{call.message.chat.id}_1.wav')[7000:14000]
                beat1 = beat1.export(f"output_beats/{call.message.chat.id}_1_short.wav", format="wav")
                beat2 = AudioSegment.from_wav(f'output_beats/{call.message.chat.id}_2.wav')[7000:14000]
                beat2 = beat2.export(f"output_beats/{call.message.chat.id}_2_short.wav", format="wav")
                beat3 = AudioSegment.from_wav(f'output_beats/{call.message.chat.id}_3.wav')[7000:14000]
                beat3 = beat3.export(f"output_beats/{call.message.chat.id}_3_short.wav", format="wav")

                # Скинуть файл
                bot.send_audio(call.message.chat.id, beat1) 
                bot.send_audio(call.message.chat.id, beat2)
                beats_markup = Keyboa(items=beats_buttons, items_in_row=3)
                bot.send_audio(call.message.chat.id, beat3, reply_markup=beats_markup()) 

                # Закрыть файл
                beat1.close()
                beat2.close()
                beat3.close()

                # Удалить файл
                remove(f'output_beats/{call.message.chat.id}_1_short.wav')
                remove(f'output_beats/{call.message.chat.id}_2_short.wav')
                remove(f'output_beats/{call.message.chat.id}_3_short.wav')

            else:    
                inline_markup = Keyboa(items=menu_buttons[0], items_in_row=1)
                bot.send_message(call.message.chat.id, f'Тебе не хватает денег на балансе, пополни баланс чтобы купить бить', reply_markup=inline_markup())
    except Exception as e:
        print(repr(e))
        bot.delete_message(call.message.chat.id, msg.message_id)
        bot.send_message(call.message.chat.id, 'Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.')

@bot.callback_query_handler(func=lambda call: call.data in beats_buttons)
def beats(call):
    global msg
    try:
        if call.message:
            if call.message.chat.id not in processing:
                if msg:
                    bot.delete_message(call.message.chat.id, msg.message_id)
                bot.send_message(call.message.chat.id, f'Твой выбор: {call.data}')
                if call.data in ['1', '2', '3']:
                    
                    # Добавить пользователя в "обработку"
                    processing[call.message.chat.id] = True

                    msg = bot.send_message(call.message.chat.id, 'Скидываю полную версию...')

                    # Открыть файл
                    beat = open(f'output_beats/{call.message.chat.id}_{call.data}.wav', 'rb')

                    # Скинуть файл
                    bot.send_audio(call.message.chat.id, beat)

                    # Снять деньги
                    db_handler.pay(call.message.chat.id, beat_price)

                    # Увеличеть количество купленых битов на аккаунте
                    db_handler.get_beat(call.message.chat.id)

                    # Закрыть файл
                    beat.close()
                    
                    # Удалить файлы
                    remove(f'output_beats/{call.message.chat.id}_1.wav')
                    remove(f'output_beats/{call.message.chat.id}_2.wav')
                    remove(f'output_beats/{call.message.chat.id}_3.wav')

                    # Убрать пользователя из "обработки"
                    del processing[call.message.chat.id]
                else:   
                    # Добавить пользователя в "обработку"
                    processing[call.message.chat.id] = True 

                    bot.send_message(call.message.chat.id, f'Не одного бита не выбрано, ты можешь посомтреть ещё несколько битов через время.')
        
                    # Удалить файлы
                    remove(f'output_beats/{call.message.chat.id}_1.wav')
                    remove(f'output_beats/{call.message.chat.id}_2.wav')
                    remove(f'output_beats/{call.message.chat.id}_3.wav')

                    # Убрать пользователя из "обработки"
                    del processing[call.message.chat.id]
    except Exception as e:
        print(repr(e))
        bot.delete_message(call.message.chat.id, msg.message_id)
        bot.send_message(call.message.chat.id, 'Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.')

bot.infinity_polling()
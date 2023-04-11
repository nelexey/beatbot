import telebot
from keyboa import Keyboa # Для создания клавиатур
from os import listdir, remove, path
from yookassa import Configuration,Payment # Для конфигурирования и создания платежа
import asyncio # Для асинхронной функции проверки платежа
import config
import make_beat # Тут создаются биты
import db_handler # Обработчик запросов к БД
from pydub import AudioSegment # Для обрезки битов на их демо-версии
from glob import glob
import itertools
import json

# Подключение бота
bot = telebot.TeleBot(config.TOKEN)

# Подключение Юкассы
Configuration.account_id = config.SHOP_ID
Configuration.secret_key = config.SHOP_API_TOKEN

# Ключи - названия стилей на кнопках, значения - названия папок style_*
aliases = {
    'Jersey Club': 'JC',
    'Trap': 'Trap',
    'Drill': 'Drill',
    'Plug': 'Plug',
}

styles_buttons = []
for key in aliases.keys():
    styles_buttons.append(key)

beat_price = 90 # RUB

# Кнопки 
menu_buttons = ['Баланс', 'О нас', f'Заказать бит - {beat_price}₽']
balance_buttons = ['45₽', '90₽', '135₽']
# Для каждого стиля свои кнопки bpm
bpm_buttons = {'Jersey Club': ['110bpm', '130bpm', '145bpm'],
               'Trap': ['110bpm', '130bpm', '145bpm'],
               'Drill': ['110bpm', '130bpm', '145bpm'],
               'Plug': ['140bpm', '150bpm', '160bpm']}

# Начальный баланс пользователя при добавлении в БД
start_balance = 0 # RUB

@bot.message_handler(commands=['start'])
def welcome(message):
    inline_markup = Keyboa(items=menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Здарова, бот', reply_markup=inline_markup())
    # Добавление пользователя в таблицу users
    db_handler.add_user(message.chat.username, message.chat.id, start_balance)
    
@bot.message_handler(commands=['menu'])
def menu(message):
    inline_markup = Keyboa(items=menu_buttons, items_in_row=2)
    bot.send_message(message.chat.id, 'Меню:', reply_markup=inline_markup())

    # Добавление пользователя в таблицу users
    db_handler.add_user(message.chat.username, message.chat.id, start_balance)

# Переменная хранит данные пользователя, служит для уменьшения количества запросов в БД на get_user
user = {}
# Переменная показывает, в процессе ли обработки пользователь, служит для уменьшения количества запросов в БД на get_processing
processing = {}
# Переменная показывает, в процессе ли создания бита пользователь, служит для уменьшения количества запросов в БД на get_beats_generating
beats_generating = {}
# user_id: call.data (style)
user_chosen_style = {}
# Количество генерируемых демо-версий
beats = 3
# Кнопки для выбора битов
beats_buttons = [str(i) for i in range(1, beats+1)]
# Сюда сохраняется message_id, показывающее id сообщения с балансом для каждого пользователя, для последующего изменения этого сообщения. chat_id: msg.message_id
balance_messages = {}
# Сообщения для удаления. chat_id: msg
message_to_delete = {}

# Создает платёж
def payment(value,description):
	payment = Payment.create({
    "amount": {
        "value": value,
        "currency": "RUB"
    },
    "payment_method_data": {
        "type": "bank_card"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://web.telegram.org/k/#@NeuralBeatBot"
    },
    "capture": True,
    "description": description
	})

	return json.loads(payment.json())

# Подтверждает наличие "товара"
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=None)

# Обработчик всех кнопок
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    global msg
    global beats
    global beats_buttons
    global balance_messages

    # Асинхронная функция проверки статуса платежа
    async def check_payment(payment_id):
        payment = json.loads((Payment.find_one(payment_id)).json())
        while payment['status'] == 'pending':
            payment = json.loads((Payment.find_one(payment_id)).json())
            await asyncio.sleep(3)

        if payment['status']=='succeeded':
            print("SUCCSESS RETURN")
            db_handler.top_balance(call.message.chat.id, call.data.split('₽')[0])
            bot.send_message(call.message.chat.id, f'Твой баланс пополнен на {call.data}').message_id
            if call.message.chat.id in balance_messages: 
                balance_markup = Keyboa(items=balance_buttons, items_in_row=3)
                balance = db_handler.get_balance(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=balance_messages[call.message.chat.id], text=f'На твоем балансе {balance}₽', reply_markup=balance_markup())
            return True
        else:
            print("BAD RETURN")
            bot.send_message(call.message.chat.id, 'Не удалось пополнить баланс.')
            return False
        
    # Если бот перезапущен с удалением БД и значения пользователя не существуют
    if user.get(call.message.chat.id) is None:
        if db_handler.get_user(call.message.chat.id) == False:
            bot.send_message(call.message.chat.id, 'Нужно перезапустить бота командой /start')
            return
        else:
            user[call.message.chat.id] = db_handler.get_user(call.message.chat.id)
    else:
        if user[call.message.chat.id] == False:
            bot.send_message(call.message.chat.id, 'Нужно перезапустить бота командой /start')
            return

    if call.data in menu_buttons:
        try:
            if call.message:
                if call.data == f'Заказать бит - {beat_price}₽':
                    if (beats_generating.get(call.message.chat.id) is not None and beats_generating.get(call.message.chat.id) == False) or db_handler.get_beats_generating(call.message.chat.id) == 0:
                        if processing.get(call.message.chat.id) is not None or db_handler.get_processing(call.message.chat.id) == 0:
                            db_handler.set_processing(call.message.chat.id)
                            processing[call.message.chat.id] = True

                            styles_markup = Keyboa(items=styles_buttons, items_in_row=2)
                            message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, 'Выбери стиль бита:', reply_markup=styles_markup()).message_id

                            db_handler.del_processing(call.message.chat.id)
                            processing[call.message.chat.id] = False
                    else:
                        if (processing.get(call.message.chat.id) is not None and processing.get(call.message.chat.id) == False) or db_handler.get_processing(call.message.chat.id) == 0:
                            bot.send_message(call.message.chat.id, 'Ты не можешь заказать еще один бит во время заказа. Выбери версию бита и дождись её отправки.')    
                        else:
                            bot.send_message(call.message.chat.id, 'Ты не можешь заказать еще один бит во время заказа.')    
                elif call.data == 'Баланс':
                    balance_markup = Keyboa(items=balance_buttons, items_in_row=3)
                    # Запрос баланса пользователя в таблице users
                    balance = db_handler.get_balance(call.message.chat.id)
                    if balance == 0:
                        balance_messages[call.message.chat.id] = bot.send_message(call.message.chat.id, f'На твоем балансе {balance}₽\n\n⚠️ Зачисленные деньги будут лежать на балансе сколько угодно, на них в любой момент можно купить бит!', reply_markup=balance_markup()).message_id
                    else:
                        balance_messages[call.message.chat.id] = bot.send_message(call.message.chat.id, f'На твоем балансе {balance}₽', reply_markup=balance_markup()).message_id
                elif call.data == 'О нас':
                    bot.send_message(call.message.chat.id, 'О нас много не скажешь.')   
        except Exception as e:
            print(repr(e))
            db_handler.del_processing(call.message.chat.id)
        return
    elif call.data in balance_buttons:
        try:
            if call.message:
                # Получение цены из callback_data
                price = int(call.data.split('₽')[0])
                # Отправка счета пользователю
                payment_data = payment(price, f'Пополнение баланса на {price}₽')
                payment_id = payment_data['id']
                confirmation_url = payment_data['confirmation']['confirmation_url']
                bot.send_message(call.message.chat.id, f'Для пополнения баланса перейди по этой ссылке: {confirmation_url}')
                asyncio.run(check_payment(payment_id))

        except Exception as e:
            print(repr(e))
        return
    elif call.data in styles_buttons:
        try:
            if call.message:
                if processing.get(call.message.chat.id) is not None or db_handler.get_processing(call.message.chat.id) == 0:
                    db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True

                    if message_to_delete.get(call.message.chat.id) is not None:
                        bot.delete_message(call.message.chat.id, message_to_delete[call.message.chat.id])
                        del message_to_delete[call.message.chat.id]

                    bpm_markup = Keyboa(items=bpm_buttons[call.data], items_in_row=3)
                    message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, f'{call.data} - отличный выбор! Теперь выбери темп:', reply_markup=bpm_markup()).message_id 
                    
                    db_handler.set_chosen_style(call.message.chat.id, call.data)
                    user_chosen_style[call.message.chat.id] = call.data

                    db_handler.del_processing(call.message.chat.id)
                    processing[call.message.chat.id] = False

        except Exception as e:
            print(repr(e))
            db_handler.del_processing(call.message.chat.id)
        return
    elif call.data in list(itertools.chain(*bpm_buttons.values())):
        try:
            if call.message:
                if processing.get(call.message.chat.id) is not None or db_handler.get_processing(call.message.chat.id) == 0:
                    if user_chosen_style.get(call.message.chat.id) is not None:
                        if call.data not in bpm_buttons[user_chosen_style[call.message.chat.id]]:
                            bot.send_message(call.message.chat.id, 'Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых')
                            return
                    else:
                        if call.data not in bpm_buttons[db_handler.get_chosen_style[call.message.chat.id]]:
                            bot.send_message(call.message.chat.id, 'Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых')
                            return
                        
                    db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True
                    if db_handler.get_balance(call.message.chat.id) >= beat_price:

                        db_handler.set_beats_generating(call.message.chat.id)
                        beats_generating[call.message.chat.id] = True

                        if message_to_delete.get(call.message.chat.id) is not None:
                            bot.delete_message(call.message.chat.id, message_to_delete[call.message.chat.id])
                            del message_to_delete[call.message.chat.id]

                        message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, 'Создаю версии битов, это может занять несколько минут...').message_id
                        
                        # style - стиль бита, num - сколько битов сделать
                        def generate_beats(style, num):
                            for i in range(1, num+1):
                                if style == 'Jersey Club':
                                    make_beat.jersey_club(call.message.chat.id, call.data, i)
                                elif style == 'Trap':
                                    make_beat.trap(call.message.chat.id, call.data, i)
                                elif style == 'Drill':
                                    make_beat.drill(call.message.chat.id, call.data, i)
                                elif style == 'Plug':
                                    make_beat.plug(call.message.chat.id, call.data, i)
                        
                        # Обрезать аудио
                        def trimmed_audio(files_list):
                            for file_path in files_list:
                                sound = AudioSegment.from_wav(file_path)
                                trimmed = sound[45000:55000]
                                new_file_path = f"{path.splitext(file_path)[0]}_short.wav"
                                trimmed_sound = trimmed.export(new_file_path, format="wav")
                                if files_list.index(file_path) == len(files_list)-1:           
                                    beats_markup = Keyboa(items=beats_buttons, items_in_row=3)   
                                    bot.send_audio(call.message.chat.id, trimmed_sound, reply_markup=beats_markup())
                                    return
                                else:
                                    bot.send_audio(call.message.chat.id, trimmed_sound)
                            
                        # Сделать бит     
                        generate_beats(db_handler.get_chosen_style(call.message.chat.id), beats)

                        if message_to_delete.get(call.message.chat.id) is not None:
                            bot.delete_message(call.message.chat.id, message_to_delete[call.message.chat.id])
                            del message_to_delete[call.message.chat.id]
                        # Отправить бит
                        message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, f'Вот 3 демо версии битов на твой вкус:').message_id

                        trimmed_audio(glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'))

                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}]_short.wav'):         
                            remove(file)

                    else:    
                        inline_markup = Keyboa(items=menu_buttons[0], items_in_row=1)
                        bot.send_message(call.message.chat.id, f'Тебе не хватает денег на балансе, пополни баланс чтобы купить бит', reply_markup=inline_markup())
                        db_handler.del_beats_generating(call.message.chat.id)
                        beats_generating[call.message.chat.id] = False
                    db_handler.del_processing(call.message.chat.id)
                    processing[call.message.chat.id] = False
        except Exception as e:
            print(repr(e))
            db_handler.del_processing(call.message.chat.id)
            db_handler.del_beats_generating(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Не удалось отправить пробные версии битов, деньги за транзакцию не сняты. Попробуй ещё раз.')
        return
    elif call.data in beats_buttons:
        try:
            if call.message:
                if processing.get(call.message.chat.id) is not None or db_handler.get_processing(call.message.chat.id) == 0:
                    # Добавить пользователя в "обработку"
                    db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True

                    # Записать в переменную и удалить выбранный стиль
                    if user_chosen_style.get(call.message.chat.id) is not None: 
                        chosen_style = user_chosen_style[call.message.chat.id]
                        del user_chosen_style[call.message.chat.id]
                    else:
                        chosen_style = db_handler.get_chosen_style(call.message.chat.id)
                    db_handler.del_chosen_style(call.message.chat.id)

                    bot.send_message(call.message.chat.id, f'Твой выбор: версия {call.data} в стиле {chosen_style}')
                    
                    if call.data in beats_buttons:
                        
                        message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, 'Скидываю полную версию...').message_id

                        # Открыть файл
                        beat = open(f'output_beats/{call.message.chat.id}_{call.data}.wav', 'rb')

                        # Скинуть файл
                        bot.send_audio(call.message.chat.id, beat)
                        
                        if message_to_delete.get(call.message.chat.id) is not None:
                            bot.delete_message(call.message.chat.id, message_to_delete[call.message.chat.id])
                            del message_to_delete[call.message.chat.id]

                        # Закрыть файл
                        beat.close()
                        
                        # Удалить файлы
                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'):
                            remove(file)

                    elif call.data == 'Никакой':   
                        bot.send_message(call.message.chat.id, f'Не одного бита не выбрано, ты можешь посомтреть ещё несколько битов через время.')
                        # Удалить файлы
                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'):
                            remove(file)

                    # Убрать пользователя из "обработки"
                    db_handler.del_processing(call.message.chat.id)
                    processing[call.message.chat.id] = False
                    db_handler.del_beats_generating(call.message.chat.id)
                    beats_generating[call.message.chat.id] = False

                    # Снять деньги
                    db_handler.pay(call.message.chat.id, beat_price)

                    # Увеличеть количество купленых битов на аккаунте
                    db_handler.get_beat(call.message.chat.id)
                    
        except Exception as e:
            print(repr(e))
            db_handler.del_processing(call.message.chat.id)
            db_handler.del_beats_generating(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.')

bot.polling()
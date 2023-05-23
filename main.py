import telebot
from telebot import types
from keyboa import Keyboa # Для создания клавиатур
from os import listdir, remove, path
from yookassa import Configuration,Payment # Для конфигурирования и создания платежа
import asyncio # Для асинхронной функции проверки платежа
import config
import launch
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
menu_buttons = ['💰 Баланс', '🏡 О нас', f'🎵 Сгенерировать бит - {beat_price}₽ 🎵']
balance_buttons = ['90₽', '180₽', '360₽']
# Для каждого стиля свои кнопки bpm
bpm_buttons = {'Jersey Club': ['140bpm', '150bpm', '160bpm'],
               'Trap': ['110bpm', '130bpm', '145bpm'],
               'Drill': ['110bpm', '130bpm', '145bpm'],
               'Plug': ['140bpm', '150bpm', '160bpm']}

# Начальный баланс пользователя при добавлении в БД
start_balance = 0 # RUB
# Переменная хранит данные пользователя, служит для уменьшения количества запросов в БД на add_user
is_added = {}
# Переменная хранит id menu сообщения пользователя, служит для уменьшения количества запросов в БД на get_menu_id
menu_id = {}

if launch.mailing_list is not None:
    for chat_id in launch.mailing_list:
        inline_markup = Keyboa(items=menu_buttons[2], items_in_row=1)
        bot.send_message(chat_id, 'Сожалею, но во время создания твоих битов бот перезапустился 😵‍💫\n\nЭто происходит очень редко, но необходимо для стабильной работы бота. Деньги за транзакцию не сняты.\n\nТы можшеь заказать бит еще раз 👉', reply_markup=inline_markup())

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет! 👋\n\nЯ телеграм-бот, который поможет тебе создать качественные 🎧 биты в разных стилях.\n\nМоя главная особенность - доступная 💰 цена и большой выбор стилей. Ты можешь выбрать любой стиль, который тебе нравится, и я создам для тебя уникальный бит.\n\nНе упусти возможность создать свой собственный звук и выделиться на фоне других исполнителей! 🎶\n\nЧтобы начать, используй команду\n/menu')
    user_initials = f'{message.from_user.first_name} {message.from_user.last_name}'

    # Добавление пользователя в таблицу users
    if is_added.get(message.chat.id) is None:
        is_added[message.chat.id] = True
        db_handler.add_user(message.chat.username, message.chat.id, user_initials, start_balance)
    
@bot.message_handler(commands=['menu'])
def menu(message):
    inline_markup = Keyboa(items=menu_buttons, items_in_row=2)

    bot.send_message(message.chat.id, "🎶 Привет! Это меню заказа битов 🎶\n\n💥 Ты можешь ознакомиться с примером бита, который я могу создать, используя команду /example_beats. Просто отправь эту команду в чат и ты получишь ссылку на наш пример.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=inline_markup())

    # Добавить id сообщения в базу данных
    menu_id[message.chat.id] = message.message_id
    db_handler.set_menu_id(message.chat.id, message.message_id)

    user_initials = f'{message.from_user.first_name} {message.from_user.last_name}'

    # Добавление пользователя в таблицу users
    if is_added.get(message.chat.id) is None:
        is_added[message.chat.id] = True
        db_handler.add_user(message.chat.username, message.chat.id, user_initials, start_balance)

# Если пользователю уже отправлялись примеры битов, то значение под ключем его chat_id будет True
got_example_beats = {}

@bot.message_handler(commands=['example_beats'])
def example(message):
    if got_example_beats.get(message.chat.id) is None:
        bot.send_message(message.chat.id, "Конечно! Вот несколько примеров готовых битов 💾\nНе сомневайся, бот сделает такие же и тебе!")
        for file_path in glob('example_beats/*.wav'):
            example_beat = open(file_path, 'rb')
            bot.send_audio(message.chat.id, example_beat)
            example_beat.close()
        got_example_beats[message.chat.id] = True
    else:
        inline_markup = Keyboa(items=menu_buttons[2], items_in_row=1)
        bot.send_message(message.chat.id, "Тебе уже отправлены примеры битов 😵‍💫\n\n Если хочешь ещё, бот может сгенерировать тебе собственный бит 😉", reply_markup=inline_markup())
# Переменная хранит данные пользователя, служит для уменьшения количества запросов в БД на get_user
user = {}
# Переменная показывает, в процессе ли обработки пользователь, служит для уменьшения количества запросов в БД на get_processing
processing = {}
# Переменная показывает, в процессе ли создания бита пользователь, служит для уменьшения количества запросов в БД на get_beats_generating
beats_generating = {}
# user_id: call.data (style)
user_chosen_style = {}
# Количество генерируемых демо-версий
beats = launch.beats
# Кнопки для выбора битов
beats_buttons = [str(i) for i in range(1, beats+1)]
# Сюда сохраняется message_id, показывающее id сообщения с балансом для каждого пользователя, для последующего изменения этого сообщения. chat_id: msg.message_id
balance_messages = {}
# Сообщения для удаления. chat_id: msg
message_to_delete = {}

# # Создает платёж
# def payment(value,description):
# 	payment = Payment.create({
#     "amount": {
#         "value": value,
#         "currency": "RUB"
#     },
#     "payment_method_data": {
#         "type": "bank_card"
#     },
#     "confirmation": {
#         "type": "redirect",
#         "return_url": "https://web.telegram.org/k/#@NeuralBeatBot"
#     },
#     "capture": True,
#     "description": description
# 	})

# 	return json.loads(payment.json())

# # Подтверждает наличие "товара"
# @bot.pre_checkout_query_handler(func=lambda query: True)
# def process_pre_checkout_query(pre_checkout_query):
#     bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=None)

# Обработчик всех кнопок
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    global msg
    global beats
    global beats_buttons
    global balance_messages

    # # Асинхронная функция проверки статуса платежа
    # async def check_payment(payment_id):
    #     payment = json.loads((Payment.find_one(payment_id)).json())
    #     while payment['status'] == 'pending':
    #         payment = json.loads((Payment.find_one(payment_id)).json())
    #         await asyncio.sleep(3)

    #     if payment['status']=='succeeded':
    #         print("SUCCSESS RETURN")
    #         db_handler.top_balance(call.message.chat.id, call.data.split('₽')[0])
    #         bot.send_message(call.message.chat.id, f'🤑 Твой баланс пополнен на {call.data}').message_id
    #         if call.message.chat.id in balance_messages: 
    #             balance_markup = Keyboa(items=balance_buttons, items_in_row=3)
    #             balance = db_handler.get_balance(call.message.chat.id)
    #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=balance_messages[call.message.chat.id], text=f'🏦 На твоем балансе {balance}₽\n\n👉 Выбери сумму для пополнения:', reply_markup=balance_markup())
    #         return True
    #     else:
    #         print("BAD RETURN")
    #         bot.send_message(call.message.chat.id, 'Не удалось пополнить баланс.')
    #         return False

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
                if call.data == f'🎵 Сгенерировать бит - {beat_price}₽ 🎵':
                    if (beats_generating.get(call.message.chat.id) is not None and beats_generating.get(call.message.chat.id) == False) or db_handler.get_beats_generating(call.message.chat.id) == 0:
                        if processing.get(call.message.chat.id) is not None or db_handler.get_processing(call.message.chat.id) == 0:
                            db_handler.set_processing(call.message.chat.id)
                            processing[call.message.chat.id] = True

                            styles_markup = Keyboa(items=styles_buttons, items_in_row=2)
                            message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, '🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=styles_markup()).message_id

                            db_handler.del_processing(call.message.chat.id)
                            processing[call.message.chat.id] = False
                    else:
                        if (processing.get(call.message.chat.id) is not None and processing.get(call.message.chat.id) == False) or db_handler.get_processing(call.message.chat.id) == 0:
                            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'):
                                if path.isfile(file):
                                    pass
                                else:
                                    inline_markup = Keyboa(items=menu_buttons[2], items_in_row=1)
                                    bot.send_message(call.message.chat.id, f"🔄 Твои ранее сгенерированные версии битов по прошлому запросу уже удалились.\n\nЧтобы сгенерировать новые биты нажми на кнопку 👉", reply_markup=inline_markup())
                                    # Убрать пользователя из "обработки"
                                    db_handler.del_processing(call.message.chat.id)
                                    processing[call.message.chat.id] = False
                                    db_handler.del_beats_generating(call.message.chat.id)
                                    beats_generating[call.message.chat.id] = False
                                    return
                            bot.send_message(call.message.chat.id, 'Ты не можешь заказать еще один бит во время заказа. Выбери версию бита и дождись её отправки.')
                        else:
                            bot.send_message(call.message.chat.id, 'Ты не можешь заказать еще один бит во время заказа.')    
                elif call.data == '💰 Баланс':
                    balance_markup = Keyboa(items=balance_buttons, items_in_row=3)
                    # Запрос баланса пользователя в таблице users
                    balance = db_handler.get_balance(call.message.chat.id) 
                    balance_messages[call.message.chat.id] = bot.send_message(call.message.chat.id, f'🏦 На твоем балансе {balance}₽\n\n🛑НА ДАННЫЙ МОМЕНТ ОПЛАТА РАБОТАЕТ В ТЕСТОВОМ РЕЖИМЕ 🛑 Рабочая оплата будет после одобрения кассы.\n\n👉 Выбери сумму для пополнения:', reply_markup=balance_markup()).message_id
                elif call.data == '🏡 О нас':
                    bot.send_message(call.message.chat.id, '📌Услугу предоставляет:\n\nИНН: 910821614530\n👤Сычёв Егор Владимирович\n\n✉️Почта для связи:\ntech.beatbot@mail.ru\n\n📞Телефон для связи:\n+79781055722\n\n🌍Официальный сайт:\nhttps://beatmaker.site')   
        except Exception as e:
            print(repr(e))
            db_handler.del_processing(call.message.chat.id)
        return
    elif call.data in balance_buttons:
        try:
            if call.message:
                # # Получение цены из callback_data
                # price = int(call.data.split('₽')[0])
                # # Отправка счета пользователю
                # payment_data = payment(price, f'Пополнение баланса на {price}₽')
                # payment_id = payment_data['id']
                # confirmation_url = payment_data['confirmation']['confirmation_url']
                # # Создаем объект кнопки с ссылкой на документацию pytelegrambotapi
                # btn = types.InlineKeyboardButton(f'Оплатить {price}₽', url=confirmation_url)
                # # Создаем объект клавиатуры и добавляем на нее кнопку
                # keyboard = types.InlineKeyboardMarkup()
                # keyboard.add(btn)
                # bot.send_message(call.message.chat.id, f'💳 Теперь перейди по ссылке', reply_markup=keyboard)
                # asyncio.run(check_payment(payment_id))
                print("SUCCSESS RETURN")
                db_handler.top_balance(call.message.chat.id, call.data.split('₽')[0])
                bot.send_message(call.message.chat.id, f'🤑 Твой баланс пополнен на {call.data}').message_id
                if call.message.chat.id in balance_messages: 
                    balance_markup = Keyboa(items=balance_buttons, items_in_row=3)
                    balance = db_handler.get_balance(call.message.chat.id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=balance_messages[call.message.chat.id], text=f'🏦 На твоем балансе {balance}₽\n\n🛑НА ДАННЫЙ МОМЕНТ ОПЛАТА РАБОТАЕТ В ТЕСТОВОМ РЕЖИМЕ 🛑 Рабочая оплата будет после одобрения кассы.\n\nВыбери сумму для пополнения:', reply_markup=balance_markup())

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
                            bot.send_message(call.message.chat.id, '⚠️ Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых')
                            return
                    else:
                        if call.data not in bpm_buttons[db_handler.get_chosen_style[call.message.chat.id]]:
                            bot.send_message(call.message.chat.id, '⚠️ Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых')
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
                                    status = make_beat.jersey_club(call.message.chat.id, call.data, i)
                                elif style == 'Trap':
                                    status = make_beat.trap(call.message.chat.id, call.data, i)
                                elif style == 'Drill':
                                    status = make_beat.drill(call.message.chat.id, call.data, i)
                                elif style == 'Plug':
                                    status = make_beat.plug(call.message.chat.id, call.data, i)
                            if status:
                                return True
                            else:
                                return False   
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
                        if generate_beats(db_handler.get_chosen_style(call.message.chat.id), beats) == False:
                            db_handler.del_processing(call.message.chat.id)
                            db_handler.del_beats_generating(call.message.chat.id)
                            # Удалить файлы
                            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'):
                                remove(file)
                            return bot.send_message(call.message.chat.id, '⚠️ Не удалось отправить пробные версии битов, деньги за транзакцию не сняты. Попробуй ещё раз.')

                        if message_to_delete.get(call.message.chat.id) is not None:
                            bot.delete_message(call.message.chat.id, message_to_delete[call.message.chat.id])
                            del message_to_delete[call.message.chat.id]
                        # Отправить бит
                        message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, f'Вот 3 демо версии битов на твой вкус: {db_handler.get_chosen_style(call.message.chat.id)}').message_id

                        trimmed_audio(glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'))

                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}]_short.wav'):         
                            remove(file)

                    else:    
                        inline_markup = Keyboa(items=menu_buttons[0], items_in_row=1)
                        bot.send_message(call.message.chat.id, f'⚠️ Тебе не хватает денег на балансе, пополни баланс чтобы купить бит', reply_markup=inline_markup())
                        db_handler.del_beats_generating(call.message.chat.id)
                        beats_generating[call.message.chat.id] = False
                    db_handler.del_processing(call.message.chat.id)
                    processing[call.message.chat.id] = False
        except Exception as e:
            print(repr(e))
            db_handler.del_processing(call.message.chat.id)
            db_handler.del_beats_generating(call.message.chat.id)
            bot.send_message(call.message.chat.id, '⚠️ Не удалось отправить пробные версии битов, деньги за транзакцию не сняты. Попробуй ещё раз.')
            # Удалить файлы
            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'):
                remove(file)
        return
    elif call.data in beats_buttons:
        try:
            if call.message:
                if (processing.get(call.message.chat.id) is not None or db_handler.get_processing(call.message.chat.id) == 0) and (beats_generating.get(call.message.chat.id) is not None or db_handler.get_beats_generating(call.message.chat.id) != 0):
                    # Добавить пользователя в "обработку"
                    db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True

                    bot.send_message(call.message.chat.id, f'Твой выбор: {call.data}')
                    
                    if call.data in beats_buttons:
                        
                        message_to_delete[call.message.chat.id] = bot.send_message(call.message.chat.id, 'Скидываю полную версию...').message_id

                        # Открыть файл
                        beat = open(f'output_beats/{call.message.chat.id}_{call.data}.wav', 'rb')

                        # Скинуть файл
                        bot.send_audio(call.message.chat.id, beat)
                        bot.send_message(call.message.chat.id, f'С твоего баланса снято {beat_price}₽\nНадеюсь тебе понравится бит😉')
                        
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
            # Удалить файлы
            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].wav'):
                remove(file)
            bot.send_message(call.message.chat.id, '⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.')

bot.polling()
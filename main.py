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
    'Old School': 'OldSchool'
}

styles_buttons = []
for key in aliases.keys():
    styles_buttons.append(key)

beat_price = 90 # RUB

# Кнопки 
menu_buttons = ['💰 Баланс', '🏡 О нас', f'🎵 Сгенерировать бит - {beat_price}₽ 🎵']
balance_buttons = ['90₽', '180₽', '360₽']
extensions_buttons = ['wav', 'mp3']
undo_button = ['⬅️ Назад']
menu_button = ['⬅️ В меню']
styles_button = ['⬅️ К стилям']

# Для каждого стиля свои кнопки bpm
bpm_buttons = {'Jersey Club': ['140bpm', '150bpm', '160bpm'],
               'Trap': ['110bpm', '130bpm', '145bpm'],
               'Drill': ['110bpm', '130bpm', '145bpm'],
               'Plug': ['140bpm', '150bpm', '160bpm'],
               'Old School': ['155bpm', '170bpm', '185bpm']}

# Начальный баланс пользователя при добавлении в БД
start_balance = 0 # RUB
# Переменная хранит данные пользователя, служит для уменьшения количества запросов в БД на add_user
is_added = {}

if launch.mailing_list is not None:
    try:
        for chat_id in launch.mailing_list:
            inline_markup = Keyboa(items=menu_buttons[2], items_in_row=1)
            bot.send_message(chat_id, 'Сожалею, но во время создания твоих битов бот перезапустился 😵‍💫\n\nЭто происходит очень редко, но необходимо для стабильной работы бота. Деньги за транзакцию не сняты.\n\nТы можешь заказать бит еще раз 👉', reply_markup=inline_markup())         
        for chat_id in launch.chat_ids_by_messages_to_del_ids:
            messages_ids = db_handler.get_beats_versions_messages_ids(chat_id).split(', ')
            for mes_id in messages_ids:
                bot.delete_message(chat_id, mes_id)
            db_handler.del_beats_versions_messages_ids(chat_id)
    except:
        db_handler.del_beats_versions_messages_ids(chat_id)

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
    bot.send_message(message.chat.id, "🎶 Привет! Это меню заказа битов 🎶\n\n💥 Ты можешь ознакомиться с примером бита, который я могу создать, используя команду /example_beats. Просто отправь эту команду в чат и ты получишь ссылку на наш пример.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=inline_markup()).id

    user_initials = f'{message.from_user.first_name} {message.from_user.last_name}'

    # Добавление пользователя в таблицу users
    if is_added.get(message.chat.id) is None:
        is_added[message.chat.id] = True
        db_handler.add_user(message.chat.username, message.chat.id, user_initials, start_balance)

# Если пользоват елю уже отправлялись примеры битов, то значение под ключем его chat_id будет True
got_example_beats = {}

@bot.message_handler(commands=['example_beats'])
def example(message):
    if got_example_beats.get(message.chat.id) is None and ((beats_generating.get(message.chat.id) is not None and beats_generating.get(message.chat.id) == False) or db_handler.get_beats_generating(message.chat.id) == 0):
        got_example_beats[message.chat.id] = True
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
message_to_edit = {}
# chat_id: call.data (bpm)
user_chosen_bpm = {}
# chat_id: call.data (extension)
user_chosen_extension = {}

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
    global msg, user, beats, beats_buttons, user_bpm, balance_messages, message_to_edit, beats_generating, processing

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
    if call.data in undo_button+menu_button:
        try:
            if call.message:
                inline_markup = Keyboa(items=menu_buttons, items_in_row=2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🎶 Привет! Это меню заказа битов 🎶\n\n💥 Ты можешь ознакомиться с примером бита, который я могу создать, используя команду /example_beats. Просто отправь эту команду в чат и ты получишь ссылку на наш пример.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=inline_markup())
        except Exception as e:
            print(repr(e))
    if call.data in styles_button:
        try:
            if call.message:
                # db_handler.set_processing(call.message.chat.id)
                processing[call.message.chat.id] = True
                
                styles_markup = Keyboa(items=styles_buttons + undo_button, items_in_row=2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🎵 Генерация бита 🎵\n\n🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=styles_markup()).message_id
                
                # db_handler.del_processing(call.message.chat.id)
                del processing[call.message.chat.id]
        except Exception as e:
            print(repr(e))
        return
    if call.data in menu_buttons:
        try:
            if call.message:    
                if call.data == f'🎵 Сгенерировать бит - {beat_price}₽ 🎵':
                    if (beats_generating.get(call.message.chat.id) is not None and beats_generating.get(call.message.chat.id) == False) or db_handler.get_beats_generating(call.message.chat.id) == 0:
                        # if processing.get(call.message.chat.id) is None or db_handler.get_processing(call.message.chat.id) == 0:
                        if processing.get(call.message.chat.id) is None:
                            # db_handler.set_processing(call.message.chat.id)
                            processing[call.message.chat.id] = True

                            styles_markup = Keyboa(items=styles_buttons + undo_button, items_in_row=2)
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🎵 Генерация бита 🎵\n\n🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=styles_markup()).message_id

                            # db_handler.del_processing(call.message.chat.id)
                            del processing[call.message.chat.id]
                    else:
                        # if (processing.get(call.message.chat.id) is None and processing.get(call.message.chat.id) == False) or db_handler.get_processing(call.message.chat.id) == 0:
                        if processing.get(call.message.chat.id) is None and processing.get(call.message.chat.id) == False:

                            bot.send_message(call.message.chat.id, 'Ты не можешь заказать еще один бит во время заказа. Выбери версию бита и дождись её отправки.')
                        else:
                            bot.send_message(call.message.chat.id, 'Ты не можешь заказать еще один бит во время заказа.')    
                
                elif call.data == '💰 Баланс':
                    balance_markup = Keyboa(items=balance_buttons + undo_button, items_in_row=3)
                    # Запрос баланса пользователя в таблице users
                    balance = db_handler.get_balance(call.message.chat.id) 
                    balance_messages[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'💰 Баланс\n\n🏦 На твоем балансе *{balance}₽*\n\n🛑НА ДАННЫЙ МОМЕНТ ОПЛАТА РАБОТАЕТ В ТЕСТОВОМ РЕЖИМЕ 🛑 Рабочая оплата будет после одобрения кассы.\n\n👉 Выбери сумму для пополнения:', reply_markup=balance_markup(), parse_mode='Markdown').message_id
                
                elif call.data == '🏡 О нас':
                    about_markup = Keyboa(items=undo_button)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'🏡 О нас\n\n📌Услугу предоставляет:\n\nИНН: 910821614530\n👤Сычёв Егор Владимирович\n\n✉️Почта для связи:\ntech.beatbot@mail.ru\n\n📞Телефон для связи:\n+79781055722\n\n🌍Официальный сайт:\nhttps://beatmaker.site', reply_markup=about_markup())

        except Exception as e:
            print(repr(e))
            # db_handler.del_processing(call.message.chat.id)
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
                inline_markup = Keyboa(items=menu_buttons[2], items_in_row=1)
                bot.send_message(call.message.chat.id, f'🤑 Твой баланс пополнен на *{call.data}*', reply_markup=inline_markup(), parse_mode='Markdown').message_id
                if call.message.chat.id in balance_messages: 
                    balance_markup = Keyboa(items=balance_buttons + undo_button, items_in_row=3)
                    balance = db_handler.get_balance(call.message.chat.id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=balance_messages[call.message.chat.id], text=f'🏦 На твоем балансе *{balance}₽*\n\n🛑НА ДАННЫЙ МОМЕНТ ОПЛАТА РАБОТАЕТ В ТЕСТОВОМ РЕЖИМЕ 🛑 Рабочая оплата будет после одобрения кассы.\n\nВыбери сумму для пополнения:', reply_markup=balance_markup(), parse_mode='Markdown')

        except Exception as e:
            print(repr(e))
        return
    elif call.data in styles_buttons:
        try:
            if call.message:
                # if processing.get(call.message.chat.id) is None or db_handler.get_processing(call.message.chat.id) == 0:
                if processing.get(call.message.chat.id) is None:
                    # db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True

                    bpm_markup = Keyboa(items=bpm_buttons[call.data] + styles_button, items_in_row=3)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'*{call.data}* - отличный выбор! Теперь выбери темп:\n\n*{bpm_buttons[call.data][0]}* - замедлено\n*{bpm_buttons[call.data][1]}* - нормально\n*{bpm_buttons[call.data][2]}* - ускорено', reply_markup=bpm_markup(), parse_mode='Markdown').message_id 
                    
                    db_handler.set_chosen_style(call.message.chat.id, call.data)
                    user_chosen_style[call.message.chat.id] = call.data

                    # db_handler.del_processing(call.message.chat.id)
                    del processing[call.message.chat.id]

        except Exception as e:
            print(repr(e))
            # db_handler.del_processing(call.message.chat.id)
        return
    
    elif call.data in list(itertools.chain(*bpm_buttons.values())):
        try:
            if call.message:
                # if processing.get(call.message.chat.id) is None or db_handler.get_processing(call.message.chat.id) == 0:
                if processing.get(call.message.chat.id) is None:
                    user_chosen_bpm[call.message.chat.id] = call.data
                    if user_chosen_style.get(call.message.chat.id) is not None:
                        if user_chosen_bpm[call.message.chat.id] not in bpm_buttons[user_chosen_style[call.message.chat.id]]:
                            bot.send_message(call.message.chat.id, '⚠️ Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых')
                            return
                    else:
                        if user_chosen_bpm[call.message.chat.id] not in bpm_buttons[db_handler.get_chosen_style[call.message.chat.id]]:
                            bot.send_message(call.message.chat.id, '⚠️ Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых')
                            return
                    # db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True

                    bpm_markup = Keyboa(items=extensions_buttons + styles_button, items_in_row=2)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'В каком формате скинуть финальный бит?\n\n*.wav* - оригинальное качество, используется профессионалами для записи. (Не воспроизводится на iphone)\n\n*.mp3* - более низкое качество, значительно меньше весит, не подходит для профессиональной записи.', reply_markup=bpm_markup(), parse_mode='Markdown').message_id 
    

                    # db_handler.del_processing(call.message.chat.id)
                    del processing[call.message.chat.id]
        except Exception as e:
            print(repr(e))
            # db_handler.del_processing(call.message.chat.id)
            db_handler.del_beats_generating(call.message.chat.id)
            del processing[call.message.chat.id]
            error_markup = Keyboa(items=undo_button, items_in_row=3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠️ Не удалось отправить пробные версии битов, деньги за транзакцию не сняты. Попробуй ещё раз.', reply_markup=error_markup())
            # Удалить файлы
            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
                remove(file)
        return
    elif call.data in extensions_buttons:
        try:
            if call.message:
                # if processing.get(call.message.chat.id) is None or db_handler.get_processing(call.message.chat.id) == 0:
                if (processing.get(call.message.chat.id) is None) and (beats_generating.get(call.message.chat.id) is not None and beats_generating.get(call.message.chat.id) == False) or db_handler.get_beats_generating(call.message.chat.id) == 0:
                    
                        
                        
                    # db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True
                    if db_handler.get_balance(call.message.chat.id) >= beat_price:

                        db_handler.set_beats_generating(call.message.chat.id)
                        beats_generating[call.message.chat.id] = True

                        user_chosen_extension[call.message.chat.id] = call.data

                        generating_markup = Keyboa(items=undo_button)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='💽 Создаю версии битов, это может занять несколько минут...\n\n🔽Версии появятся внизу🔽', reply_markup=generating_markup())
                        # style - стиль бита, num - сколько битов сделать
                        # def generate_beats(aliases, num, style, chat_id, bpm, extension):
                        #     status = make_beat.generate_some_beats(aliases, num, style, chat_id, bpm, extension)
                        #     if status:
                        #         return True
                        #     else:
                        #         return False

                        # # Обрезать аудио на демо-версии и отправить пользователю, добавить id демо версии в бд
                        # def trimmed_audio(files_list):
                        #     for file_path in files_list:
                                
                        #         sound = AudioSegment.from_file(file_path)
                        #         trimmed = sound[45000:55000]
                        #         new_file_path = f"{path.splitext(file_path)[0]}_short.mp3"
                        #         trimmed.export(new_file_path, format=f"mp3")
                                                        
                        async def check_response():
                            while True:
                                beats_files = sorted(glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'))
                                beats_shorts_files = sorted(glob(f'output_beats/{call.message.chat.id}_[1-{beats}]_short.*'))
                                
                                print(beats_shorts_files)
                                if len(beats_files)==beats and len(beats_shorts_files)==beats:
                                    message_to_edit[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'🚀 Вот 3 демо версии битов, выбери ту, которая понравилась:\n\nСтиль - *{db_handler.get_chosen_style(call.message.chat.id)}* Темп - *{user_chosen_bpm[call.message.chat.id]}*', parse_mode='Markdown').message_id
                        
                                    files_list = beats_shorts_files

                                    messages_ids = []

                                    for file_path in files_list:
                                        with open(file_path, 'rb') as trimmed_sound:
                                            if files_list.index(file_path) == len(files_list)-1:
                                                beats_markup = Keyboa(items=beats_buttons, items_in_row=3)
                                                messages_ids.append(bot.send_audio(call.message.chat.id, trimmed_sound, reply_markup=beats_markup()).message_id)
                                                db_handler.set_beats_versions_messages_ids(call.message.chat.id, ', '.join(str(messages_id) for messages_id in messages_ids))
                                                trimmed_sound.close()
                                                for file in files_list:         
                                                    remove(file)
                                                del messages_ids
                                                return
                                            else:
                                                messages_ids.append(bot.send_audio(call.message.chat.id, trimmed_sound).message_id)
                    
                                await asyncio.sleep(2)
                            

                        # Добавить в очередь 
                        db_handler.set_query(call.message.chat.id, user_chosen_style[call.message.chat.id], user_chosen_bpm[call.message.chat.id], call.data)
                        asyncio.run(check_response())
                        
                    else:    
                        inline_markup = Keyboa(items=menu_buttons[0], items_in_row=1)
                        bot.send_message(call.message.chat.id, f'⚠️ Тебе не хватает денег на балансе, пополни баланс чтобы купить бит', reply_markup=inline_markup())
                        db_handler.del_beats_generating(call.message.chat.id)
                        beats_generating[call.message.chat.id] = False
                    # db_handler.del_processing(call.message.chat.id)
                    del processing[call.message.chat.id]
        except Exception as e:
            print(repr(e))
            # db_handler.del_processing(call.message.chat.id)
            db_handler.del_beats_generating(call.message.chat.id)
            del processing[call.message.chat.id]
            error_markup = Keyboa(items=undo_button, items_in_row=3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⚠️ Не удалось отправить пробные версии битов, деньги за транзакцию не сняты. Попробуй ещё раз.', reply_markup=error_markup())
            # Удалить файлы
            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
                remove(file)
        return
    elif call.data in beats_buttons:
        try:
            if call.message:
                # if (processing.get(call.message.chat.id) is None or db_handler.get_processing(call.message.chat.id) == 0) and (beats_generating.get(call.message.chat.id) is not None or db_handler.get_beats_generating(call.message.chat.id) != 0):
                if (processing.get(call.message.chat.id) is None) and (beats_generating.get(call.message.chat.id) is not None or db_handler.get_beats_generating(call.message.chat.id) != 0): 
                    # Добавить пользователя в "обработку"
                    # db_handler.set_processing(call.message.chat.id)
                    processing[call.message.chat.id] = True

                    if call.data in beats_buttons:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_to_edit[call.message.chat.id], text='📤 Скидываю полную версию... 📤')

                        # Удалить примеры битов
                        messages_to_delete_ids = db_handler.get_beats_versions_messages_ids(call.message.chat.id)
                        if messages_to_delete_ids != '':
                            for mes_id in messages_to_delete_ids.split(', '):
                                bot.delete_message(call.message.chat.id, mes_id)
                        db_handler.del_beats_versions_messages_ids(call.message.chat.id)

                        # Открыть файл

                        beat = open(f'output_beats/{call.message.chat.id}_{call.data}.{user_chosen_extension[call.message.chat.id]}', 'rb')

                        # Скинуть файл
                        bot.send_audio(call.message.chat.id, beat)
                        
                        # Закрыть файл
                        beat.close()

                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_to_edit[call.message.chat.id], text='🔽 Держи 🔽')
                        end_markup = Keyboa(items=menu_button, items_in_row=3)
                        bot.send_message(call.message.chat.id, f'С твоего баланса снято *{beat_price}₽*\nНадеюсь тебе понравится бит😉', reply_markup=end_markup(), parse_mode='Markdown')                        
                        
                        # Удалить файлы
                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
                            remove(file)


                    elif call.data == 'Никакой':   
                        bot.send_message(call.message.chat.id, f'Не одного бита не выбрано, ты можешь посомтреть ещё несколько битов через время.')
                        # Удалить файлы
                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
                            remove(file)

                    # Убрать пользователя из "обработки"
                    # db_handler.del_processing(call.message.chat.id)
                    del processing[call.message.chat.id]
                    del user_chosen_extension[call.message.chat.id]
                    db_handler.del_beats_generating(call.message.chat.id)
                    beats_generating[call.message.chat.id] = False

                    # Снять деньги
                    db_handler.pay(call.message.chat.id, beat_price)

                    # Увеличеть количество купленых битов на аккаунте
                    db_handler.get_beat(call.message.chat.id)
                    
        except Exception as e:
            print(repr(e))
            # db_handler.del_processing(call.message.chat.id)
            del processing[call.message.chat.id]
            del user_chosen_extension[call.message.chat.id]
            db_handler.del_beats_generating(call.message.chat.id)
            # Удалить файлы
            for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
                remove(file)
            error_markup = Keyboa(items=undo_button, items_in_row=3)
            bot.send_message(call.message.chat.id, '⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.', reply_markup=error_markup())

bot.polling()
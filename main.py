import telebot
# Клавиатура
from keyboa import Keyboa 
# Инструмент для выборки путей к файлам
from glob import glob
# Файл данных
import config
# Файл для безопасного запуска бота
import launch
# Файл оверлеев битов
import make_beat
# Файл обработчика запросов к БД
import db_handler
# Для конфигурирования и создания платежа
# from yookassa import Configuration,Payment 

import itertools
import time
from os import remove

# Подключение бота
bot = telebot.TeleBot(config.TOKEN)

# Подключение Юкассы
# Configuration.account_id = config.SHOP_ID
# Configuration.secret_key = config.SHOP_API_TOKEN

# Цена бита
beat_price = 180 # RUB

# Начальный баланс пользователя при добавлении в БД
start_balance = 0 # RUB

# Количество битов для создания
beats = launch.beats

# Инициализация кнопок
# Кнопки меню
BUTTON_GENERATE_BEAT = f'🎵 Сгенерировать бит - {beat_price}₽ 🎵'
BUTTON_BALANCE = '💰 Баланс'
BUTTON_ABOUT = '🏡 О нас'

MENU_BUTTONS = [BUTTON_BALANCE, BUTTON_ABOUT, BUTTON_GENERATE_BEAT]

# Кнопки баланса

BALANCE_BUTTONS = ['180₽', '360₽', '540₽']

# Кнопки расширения
BUTTON_MP3 = '.mp3'
BUTTON_WAV = '.wav'

EXTENSIONS_BUTTONS = {BUTTON_WAV: 'wav', BUTTON_MP3: 'mp3'}

# Кнопки интерфейса
UNDO_BUTTON = '⬅️ Назад'
MENU_BUTTON = '⬅️ В меню'
STYLES_BUTTON = '⬅️ К стилям'

# Кнопки стилей
# Ключи - названия стилей на кнопках, значения - названия папок style_*
aliases = {
    'Jersey Club': 'JC',
    'Trap': 'Trap',
    'Drill': 'Drill',
    'Plug': 'Plug',
    'Old School': 'OldSchool'
}

STYLES_BUTTONS = [key for key in aliases.keys()]

# Кнопки битов
BEATS_BUTTONS = [str(i) for i in range(1, beats+1)]

# Кнопки темпов
# Для каждого стиля свои кнопки bpm
BPM_BUTTONS = {'Jersey Club': ['140bpm', '150bpm', '160bpm'],
               'Trap': ['110bpm', '130bpm', '145bpm'],
               'Drill': ['110bpm', '130bpm', '145bpm'],
               'Plug': ['140bpm', '150bpm', '160bpm'],
               'Old School': ['155bpm', '170bpm', '185bpm']}

### Запуск бота

# Для правильной обработки тех пользователей, во время работы с которыми бот перезапустился

##########

if launch.mailing_list is not None:
    try:
        for chat_id in launch.mailing_list:
            inline_markup = Keyboa(items=MENU_BUTTONS[2], items_in_row=1)
            bot.send_message(chat_id, 'Сожалею, но во время создания твоих битов бот перезапустился 😵‍💫\n\nЭто происходит очень редко, но необходимо для стабильной работы бота. Деньги за транзакцию не сняты.\n\nТы можешь заказать бит еще раз 👉', reply_markup=inline_markup())         
        for chat_id in launch.chat_ids_by_messages_to_del_ids:
            messages_ids = db_handler.get_beats_versions_messages_ids(chat_id).split(', ')
            for mes_id in messages_ids:
                bot.delete_message(chat_id, mes_id)
            db_handler.del_beats_versions_messages_ids(chat_id)
    except:
        db_handler.del_beats_versions_messages_ids(chat_id)

##########

### Работа бота

## Обработка команд

@bot.message_handler(commands=['start'])
def welcome(message):  
    # Отправка сообщения
    bot.send_message(message.chat.id, 'Привет! 👋\n\nЯ телеграм-бот, который поможет тебе создать качественные 🎧 биты в разных стилях.\n\nМоя главная особенность - доступная 💰 цена и большой выбор стилей. Ты можешь выбрать любой стиль, который тебе нравится, и я создам для тебя уникальный бит.\n\nНе упусти возможность создать свой собственный звук и выделиться на фоне других исполнителей! 🎶\n\nЧтобы начать, используй команду\n/menu')

@bot.message_handler(commands=['menu'])
def menu(message):
    # Отправка сообщения
    inline_markup = Keyboa(items=MENU_BUTTONS, items_in_row=2)
    bot.send_message(message.chat.id, "🎶 Это меню заказа битов 🎶\n\n💥 Ты можешь ознакомиться с примером бита, который я могу создать, используя команду /example_beats. Просто отправь эту команду в чат и ты получишь ссылку на наш пример.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=inline_markup()).id

    # Добавление в БД

    # Имя и фамилия пользователя
    user_initials = f'{message.from_user.first_name} {message.from_user.last_name}'
    # Если пользователь уже добавлен то повторная запись не произойдет
    db_handler.add_user(message.chat.username, message.chat.id, user_initials, start_balance)

@bot.message_handler(commands=['example_beats'])
def send_example_beats(message):
    # Отправка сообщения и битов
    bot.send_message(message.chat.id, "Конечно! Вот несколько примеров готовых битов 💾\nНе сомневайся, бот сделает такие же и тебе!")
    for file_path in glob('example_beats/*.wav'):
            example_beat = open(file_path, 'rb')
            bot.send_audio(message.chat.id, example_beat)
            example_beat.close()

## Обработка кнопок

# Обработка кнопок интерфейса

def get_user(chat_id):
    if db_handler.get_user(chat_id) == False:
        # Отправка сообщения
        bot.send_message(chat_id, 'Нужно перезапустить бота командой /start')
        return False
    else:
        return True
    
def reset_chosen_params(chat_id):
    db_handler.del_chosen_bpm(chat_id)
    db_handler.del_chosen_style(chat_id)

@bot.callback_query_handler(func=lambda call: call.data in STYLES_BUTTON)
def return_to_styles(call):
    chat_id = call.message.chat.id
    if get_user(chat_id):
        # Проверить, не находится ли пользователь в beats_generating
        if db_handler.get_beats_generating(chat_id) == 0:
            # Проверить, не находится ли пользователь в processing
            if db_handler.get_processing(chat_id) == 0:
                # Установить processing для пользователя
                db_handler.set_processing(chat_id)

                # Обнулить выбранные пользователем параметры бита
                reset_chosen_params(chat_id)
                
                # Отправка сообщения
                styles_markup = Keyboa(items=STYLES_BUTTONS + [UNDO_BUTTON], items_in_row=2)
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='🎵 Генерация бита 🎵\n\n🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=styles_markup()).message_id
                
                # Удалить processing для пользователя
                db_handler.del_processing(chat_id)
    else:
        # Отправка оповещения
        bot.answer_callback_query(callback_query_id=call.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data in UNDO_BUTTON or call.data in MENU_BUTTON)
def return_to_menu(call):
    chat_id = call.message.chat.id
    if get_user(chat_id):
        # Обнулить выбранные пользователем параметры бита
        reset_chosen_params(chat_id)
        # Отправка сообщения
        inline_markup = Keyboa(items=MENU_BUTTONS, items_in_row=2)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🎶 Это меню заказа битов 🎶\n\n💥 Ты можешь ознакомиться с примером бита, который я могу создать, используя команду /example_beats. Просто отправь эту команду в чат и ты получишь ссылку на наш пример.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=inline_markup()).id

@bot.callback_query_handler(func=lambda call: call.data in MENU_BUTTONS)
def show_menu(call):
    try:
        
        chat_id = call.message.chat.id
        pressed_button = call.data

        if get_user(chat_id):
            if pressed_button == BUTTON_GENERATE_BEAT:
                # Проверить, не находится ли пользователь в beats_generating
                if db_handler.get_beats_generating(chat_id) == 0:
                    # Проверить, не находится ли пользователь в processing
                    if db_handler.get_processing(chat_id) == 0:
                        # Установить processing для пользователя
                        db_handler.set_processing(chat_id)

                        # Обнулить выбранные пользователем параметры бита
                        reset_chosen_params(call.message.chat.id)

                        # Отправка сообщения
                        styles_markup = Keyboa(items=STYLES_BUTTONS + [UNDO_BUTTON], items_in_row=2)
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text='🎵 Генерация бита 🎵\n\n🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=styles_markup()).message_id
                        
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                else:
                    # Отправка оповещения
                    bot.answer_callback_query(callback_query_id=call.id, text='Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

            elif pressed_button == BUTTON_BALANCE:
                # Запрос баланса пользователя в таблице users
                balance = db_handler.get_balance(chat_id)
                # Отправка сообщения
                balance_markup = Keyboa(items=BALANCE_BUTTONS + [UNDO_BUTTON], items_in_row=3)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'💰 Баланс\n\n🏦 На твоем балансе *{balance}₽*\n\n🛑НА ДАННЫЙ МОМЕНТ ОПЛАТА РАБОТАЕТ В ТЕСТОВОМ РЕЖИМЕ 🛑 Рабочая оплата будет после одобрения кассы.\n\n👉 Выбери сумму для пополнения:', reply_markup=balance_markup(), parse_mode='Markdown').message_id

            elif pressed_button == BUTTON_ABOUT:
                # Отправка сообщения
                about_markup = Keyboa(items=UNDO_BUTTON)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'🏡 О нас\n\n📌Услугу предоставляет:\n\nИНН: 910821614530\n👤Сычёв Егор Владимирович\n\n✉️Почта для связи:\ntech.beatbot@mail.ru\n\n📞Телефон для связи:\n+79781055722\n\n🌍Официальный сайт:\nhttps://beatmaker.site', reply_markup=about_markup())
            
    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data in BALANCE_BUTTONS)
def generate_query_payment(call):
    
    chat_id = call.message.chat.id
    if get_user(chat_id):

        # Отправка сообщения
        pass

@bot.callback_query_handler(func=lambda call: call.data in STYLES_BUTTONS)
def show_bpm(call):
    try:
        
        chat_id = call.message.chat.id
        user_chosen_style = call.data

        if get_user(chat_id):     
            # Проверить, не находится ли пользователь в beats_generating
            if db_handler.get_beats_generating(chat_id) == 0:
                # Проверить, не находится ли пользователь в processing
                if db_handler.get_processing(chat_id) == 0:
                    if db_handler.get_chosen_style(chat_id) == '':
                        # Установить processing для пользователя
                        db_handler.set_processing(chat_id)

                        db_handler.set_chosen_style(chat_id, user_chosen_style)

                        # Отправка сообщения
                        bpm_markup = Keyboa(items=BPM_BUTTONS[user_chosen_style] + [STYLES_BUTTON], items_in_row=3)
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'*{call.data}* - отличный выбор! Теперь выбери темп:\n\n*{BPM_BUTTONS[user_chosen_style][0]}* - замедлено\n*{BPM_BUTTONS[user_chosen_style][1]}* - нормально\n*{BPM_BUTTONS[user_chosen_style][2]}* - ускорено', reply_markup=bpm_markup(), parse_mode='Markdown').message_id 
                        
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                    else:
                        bpm_markup = Keyboa(items=[STYLES_BUTTON], items_in_row=3)
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'⚠️ Похоже, что ты уже выбрал другой стиль в другом сообщении, закончи выбор параметров твоего бита там же\n\n...или начни новый выбор параметров здесь 👉', reply_markup=bpm_markup(), parse_mode='Markdown').message_id 

            else:
                # Отправка оповещения
                bot.answer_callback_query(callback_query_id=call.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data in list(itertools.chain(*BPM_BUTTONS.values())))
def show_extensions(call):
    try:
        
        chat_id = call.message.chat.id
        user_chosen_bpm = call.data

        if get_user(chat_id):     
            # Проверить, не находится ли пользователь в beats_generating
            if db_handler.get_beats_generating(chat_id) == 0:
                # Проверить, не находится ли пользователь в processing
                if db_handler.get_processing(chat_id) == 0:
                    user_chosen_style = db_handler.get_chosen_style(chat_id)
                    # Проверить, есть ли в базе выбранный пользователем стиль
                    if  user_chosen_style != '':
                        # Установить processing для пользователя
                        db_handler.set_processing(chat_id)

                        if user_chosen_bpm in BPM_BUTTONS[user_chosen_style]:

                            db_handler.set_chosen_bpm(chat_id, user_chosen_bpm)
                            # Отправка сообщения
                            bpm_markup = Keyboa(items=list(EXTENSIONS_BUTTONS.keys()) + [STYLES_BUTTON], items_in_row=2)
                            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'В каком формате скинуть финальный бит?\n\n*.wav* - оригинальное качество, используется профессионалами для записи. (Не воспроизводится на iphone)\n\n*.mp3* - более низкое качество, значительно меньше весит, не подходит для профессиональной записи.', reply_markup=bpm_markup(), parse_mode='Markdown').message_id       
                        else:
                            # Отправка оповещения
                            bot.answer_callback_query(callback_query_id=call.id, text='⚠️ Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых', show_alert=True)
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                    else:
                        # Отправка сообщения
                        bpm_markup = Keyboa(items=[STYLES_BUTTON], items_in_row=3)
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'⚠️ Не удалось выбрать bpm, пожалуйста выбери стиль ещё раз', reply_markup=bpm_markup(), parse_mode='Markdown').message_id 
            else:
                # Отправка оповещения
                bot.answer_callback_query(callback_query_id=call.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(call.message.chat.id)

# Сообщение для редактирования
message_to_edit = {}

@bot.callback_query_handler(func=lambda call: call.data in EXTENSIONS_BUTTONS.keys())
def make_query(call):
    
    try:
        chat_id = call.message.chat.id
        user_chosen_extension = call.data

        if get_user(chat_id):     
            # Проверить, не находится ли пользователь в beats_generating
            if db_handler.get_beats_generating(chat_id) == 0:
                # Проверить, не находится ли пользователь в processing
                if db_handler.get_processing(chat_id) == 0:
                    # Установить processing для пользователя
                    db_handler.set_processing(chat_id)

                    user_chosen_style = db_handler.get_chosen_style(chat_id)
                    user_chosen_bpm = db_handler.get_chosen_bpm(chat_id)

                    # Проверить, есть ли в базе выбранный пользователем style и bpm
                    if db_handler.get_balance(chat_id) >= beat_price:
                        if  user_chosen_style != '' and user_chosen_bpm != '':
                            
                            # Установить processing для пользователя
                            db_handler.set_chosen_extension(chat_id, user_chosen_extension)

                            # Добавить пользователя в beats_generating
                            db_handler.set_beats_generating(chat_id)

                            generating_markup = Keyboa(items=[UNDO_BUTTON])
                            message_to_edit[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='💽 Создаю версии битов, это может занять несколько минут...\n\n🔽Версии появятся внизу🔽', reply_markup=generating_markup()).message_id

                            # Удалить файлы
                            for file in glob(f'output_beats/{chat_id}_[1-{beats}]*.*'):
                                remove(file)
                                                            
                            def check_response():
                                order_number = 0
                                while True:
                                    beats_files = sorted(glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'))
                                    beats_shorts_files = sorted(glob(f'output_beats/{call.message.chat.id}_[1-{beats}]_short.*'))
                                    
                                    print(beats_shorts_files)
                                    if len(beats_files)==beats and len(beats_shorts_files)==beats:
                                        message_to_edit[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_to_edit[call.message.chat.id], text=f'🚀 Вот 3 демо версии битов, выбери ту, которая понравилась:\n\nСтиль - *{db_handler.get_chosen_style(chat_id)}* Темп - *{db_handler.get_chosen_bpm(chat_id)}*', parse_mode='Markdown').message_id
                            
                                        files_list = beats_shorts_files

                                        messages_ids = []

                                        for file_path in files_list:
                                            with open(file_path, 'rb') as trimmed_sound:
                                                if files_list.index(file_path) == len(files_list)-1:
                                                    beats_markup = Keyboa(items=BEATS_BUTTONS, items_in_row=3)
                                                    messages_ids.append(bot.send_audio(call.message.chat.id, trimmed_sound, reply_markup=beats_markup()).message_id)
                                                    db_handler.set_beats_versions_messages_ids(call.message.chat.id, ', '.join(str(messages_id) for messages_id in messages_ids))
                                                    trimmed_sound.close()
                                                    for file in files_list:         
                                                        remove(file)
                                                    del messages_ids
                                                    return
                                                else:
                                                    messages_ids.append(bot.send_audio(call.message.chat.id, trimmed_sound).message_id)

                                    new_order_number = db_handler.get_query_by_chat_id(call.message.chat.id)
                                    # Если заявка пользователя удалится из очереди, то количество заявок перед ним будет 0, т.к биты не скинулись а заявка удалена отправить ошибку
                                    if new_order_number==0:
                                        # Удалить beats_generating для пользователя
                                        db_handler.del_beats_generating(call.message.chat.id)
                                        # Удалить файлы
                                        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
                                            remove(file)
                                        error_markup = Keyboa(items=[UNDO_BUTTON], items_in_row=3)
                                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.', reply_markup=error_markup())
                                        return
                                    print(new_order_number)
                                    if new_order_number != order_number:
                                        order_number = new_order_number
                                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'💽 Создаю версии битов, это может занять несколько минут...\n\nТвоё место в очереди: {order_number}\n\n🔽Версии появятся внизу🔽', parse_mode='Markdown')  
                            
                                    time.sleep(2)
                            # Добавить в очередь 
                            db_handler.set_query(chat_id, db_handler.get_chosen_style(chat_id), db_handler.get_chosen_bpm(chat_id), db_handler.get_chosen_extension(chat_id).split('.')[-1])

                            check_response()
            
                        else:
                            # Отправка сообщения
                            extension_markup = Keyboa(items=[STYLES_BUTTON], items_in_row=3)
                            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'⚠️ Не удалось выбрать расширение, попробуй ещё раз. Выбрать параметры бита нужно строго в предлагаемом ботом порядке и в одном окне', reply_markup=extension_markup(), parse_mode='Markdown').message_id 
                    else:
                        extension_markup = Keyboa(items=MENU_BUTTONS[0], items_in_row=3)
                        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'⚠️ Сперва тебе нужно пополнить баланс', reply_markup=extension_markup(), parse_mode='Markdown').message_id 

                # Удалить processing для пользователя
                db_handler.del_processing(chat_id)
            else:
                # Отправка оповещения
                bot.answer_callback_query(callback_query_id=call.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.del_processing(call.message.chat.id)
        # Удалить beats_generating для пользователя
        db_handler.del_beats_generating(call.message.chat.id)
        # Удалить файлы
        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
            remove(file)
            
        error_markup = Keyboa(items=[UNDO_BUTTON], items_in_row=3)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f'⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.', reply_markup=error_markup())

    
@bot.callback_query_handler(func=lambda call: call.data in BEATS_BUTTONS)
def send_beat(call):
    try:  
        chat_id = call.message.chat.id
        pressed_button = call.data

        if get_user(chat_id):
            
            # Проверить, не находится ли пользователь в processing
            if db_handler.get_processing(chat_id) == 0:
                # Установить processing для пользователя
                db_handler.set_processing(chat_id)

                bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit[chat_id], text='📤 Скидываю полную версию... 📤')

                # Удалить примеры битов
                messages_to_delete_ids = db_handler.get_beats_versions_messages_ids(chat_id)
                if messages_to_delete_ids != '':
                    for mes_id in messages_to_delete_ids.split(', '):
                        bot.delete_message(chat_id, mes_id)
                db_handler.del_beats_versions_messages_ids(chat_id)

                # Открыть файл
                beat = open(f'output_beats/{chat_id}_{pressed_button}.{db_handler.get_chosen_extension(chat_id).split(".")[-1]}', 'rb')

                # Скинуть файл
                bot.send_audio(chat_id, beat)
                
                # Закрыть файл
                beat.close()
        
                # Отправка сообщения
                bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit[chat_id], text='🔽 Держи 🔽')
                end_markup = Keyboa(items=[MENU_BUTTON], items_in_row=3)
                bot.send_message(chat_id, f'С твоего баланса снято *{beat_price}₽*\nНадеюсь, тебе понравится бит 😉', reply_markup=end_markup(), parse_mode='Markdown')                        
                
                # Удалить файлы
                for file in glob(f'output_beats/{chat_id}_[1-{beats}]*.*'):
                    remove(file)

                # Снять деньги
                db_handler.pay(chat_id, beat_price)

                # Увеличеть количество купленых битов на аккаунте
                db_handler.get_beat(chat_id)
                                
                # Обнулить выбранные пользователем параметры бита
                reset_chosen_params(chat_id)
                # Удалить processing для пользователя
                db_handler.del_processing(chat_id)
                # Удалить beats_generating для пользователя
                db_handler.del_beats_generating(chat_id)
                # Удалить chosen_extension для пользователя
                db_handler.del_chosen_extension(chat_id)

    except Exception as e:
        print(repr(e))
        # Обнулить выбранные пользователем параметры бита
        reset_chosen_params(call.message.chat.id)
        # Удалить processing для пользователя
        db_handler.del_processing(chat_id)
        # Удалить beats_generating для пользователя
        db_handler.del_beats_generating(chat_id)
        # Удалить файлы
        for file in glob(f'output_beats/{call.message.chat.id}_[1-{beats}].*'):
            remove(file)
            
        error_markup = Keyboa(items=[UNDO_BUTTON], items_in_row=3)
        bot.send_message(call.message.chat.id, '⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.', reply_markup=error_markup())

bot.polling()
     




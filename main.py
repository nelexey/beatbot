import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

# Инструмент для выборки путей к файлам
from glob import glob
# Файл данных
import config
# Файл для безопасного запуска бота
import launch
# Файл оверлеев битов
# import make_beat
# Файл обработчика запросов к БД
import db_handler
# Клавиатура
import keyboards
# Для конфигурирования и создания платежа
from yookassa import Configuration,Payment 

import itertools
from os import remove
import json

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# Подключение Юкассы
Configuration.account_id = config.SHOP_ID
Configuration.secret_key = config.SHOP_API_TOKEN

# Цена бита
beat_price = config.beat_price # RUB

# Начальный баланс пользователя при добавлении в БД
start_balance = config.start_balance # RUB

# Количество битов для создания
beats = config.beats

# Безопасный запуск
async def safe_launch():
    if launch.mailing_list is not None:
        try:
            for chat_id in launch.mailing_list:
                beat_keyboard = InlineKeyboardMarkup().add(keyboards.btn_generate_beat)
                await bot.send_message(chat_id, 'Сожалею, но во время создания твоих битов бот перезапустился 😵‍💫\n\nЭто происходит очень редко, но необходимо для стабильной работы бота. Деньги за транзакцию не сняты.\n\nТы можешь заказать бит еще раз 👉', reply_markup=beat_keyboard)         
            for chat_id in launch.chat_ids_by_messages_to_del_ids:
                messages_ids = db_handler.get_beats_versions_messages_ids(chat_id).split(', ')
                for mes_id in messages_ids:
                    await bot.delete_message(chat_id, mes_id)
                db_handler.del_beats_versions_messages_ids(chat_id)
        except:
            db_handler.del_beats_versions_messages_ids(chat_id)

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_hello(message: types.Message):
    # Отправка сообщения
    await bot.send_message(message.chat.id, text='Привет! 👋\n\nЯ телеграм-бот, который поможет тебе создать качественные 🎧 биты в разных стилях.\n\nМоя главная особенность - доступная 💰 цена и большой выбор стилей. Ты можешь выбрать любой стиль, который тебе нравится, и я создам для тебя уникальный бит.\n\nНе упусти возможность создать свой собственный звук и выделиться на фоне других исполнителей! 🎶\n\nЧтобы начать, используй команду\n/menu')
# Обработка команды /menu
@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    # Отправка сообщения

    await bot.send_message(message.chat.id, text="🎶 Это меню заказа битов 🎶\n\nОсновное предназначение бота - писать качественные биты за доступную цену, отправь эту команду в чат, чтобы получить примеры битов, созданных ботом 👉\n/example_beats.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=keyboards.menu_keyboard)
    # Добавление в БД
    # Имя и фамилия пользователя
    user_initials = f'{message.from_user.first_name} {message.from_user.last_name}'
    # Если пользователь уже добавлен то повторная запись не произойдет
    db_handler.add_user(message.chat.username, message.chat.id, user_initials, start_balance)

# Обработка команды /example_beats
got_example_beats = {}
@dp.message_handler(commands=['example_beats'])
async def menu(message: types.Message):
    
    if db_handler.get_beats_generating(message.chat.id) == 0:
        if got_example_beats.get(message.chat.id) is None:
            # Отправка сообщения
            await bot.send_message(message.chat.id, "Конечно! Вот несколько примеров готовых битов 💾\nНе сомневайся, бот сделает такие же и тебе!")
            for file_path in glob('example_beats/*.wav'):
                example_beat = open(file_path, 'rb')
                # Отправка аудио
                await bot.send_audio(message.chat.id, example_beat)
                example_beat.close()
            got_example_beats[message.chat.id] = True
        else:
            # Отправка сообщения
            beat_keyboard = InlineKeyboardMarkup().add(keyboards.btn_generate_beat)
            await bot.send_message(message.chat.id, "Тебе уже отправлены примеры битов 😵‍💫\n\nЕсли хочешь ещё, бот может сгенерировать тебе собственный бит 😉", reply_markup=beat_keyboard)
    else:
        # Отправка оповещения
        pass

## Обработка текста

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, 'Я не воспринимаю текстовые команды\n\nВызвать меню можно по команде /menu или нажав на кнопку в нижнем левом углу экрана.')


## Обработка кнопок

# Обработка кнопок интерфейса
async def get_user(chat_id):
    if db_handler.get_user(chat_id) == False:
        # Отправка сообщения
        await bot.send_message(chat_id, 'Нужно перезапустить бота командой /start')
        return False
    else:
        return True

async def reset_chosen_params(chat_id: int) -> None:
    db_handler.del_chosen_bpm(chat_id)
    db_handler.del_chosen_style(chat_id)

@dp.callback_query_handler(lambda c: c.data in keyboards.STYLES_BUTTON)
async def return_to_styles(c: types.CallbackQuery):
    chat_id = c.message.chat.id
    if await get_user(chat_id):
        # Проверить, не находится ли пользователь в beats_generating
        if db_handler.get_beats_generating(chat_id) == 0:
            # Проверить, не находится ли пользователь в processing
            if db_handler.get_processing(chat_id) == 0:
                # Установить processing для пользователя
                db_handler.set_processing(chat_id)

                # Обнулить выбранные пользователем параметры бита
                await reset_chosen_params(chat_id)
                
                # Отправка сообщения
                await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text='🎵 Генерация бита 🎵\n\n🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=keyboards.styles_keyboard)
                
                # Удалить processing для пользователя
                db_handler.del_processing(chat_id)
        else:
            # Отправка оповещения
            await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

@dp.callback_query_handler(lambda c: c.data in keyboards.UNDO_BUTTON or c.data in keyboards.MENU_BUTTON)
async def return_to_menu(c: types.CallbackQuery):
    chat_id = c.message.chat.id
    if await get_user(chat_id):
        # Обнулить выбранные пользователем параметры бита
        await reset_chosen_params(chat_id)
        # Отправка сообщения
        await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text="🎶 Это меню заказа битов 🎶\n\nОсновное предназначение бота - писать качественные биты за доступную цену, отправь эту команду в чат, чтобы получить примеры битов, созданных ботом 👉\n/example_beats.\n\n🎵 Нажми на кнопку 'Заказать бит' и выбери стиль\n\n👉 Чтобы начать, нажми на одну из кнопок ниже:", reply_markup=keyboards.menu_keyboard)

@dp.callback_query_handler(lambda c: c.data in keyboards.MENU_BUTTONS)
async def show_menu(c: types.CallbackQuery):
    try:  
        chat_id = c.message.chat.id
        pressed_button = c.data

        if await get_user(chat_id):
            if pressed_button == keyboards.BUTTON_GENERATE_BEAT:
                # Проверить, не находится ли пользователь в beats_generating
                if db_handler.get_beats_generating(chat_id) == 0:
                    # Проверить, не находится ли пользователь в processing
                    if db_handler.get_processing(chat_id) == 0:
                        # Установить processing для пользователя
                        db_handler.set_processing(chat_id)

                        # Обнулить выбранные пользователем параметры бита
                        await reset_chosen_params(c.message.chat.id)

                        # Отправка сообщения
                        await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text='🎵 Генерация бита 🎵\n\n🔥 Выбери стиль, в котором я сгенерирую бит:', reply_markup=keyboards.styles_keyboard)
                        
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                else:
                    # Отправка оповещения
                    await bot.answer_callback_query(callback_query_id=c.id, text='Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

            elif pressed_button == keyboards.BUTTON_BALANCE:
                # Запрос баланса пользователя в таблице users
                balance = db_handler.get_balance(chat_id)
                # Отправка сообщения
                await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f'💰 Баланс\n\nНа твоем балансе: *{balance}₽*\n\n👉 Выбери сумму для пополнения:', reply_markup=keyboards.balance_keyboard, parse_mode='Markdown')

            elif pressed_button == keyboards.BUTTON_ABOUT:
                # Отправка сообщения
                await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f'🏡 О нас\n\n📌 Услугу предоставляет:\n\n👤 ИНН: 910821614530\n\n✉️Почта для связи:\ntech.beatbot@mail.ru\n\n🌍Официальный сайт:\nhttps://beatmaker.site', reply_markup=keyboards.undo_keyboard)
            
    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(c.message.chat.id)

# Создает платёж
async def payment(value,description):
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
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Перед запуском асинхронной функции создается пара ключ значение user: value.
# Это сделано для того, чтобы не создавать лишние ссылки и не запускать лишние асинхронные функции, для экономии ресурсов
users_payment_transactions = {}

# Асинхронная функция проверки статуса платежа
async def check_payment(payment_id, c):
    payment = json.loads((Payment.find_one(payment_id)).json())
    
    db_handler.set_payment_checking(c.message.chat.id)

    # Удаление пары ключ значение user: value.
    def del_user_payment_transactions(chat_id, value):
        users_payment_transactions[chat_id].remove(value)

    while payment['status'] == 'pending':
        payment = json.loads((Payment.find_one(payment_id)).json())
        await asyncio.sleep(3)

    if payment['status']=='succeeded':
        print("SUCCSESS RETURN")
        db_handler.top_balance(c.message.chat.id, c.data.split('₽')[0])
        
        await bot.send_message(c.message.chat.id, f'💵 Твой баланс пополнен на {c.data}', reply_markup=keyboards.to_menu_keyboard)
        # Удалить payment_checking для пользователя
        db_handler.del_payment_checking(c.message.chat.id)

        del_user_payment_transactions(c.message.chat.id, c.data)
        return True
    else:
        print("BAD RETURN")
        # await bot.send_message(c.message.chat.id, 'Время ожидания на оплату по ссылке истекло.')
        # Удалить payment_checking для пользователя
        db_handler.del_payment_checking(c.message.chat.id)

        del_user_payment_transactions(c.message.chat.id, c.data)
        return False

@dp.callback_query_handler(lambda c: c.data in keyboards.BALANCE_BUTTONS)
async def prepare_payment(c: types.CallbackQuery):
    try:

        chat_id = c.message.chat.id

        if await get_user(chat_id):
            # Проверить, не находится ли пользователь в beats_generating
            if db_handler.get_beats_generating(chat_id) == 0:
                # Проверить, не находится ли пользователь в processing
                if db_handler.get_processing(chat_id) == 0:
                    # Установить processing для пользователя
                    db_handler.set_processing(chat_id)

                    # Получение цены из callback_data
                    price = int(c.data.split('₽')[0])

                    print(users_payment_transactions)

                    if users_payment_transactions.get(chat_id) is not None and c.data in users_payment_transactions[chat_id]:
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                        return await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Вам уже сгенерирована ссылка на эту сумму для оплаты, пожалуйста оплатите по ней.', show_alert=True)
                                
                    # Добавление транзакции оплаты пользователя
                    if users_payment_transactions.get(chat_id) is None:
                        users_payment_transactions[chat_id] = []
                    users_payment_transactions[chat_id].append(c.data)

                    # Отправка счета пользователю
                    payment_data = await payment(price, f'Пополнение баланса на {price}₽')
                    payment_id = payment_data['id']
                    confirmation_url = payment_data['confirmation']['confirmation_url'] 
                    # Создаем объект кнопки
                    btn = types.InlineKeyboardButton(f'Оплатить {price}₽', url=confirmation_url)
                    # Создаем объект клавиатуры и добавляем на нее кнопку
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(btn)
                    await bot.send_message(c.message.chat.id, f'💳 Нажмите на ссылку под сообщением, оплатите удобным вам способом.\n\n💾 Идентификатор чата - *{c.message.chat.id}*\nУслугу предоставляет: ИНН: 910821614530\n\n🎟️ Заказывая услугу, вы соглашаетесь с договором оферты: https://beatmaker.site/offer\n\n✉️ Техническая поддержка: *tech.beatbot@mail.ru*', reply_markup=keyboard, parse_mode='Markdown')
                    # Удалить processing для пользователя
                    db_handler.del_processing(chat_id)
                    await check_payment(payment_id, c)
            else:
                # Отправка оповещения
                await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Ты не можешь пополнить баланс во время генерации бита.', show_alert=True)
    except Exception as e:   
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(c.message.chat.id) 
@dp.callback_query_handler(lambda c: c.data in keyboards.STYLES_BUTTONS)
async def show_bpm(c: types.CallbackQuery):
    try:
        chat_id = c.message.chat.id
        user_chosen_style = c.data

        if await get_user(chat_id):     
            # Проверить, не находится ли пользователь в beats_generating
            if db_handler.get_beats_generating(chat_id) == 0:
                # Проверить, не находится ли пользователь в processing
                if db_handler.get_processing(chat_id) == 0:
                    if db_handler.get_chosen_style(chat_id) == '':
                        # Установить processing для пользователя
                        db_handler.set_processing(chat_id)

                        db_handler.set_chosen_style(chat_id, user_chosen_style)

                        # Отправка сообщения
                        btn_bpm1 = InlineKeyboardButton(keyboards.BPM_BUTTONS[user_chosen_style][0], callback_data=keyboards.BPM_BUTTONS[user_chosen_style][0])
                        btn_bpm2 = InlineKeyboardButton(keyboards.BPM_BUTTONS[user_chosen_style][1], callback_data=keyboards.BPM_BUTTONS[user_chosen_style][1])
                        btn_bpm3 = InlineKeyboardButton(keyboards.BPM_BUTTONS[user_chosen_style][2], callback_data=keyboards.BPM_BUTTONS[user_chosen_style][2])
                        btn_to_styles = keyboards.btn_to_styles
                        bpm_keyboard = InlineKeyboardMarkup(row_width=3).add(btn_bpm1, btn_bpm2, btn_bpm3, btn_to_styles)
                        
                        await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text=f'*{c.data}* - отличный выбор! Теперь выбери темп:\n\n*{keyboards.BPM_BUTTONS[user_chosen_style][0]}* - замедлено\n*{keyboards.BPM_BUTTONS[user_chosen_style][1]}* - нормально\n*{keyboards.BPM_BUTTONS[user_chosen_style][2]}* - ускорено', reply_markup=bpm_keyboard, parse_mode='Markdown') 
                        
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                    else:
                        await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text=f'⚠️ Похоже, что ты уже выбрал другой стиль в другом сообщении, закончи выбор параметров твоего бита там же\n\n...или начни новый выбор параметров здесь 👉', reply_markup=keyboards.to_styles_keyboard, parse_mode='Markdown')

            else:
                # Отправка оповещения
                await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(c.message.chat.id)

@dp.callback_query_handler(lambda c: c.data in list(itertools.chain(*keyboards.BPM_BUTTONS.values())))
async def show_extensions(c: types.CallbackQuery):
    try:
        
        chat_id = c.message.chat.id
        user_chosen_bpm = c.data

        if await get_user(chat_id):     
            # Проверить, не находится ли пользователь в beats_generating
            if db_handler.get_beats_generating(chat_id) == 0:
                # Проверить, не находится ли пользователь в processing
                if db_handler.get_processing(chat_id) == 0:
                    user_chosen_style = db_handler.get_chosen_style(chat_id)
                    # Проверить, есть ли в базе выбранный пользователем стиль
                    if  user_chosen_style != '':
                        # Установить processing для пользователя
                        db_handler.set_processing(chat_id)

                        if user_chosen_bpm in keyboards.BPM_BUTTONS[user_chosen_style]:

                            db_handler.set_chosen_bpm(chat_id, user_chosen_bpm)
                            # Отправка сообщения
                            await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text=f'В каком формате скинуть финальный бит?\n\n*.wav* - оригинальное качество, используется профессионалами для записи. (Не воспроизводится на iphone)\n\n*.mp3* - более низкое качество, значительно меньше весит, не подходит для профессиональной записи.\n\nПосле выбора формата начнётся генерация битов', reply_markup=keyboards.extensions_keyboard, parse_mode='Markdown')       
                        else:
                            # Отправка оповещения
                            await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Ты не можешь выбрать этот bpm для этого стиля, выбери из вышеприведённых', show_alert=True)
                        # Удалить processing для пользователя
                        db_handler.del_processing(chat_id)
                    else:
                        # Отправка сообщения
                        await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text=f'⚠️ Не удалось выбрать bpm, пожалуйста выбери стиль ещё раз', reply_markup=keyboards.to_styles_keyboard, parse_mode='Markdown')
            else:
                # Отправка оповещения
                await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.set_processing(c.message.chat.id)

# Сообщение для редактирования
message_to_edit = {}

async def check_response(chat_id, message_id):
    order_number = 0

    while True:
        beats_files = sorted(glob(f'output_beats/{chat_id}_[1-{beats}].*'))
        beats_shorts_files = sorted(glob(f'output_beats/{chat_id}_[1-{beats}]_short.*'))
        
        print(beats_shorts_files)
        if len(beats_files)==beats and len(beats_shorts_files)==beats:
            return True
        
        new_order_number = db_handler.get_query_by_chat_id(chat_id)
        if new_order_number != order_number:
            order_number = new_order_number
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'💽 Создаю версии битов, это может занять несколько минут...\n\nТвоё место в очереди: *{order_number}*\n\n🔽Версии появятся внизу🔽', parse_mode='Markdown')  

        await asyncio.sleep(2*order_number)
            
@dp.callback_query_handler(lambda c: c.data in keyboards.EXTENSIONS_BUTTONS)
async def make_query(c: types.CallbackQuery):
    try:
        chat_id = c.message.chat.id
        user_chosen_extension = c.data

        if await get_user(chat_id):     
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

                            message = await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='💽 Создаю версии битов, это может занять несколько минут...\n\n🔽Версии появятся внизу🔽')
                            message_to_edit[chat_id] = message.message_id

                            # Удалить файлы
                            for file in glob(f'output_beats/{chat_id}_[1-{beats}]*.*'):
                                remove(file)
                                                        
                            # Добавить в очередь 
                            db_handler.set_query(chat_id, db_handler.get_chosen_style(chat_id), db_handler.get_chosen_bpm(chat_id), db_handler.get_chosen_extension(chat_id).split('.')[-1])
                            
                            if await check_response(chat_id, message_to_edit[chat_id]):
                                files_list = sorted(glob(f'output_beats/{chat_id}_[1-{beats}]_short.*'))

                                messages_ids = []

                                await bot.delete_message(chat_id=chat_id, message_id=c.message.message_id)

                                message = await bot.send_message(chat_id=chat_id, text=f'✅ Вот 3 демо-версии битов, выбери ту, которая понравилась, и я скину полную версию:\n\nСтиль - *{user_chosen_style}* Темп - *{user_chosen_bpm}*', parse_mode='Markdown')
                                message_to_edit[chat_id] = message.message_id

                                for file_path in files_list:
                                    with open(file_path, 'rb') as trimmed_sound:
                                        if files_list.index(file_path) == len(files_list)-1:
                                            message = await bot.send_audio(c.message.chat.id, trimmed_sound, reply_markup=keyboards.beats_keyboard)
                                            messages_ids.append(message.message_id)
                                            db_handler.set_beats_versions_messages_ids(c.message.chat.id, ', '.join(str(messages_id) for messages_id in messages_ids))
                                            trimmed_sound.close()
                                            for file in files_list:         
                                                remove(file)
                                            del messages_ids
                                            
                                        else:
                                            message = await bot.send_audio(c.message.chat.id, trimmed_sound)
                                            messages_ids.append(message.message_id)
                                # Удалить processing для пользователя
                                db_handler.del_processing(chat_id)
                        else:
                            # Отправка сообщения
                            await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text=f'⚠️ Не удалось выбрать расширение, попробуй ещё раз. Выбрать параметры бита нужно строго в предлагаемом ботом порядке и в одном окне', reply_markup=keyboards.to_styles_keyboard, parse_mode='Markdown')
                    else:
                        balance_keyboard = InlineKeyboardMarkup().add(keyboards.btn_balance)
                        await bot.edit_message_text(chat_id=chat_id, message_id=c.message.message_id, text=f'⚠️ Сперва тебе нужно пополнить баланс', reply_markup=balance_keyboard, parse_mode='Markdown')

                # Удалить processing для пользователя
                db_handler.del_processing(chat_id)
            else:
                # Отправка оповещения
                await bot.answer_callback_query(callback_query_id=c.id, text='⚠️ Ты не можешь заказать еще один бит во время осуществления текущего заказа.', show_alert=True)

    except Exception as e:
        print(repr(e))
        # Удалить processing для пользователя
        db_handler.del_processing(c.message.chat.id)
        # Удалить beats_generating для пользователя
        db_handler.del_beats_generating(c.message.chat.id)
        # Удалить файлы 
        for file in glob(f'output_beats/{c.message.chat.id}_[1-{beats}]*.*'):
            remove(file)
            
        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=f'⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.', reply_markup=keyboards.undo_keyboard)

@dp.callback_query_handler(lambda c: c.data in keyboards.BEATS_BUTTONS)
async def send_beat(c: types.CallbackQuery):
    try:  
        chat_id = c.message.chat.id
        pressed_button = c.data

        if await get_user(chat_id):
            
            # Проверить, не находится ли пользователь в processing
            if db_handler.get_processing(chat_id) == 0:
                # Установить processing для пользователя
                db_handler.set_processing(chat_id)

                message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit[chat_id], text='📤 Скидываю полную версию... 📤')
                message_to_edit[chat_id] = message.message_id

                # Удалить примеры битов
                messages_to_delete_ids = db_handler.get_beats_versions_messages_ids(chat_id)
                if messages_to_delete_ids != '':
                    for mes_id in messages_to_delete_ids.split(', '):
                        await bot.delete_message(chat_id, mes_id)
                db_handler.del_beats_versions_messages_ids(chat_id)

                # Открыть файл
                beat = open(f'output_beats/{chat_id}_{pressed_button}.{db_handler.get_chosen_extension(chat_id).split(".")[-1]}', 'rb')

                # Скинуть файл
                await bot.send_audio(chat_id, beat)
                
                # Закрыть файл
                beat.close()
        
                # Отправка сообщения
                message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit[chat_id], text='🔽 Держи 🔽')
                message_to_edit[chat_id] = message.message_id
                await bot.send_message(chat_id, f'С твоего баланса снято *{beat_price}₽*\nНадеюсь, тебе понравится бит 😉', reply_markup=keyboards.to_menu_keyboard, parse_mode='Markdown')                        
                
                # Удалить файлы
                for file in glob(f'output_beats/{chat_id}_[1-{beats}]*.*'):
                    remove(file)

                # Снять деньги
                db_handler.pay(chat_id, beat_price)

                # Увеличеть количество купленых битов на аккаунте
                db_handler.get_beat(chat_id)
                                
                # Обнулить выбранные пользователем параметры бита
                await reset_chosen_params(chat_id)
                # Удалить processing для пользователя
                db_handler.del_processing(chat_id)
                # Удалить beats_generating для пользователя
                db_handler.del_beats_generating(chat_id)
                # Удалить chosen_extension для пользователя
                db_handler.del_chosen_extension(chat_id)

    except Exception as e:
        print(repr(e))
        # Обнулить выбранные пользователем параметры бита
        await reset_chosen_params(c.message.chat.id)
        # Удалить processing для пользователя
        db_handler.del_processing(c.message.chat.id)
        # Удалить beats_generating для пользователя
        db_handler.del_beats_generating(c.message.chat.id)
        # Удалить файлы
        for file in glob(f'output_beats/{c.message.chat.id}_[1-{beats}].*'):
            remove(file)
            
        await bot.send_message(c.message.chat.id, '⚠️ Не удалось отправить бит, деньги за транзакцию не сняты. Попробуйте ещё раз.', reply_markup=keyboards.undo_keyboard)

# Запуск бота
if __name__ == '__main__':
    executor.start(dp, safe_launch())
    executor.start_polling(dp, skip_updates=True)
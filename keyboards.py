from config import beats, beat_price
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Инициализация кнопок
# Кнопки меню
BUTTON_GENERATE_BEAT = f'🎙️ Бит под запись 🎙️'
BUTTON_BALANCE = '💰 Баланс'
BUTTON_ABOUT = '🏡 О нас'
BUTTON_TUTORIAL = '🎥 Что умеет Битбот?'

MENU_BUTTONS = [BUTTON_BALANCE, BUTTON_ABOUT, BUTTON_GENERATE_BEAT, BUTTON_TUTORIAL]

# Кнопки баланса

PREMIUM_BUTTON = 'Безлимит на месяц - 49₽'
BALANCE_BUTTONS = ['180₽', '360₽', '540₽']

# Кнопки расширения
BUTTON_MP3 = '.mp3'
BUTTON_WAV = '.wav'

EXTENSIONS_BUTTONS = [BUTTON_WAV,
                      BUTTON_MP3]

# Кнопки интерфейса
UNDO_BUTTON = '⬅️ Назад'
MENU_BUTTON = '⬅️ В меню'
STYLES_BUTTON = '⬅️ К стилям'

# Кнопки стилей
# Ключи - названия стилей на кнопках, значения - названия папок style_*
aliases = {
    'Jersey Club':'JC',
    'Trap':       'Trap',
    'Drill':      'Drill',
    'Plug':       'Plug',
    'Old School': 'OldSchool',
    'Opium':      'Opium',
    'NewJazz':    'NewJazz'
}

options = {
    'Speed UP':   'speed_up',
    'Slowed+RVB': 'slow_down',
    'Remove Vocal': 'remove_vocal',
    'Улучшение звука': 'normalize_sound',
    'Опр. тональность': 'key_finder',
    'Опр. темп': 'bpm_finder',
    'BASSBOOST': 'bass_boost'
}


# Бесплатные опции
BUTTON_CATEGORY_FREE_OPTIONS = '🆓 Бесплатные опции'
CATEGORIES_BUTTONS = [BUTTON_CATEGORY_FREE_OPTIONS]

OPTIONS_BUTTONS = [key for key in options.keys()]

STYLES_BUTTONS = [key for key in aliases.keys()]

# Кнопки битов
BEATS_BUTTONS = [str(i) for i in range(1, beats+1)]

GET_EXAMPLE_BEAT = '📝 Пример бита'

# Кнопки темпов
# Для каждого стиля свои кнопки bpm
BPM_BUTTONS = {'Jersey Club': ['140bpm', '150bpm', '160bpm'],
               'Trap':        ['110bpm', '130bpm', '145bpm'],
               'Drill':       ['110bpm', '130bpm', '145bpm'],
               'Plug':        ['140bpm', '150bpm', '160bpm'],
               'Old School':  ['155bpm', '170bpm', '185bpm'],
               'Opium':       ['140bpm', '150bpm', '160bpm'],
               'NewJazz':     ['110bpm', '130bpm', '145bpm']}

BPM_BUTTONS_CONTROLLER = {'up':   ['+1', '+5', '+10'],
                          'down': ['-1', '-5', '-10']}

BPM_CONFIRM = 'BPM_CONFIRM'

# Кнопки ладов
KEY_BUTTONS = ['minor',
               'major']

# Клавиатура меню
btn_balance = InlineKeyboardButton(BUTTON_BALANCE, callback_data=BUTTON_BALANCE)
btn_about = InlineKeyboardButton(BUTTON_ABOUT, callback_data=BUTTON_ABOUT)
btn_generate_beat = InlineKeyboardButton(BUTTON_GENERATE_BEAT, callback_data=BUTTON_GENERATE_BEAT)
btn_free_options = InlineKeyboardButton(CATEGORIES_BUTTONS[0], callback_data=CATEGORIES_BUTTONS[0])
btn_tutorial =  InlineKeyboardButton(BUTTON_TUTORIAL, callback_data=BUTTON_TUTORIAL)
menu_keyboard = InlineKeyboardMarkup(row_width=2)
menu_keyboard.add(btn_balance, btn_about)
menu_keyboard.row(btn_generate_beat)
menu_keyboard.row(btn_free_options)
menu_keyboard.row(btn_tutorial)

# Клавиатура "назад"
btn_undo = InlineKeyboardButton(UNDO_BUTTON, callback_data=UNDO_BUTTON)
undo_keyboard = InlineKeyboardMarkup().add(btn_undo)

# Клавиатура "в меню"
btn_menu = InlineKeyboardButton(MENU_BUTTON, callback_data=MENU_BUTTON)
to_menu_keyboard = InlineKeyboardMarkup().add(btn_menu)

# Клавиатура "к стилям"
btn_to_styles = InlineKeyboardButton(STYLES_BUTTON, callback_data=STYLES_BUTTON)
to_styles_keyboard = InlineKeyboardMarkup().add(btn_to_styles)

# Клавиатура "Бесплатные опции"
btn_speed_up = InlineKeyboardButton(OPTIONS_BUTTONS[0], callback_data=OPTIONS_BUTTONS[0])
btn_slow_down = InlineKeyboardButton(OPTIONS_BUTTONS[1], callback_data=OPTIONS_BUTTONS[1])
btn_remove_vocal = InlineKeyboardButton(OPTIONS_BUTTONS[2], callback_data=OPTIONS_BUTTONS[2])
btn_normalize_sound = InlineKeyboardButton(OPTIONS_BUTTONS[3], callback_data=OPTIONS_BUTTONS[3])
btn_key_finder = InlineKeyboardButton(OPTIONS_BUTTONS[4], callback_data=OPTIONS_BUTTONS[4])
btn_bpm_finder = InlineKeyboardButton(OPTIONS_BUTTONS[5], callback_data=OPTIONS_BUTTONS[5])
btn_bass_boost = InlineKeyboardButton(OPTIONS_BUTTONS[6], callback_data=OPTIONS_BUTTONS[6])
free_keyboard = InlineKeyboardMarkup(row_width=2)
free_keyboard.row(btn_speed_up, btn_slow_down)
free_keyboard.row(btn_bass_boost)
free_keyboard.row(btn_remove_vocal)
free_keyboard.row(btn_key_finder, btn_bpm_finder)
free_keyboard.row(btn_normalize_sound)
free_keyboard.row(btn_undo)

# Клавиатура баланса
btn_pay1 = InlineKeyboardButton(BALANCE_BUTTONS[0], callback_data=BALANCE_BUTTONS[0])
btn_pay2 = InlineKeyboardButton(BALANCE_BUTTONS[1], callback_data=BALANCE_BUTTONS[1])
btn_pay3 = InlineKeyboardButton(BALANCE_BUTTONS[2], callback_data=BALANCE_BUTTONS[2])
btn_pay4 = InlineKeyboardButton(PREMIUM_BUTTON, callback_data=PREMIUM_BUTTON)
balance_keyboard = InlineKeyboardMarkup(row_width=3)
balance_keyboard.add(btn_pay1, btn_pay2, btn_pay3)
balance_keyboard.row(btn_pay4)
balance_keyboard.row(btn_undo)

# Клавиатура стилей
btn_jc = InlineKeyboardButton(STYLES_BUTTONS[0], callback_data=STYLES_BUTTONS[0])
btn_trap = InlineKeyboardButton(STYLES_BUTTONS[1], callback_data=STYLES_BUTTONS[1])
btn_drill= InlineKeyboardButton(STYLES_BUTTONS[2], callback_data=STYLES_BUTTONS[2])
btn_plug = InlineKeyboardButton(STYLES_BUTTONS[3], callback_data=STYLES_BUTTONS[3])
btn_oldshcool = InlineKeyboardButton(STYLES_BUTTONS[4], callback_data=STYLES_BUTTONS[4])
btn_opium = InlineKeyboardButton(STYLES_BUTTONS[5], callback_data=STYLES_BUTTONS[5])
btn_newjazz = InlineKeyboardButton(STYLES_BUTTONS[6], callback_data=STYLES_BUTTONS[6])
styles_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_jc, btn_trap, btn_drill, btn_plug, btn_oldshcool, btn_opium, btn_newjazz, btn_undo)

# Клавиатура bpm

## *Создаётся непосредственно в боте*

btn_confirm_bpm = InlineKeyboardButton('Подтвердить', callback_data=BPM_CONFIRM)
btn_down_10 = InlineKeyboardButton(BPM_BUTTONS_CONTROLLER['down'][2], callback_data=BPM_BUTTONS_CONTROLLER['down'][2])
btn_down_5 = InlineKeyboardButton(BPM_BUTTONS_CONTROLLER['down'][1], callback_data=BPM_BUTTONS_CONTROLLER['down'][1])
btn_down_1 = InlineKeyboardButton(BPM_BUTTONS_CONTROLLER['down'][0], callback_data=BPM_BUTTONS_CONTROLLER['down'][0])
btn_up_1 = InlineKeyboardButton(BPM_BUTTONS_CONTROLLER['up'][0], callback_data=BPM_BUTTONS_CONTROLLER['up'][0])
btn_up_5 = InlineKeyboardButton(BPM_BUTTONS_CONTROLLER['up'][1], callback_data=BPM_BUTTONS_CONTROLLER['up'][1])
btn_up_10 = InlineKeyboardButton(BPM_BUTTONS_CONTROLLER['up'][2], callback_data=BPM_BUTTONS_CONTROLLER['up'][2])
btn_example_beat = InlineKeyboardButton(GET_EXAMPLE_BEAT, callback_data=GET_EXAMPLE_BEAT)

bpm_keyboard = InlineKeyboardMarkup(row_width=2)
bpm_keyboard.add(btn_confirm_bpm)
bpm_keyboard.row(btn_down_10, btn_down_5, btn_down_1, btn_up_1, btn_up_5, btn_up_10)
bpm_keyboard.row(btn_example_beat, btn_to_styles)

# Клавиатура ладов 
btn_major = InlineKeyboardButton(f'🌕 {KEY_BUTTONS[1]}', callback_data=KEY_BUTTONS[1])
btn_minor = InlineKeyboardButton(f'🌑 {KEY_BUTTONS[0]}', callback_data=KEY_BUTTONS[0])
keys_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_major, btn_minor, btn_to_styles)

# Клавиатура расширений 
btn_wav = InlineKeyboardButton(EXTENSIONS_BUTTONS[0], callback_data=EXTENSIONS_BUTTONS[0])
btn_mp3 = InlineKeyboardButton(EXTENSIONS_BUTTONS[1], callback_data=EXTENSIONS_BUTTONS[1])
extensions_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_wav, btn_mp3, btn_to_styles)

# Клавиатура версий битов
btn_beat1 = InlineKeyboardButton(BEATS_BUTTONS[0], callback_data=BEATS_BUTTONS[0])
btn_beat2 = InlineKeyboardButton(BEATS_BUTTONS[1], callback_data=BEATS_BUTTONS[1])
btn_beat3 = InlineKeyboardButton(BEATS_BUTTONS[2], callback_data=BEATS_BUTTONS[2])

beats_keyboard = InlineKeyboardMarkup(row_width=3).add(btn_beat1, btn_beat2, btn_beat3)
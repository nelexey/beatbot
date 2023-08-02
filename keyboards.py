from config import beats, beat_price
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Инициализация кнопок
# Кнопки меню
BUTTON_GENERATE_BEAT = f'🎙️ Бит под запись 🎙️'
BUTTON_BALANCE = '💰 Баланс'
BUTTON_ABOUT = '🏡 О нас'

MENU_BUTTONS = [BUTTON_BALANCE, BUTTON_ABOUT, BUTTON_GENERATE_BEAT]

# Кнопки баланса

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
    'Old School': 'OldSchool'
}

STYLES_BUTTONS = [key for key in aliases.keys()]

# Кнопки битов
BEATS_BUTTONS = [str(i) for i in range(1, beats+1)]

GET_EXAMPLE_BEAT = 'Пример бита'

# Кнопки темпов
# Для каждого стиля свои кнопки bpm
BPM_BUTTONS = {'Jersey Club': ['140bpm', '150bpm', '160bpm'],
               'Trap':        ['110bpm', '130bpm', '145bpm'],
               'Drill':       ['110bpm', '130bpm', '145bpm'],
               'Plug':        ['140bpm', '150bpm', '160bpm'],
               'Old School':  ['155bpm', '170bpm', '185bpm']}

# Клавиатура меню
btn_balance = InlineKeyboardButton(BUTTON_BALANCE, callback_data=BUTTON_BALANCE)
btn_about = InlineKeyboardButton(BUTTON_ABOUT, callback_data=BUTTON_ABOUT)
btn_generate_beat = InlineKeyboardButton(BUTTON_GENERATE_BEAT, callback_data=BUTTON_GENERATE_BEAT)
menu_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_balance, btn_about, btn_generate_beat)

# Клавиатура "назад"
btn_undo = InlineKeyboardButton(UNDO_BUTTON, callback_data=UNDO_BUTTON)
undo_keyboard = InlineKeyboardMarkup().add(btn_undo)

# Клавиатура "в меню"
btn_menu = InlineKeyboardButton(MENU_BUTTON, callback_data=MENU_BUTTON)
to_menu_keyboard = InlineKeyboardMarkup().add(btn_menu)

# Клавиатура "к стилям"
btn_to_styles = InlineKeyboardButton(STYLES_BUTTON, callback_data=STYLES_BUTTON)
to_styles_keyboard = InlineKeyboardMarkup().add(btn_to_styles)

# Клавиатура баланса
btn_pay1 = InlineKeyboardButton(BALANCE_BUTTONS[0], callback_data=BALANCE_BUTTONS[0])
btn_pay2 = InlineKeyboardButton(BALANCE_BUTTONS[1], callback_data=BALANCE_BUTTONS[1])
btn_pay3 = InlineKeyboardButton(BALANCE_BUTTONS[2], callback_data=BALANCE_BUTTONS[2])
balance_keyboard = InlineKeyboardMarkup(row_width=3).add(btn_pay1, btn_pay2, btn_pay3, btn_undo)

# Клавиатура стилей
btn_jc = InlineKeyboardButton(STYLES_BUTTONS[0], callback_data=STYLES_BUTTONS[0])
btn_trap = InlineKeyboardButton(STYLES_BUTTONS[1], callback_data=STYLES_BUTTONS[1])
btn_drill= InlineKeyboardButton(STYLES_BUTTONS[2], callback_data=STYLES_BUTTONS[2])
btn_plug = InlineKeyboardButton(STYLES_BUTTONS[3], callback_data=STYLES_BUTTONS[3])
btn_oldshcool = InlineKeyboardButton(STYLES_BUTTONS[4], callback_data=STYLES_BUTTONS[4])
styles_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_jc, btn_trap, btn_drill, btn_plug, btn_oldshcool, btn_undo)

# Клавиатура bpm

## *Создаётся непосредственно в боте*

# Клавиатура расширений 
btn_wav = InlineKeyboardButton(EXTENSIONS_BUTTONS[0], callback_data=EXTENSIONS_BUTTONS[0])
btn_mp3 = InlineKeyboardButton(EXTENSIONS_BUTTONS[1], callback_data=EXTENSIONS_BUTTONS[1])
extensions_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_wav, btn_mp3, btn_to_styles)

# Клавиатура версий битов
btn_beat1 = InlineKeyboardButton(BEATS_BUTTONS[0], callback_data=BEATS_BUTTONS[0])
btn_beat2 = InlineKeyboardButton(BEATS_BUTTONS[1], callback_data=BEATS_BUTTONS[1])
btn_beat3 = InlineKeyboardButton(BEATS_BUTTONS[2], callback_data=BEATS_BUTTONS[2])

beats_keyboard = InlineKeyboardMarkup(row_width=3).add(btn_beat1, btn_beat2, btn_beat3)
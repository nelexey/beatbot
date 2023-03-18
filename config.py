from os import listdir

TOKEN = '5709035569:AAHYX8pc7RIBN7mzq8R_ROUGCZilUDpVE8c'

dirs = listdir()
styles = []

for dir in dirs:
    if dir.split('_')[0] == 'style':
        styles.append(dir)

aliases = {
    'Jersey Club': 'JC',
    'Trap': 'Trap',
    'Drill': 'drill',
    'Plug': 'plug',
}

styles_markup = []
for key in aliases.keys():
    styles_markup.append(key)

beat_price = 45

# кнопки

menu_buttons = ['Баланс', 'О нас', f'Заказать бит - {beat_price}₽']

balance_buttons = ['45₽', '90₽', '135₽']

navigation_buttons = ['<<Назад']

bpm_buttons = ['110bpm', '130bpm', '145bpm']

start_balance = 0

# данные PostgreSQL
host = 'localhost'
user = 'postgres'
password = '1234567890'
db_name = 'beatbotdb'
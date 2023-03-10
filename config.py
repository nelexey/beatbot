from os import listdir

TOKEN = '5709035569:AAHYX8pc7RIBN7mzq8R_ROUGCZilUDpVE8c'

dirs = listdir()
styles = []

for dir in dirs:
    if dir.split('_')[0] == 'style':
        styles.append(dir)

aliases = {
    'Jersey Club': 'JC',
    'Plug': 'Plug'
}

styles_markup = []
for key in aliases.keys():
    styles_markup.append(key)

menu_buttons = ['Баланс', 'О нас', 'Заказать бит']

balance_buttons = ['Пополнить']

navigation_buttons = ['<<Назад']

bpm_buttons = ['110bpm', '130bpm', '145bpm']
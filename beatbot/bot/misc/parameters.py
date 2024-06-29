from typing import Final

CHANNELS: Final = ['@beatbotnews']

"""Кол-во ежесуточных бесплатных опций на пользователя"""
OPTION_CREDITS: Final = 10

"""Цена бита в рублях"""
BEAT_PRICE: Final = {'platinum': 199,
                     'beatfusion': 199}

STYLES: Final = {
    'platinum': {
        'trap': ('Trap', (110, 130, 180), {'bass': True, 'harmonic': True}),
        'drill': ('Drill', (110, 130, 145), {'bass': True, 'harmonic': False}),
        'jc': ('Jersey Club', (140, 150, 160), {'bass': True, 'harmonic': False}),
        'plug': ('Plug', (140, 150, 160), {'bass': True, 'harmonic': False}),
        'old_school': ('Old School', (155, 170, 185), {'bass': True, 'harmonic': False}),
        'opium': ('Opium', (140, 150, 160), {'bass': True, 'harmonic': False}),
        'new_jazz': ('NewJazz', (110, 130, 145), {'bass': False, 'harmonic': False}),
    }
}
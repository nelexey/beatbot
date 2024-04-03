"""
    Instruments:
        main - главный инструмент трека, в треке только один вид клавного инструмента.
        drum - все остальные инструменты, может быть множество видов в одном треке.
"""

from random import choice

main_instruments = ['lead', 'piano', 'aguitar', 'eguitar']

"""
    Словарь инструментов стилей и их параметров, которые используются при создании аудиодорожек.
    'Style': {
        'instrument' - название инструмента:{
        'start': int - с какого момента накладывать семплы инструмента на тишину,
        'samples': int - количество семплов, идущих подряд,
        'silents': {
            int - номер семпла: ((момент начала тишины в %, момент конца тишины в %). (..., ...)),
        },
        }
    }
"""
style_instruments = {
    'Trap': {
            'voicetag': {'start': 0,
                      'samples': 1,
                      'silents': {
                                  }, 
                      'reverb': {
                                 }
                        },
            'lead': {'start': 0,
                      'samples': 12,
                      'silents': {
                                  }, 
                      'reverb': {'room_size': 0.85,
                                 'wet_level': 0.25
                                 }
                      },
            'piano': {'start': 0,
                      'samples': 12,
                      'silents': {
                                  },
                      'reverb': {'room_size': 0.85,
                                 'wet_level': 0.25
                                 }
                      },
            'eguitar': {'start': 0,
                      'samples': 12,
                      'silents': {
                                  },
                      'reverb': {'room_size': 0.85,
                                 'wet_level': 0.25
                                 }         
                      },
            'aguitar': {'start': 0,
                      'samples': 12,
                      'silents': {
                                  },
                      'reverb': {'room_size': 0.85,
                                 'wet_level': 0.25
                                 }
                      },
            'bass': {'start': 1,
                      'samples': 11,
                      'silents': {3: ((0, 25),),
                                  },
                      'volume': 0.6
                      },
            'kick': {'start': 1,
                      'samples': 10,
                      'silents': {3: ((0, 25),),
                                  7: ((0, 25),),
                                  },
                    #   'volume': 0.8
                      },
            'clap': {'start': 0,
                      'samples': 10,
                      'silents': {0: ((0, 87.5),),
                                  3: ((0, 12.5),),
                                  7: ((0, 12.5),),
                                  }
                      },
            'hihat': {'start': 0,
                      'samples': 10,
                      'silents': {0: ((0, 87.5),),
                                  3: ((0, 12.5),),
                                  7: ((0, 12.5),),
                                  }
                      }
            },
}
#TODO
style_instruments['Drill'] = style_instruments['Trap']
style_instruments['JC'] = style_instruments['Trap']
style_instruments['Jerk'] = style_instruments['Trap']

"""
    Эффекты над семплами.
    duration: int - длина появления и затухания звука
"""
instruments = {
    'lead': {'duration': 10},
    'piano': {'duration': 10},
    'eguitar': {'duration': 10},
    'aguitar': {'duration': 0},
    'bass': {'duration': 10},
    'kick': {'duration': 0},
    'clap': {'duration': 0},
    'hihat': {'duration': 0},
    'voicetag': {'duration': 0},
}

### Наполнение семплов стиля
def get_instruments_pack(style):
    
    style_mains = [(inst, instruments[inst]['duration']) for inst in style_instruments[style].keys() if inst in main_instruments]
    style_drums = [(inst, instruments[inst]['duration']) for inst in style_instruments[style].keys() if inst not in main_instruments]

    return [choice(style_mains)] + style_drums

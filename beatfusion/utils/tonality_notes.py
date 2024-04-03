"""Определить используемые в тональности ноты"""

from musical_scales import scale

def get_notes(tonality, lad):
    lads_intervals = {'major': 'harmonic major',
                      'minor': 'harmonic minor'}
    
    n = scale(tonality, lads_intervals[lad])
    
    notes = [str(note) for note in n]

    return notes

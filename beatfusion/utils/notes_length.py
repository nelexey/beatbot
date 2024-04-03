import random

def divide_length(lengths: list, number=128) -> list:
    #TODO !!!!!
    # CONSTANT NUMBER OF SQUARES IN ONE SAMPLE
    result = []

    restart_limit = 50

    while restart_limit>0:
        if sum(result)==number: return result

        available_lengths = []
        for l in lengths:
            if l<=number-sum(result): available_lengths.append(l) 
        
        if not available_lengths: 
            result = []
            restart_limit-=1
        else: result.append(random.choice(available_lengths))

    print('Can`t more restart')
    return
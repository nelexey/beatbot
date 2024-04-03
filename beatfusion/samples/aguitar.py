from random import shuffle, choice

from .lead import Generator as Lead_Gen

class Generator:
    @staticmethod
    def generate(notes, s_length, sq_length, notes_length) -> list:
        return(Lead_Gen.generate(notes, s_length, sq_length, notes_length))
        

            

            
        


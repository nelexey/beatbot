
class MarkupException(Exception):
    """
    Исключения для части библиотеки, создающей разметку.
    """
    def __init__(self, message):
        self.message = message
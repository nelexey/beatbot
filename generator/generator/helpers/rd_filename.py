import random
import string


def generate_random_filename(k=16):
    # Generate a random filename of 16 characters
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return filename

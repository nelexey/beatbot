import os
import random
import string

def generate_unique_folder_name(dir=''):
    folder_name_template = 'beatfusion_{eight_random_chars}'
    while True:
        eight_random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        folder_name = folder_name_template.format(eight_random_chars=eight_random_chars)
        if not os.path.exists(f'{dir}/{folder_name}'):
            return folder_name
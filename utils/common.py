import random
import string
import time

def get_time_last_digit(n_digits):
    return str(int(time.time_ns()) % 10 ** n_digits).zfill(n_digits)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
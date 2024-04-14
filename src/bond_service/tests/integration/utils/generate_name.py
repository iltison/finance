import random
import string


def generate_random_name():
    length = 10
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

from random import sample
import string


def generate_code():
    data = sample(string.ascii_letters, 15)
    result = "".join(data)
    return result
import random
import string

ID_LEN = 22


def random_id():
    return ''.join(random.choices(string.digits + string.ascii_letters + string.punctuation, k=ID_LEN))

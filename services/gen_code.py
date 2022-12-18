import random
import string


def gen_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


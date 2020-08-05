import string
import random
import os
import datetime


def new_id():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for i in range(10))

import base64
import random
import string
import time

def generate_base64_token(length = 64):

    charset = string.ascii_letters + string.digits

    random_string = ''.join(random.choices(charset, k = length))

    base64_token = base64.urlsafe_b64encode(random_string.encode()).decode('utf-8')

    return str(time.time()).replace(".", "") + base64_token[:length]
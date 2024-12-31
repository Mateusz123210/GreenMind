import uuid
import time
import random

def generate_uuid():
    return str(time.time()) + str(random.randint(0, 10000)) + str(uuid.uuid4())


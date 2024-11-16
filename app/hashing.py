import hashlib
import base64

def hash_password(password: str):
    hash = hashlib.sha512()
    hash.update(b'A2rx2R6MqhD3rfkMXO1suUb3sCc5IX6KS7TeUz55pxc=')
    hash.update(password.encode("utf-8"))

    return base64.urlsafe_b64encode(hash.digest()).decode("utf-8")
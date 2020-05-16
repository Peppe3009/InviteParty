import secrets
import string
import hashlib

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'tecwebprogetto@gmail.com',
    "MAIL_PASSWORD": 'progetto97@'
}
KEY = "notSoSecret"


def stringa_random():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def codifica(stringa):
    temp = hashlib.sha224(stringa.encode())
    return temp.hexdigest()

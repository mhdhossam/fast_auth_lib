from cryptography.fernet import Fernet
from django.conf import settings

def encrypt_token(token):
    fernet = Fernet(settings.MY_AUTH_LIB['FERNET_KEY'])
    return fernet.encrypt(token.encode())

def decrypt_token(encrypted_token):
    fernet = Fernet(settings.MY_AUTH_LIB['FERNET_KEY'])
    return fernet.decrypt(encrypted_token).decode()

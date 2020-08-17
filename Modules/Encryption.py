import platform
import keyring
from cryptography.fernet import Fernet
import os


class DatabaseEncrypt(object):
    def __init__(self):
        current_os = platform.system()
        if current_os == 'Windows':
            user = os.environ.get('USERNAME')
        else:
            user = os.environ.get('USER')
        if keyring.get_password('fbdb', user) is None:
            keyring.set_password('fbdb', user, Fernet.generate_key())
        self.f = Fernet(keyring.get_password('fbdb', user))

    def encrypt(self, password):
        return self.f.encrypt(bytes(password.encode()))

    def decrypt(self, encrypted_password):
        return self.f.decrypt(encrypted_password).decode()

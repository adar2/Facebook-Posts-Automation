import keyring
from cryptography.fernet import Fernet
import os


class DatabaseEncrypt(object):
    def __init__(self):
        if keyring.get_password('fbdb', os.getlogin()) is None:
            keyring.set_password('fbdb', os.getlogin(), Fernet.generate_key())
        self.f = Fernet(keyring.get_password('fbdb', os.getlogin()))

    def encrypt(self, password):
        return self.f.encrypt(bytes(password.encode()))

    def decrypt(self, encrypted_password):
        return self.f.decrypt(encrypted_password).decode()



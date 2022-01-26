import binascii
import random
import constants as k

import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:

    def __init__(self):

        # Generador de números random
        random_crypto_number = Crypto.Random.new().read
        random_exponent = random.SystemRandom()

        # RSA necesita que el exponente sea impar
        exponent = 0
        while exponent % 2 == 0 or exponent < 3:
            exponent = random_exponent.randint(1, k.MAX_EXPONENT)

        # Construcción de la identidad del cliente
        self._private_key = RSA.generate(1024, random_crypto_number, e=exponent)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        self._address = '0x' + binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')[-40:]
        self._balance = 0
        
    # Retorna la clave pública
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    
    # Retorna el signer asociado a la identidad
    @property
    def signer(self):
        return self._signer
    
    # Retorna la address del cliente
    @property
    def address(self):
        return self._address

    # Retorna el balance del cliente
    @property
    def balance(self):
        return self._balance

    # Métodos para actualizar balance
    def add_balance(self, value):
        self._balance += value

    def sub_balance(self, value):
        self._balance -= value
import binascii
import random
import constants as k

# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:

    def __init__(self):
        exponent = 0

        random_crypto_number = Crypto.Random.new().read
        random_exponent = random.SystemRandom()

        while exponent % 2 == 0 or exponent < 3:
            exponent = random_exponent.randint(1, k.MAX_EXPONENT)

        self._private_key = RSA.generate(1024, random_crypto_number, e=exponent)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        self._address = '0x' + binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')[-40:]
        self._balance = 0
        
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    
    @property
    def signer(self):
        return self._signer
    
    @property
    def address(self):
        return self._address

    @property
    def balance(self):
        return self._balance

    def add_balance(self, value):
        self._balance += value

    def sub_balance(self, value):
        self._balance -= value
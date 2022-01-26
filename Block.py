import hashlib
import constants as keys

class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""
        self.last_block_hash = ""

    def sha256(self, message):
        return hashlib.sha256(message.encode('ascii')).hexdigest()

    # Minado
    def mine(self, message, difficulty=1):
        assert difficulty >= 1
        prefix = '0' * difficulty
        for i in range(keys.MAX_EXPONENT):
            digest = self.sha256(str(hash(message)) + str(i))
            if digest.startswith(prefix):
                print ("Después de " + str(i) + " iteraciones nonce encontrado: "+ digest)
                return digest
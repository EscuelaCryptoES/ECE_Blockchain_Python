import binascii
import datetime
import collections
from Crypto.Hash import SHA

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()
        
        # Actualización de balances
        recipient.add_balance(value)
        if sender != "Genesis":
            sender.sub_balance(value)

    # Método usado para imprimir la transacción
    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.address
        
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient.address,
            'value': self.value,
            'time' : self.time
        })

    # Firma de la transacción
    def sign_transaction(self):
        signer = self.sender.signer
        # New SHA hash
        hash = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(hash)).decode('ascii')

    # método toString 
    def display_transaction(tx):
        dict = tx.to_dict()
        print ("--------------------------------------------------------------------")
        print ("sender: " + dict['sender'])
        print ("recipient: " + dict['recipient'])
        print ("value: " + str(dict['value']))
        print ("time: " + str(dict['time']))
        print ("--------------------------------------------------------------------")
import Client

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
        
        recipient.add_balance(value)
        if sender != "Genesis":
            sender.sub_balance(value)

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

    def sign_transaction(self):
        signer = self.sender.signer
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

    def display_transaction(tx):
        dict = tx.to_dict()
        print ("sender: " + dict['sender'])
        print ("recipient: " + dict['recipient'])
        print ("value: " + str(dict['value']))
        print ("time: " + str(dict['time']))
        print ("--------------------------------------------------------------------")
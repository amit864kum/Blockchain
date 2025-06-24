import json
from ecdsa import VerifyingKey, SECP256k1

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }

    def sign(self, priv_key):
        message = json.dumps(self.to_dict(), sort_keys=True)
        self.signature = priv_key.sign(message.encode()).hex()

    def is_valid(self):
        if self.sender == "COINBASE": return True
        message = json.dumps(self.to_dict(), sort_keys=True)
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
            return vk.verify(bytes.fromhex(self.signature), message.encode())
        except:
            return False
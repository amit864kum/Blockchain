from ecdsa import SigningKey, VerifyingKey, SECP256k1

class Wallet:
    def __init__(self):
        self.private = SigningKey.generate(curve=SECP256k1)
        self.public = self.private.get_verifying_key()

    def sign(self, message):
        return self.private.sign(message.encode())

    def get_address(self):
        return self.public.to_string().hex()
from signature import generate_keypair, serialize_public_key

class Wallet:
    def __init__(self):
        self.private_key, self.public_key = generate_keypair()
        self.public_pem = serialize_public_key(self.public_key)

    def get_keys(self):
        return self.private_key, self.public_pem
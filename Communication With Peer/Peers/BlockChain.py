import hashlib

class CBlock:
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        self.previousHash = previousBlock.computeHash() if previousBlock else None
        self.nonce = None

    def computeHash(self):
        data_bytes = str(self.data).encode('utf-8')
        prev_bytes = str(self.previousHash).encode('utf-8') if self.previousHash else b''
        nonce_bytes = str(self.nonce).encode('utf-8') if self.nonce else b''
        return hashlib.sha256(data_bytes + prev_bytes + nonce_bytes).hexdigest()

    def is_valid(self):
        if self.previousBlock is None:
            return True
        return self.previousHash == self.previousBlock.computeHash()

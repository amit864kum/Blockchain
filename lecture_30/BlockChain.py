# Blockchain.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import json

class CBlock:
    def __init__(self, data, previousBlock=None):
        self.data = data
        self.previousBlock = previousBlock
        self.previousHash = previousBlock.computeHash() if previousBlock else None

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        # Serialize data to JSON for consistent hashing
        try:
            data_string = json.dumps(self.data, sort_keys=True)
        except TypeError:
            data_string = str(self.data)
        digest.update(data_string.encode('utf-8'))
        if self.previousHash:
            phash = self.previousHash
            if isinstance(phash, bytes):
                phash = phash.hex()
            digest.update(phash.encode('utf-8'))
        return digest.finalize().hex()

if __name__ == "__main__":
    root = CBlock("Genesis Block")
    block1 = CBlock({"transactions": 1234}, root)
    block2 = CBlock(["some", "list", "data"], block1)

    print("Root hash:", root.computeHash())
    print("Block1 hash:", block1.computeHash())
    print("Block2 hash:", block2.computeHash())

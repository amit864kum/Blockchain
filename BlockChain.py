from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import time
import json

class someClass:
    def __init__(self, mystring):
        self.string = mystring
        self.num = 328965

    def __repr__(self):
        return self.string + "^^^" + str(self.num)

class CBlock:
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        self.timestamp = time.time()
        self.nonce = 0  # For proof-of-work
        if previousBlock is not None:
            self.previousHash = previousBlock.computeHash()
        else:
            self.previousHash = None
        self.hash = self.computeHashWithProofOfWork()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

        # Convert data to bytes
        data_bytes = self.data if isinstance(self.data, bytes) else str(self.data).encode('utf-8')
        digest.update(data_bytes)

        # Previous hash
        digest.update(self.previousHash if self.previousHash else b'None')

        # Timestamp and nonce
        digest.update(str(self.timestamp).encode('utf-8'))
        digest.update(str(self.nonce).encode('utf-8'))

        return digest.finalize()

    def computeHashWithProofOfWork(self, difficulty=2):
        prefix = '0' * difficulty
        while True:
            hash_result = self.computeHash()
            if hash_result.hex().startswith(prefix):
                return hash_result
            self.nonce += 1

    def to_dict(self):
        return {
            'data': str(self.data),
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'previousHash': self.previousHash.hex() if self.previousHash else None,
            'hash': self.hash.hex()
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return CBlock("Genesis Block", None)

    def addBlock(self, data):
        previousBlock = self.chain[-1]
        newBlock = CBlock(data, previousBlock)
        self.chain.append(newBlock)
        return newBlock

    def isValid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.previousHash != prev.hash:
                return False
            if current.computeHash() != current.hash:
                return False
        return True

    def saveToFile(self, filename='blockchain.json'):
        with open(filename, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def printChain(self):
        for block in self.chain:
            print(json.dumps(block.to_dict(), indent=4))

# Example usage
if __name__ == "__main__":
    bc = Blockchain()
    bc.addBlock(b'I am B1')
    bc.addBlock('I am B2')
    bc.addBlock(12345)
    bc.addBlock(someClass("Hi there!"))
    bc.addBlock("Top block")

    bc.printChain()
    print("\nIs blockchain valid?", bc.isValid())

    # Save to file
    bc.saveToFile()

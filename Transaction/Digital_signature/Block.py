import time
import hashlib
import json

class Block:
    def __init__(self, transactions, previous_hash, difficulty):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce, self.hash = self.mine_block(difficulty)

    def compute_hash(self, nonce):
        block_string = json.dumps({
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        prefix = '0' * difficulty
        nonce = 0
        while True:
            h = self.compute_hash(nonce)
            if h.startswith(prefix):
                return nonce, h
            nonce += 1
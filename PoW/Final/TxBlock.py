import hashlib
import json
import time
from Transactions import Tx

class TxBlock:
    def __init__(self, previous_block):
        self.previous_block = previous_block
        self.nonce = 0
        self.tx_list = []
        self.timestamp = time.time()

    def addTx(self, tx):
        if tx.is_valid():
            self.tx_list.append(tx)

    def compute_hash(self):
        data = {
            "txs": [tx._Tx__gather() for tx in self.tx_list],
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "prev": self.previous_block.compute_hash() if self.previous_block else None
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def findNonce(self, difficulty=4):
        prefix = '0' * difficulty
        while True:
            if self.compute_hash().startswith(prefix):
                return True
            self.nonce += 1

    def is_valid(self, difficulty=4):
        if not self.compute_hash().startswith('0' * difficulty):
            return False
        for tx in self.tx_list:
            if not tx.is_valid():
                return False
        if self.previous_block is not None:
            return self.previous_block.is_valid(difficulty)
        return True

    def chain_length(self):
        if self.previous_block:
            return 1 + self.previous_block.chain_length()
        else:
            return 1

    def display(self):
        print("\n🧱 BLOCK DETAILS")
        print(f"⏱️ Timestamp: {self.timestamp}")
        print(f"🔢 Nonce: {self.nonce}")
        print(f"🔗 Previous Hash: {self.previous_block.compute_hash() if self.previous_block else None}")
        print(f"🧾 Current Hash: {self.compute_hash()}")
        print("📦 Block Header: {\"nonce\": %d, \"timestamp\": %.2f}" % (self.nonce, self.timestamp))
        print("📄 Transactions:")
        for tx in self.tx_list:
            print("  🔹 TX:")
            print(f"     Inputs: {tx.inputs}")
            print(f"     Outputs: {tx.outputs}")
            print(f"     Reqs: {tx.reqs}")
            print(f"     Sigs: {[sig.hex() if isinstance(sig, bytes) else sig for sig in tx.sigs]}")

import time
from hashlib import sha256
import json
from signature import sign_data, verify_signature

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, signature: str = None, timestamp: float = None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.signature = signature

    def to_dict(self) -> dict:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def sign(self, private_key_pem: str):
        """
        Create a digital signature over the transaction data.
        """
        self.signature = sign_data(self.to_dict(), private_key_pem)

    def is_valid(self) -> bool:
        """
        Check signature validity. SYSTEM transactions are always valid.
        """
        if self.sender == 'SYSTEM':
            return True
        return verify_signature(self.to_dict(), self.signature, self.sender)

class Block:
    def __init__(self,
                 index: int,
                 transactions: list,
                 previous_hash: str,
                 difficulty: int = 2,
                 max_size: int = 5):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions[:max_size]
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.max_size = max_size
        self.hash = None

    def compute_hash(self) -> str:
        """
        Compute SHA-256 hash of the block's contents.
        """
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode('utf-8')
        return sha256(block_string).hexdigest()

    def mine(self):
        """
        Proof-of-Work: increment nonce until hash meets difficulty (leading zeros).
        """
        prefix = '0' * self.difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                break
            self.nonce += 1

    def to_dict(self) -> dict:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() | {'signature': tx.signature} for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash,
            'difficulty': self.difficulty,
            'max_size': self.max_size
        }

    @staticmethod
    def from_dict(data: dict) -> 'Block':
        """
        Reconstruct a Block (including Transaction objects) from a dict.
        """
        from txblock import Transaction
        txs = []
        for tx_data in data['transactions']:
            tx = Transaction(
                sender=tx_data['sender'],
                recipient=tx_data['recipient'],
                amount=tx_data['amount'],
                signature=tx_data.get('signature'),
                timestamp=tx_data.get('timestamp')
            )
            txs.append(tx)
        blk = Block(
            index=data['index'],
            transactions=txs,
            previous_hash=data['previous_hash'],
            difficulty=data['difficulty'],
            max_size=data.get('max_size', len(txs))
        )
        blk.timestamp = data['timestamp']
        blk.nonce = data['nonce']
        blk.hash = data['hash']
        return blk
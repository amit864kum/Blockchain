import time
import json
from hashlib import sha256
from typing import List, Dict, Any
from transaction import Transaction


class Block:
    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        difficulty: int = 2,
        max_size: int = 5
    ):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions[:max_size]
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.max_size = max_size
        self.hash = None

    def compute_hash(self) -> str:
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode('utf-8')
        return sha256(block_string).hexdigest()

    def mine(self) -> None:
        """
        Proof-of-Work: find a nonce such that hash has `difficulty` leading zeros.
        """
        prefix = '0' * self.difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                break
            self.nonce += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [
                {**tx.to_dict(), 'signature': tx.signature.hex() if tx.signature else None}
                for tx in self.transactions
            ],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash,
            'difficulty': self.difficulty,
            'max_size': self.max_size
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Block':
        txs = []
        for txd in data['transactions']:
            tx = Transaction(
                sender_pub=txd['sender'],
                recipient_pub=txd['recipient'],
                amount=txd['amount'],
                timestamp=txd['timestamp'],
                signature=bytes.fromhex(txd['signature']) if txd['signature'] else None
            )
            txs.append(tx)
        blk = Block(
            index=data['index'],
            transactions=txs,
            previous_hash=data['previous_hash'],
            difficulty=data['difficulty'],
            max_size=data['max_size']
        )
        blk.timestamp = data['timestamp']
        blk.nonce = data['nonce']
        blk.hash = data['hash']
        return blk
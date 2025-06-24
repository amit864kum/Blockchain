from typing import Optional, List
from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self, difficulty: int = 2, max_block_size: int = 5):
        self.chain: List[Block] = []
        self.unconfirmed_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.max_block_size = max_block_size
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis = Block(0, [], '0', self.difficulty, self.max_block_size)
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, tx: Transaction) -> bool:
        if not tx.is_valid():
            return False
        self.unconfirmed_transactions.append(tx)
        return True

    def mine(self, miner_address: str) -> Optional[Block]:
        if not self.unconfirmed_transactions:
            return None
        # Add mining reward
        reward_tx = Transaction('SYSTEM', miner_address, 1)
        self.unconfirmed_transactions.append(reward_tx)

        block = Block(
            index=self.last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            previous_hash=self.last_block.hash,
            difficulty=self.difficulty,
            max_size=self.max_block_size
        )
        block.mine()
        self.chain.append(block)
        self.unconfirmed_transactions = []
        return block

    def is_valid_chain(self, chain: List[Block]) -> bool:
        for i in range(1, len(chain)):
            current, prev = chain[i], chain[i-1]
            if current.previous_hash != prev.hash:
                return False
            if current.compute_hash() != current.hash:
                return False
            if not current.hash.startswith('0' * current.difficulty):
                return False
            for tx in current.transactions:
                if not tx.is_valid():
                    return False
        return True

    def get_balance(self, public_key: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == public_key:
                    balance -= tx.amount
                if tx.recipient == public_key:
                    balance += tx.amount
        return balance
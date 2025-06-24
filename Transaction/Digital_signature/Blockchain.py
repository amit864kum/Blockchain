from Block import Block
from Transaction import Transaction

# class Blockchain:
#     def __init__(self, difficulty=3):
#         self.chain = [self.create_genesis_block()]
#         self.pending_txs = []
#         self.difficulty = difficulty
#         self.utxos = {}

class Blockchain:
    def __init__(self, difficulty=3):
        self.difficulty = difficulty                   # Set difficulty first
        self.chain = [self.create_genesis_block()]    # Then create genesis block
        self.pending_txs = []
        self.utxos = {}


    def create_genesis_block(self):
        tx = Transaction("COINBASE", "genesis_address", 100)
        return Block([tx], "0", self.difficulty)

    def add_transaction(self, tx):
        if tx.is_valid():
            if tx.sender != "COINBASE" and self.utxos.get(tx.sender, 0) < tx.amount:
                print("\u274c Insufficient balance")
                return False
            self.pending_txs.append(tx)
            return True
        return False

    def mine_pending(self, miner_address):
        coinbase = Transaction("COINBASE", miner_address, 50)
        block = Block([coinbase] + self.pending_txs, self.chain[-1].hash, self.difficulty)
        self.chain.append(block)

        for tx in block.transactions:
            if tx.sender != "COINBASE":
                self.utxos[tx.sender] = self.utxos.get(tx.sender, 0) - tx.amount
            self.utxos[tx.receiver] = self.utxos.get(tx.receiver, 0) + tx.amount
        self.pending_txs = []
        return block
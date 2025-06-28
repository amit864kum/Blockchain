# miner_app.py
import threading
import time
from blockchain.block import Block
from proof_of_work import mine_block
from utils.logger import setup_logger

class Miner(threading.Thread):
    def __init__(self, miner_id, blockchain, mempool, utxo_set, difficulty, stop_flag, broadcast_fn):
        super().__init__()
        self.miner_id = miner_id
        self.blockchain = blockchain
        self.mempool = mempool
        self.utxo_set = utxo_set
        self.difficulty = difficulty
        self.stop_flag = stop_flag
        self.broadcast_fn = broadcast_fn
        self.logger = setup_logger(f"Miner {self.miner_id}")
        self.daemon = True

    def run(self):
        while True:
            if self.stop_flag.is_set():
                self.logger.info("Stopped mining due to external signal.")
                break

            txs = self.mempool.get_transactions(3)
            if len(txs) < 3:
                time.sleep(0.5)
                continue

            valid_txs = []
            for tx in txs:
                if tx.is_valid() and self.utxo_set.is_valid_transaction(tx):
                    valid_txs.append(tx)

            if len(valid_txs) < 3:
                continue

            last_block = self.blockchain[-1]
            new_block = Block(index=last_block.index + 1,
                              transactions=valid_txs,
                              previous_hash=last_block.hash,
                              difficulty=self.difficulty)

            self.logger.info("Started mining a block.")
            mined_block = mine_block(new_block, self.difficulty, self.stop_flag)

            if mined_block:
                self.logger.info(f"✅ Block mined Successfully 😁😁: {mined_block.hash}")
                self.broadcast_fn(mined_block)
                break
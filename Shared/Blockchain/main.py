# main.py
import threading
import time
from miner_app import Miner
from blockchain.block import Block
from transactions.utxo_set import UTXOSet
from transactions.transaction import Transaction
from mempool.mempool import Mempool
from network.node import NodeNetwork
from Signatures import generate_keys
from utils.logger import setup_logger

NUM_MINERS = 3
DIFFICULTY = 3
logger = setup_logger("Main")

def vote_fn(block):
    return True

def generate_transactions(wallets, mempool, utxo_set):
    while True:
        sender, recipient = wallets[0], wallets[1]
        tx = Transaction(sender[1], recipient[1], 5)
        tx.sign_transaction(sender[0])
        if tx.is_valid():
            mempool.add_transaction(tx)
        time.sleep(1)

def run_simulation():
    blockchain = []
    utxo_set = UTXOSet()
    mempool = Mempool()
    node = NodeNetwork(num_miners=NUM_MINERS)
    stop_flag = threading.Event()

    pr_gen, pu_gen = generate_keys()
    wallets = [generate_keys() for _ in range(2)]
    utxo_set.add_utxo(wallets[0][1], 100)

    genesis_block = Block(0, [], "0", DIFFICULTY)
    genesis_block.hash = genesis_block.compute_hash()
    blockchain.append(genesis_block)
    node.blockchain = blockchain
    logger.info("Initialized blockchain with genesis block.")

    miners = []
    for i in range(NUM_MINERS):
        miner = Miner(
            miner_id=i,
            blockchain=node.blockchain,
            mempool=mempool,
            utxo_set=utxo_set,
            difficulty=DIFFICULTY,
            stop_flag=stop_flag,
            broadcast_fn=lambda block: node.broadcast_block(block, stop_flag, vote_fn)
        )
        miners.append(miner)
        miner.start()
        logger.info(f"Started Miner {i}")

    tx_thread = threading.Thread(target=generate_transactions, args=(wallets, mempool, utxo_set))
    tx_thread.daemon = True
    tx_thread.start()
    logger.info("Transaction generator started.")

    for miner in miners:
        miner.join()

if __name__ == '__main__':
    run_simulation()

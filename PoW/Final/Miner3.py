import time
import random
from TxBlock import TxBlock
from Transactions import Tx
import Signatures
import SocketUtils

mempool = []
chain_head = None
validation_pool = {}
miner_id = 3
vote_port = 7002

priv_key, pub_key = Signatures.generate_keys()
pub_key_ser = Signatures.serialize_public_key(pub_key).decode()

def handle_transaction(tx_json):
    tx = Tx()
    tx.inputs = tx_json['inputs']
    tx.outputs = tx_json['outputs']
    tx.reqs = tx_json['reqs']
    tx.sigs = [bytes.fromhex(sig) for sig in tx_json['sigs']]
    if tx.is_valid():
        mempool.append(tx)

def handle_block(block):
    if block.is_valid():
        block_hash = block.compute_hash()
        print("\n✅ [Miner3] Received and validated block:")
        block.display()
        SocketUtils.send_vote(7000, block_hash)

def handle_vote(vote_hash):
    if vote_hash not in validation_pool:
        validation_pool[vote_hash] = set()
    validation_pool[vote_hash].add("vote")

def mine_loop():
    global chain_head
    SocketUtils.start_transaction_server(handle_transaction, 5002)
    SocketUtils.start_block_server(handle_block, 6002)
    SocketUtils.start_vote_server(handle_vote, vote_port)

    round_no = 1
    chain_head = TxBlock(None)

    while True:
        print(f"\n🔁 [Miner3] Round {round_no}...\n")
        while len(mempool) < 10:
            time.sleep(1)

        new_block = TxBlock(chain_head)
        reward_tx = Tx()
        reward_tx.outputs.append((pub_key_ser, 10))
        reward_tx.sigs.append(b'SYSTEM')
        new_block.addTx(reward_tx)

        for _ in range(10):
            new_block.addTx(mempool.pop(0))

        new_block.findNonce(difficulty=4)
        block_hash = new_block.compute_hash()

        validation_pool[block_hash] = set()
        SocketUtils.send_block_to_all(new_block, 6002)

        print("[Miner3] Waiting for votes...")
        while len(validation_pool[block_hash]) < 2:
            time.sleep(0.5)

        print("✅ [Miner3] Block approved.")
        chain_head = new_block
        chain_head.display()
        round_no += 1
        time.sleep(2)

if __name__ == "__main__":
    mine_loop()

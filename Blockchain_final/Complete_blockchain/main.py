import time
from wallet import Wallet
from transaction import Transaction
from network import Node

# Create nodes
node_a = Node()
node_b = Node() 
node_c = Node()

# Connect peers dynamically
def connect_all(nodes):
    for n in nodes:
        for m in nodes:
            if n != m:
                n.register_peer(m)

connect_all([node_a, node_b, node_c])

# Create wallets
a_wallet = Wallet()
b_wallet = Wallet()

# Create and broadcast transactions
trans1 = Transaction(a_wallet.public_key, b_wallet.public_key, 10.5)
trans1.sign_transaction(a_wallet.private_key)
node_a.broadcast_transaction(trans1)

# Mine a block on node A
generated_block = node_a.blockchain.mine(a_wallet.public_key)
if generated_block:
    node_a.broadcast_block(generated_block)
    print(f"Block {generated_block.index} mined with hash: {generated_block.hash}")
    print(f"Balance A: {node_a.blockchain.get_balance(a_wallet.public_key)}")
    print(f"Balance B: {node_a.blockchain.get_balance(b_wallet.public_key)}")

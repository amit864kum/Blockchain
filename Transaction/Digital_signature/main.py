import sys
import time
from Node import Node
from Wallet import Wallet
from Transaction import Transaction

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    peers = [int(p) for p in sys.argv[3:]] if len(sys.argv) > 3 else []

    node = Node(port, peers)
    print("🕓 Waiting for listener to initialize...")
    time.sleep(5)

    if mode == "main":
        print("\n🔐 Generating user wallet and transaction...")
        user_wallet = Wallet()
        tx = Transaction(user_wallet.get_address(), node.wallet.get_address(), 10)
        tx.sign(user_wallet.private)
        node.blockchain.utxos[user_wallet.get_address()] = 100
        if node.blockchain.add_transaction(tx):
            print("✅ Transaction added")

        print("⛏️ Mining block...")
        new_block = node.blockchain.mine_pending(node.wallet.get_address())
        print("✅ Block mined:", new_block.hash)

        time.sleep(2)  # Allow other listener to start
        node.send_block(new_block)
import time
import random
import Signatures
from Transactions import Tx
import SocketUtils

def generate_random_transaction():
    priv1, pub1 = Signatures.generate_keys()
    priv2, pub2 = Signatures.generate_keys()
    amount = random.randint(1, 20)

    tx = Tx()
    tx.add_input(pub1, amount)
    tx.add_output(pub2, amount)
    tx.sign(priv1)

    tx_json = {
        "inputs": tx.inputs,
        "outputs": tx.outputs,
        "reqs": tx.reqs,
        "sigs": [sig.hex() for sig in tx.sigs]
    }

    print("\n📝 Generated Transaction:")
    print(f"  Inputs: {tx.inputs}")
    print(f"  Outputs: {tx.outputs}")
    print(f"  Reqs: {tx.reqs}")
    print(f"  Sigs: {[sig.hex() for sig in tx.sigs]}")

    return tx_json

if __name__ == "__main__":
    while True:
        tx_json = generate_random_transaction()
        SocketUtils.send_transaction_to_all(tx_json)
        print("📤 [TxGenerator] Broadcasted transaction.")
        time.sleep(2)
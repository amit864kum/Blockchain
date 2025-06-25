# client.py
import Transactions
import Signatures
import pickle
import socket
import time
import random

TCP_PORT = 5005

def sendObj(ip_addr, obj):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_addr, TCP_PORT))
        data = pickle.dumps(obj)
        s.sendall(data)
        s.close()
    except Exception as e:
        print("Send failed:", e)

if __name__ == "__main__":
    print("Client started... Generating random transactions")
    
    # Generate 5 wallet key pairs
    wallets = [Signatures.generate_keys() for _ in range(5)]

    while True:
        sender_idx = random.randint(0, 4)
        receiver_idx = random.randint(0, 4)
        while receiver_idx == sender_idx:
            receiver_idx = random.randint(0, 4)

        pr_sender, pu_sender = wallets[sender_idx]
        _, pu_receiver = wallets[receiver_idx]

        amount = round(random.uniform(1.0, 5.0), 2)

        tx = Transactions.Tx()
        tx.add_input(pu_sender, amount)
        tx.add_output(pu_receiver, amount - 0.1)  # simulate fee
        tx.sign(pr_sender)

        print(f"Sending {amount} from Wallet {sender_idx} to {receiver_idx}")
        sendObj('localhost', tx)

        time.sleep(2)  # Wait before next tx

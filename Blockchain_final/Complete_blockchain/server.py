import threading
import socket
from socketutils import send_msg, recv_msg
from blockchain import Blockchain
from block import Block
from transaction import Transaction

HOST = '0.0.0.0'
PORT = 5000

class NodeServer:
    def __init__(self):
        self.blockchain = Blockchain()
        self.peers = []
        self.lock = threading.Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()

    def start(self):
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            client, _ = self.sock.accept()
            threading.Thread(target=self.handle, args=(client,), daemon=True).start()

    def broadcast(self, msg: dict):
        with self.lock:
            for peer in self.peers:
                try:
                    send_msg(peer, msg)
                except:
                    pass

    def handle(self, client: socket.socket):
        try:
            print(f"New connection from {client.getpeername()}")
            if client not in self.peers:
                with self.lock:
                    self.peers.append(client)
            while True:
                msg = recv_msg(client)
                if msg is None:
                    print("Client disconnected cleanly.")
                    break
                t = msg.get('type')
                if t == 'tx':
                    tx_data = msg['data']
                    try:
                        tx = Transaction(
                            sender_pub=tx_data['sender'],
                            recipient_pub=tx_data['recipient'],
                            amount=tx_data['amount'],
                            timestamp=tx_data['timestamp'],
                            signature=bytes.fromhex(tx_data['signature']) if tx_data['signature'] else None
                        )
                        if tx.is_valid():
                            print("✅ Transaction is valid:")
                            tx.display()
                            self.blockchain.add_transaction(tx)
                            self.broadcast(msg)
                        else:
                            print("❌ Invalid transaction.")
                    except Exception as e:
                        print(f"Error decoding transaction: {e}")
                elif t == 'block':
                    blk_data = msg['data']
                    try:
                        blk = Block.from_dict(blk_data)
                        print("\n📦 Received Block")
                        print(f"Index: {blk.index}")
                        print(f"Timestamp: {blk.timestamp}")
                        print(f"Nonce: {blk.nonce}")
                        print(f"Previous Hash: {blk.previous_hash}")
                        print(f"Hash: {blk.hash}")
                        print(f"Difficulty: {blk.difficulty}")
                        print("--- Transactions ---")
                        for tx in blk.transactions:
                            tx.display()
                        if hasattr(self.blockchain, 'add_block'):
                            if self.blockchain.add_block(blk):
                                print("✅ Block added to chain.")
                                self.broadcast(msg)
                            else:
                                print("❌ Block validation failed.")
                    except Exception as e:
                        print(f"Error decoding block: {e}")
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            client.close()

if __name__ == '__main__':
    NodeServer().start()
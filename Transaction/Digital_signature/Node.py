import socket
import threading
import pickle
import time
from Blockchain import Blockchain
from Wallet import Wallet
from Transaction import Transaction

class Node:
    def __init__(self, port, peers=[]):
        self.port = port
        self.peers = peers
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        self.listener_ready = threading.Event()
        threading.Thread(target=self.listen_for_blocks, daemon=True).start()
        time.sleep(1)

    def listen_for_blocks(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', self.port))
        s.listen()
        print(f"🔌 [Listener Ready] Node listening on port {self.port}")
        self.listener_ready.set()
        while True:
            conn, addr = s.accept()
            print(f"📥 Connection received from {addr}")
            data = conn.recv(65536)
            if data:
                block = pickle.loads(data)
                self.blockchain.chain.append(block)
                print("📦 Block received:")
                print("Hash:", block.hash)
            conn.close()

    def send_block(self, block):
        for peer in self.peers:
            for attempt in range(3):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(('localhost', peer))
                    s.send(pickle.dumps(block))
                    s.close()
                    print(f"✅ Block sent to peer {peer}")
                    break
                except Exception as e:
                    print(f"⚠️ Attempt {attempt+1}: Could not connect to peer {peer}, retrying...")
                    time.sleep(2)
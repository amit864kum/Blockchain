# server.py
import socket
import pickle
import Transactions
from TxBlock import TxBlock  # Use your existing TxBlock
import time

TCP_PORT = 5005
BUFFER_SIZE = 1024
previous_block = None  # Start with genesis block

def newConnection(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, TCP_PORT))
    s.listen()
    print(f"Server listening on {ip_addr}:{TCP_PORT}")
    return s

def recvObj(server_socket):
    new_sock, addr = server_socket.accept()
    print(f"Connected to {addr}")
    all_data = b''
    while True:
        data = new_sock.recv(BUFFER_SIZE)
        if not data:
            break
        all_data += data
    new_sock.close()
    try:
        obj = pickle.loads(all_data)
        return obj
    except Exception as e:
        print("Error during unpickling:", e)
        return None

if __name__ == "__main__":
    s = newConnection('localhost')

    while True:
        obj = recvObj(s)
        if obj:
            print("\n--- Received Transaction ---")
            try:
                block = TxBlock(previous_block)  # Create new block linked to previous
                block.addTx(obj)
                
                print("Mining block...⛏️")
                nonce = block.find_nonce()
                print(f"Nonce found: {nonce}")
                
                if block.is_valid():
                    print("✅ Block is valid and mined successfully.")
                    previous_block = block  # Update previous block
                else:
                    print("❌ Block or transaction is invalid.")
                
                print("Block Info:")
                print(f"Timestamp: {time.ctime()}")
                print(f"Previous Hash: {block.previousHash}")
                print(f"Current Hash: {block.compute_hash()}")
            except Exception as e:
                print("Error handling transaction or block:", e)

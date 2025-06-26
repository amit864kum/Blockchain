import socket
import threading
import json
import pickle

HOST = '127.0.0.1'

def start_transaction_server(handler, port):
    def thread_fn():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, port))
        server.listen()
        print(f"[SocketUtils] TX server listening on port {port}")
        while True:
            conn, _ = server.accept()
            data = conn.recv(4096)
            if data:
                tx_json = json.loads(data.decode())
                handler(tx_json)
            conn.close()
    threading.Thread(target=thread_fn, daemon=True).start()

def start_block_server(handler, port):
    def thread_fn():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, port))
        server.listen()
        print(f"[SocketUtils] Block server listening on port {port}")
        while True:
            conn, _ = server.accept()
            block_data = b''
            while True:
                part = conn.recv(4096)
                if not part: break
                block_data += part
            block = pickle.loads(block_data)
            handler(block)
            conn.close()
    threading.Thread(target=thread_fn, daemon=True).start()

def start_vote_server(handler, port):
    def thread_fn():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, port))
        server.listen()
        print(f"[SocketUtils] Vote server listening on port {port}")
        while True:
            conn, _ = server.accept()
            vote = conn.recv(1024).decode()
            handler(vote)
            conn.close()
    threading.Thread(target=thread_fn, daemon=True).start()

def send_transaction_to_all(tx_json):
    for port in [5000, 5001, 5002]:
        try:
            s = socket.socket()
            s.connect((HOST, port))
            s.sendall(json.dumps(tx_json).encode())
            s.close()
        except Exception as e:
            print(f"[SocketUtils] TX send failed to port {port}: {e}")

def send_block_to_all(block, self_port):
    data = pickle.dumps(block)
    for port in [6000, 6001, 6002]:
        if port == self_port:
            continue
        try:
            s = socket.socket()
            s.connect((HOST, port))
            s.sendall(data)
            s.close()
        except Exception as e:
            print(f"[SocketUtils] Block send failed to port {port}: {e}")

def send_vote(to_port, vote_msg):
    try:
        s = socket.socket()
        s.connect((HOST, to_port))
        s.sendall(vote_msg.encode())
        s.close()
    except Exception as e:
        print(f"[SocketUtils] Vote send failed to port {to_port}: {e}")

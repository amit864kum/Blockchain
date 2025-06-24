import time
import socket
from socketutils import send_msg, recv_msg
from block import Block
from transaction import Transaction
from signature import serialize_public_key

HOST = '127.0.0.1'
PORT = 5000

def miner_loop(private_key, public_key_pem):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    while True:
        send_msg(sock, {'type': 'get_unconfirmed'})
        resp = recv_msg(sock)
        txs = []
        for td in resp.get('txs', []):
            tx = Transaction(
                td['sender'], td['recipient'], td['amount'], td['timestamp'], bytes.fromhex(td['signature'])
            )
            txs.append(tx)
        if txs:
            reward = Transaction('SYSTEM', public_key_pem, 1)
            txs.append(reward)
            send_msg(sock, {'type': 'get_chain'})
            chain_resp = recv_msg(sock)
            chain_data = chain_resp.get('chain', [])
            last = chain_data[-1]
            prev_hash = last['hash']
            blk = Block(len(chain_data), txs, prev_hash)
            print("🔨 Mining block...")
            blk.mine()
            print(f"✅ Mined Block #{blk.index}")
            print(f"Timestamp: {blk.timestamp}")
            print(f"Nonce: {blk.nonce}")
            print(f"Hash: {blk.hash}")
            print("--- Transactions in Block ---")
            for tx in blk.transactions:
                tx.display()
            send_msg(sock, {'type': 'block', 'data': blk.to_dict()})
        time.sleep(5)

if __name__ == '__main__':
    from signature import generate_keypair
    private_key, public_key = generate_keypair()
    public_key_pem = serialize_public_key(public_key)
    miner_loop(private_key, public_key_pem)

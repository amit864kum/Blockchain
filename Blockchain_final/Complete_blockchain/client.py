import socket
import argparse
from socketutils import send_msg, recv_msg
from transaction import Transaction
from signature import serialize_public_key, deserialize_public_key
from cryptography.hazmat.primitives import serialization

HOST_DEFAULT = '127.0.0.1'
PORT_DEFAULT = 5000

def load_private_key(path):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path):
    with open(path, 'r') as f:
        return f.read()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')

    p_tx = sub.add_parser('send_tx')
    p_tx.add_argument('sender_priv')
    p_tx.add_argument('sender_pub')
    p_tx.add_argument('recipient_pub')
    p_tx.add_argument('amount', type=float)

    sub.add_parser('get_balance')
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST_DEFAULT, PORT_DEFAULT))

    if args.cmd == 'send_tx':
        sender_priv = load_private_key(args.sender_priv)
        sender_pub = load_public_key(args.sender_pub)
        recipient_pub = load_public_key(args.recipient_pub)

        tx = Transaction(sender_pub, recipient_pub, args.amount)
        tx.sign(sender_priv)

        print("📤 Sending Transaction:")
        tx.display()

        send_msg(sock, {'type': 'tx', 'data': tx.to_dict() | {'signature': tx.signature.hex()}})
    elif args.cmd == 'get_balance':
        send_msg(sock, {'type': 'get_balance'})
        resp = recv_msg(sock)
        print(f"Balance: {resp.get('balance')}")

    sock.close()
import socket
import json
import struct

BUFFER_SIZE = 4096

def send_msg(sock: socket.socket, msg: dict) -> None:
    data = json.dumps(msg).encode('utf-8')
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)


def recv_msg(sock: socket.socket) -> dict:
    raw_len = _recv_all(sock, 4)
    if not raw_len:
        return None
    length = struct.unpack('>I', raw_len)[0]
    data = _recv_all(sock, length)
    return json.loads(data.decode('utf-8'))


def _recv_all(sock: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf
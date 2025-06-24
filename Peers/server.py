import TxBlock
import socket
import pickle

TCP_PORT = 5005
BUFFER_SIZE=1024

def newConnection(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr,TCP_PORT))
    s.listen()
    return s

def recvObj(socket):
    new_sock, addr = socket.accept()
    all_data = b''
    while True:
        data = new_sock.recv(BUFFER_SIZE)
        if not data:
            break
        all_data += data
    return pickle.loads(all_data)

if __name__ == "__main__":
    s = newConnection('localhost')  # <-- Fixed from hardcoded IP to localhost
    newB = recvObj(s)
    print(newB.data[0])
    print(newB.data[1])
    if newB.is_valid():
        print("Success. Tx is valid")
    else:
        print("Error. Tx invalid.")
    newTx = recvObj(s)
    print(newTx)

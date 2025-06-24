import SocketUtils
import Transactions
import Signatures

head_blocks = [None]

pr1, pu1 = Signatures.generate_keys()
pr2, pu2 = Signatures.generate_keys()
pr3, pu3 = Signatures.generate_keys()

Tx1 = Transactions.Tx()
Tx2 = Transactions.Tx()

Tx1.add_input(pu1, 4.0)
Tx1.add_input(pu2, 1.0)
Tx1.add_output(pu3, 4.8)
Tx2.add_input(pu3, 4.0)
Tx2.add_output(pu2, 4.0)
Tx2.add_reqd(pu1)

Tx1.sign(pr1)
Tx1.sign(pr2)
Tx2.sign(pr3)
Tx2.sign(pr1)

try:
    SocketUtils.sendObj('localhost', Tx1)
    print("Sent Tx1")
    SocketUtils.sendObj('localhost', Tx2)
    print("Sent Tx2")
except:
    print("Error! Connection unsuccessful")

server = SocketUtils.newServerConnection('localhost', 5006)
newBlock = None
for _ in range(30):
    newBlock = SocketUtils.recvObj(server)
    if newBlock:
        break
server.close()

if newBlock.is_valid():
    print("Success! Block is valid")
if newBlock.good_nonce():
    print("Success! Nonce is valid")

for tx in newBlock.data:
    try:
        if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
            print("Tx1 is present")
    except Exception as e:
        print(f"Error checking Tx1: {e}")
    try:
        if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
            print("Tx2 is present")
    except Exception as e:
        print(f"Error checking Tx2: {e}")

for b in head_blocks:
    if newBlock.previousHash == b.computeHash():
        newBlock.previousBlock = b
        head_blocks.remove(b)
        head_blocks.append(newBlock)

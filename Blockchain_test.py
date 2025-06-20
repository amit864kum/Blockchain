# BlockChain.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class someClass:
    string = None
    num = 1264378
    def __init__(self, mystring):
        self.string = mystring
    def __repr__(self):
        return self.string

class CBlock:
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock is not None:
            self.previousHash = previousBlock.computeHash()
        else:
            self.previousHash = None

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

        if isinstance(self.data, bytes):
            digest.update(self.data)
        else:
            digest.update(str(self.data).encode('utf-8'))

        if self.previousHash is not None:
            digest.update(self.previousHash)

        return digest.finalize()

if __name__ == '__main__':
    root  = CBlock(b'I am root', None)
    B1 = CBlock('Im a child!', root)

    if root.computeHash() == B1.previousHash:
        print("Success! B1 hash matches")
    else:
        print("ERROR! B1 hash does not match")

    if B1.previousBlock.computeHash() == B1.previousHash:
        print("Success! B1 hash matches")
    else:
        print("ERROR! B1 hash does not match")

    B2 = CBlock('Im a brother', root)        
    B3 = CBlock(b'I contiain bytes', B1)
    B4 = CBlock(12354, B3)
    B5 = CBlock(someClass('Hi there!'), B4)
    B6 = CBlock("child of B5", B5)

    for b,name in [(B1,'B1'), (B2,'B2'), (B3,'B3'), (B4,'B4'), (B5,'B5')]:
        if b.previousBlock.computeHash() == b.previousHash:
            print("Success! "+name+" hash matches")
        else:
            print("ERROR! " +name+" hash does not match")

    # Tampering
    B4.data = 12345
    if B5.previousBlock.computeHash() == B5.previousHash:
        print("ERROR! Failed to detect tamper")
    else:
        print("Success! Tampering detected.")

    B5.data.num = 23678
    if B6.previousBlock.computeHash() == B6.previousHash:
        print("ERROR! Failed to detect tamper")
    else:
        print("Success! Tampering detected.")

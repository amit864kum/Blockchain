# BlockChain.py
import hashlib
import pickle

class CBlock:
    def __init__(self, data=[], previousBlock=None):
        self.data = data                          # Transactions or data in this block
        self.previousBlock = previousBlock        # Reference to the previous block
        self.previousHash = None if previousBlock is None else previousBlock.compute_hash()

    def compute_hash(self):
        """
        Compute SHA-256 hash of the block's data and previous hash.
        """
        block_data = pickle.dumps((self.data, self.previousHash))
        return hashlib.sha256(block_data).hexdigest()

    def is_valid(self):
        """
        Validate block by comparing stored previous hash with recomputed one.
        """
        if self.previousBlock is None:
            return True
        return self.previousBlock.compute_hash() == self.previousHash

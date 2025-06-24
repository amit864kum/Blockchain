from blockchain import Blockchain
from transaction import Transaction
from block import Block

class Node:
    def __init__(self):
        self.blockchain = Blockchain()
        self.mempool = []
        self.peers = []

    def register_peer(self, peer_node: 'Node') -> None:
        if peer_node not in self.peers:
            self.peers.append(peer_node)

    def broadcast_transaction(self, transaction: Transaction) -> None:
        for peer in self.peers:
            peer.receive_transaction(transaction)

    def receive_transaction(self, transaction: Transaction) -> None:
        if self.blockchain.add_transaction(transaction):
            self.mempool.append(transaction)

    def broadcast_block(self, block: Block) -> None:
        for peer in self.peers:
            peer.receive_block(block)

    def receive_block(self, block: Block) -> None:
        if self.blockchain.add_block(block):
            # clear unconfirmed transactions that made it into block
            self.mempool = [tx for tx in self.mempool if tx not in block.transactions]

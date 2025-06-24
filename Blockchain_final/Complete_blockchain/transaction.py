import time
from typing import Dict, Any
from signature import sign_data, verify_signature, serialize_public_key, deserialize_public_key

class Transaction:
    def __init__(
        self,
        sender_pub: str,
        recipient_pub: str,
        amount: float,
        timestamp: float = None,
        signature: bytes = None
    ):
        self.sender = sender_pub
        self.recipient = recipient_pub
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.signature = signature

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def sign(self, private_key) -> None:
        self.signature = sign_data(self.to_dict(), private_key)

    def is_valid(self) -> bool:
        if self.sender == 'SYSTEM':
            return True
        if not self.signature:
            return False
        pub = deserialize_public_key(self.sender)
        return verify_signature(self.to_dict(), self.signature, pub)

    def display(self):
        print("INPUTS:")
        print(f"{self.amount} from {self.sender.splitlines()[0]}")
        print("OUTPUTS:")
        print(f"{self.amount} to {self.recipient.splitlines()[0]}")
        print("REQD:")
        print("SIGS:")
        sig_str = str(self.signature[:64]) + "..." if self.signature else 'None'
        print(sig_str)
        print("END\n")

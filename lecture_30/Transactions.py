# Transaction.py
import Signatures

class Tx:
    def __init__(self):
        self.inputs = []   # list of (address_pem_str, amount)
        self.outputs = []  # list of (address_pem_str, amount)
        self.reqd = []     # list of addresses that must sign (address_pem_str)
        self.sigs = []     # list of base64-encoded signatures

    def add_input(self, from_addr_pem, amount):
        self.inputs.append((from_addr_pem, amount))

    def add_output(self, to_addr_pem, amount):
        self.outputs.append((to_addr_pem, amount))

    def add_reqd(self, addr_pem):
        self.reqd.append(addr_pem)

    def sign(self, private_pem):
        message = self.__gather()
        new_sig = Signatures.sign(message, private_pem)
        self.sigs.append(new_sig)

    def is_valid(self):
        total_in = sum(amount for _, amount in self.inputs)
        total_out = sum(amount for _, amount in self.outputs)

        if any(amount < 0 for _, amount in self.inputs + self.outputs):
            print("Negative amount detected")
            return False

        if total_out > total_in:
            print("Outputs exceed inputs")
            return False

        message = self.__gather()

        # Check each input has a matching valid signature
        for addr, _ in self.inputs:
            if not any(Signatures.verify(message, sig, addr) for sig in self.sigs):
                print("No valid signature for input address")
                return False

        # Check required signers
        for req_addr in self.reqd:
            if not any(Signatures.verify(message, sig, req_addr) for sig in self.sigs):
                print("No valid signature for required address")
                return False

        return True

    def __gather(self):
        # Use tuple of tuples for immutable structure
        return (tuple(self.inputs), tuple(self.outputs), tuple(self.reqd))

if __name__ == "__main__":
    priv1, pub1 = Signatures.generate_keys()
    priv2, pub2 = Signatures.generate_keys()

    tx = Tx()
    tx.add_input(pub1, 10)
    tx.add_output(pub2, 10)
    tx.sign(priv1)

    print("Transaction valid?", tx.is_valid())

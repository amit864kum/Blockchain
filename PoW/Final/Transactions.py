import Signatures
import json

class Tx:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.reqs = []
        self.sigs = []

    def add_input(self, from_addr, amount):
        ser_addr = Signatures.serialize_public_key(from_addr).decode()
        self.inputs.append((ser_addr, amount))

    def add_output(self, to_addr, amount):
        ser_addr = Signatures.serialize_public_key(to_addr).decode()
        self.outputs.append((ser_addr, amount))

    def add_reqd(self, addr):
        ser_addr = Signatures.serialize_public_key(addr).decode()
        self.reqs.append(ser_addr)

    def sign(self, private_key):
        message = self.__gather().encode()
        sig = Signatures.sign(message, private_key)
        self.sigs.append(sig)

    def is_valid(self):
        message = self.__gather().encode()

        for i, (ser_pubkey, _) in enumerate(self.inputs):
            pubkey = Signatures.deserialize_public_key(ser_pubkey.encode())
            if i >= len(self.sigs):
                return False
            if not Signatures.verify(message, self.sigs[i], pubkey):
                return False

        for ser_req in self.reqs:
            pubkey = Signatures.deserialize_public_key(ser_req.encode())
            found = False
            for sig in self.sigs:
                if Signatures.verify(message, sig, pubkey):
                    found = True
                    break
            if not found:
                return False

        return True

    def __gather(self):
        data = {
            "inputs": self.inputs,
            "outputs": self.outputs,
            "reqs": self.reqs
        }
        return json.dumps(data, sort_keys=True)

    def __repr__(self):
        return f"Tx(Inputs={self.inputs}, Outputs={self.outputs}, Reqs={self.reqs}, Sigs={len(self.sigs)})"

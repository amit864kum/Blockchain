import Signatures
from Signatures import serialize_public_key, deserialize_public_key

class Tx:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append((serialize_public_key(from_addr), amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((serialize_public_key(to_addr), amount))

    def add_reqd(self, addr):
        self.reqd.append(serialize_public_key(addr))

    def sign(self, private):
        message = self.__gather()
        newsig = Signatures.sign(message, private)
        self.sigs.append(newsig)

    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()

        for addr_str, amount in self.inputs:
            found = False
            pub_key = deserialize_public_key(addr_str)
            for s in self.sigs:
                if Signatures.verify(message, s, pub_key):
                    found = True
            if not found or amount < 0:
                return False
            total_in += amount

        for addr_str in self.reqd:
            found = False
            pub_key = deserialize_public_key(addr_str)
            for s in self.sigs:
                if Signatures.verify(message, s, pub_key):
                    found = True
            if not found:
                return False

        for addr_str, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount

        return True

    def __gather(self):
        return [self.inputs, self.outputs, self.reqd]

    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr += f"{amt} from {addr[:20]}...\n"
        reprstr += "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr += f"{amt} to {addr[:20]}...\n"
        reprstr += "REQD:\n"
        for r in self.reqd:
            reprstr += f"{r[:20]}...\n"
        reprstr += "SIGS:\n"
        for s in self.sigs:
            reprstr += str(s)[:20] + "...\n"
        reprstr += "END\n"
        return reprstr

from ecdsa import SigningKey, VerifyingKey, NIST384p
import hashlib
import base64
import os

# === Key Generation ===
def generate_keys():
    private_key = SigningKey.generate(curve=NIST384p)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

# === Sign and Verify ===
def sign(message, private_key):
    if isinstance(message, str):
        message = message.encode()
    hashed = hashlib.sha256(message).digest()
    signature = private_key.sign(hashed)
    return base64.b64encode(signature).decode()

def verify(message, signature, public_key):
    try:
        if isinstance(message, str):
            message = message.encode()
        hashed = hashlib.sha256(message).digest()
        signature_bytes = base64.b64decode(signature)
        return public_key.verify(signature_bytes, hashed)
    except:
        return False

# === Save and Load Keys ===
def save_private_key(private_key, filepath):
    with open(filepath, 'wb') as f:
        f.write(private_key.to_pem())

def load_private_key(filepath):
    with open(filepath, 'rb') as f:
        return SigningKey.from_pem(f.read())

def save_public_key(public_key, filepath):
    with open(filepath, 'wb') as f:
        f.write(public_key.to_pem())

def load_public_key(filepath):
    with open(filepath, 'rb') as f:
        return VerifyingKey.from_pem(f.read())

# === Example usage ===
if __name__ == "__main__":
    # Generate and save keys
    priv, pub = generate_keys()
    save_private_key(priv, "private_key.pem")
    save_public_key(pub, "public_key.pem")

    # Load keys back
    priv2 = load_private_key("private_key.pem")
    pub2 = load_public_key("public_key.pem")

    # Sign and verify
    msg = "Hello blockchain"
    sig = sign(msg, priv2)
    if verify(msg, sig, pub2):
        print("Signature is valid.")
    else:
        print("Signature is invalid.")

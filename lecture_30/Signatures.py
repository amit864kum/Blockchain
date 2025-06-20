# Signature.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import base64

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    # Return PEM-encoded keys (bytes)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')

def sign(message, private_pem_str):
    private_key = serialization.load_pem_private_key(
        private_pem_str.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    message_bytes = str(message).encode('utf-8')
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

def verify(message, signature_b64, public_pem_str):
    public_key = serialization.load_pem_public_key(
        public_pem_str.encode('utf-8'),
        backend=default_backend()
    )
    signature = base64.b64decode(signature_b64)
    message_bytes = str(message).encode('utf-8')
    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False

if __name__ == "__main__":
    priv, pub = generate_keys()
    msg = "Sample message"
    sig = sign(msg, priv)
    print(f"Signature valid? {verify(msg, sig, pub)}")

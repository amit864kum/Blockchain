import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

def generate_keypair(key_size: int = 2048):
    """
    Generate RSA key pair. Returns (private_key_obj, public_key_obj).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def sign_data(data: dict, private_key) -> bytes:
    """
    Sign JSON-serializable dict with RSA private key. Returns signature bytes.
    """
    message = json.dumps(data, sort_keys=True).encode('utf-8')
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verify_signature(data: dict, signature: bytes, public_key) -> bool:
    """
    Verify signature bytes against JSON data and RSA public key.
    """
    message = json.dumps(data, sort_keys=True).encode('utf-8')
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def serialize_public_key(public_key) -> str:
    """
    Serialize RSA public key to PEM string.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')


def deserialize_public_key(pem_str: str):
    """
    Load RSA public key from PEM string.
    """
    return serialization.load_pem_public_key(
        pem_str.encode('utf-8'),
        backend=default_backend()
    )
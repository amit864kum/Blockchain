from signature import generate_keypair, serialize_public_key
from cryptography.hazmat.primitives import serialization

def save_keypair(prefix):
    priv, pub = generate_keypair()
    with open(f'{prefix}_priv.pem', 'wb') as f:
        f.write(priv.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        ))
    with open(f'{prefix}_pub.pem', 'wb') as f:
        f.write(serialize_public_key(pub).encode('utf-8'))

save_keypair('sender')
save_keypair('recipient')
save_keypair('miner')

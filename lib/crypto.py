"""
SuperSecret crypto core
Pure Python, zero dependencies.
scrypt key derivation + SHA-256 stream cipher (XOR).
"""

from __future__ import annotations
import hashlib
import os
from typing import Final

SALT: Final[bytes] = b"supersecret-v2-2026"
SCRYPT_N: Final[int] = 2**15          # higher than v1
SCRYPT_R: Final[int] = 8
SCRYPT_P: Final[int] = 1
KEY_LEN: Final[int] = 32


def derive_key(password: str, salt: bytes = SALT) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=KEY_LEN,
    )


def _keystream(key: bytes, length: int) -> bytes:
    stream = bytearray()
    counter = 0
    while len(stream) < length:
        block = hashlib.sha256(key + counter.to_bytes(8, "big")).digest()
        stream.extend(block)
        counter += 1
    return bytes(stream[:length])


def encrypt(plaintext: bytes, password: str) -> bytes:
    key = derive_key(password)
    # Prepend a random 16-byte nonce for future-proofing
    nonce = os.urandom(16)
    stream = _keystream(key + nonce, len(plaintext))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, stream))
    return nonce + ciphertext


def decrypt(blob: bytes, password: str) -> bytes:
    if len(blob) < 16:
        raise ValueError("Ciphertext too short")
    nonce = blob[:16]
    ciphertext = blob[16:]
    key = derive_key(password)
    stream = _keystream(key + nonce, len(ciphertext))
    return bytes(a ^ b for a, b in zip(ciphertext, stream))

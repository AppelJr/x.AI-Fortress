#!/usr/bin/env python3
"""Password hashing utilities — direct bcrypt, no passlib."""
import hashlib
import bcrypt


def get_password_hash(password: str) -> str:
    """Hash a password. SHA-256 pre-hash keeps input under bcrypt's 72-byte limit."""
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hashpw(digest, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash."""
    digest = hashlib.sha256(plain_password.encode("utf-8")).digest()
    try:
        return bcrypt.checkpw(digest, hashed_password.encode("utf-8"))
    except ValueError:
        return False

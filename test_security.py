import pytest
from app.core.security import get_password_hash, verify_password


def test_hash_and_verify_short():
    pw = "shortpass"
    h = get_password_hash(pw)
    assert verify_password(pw, h)
    assert not verify_password("wrong", h)


def test_hash_and_verify_long():
    pw = "a" * 128
    h = get_password_hash(pw)
    assert verify_password(pw, h)
    assert not verify_password("a" * 127, h)


def test_hash_deterministic_length():
    h = get_password_hash("x")
    assert len(h) == 60
    assert h.startswith("$2b$")


def test_empty_password():
    h = get_password_hash("")
    assert verify_password("", h)

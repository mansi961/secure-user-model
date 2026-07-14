"""
Unit tests for password hashing functions.
These don't touch the database — pure function testing.
"""
from app.security import hash_password, verify_password
def test_hash_password_returns_different_string_than_input():
    plain = "MySecret123"
    hashed = hash_password(plain)
    assert hashed != plain
def test_hash_password_produces_bcrypt_format():
    hashed = hash_password("MySecret123")
    assert hashed.startswith("$2b$")
def test_verify_password_correct_password_returns_true():
    plain = "MySecret123"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True
def test_verify_password_incorrect_password_returns_false():
    hashed = hash_password("MySecret123")
    assert verify_password("WrongPassword", hashed) is False
def test_hash_password_is_not_deterministic():
    """Same password hashed twice should produce different hashes (random salt)."""
    plain = "MySecret123"
    hash1 = hash_password(plain)
    hash2 = hash_password(plain)
    assert hash1 != hash2
    # but both should still verify correctly
    assert verify_password(plain, hash1) is True
    assert verify_password(plain, hash2) is True

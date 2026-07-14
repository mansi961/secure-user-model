"""
Password hashing utilities using bcrypt directly.
hash_password:   turns a plain-text password into a secure hash for storage.
verify_password: checks a plain-text password against a stored hash at login.
"""
import bcrypt
def hash_password(password: str) -> str:
    """Hash a plain-text password for storage in the database."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
)

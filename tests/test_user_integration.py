"""
Integration tests for the User model against a real Postgres database.
These require the Postgres test container to be running (see tests/conftest.py).
"""
import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.security import hash_password, verify_password


def test_create_user_success(db_session):
    """A valid user should be created and retrievable from the database."""
    user = User(
        username="mgs43",
        email="mgs43@njit.edu",
        password_hash=hash_password("SecurePass1"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username == "mgs43"
    assert user.email == "mgs43@njit.edu"
    assert user.created_at is not None
    # Confirm the stored hash actually verifies against the original password
    assert verify_password("SecurePass1", user.password_hash) is True


def test_duplicate_username_raises_integrity_error(db_session):
    """Creating two users with the same username should violate the unique constraint."""
    user1 = User(
        username="mgs43",
        email="mgs43@njit.edu",
        password_hash=hash_password("SecurePass1"),
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        username="mgs43",
        email="different_email@njit.edu",
        password_hash=hash_password("AnotherPass1"),
    )
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_duplicate_email_raises_integrity_error(db_session):
    """Creating two users with the same email should violate the unique constraint."""
    user1 = User(
        username="mgs43",
        email="mgs43@njit.edu",
        password_hash=hash_password("SecurePass1"),
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        username="different_username",
        email="mgs43@njit.edu",
        password_hash=hash_password("AnotherPass1"),
    )
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_password_hash_is_never_stored_in_plaintext(db_session):
    """The stored password_hash should never equal the original plain-text password."""
    plain_password = "SecurePass1"
    user = User(
        username="mgs43",
        email="mgs43@njit.edu",
        password_hash=hash_password(plain_password),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.password_hash != plain_password
    assert user.password_hash.startswith("$2b$")


def test_created_at_is_set_automatically(db_session):
    """created_at should be populated by the database without being explicitly set."""
    user = User(
        username="mgs43",
        email="mgs43@njit.edu",
        password_hash=hash_password("SecurePass1"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.created_at is not None

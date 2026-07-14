"""
Unit tests for Pydantic schema validation (UserCreate, UserRead).
These don't touch the database — pure validation testing.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserRead


def test_user_create_valid_data():
    user = UserCreate(username="mgs43", email="mgs43@njit.edu", password="SecurePass1")
    assert user.username == "mgs43"
    assert user.email == "mgs43@njit.edu"
    assert user.password == "SecurePass1"


def test_user_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="mgs43", email="not-an-email", password="SecurePass1")


def test_user_create_rejects_short_username():
    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="mgs43@njit.edu", password="SecurePass1")


def test_user_create_rejects_short_password():
    with pytest.raises(ValidationError):
        UserCreate(username="mgs43", email="mgs43@njit.edu", password="short")


def test_user_read_from_attributes():
    """UserRead should build correctly from an object with matching attributes."""

    class FakeUser:
        id = 1
        username = "mgs43"
        email = "mgs43@njit.edu"
        password_hash = "shouldnotappear"
        created_at = datetime.now()

    user_read = UserRead.model_validate(FakeUser())
    assert user_read.username == "mgs43"
    assert user_read.email == "mgs43@njit.edu"
    assert not hasattr(user_read, "password_hash")


def test_user_read_excludes_password_hash_field():
    """UserRead schema should not even define a password_hash field."""
    assert "password_hash" not in UserRead.model_fields
    assert "password" not in UserRead.model_fields

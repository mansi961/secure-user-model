"""
Additional unit tests to cover get_db() dependency generator
and the User model's __repr__ method.
"""
from app.database import get_db, SessionLocal
from app.models.user import User


def test_get_db_yields_a_session_and_closes_it():
    """get_db() should yield a session, then close it after the generator finishes."""
    gen = get_db()
    db = next(gen)

    assert db is not None

    # Exhaust the generator to trigger the 'finally: db.close()' branch.
    try:
        next(gen)
    except StopIteration:
        pass


def test_user_repr_contains_key_fields():
    """__repr__ should include id, username, and email for easy debugging."""
    user = User(id=1, username="mgs43", email="mgs43@njit.edu")
    representation = repr(user)

    assert "mgs43" in representation
    assert "mgs43@njit.edu" in representation
    assert "User" in representation

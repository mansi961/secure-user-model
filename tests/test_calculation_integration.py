
"""
Integration tests for the Calculation model against a real Postgres database.

These require the Postgres test container to be running (see tests/conftest.py).

"""
import pytest

from sqlalchemy.exc import IntegrityError

from app.models.user import User

from app.models.calculation import Calculation

from app.security import hash_password

def _make_user(db_session, username="mgs43", email="mgs43@njit.edu"):

    """Helper: create and commit a User so calculations have a valid FK."""

    user = User(

        username=username,

        email=email,

        password_hash=hash_password("SecurePass1"),

)
    db_session.add(user)

    db_session.commit()

    db_session.refresh(user)

    return user

def test_create_calculation_success(db_session):

    """A valid calculation should be created, computed, and retrievable from the database."""

    user = _make_user(db_session)

    calc = Calculation(a=10, b=5, type="Add", user_id=user.id)

    calc.result = calc.compute_result()

    db_session.add(calc)

    db_session.commit()

    db_session.refresh(calc)

    assert calc.id is not None

    assert calc.a == 10

    assert calc.b == 5

    assert calc.type == "Add"

    assert calc.result == 15

    assert calc.user_id == user.id

    assert calc.created_at is not None

def test_divide_calculation_computes_correct_result(db_session):

    """A divide calculation should store the correct computed result."""

    user = _make_user(db_session)

    calc = Calculation(a=20, b=4, type="Divide", user_id=user.id)

    calc.result = calc.compute_result()

    db_session.add(calc)

    db_session.commit()

    db_session.refresh(calc)

    assert calc.result == 5

def test_divide_by_zero_raises_value_error_before_insert(db_session):

    """Computing a division by zero should raise before it's ever stored."""

    user = _make_user(db_session)

    calc = Calculation(a=10, b=0, type="Divide", user_id=user.id)

    with pytest.raises(ValueError):

        calc.compute_result()

def test_invalid_type_raises_value_error_on_compute(db_session):

    """An invalid operation type should raise when computing, even though the

    DB column itself doesn't enforce an enum constraint."""

    user = _make_user(db_session)

    calc = Calculation(a=10, b=5, type="Modulo", user_id=user.id)

    with pytest.raises(ValueError):

        calc.compute_result()

def test_calculation_requires_valid_user_id(db_session):

    """A calculation referencing a non-existent user_id should violate the FK constraint."""

    calc = Calculation(a=10, b=5, type="Add", result=15, user_id=999999)

    db_session.add(calc)

    with pytest.raises(IntegrityError):

        db_session.commit()

def test_calculation_persists_correct_data_across_operations(db_session):

    """Confirm each operation type stores the correct result when persisted."""

    user = _make_user(db_session)

    cases = [

        ("Add", 6, 4, 10),

        ("Sub", 6, 4, 2),

        ("Multiply", 6, 4, 24),

        ("Divide", 6, 4, 1.5),

]
    for calc_type, a, b, expected in cases:

        calc = Calculation(a=a, b=b, type=calc_type, user_id=user.id)

        calc.result = calc.compute_result()

        db_session.add(calc)

        db_session.commit()

        db_session.refresh(calc)

        assert calc.result == expected


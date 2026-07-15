
"""

Unit tests for the CalculationFactory and Pydantic schema validation.

These do not touch the database — pure logic tests.

"""
import pytest

from pydantic import ValidationError

from app.factories.calculation_factory import (

    CalculationFactory,     AddOperation,     SubOperation,     MultiplyOperation,     DivideOperation,)





from app.schemas.calculation import CalculationCreate

def test_factory_creates_add_operation():

    operation = CalculationFactory.create("Add")

    assert isinstance(operation, AddOperation)

    assert operation.execute(2, 3) == 5

def test_factory_creates_sub_operation():

    operation = CalculationFactory.create("Sub")

    assert isinstance(operation, SubOperation)

    assert operation.execute(5, 3) == 2

def test_factory_creates_multiply_operation():

    operation = CalculationFactory.create("Multiply")

    assert isinstance(operation, MultiplyOperation)

    assert operation.execute(4, 3) == 12

def test_factory_creates_divide_operation():

    operation = CalculationFactory.create("Divide")

    assert isinstance(operation, DivideOperation)

    assert operation.execute(10, 2) == 5

def test_factory_divide_by_zero_raises_value_error():

    operation = CalculationFactory.create("Divide")

    with pytest.raises(ValueError):

        operation.execute(10, 0)

def test_factory_unsupported_type_raises_value_error():

    with pytest.raises(ValueError):

        CalculationFactory.create("Modulo")

def test_factory_compute_convenience_method():

    assert CalculationFactory.compute("Add", 2, 3) == 5

    assert CalculationFactory.compute("Multiply", 4, 3) == 12

def test_calculation_create_accepts_valid_data():

    schema = CalculationCreate(a=10, b=5, type="Divide")

    assert schema.a == 10

    assert schema.b == 5

    assert schema.type == "Divide"

def test_calculation_create_rejects_invalid_type():

    with pytest.raises(ValidationError):

        CalculationCreate(a=10, b=5, type="Modulo")

def test_calculation_create_rejects_zero_divisor():

    with pytest.raises(ValidationError):

        CalculationCreate(a=10, b=0, type="Divide")

def test_calculation_create_allows_zero_divisor_for_other_types():

    # b=0 is only invalid for Divide; other operations should accept it fine.

    schema = CalculationCreate(a=10, b=0, type="Add")

    assert schema.b == 0


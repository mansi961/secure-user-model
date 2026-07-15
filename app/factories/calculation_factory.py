
"""
Factory pattern for calculation operations.

Decouples "which math operation to run" from the Calculation model itself,

so new operation types can be added without touching model or schema code.

"""
from abc import ABC, abstractmethod

class Operation(ABC):

    """Base class for a calculation operation."""

    @abstractmethod

    def execute(self, a: float, b: float) -> float:

        pass

class AddOperation(Operation):

    def execute(self, a: float, b: float) -> float:

        return a + b

class SubOperation(Operation):

    def execute(self, a: float, b: float) -> float:

        return a - b

class MultiplyOperation(Operation):

    def execute(self, a: float, b: float) -> float:

        return a * b

class DivideOperation(Operation):

    def execute(self, a: float, b: float) -> float:

        if b == 0:

            raise ValueError("Cannot divide by zero")

        return a / b

class CalculationFactory:

    _operations = {

        "Add": AddOperation,

        "Sub": SubOperation,

        "Multiply": MultiplyOperation,

        "Divide": DivideOperation,

}
    @classmethod

    def create(cls, calculation_type: str) -> Operation:

        operation_cls = cls._operations.get(calculation_type)

        if operation_cls is None:

            raise ValueError("Unsupported calculation type: " + str(calculation_type))

        return operation_cls()

    @classmethod

    def compute(cls, calculation_type: str, a: float, b: float) -> float:

        operation = cls.create(calculation_type)

        return operation.execute(a, b)


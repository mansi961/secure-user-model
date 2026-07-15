
"""
Pydantic schemas for Calculation data validation and serialization.

- CalculationCreate: what a client sends to create a new calculation.

- CalculationRead:   what the API returns.

"""
from datetime import datetime

from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, model_validator

class CalculationCreate(BaseModel):

    """Schema for creating a new calculation. Validates operands and type."""

    a: float

    b: float

    type: Literal["Add", "Sub", "Multiply", "Divide"]

    @model_validator(mode="after")

    def check_no_zero_divisor(self):

        if self.type == "Divide" and self.b == 0:

            raise ValueError("Division by zero is not allowed")

        return self

class CalculationRead(BaseModel):

    """Schema for returning calculation data."""

    model_config = ConfigDict(from_attributes=True)

    id: int

    a: float

    b: float

    type: str

    result: float | None

    user_id: int

    created_at: datetime


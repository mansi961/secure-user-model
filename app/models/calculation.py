
"""
SQLAlchemy Calculation model.

Stores two operands (a, b), an operation type, and the computed result.

"""
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database import Base
from app.factories.calculation_factory import CalculationFactory

class Calculation(Base):

    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)

    a = Column(Float, nullable=False)

    b = Column(Float, nullable=False)

    type = Column(String(20), nullable=False)  # "Add", "Sub", "Multiply", "Divide"

    result = Column(Float, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="calculations")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def compute_result(self) -> float:

        return CalculationFactory.compute(self.type, self.a, self.b)

    def __repr__(self):

        return f"<Calculation(id={self.id}, a={self.a}, b={self.b}, type='{self.type}', result={self.result})>"


from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database.db import Base

class TaxResult(Base):
    __tablename__ = "tax_results"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    calculated_income = Column(Float, nullable=False)
    calculated_tax = Column(Float, nullable=False)
    status = Column(String, nullable=False)   # COMPLIANT / NON_COMPLIANT
    year = Column(Integer, nullable=False)

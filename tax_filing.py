from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime
from app.database.db import Base

class TaxFiling(Base):
    __tablename__ = "tax_filings"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    declared_income = Column(Float, nullable=False)
    deductions = Column(Float, default=0)
    year = Column(Integer, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, Float
from app.database.db import Base

class TaxSlab(Base):
    __tablename__ = "tax_slabs"

    id = Column(Integer, primary_key=True, index=True)
    min_income = Column(Float, nullable=False)
    max_income = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)   # percentage
    year = Column(Integer, nullable=False)

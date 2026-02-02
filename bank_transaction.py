from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database.db import Base

class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    date = Column(Date)
    description = Column(String)
    amount = Column(Float)
    type = Column(String)  # credit or debit

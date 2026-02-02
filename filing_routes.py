from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.tax_filing import TaxFiling

router = APIRouter(
    prefix="/filings",
    tags=["Filings"]
)

@router.post("/submit")
def submit_filing(
    company_id: int = Form(...),
    declared_income: float = Form(...),
    deductions: float = Form(...),
    year: int = Form(...),
    db: Session = Depends(get_db)
):
    filing = TaxFiling(
        company_id=company_id,
        declared_income=declared_income,
        deductions=deductions,
        year=year
    )

    db.add(filing)
    db.commit()
    db.refresh(filing)

    return {
        "message": "Filing submitted successfully",
        "filing_id": filing.id
    }

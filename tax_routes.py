from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.tax_filing import TaxFiling
from app.models.tax_result import TaxResult
from app.services.tax_engine import calculate_real_income

router = APIRouter(
    prefix="/tax",
    tags=["Tax"]
)

@router.post("/evaluate")
def evaluate_tax(
    filing_id: int = Form(...),
    db: Session = Depends(get_db)
):
    filing = db.query(TaxFiling).filter(
        TaxFiling.id == filing_id
    ).first()

    if not filing:
        return {"error": "Filing not found"}

    real_income = calculate_real_income(db, filing.company_id)

    taxable_income = real_income - filing.deductions
    tax = taxable_income * 0.20

    status = "COMPLIANT"
    if abs(real_income - filing.declared_income) > 5000:
        status = "NON-COMPLIANT"

    result = TaxResult(
        company_id=filing.company_id,
        year=filing.year,
        calculated_income=real_income,
        calculated_tax=tax,
        status=status
    )

    db.add(result)
    db.commit()

    return {
        "real_income": real_income,
        "taxable_income": taxable_income,
        "calculated_tax": tax,
        "status": status
    }

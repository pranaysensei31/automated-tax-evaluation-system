from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.company import Company
from app.models.tax_result import TaxResult
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/company/{company_id}")
def generate_company_report(company_id: int, db: Session = Depends(get_db)):

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    result = db.query(TaxResult).filter(
        TaxResult.company_id == company_id
    ).order_by(TaxResult.id.desc()).first()

    if not company or not result:
        return {"error": "Data not found"}

    filename = f"report_company_{company_id}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Automated Tax Evaluation Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Company: {company.name}")
    c.drawString(50, 740, f"Registration No: {company.registration_no}")
    c.drawString(50, 720, f"Year: {result.year}")

    c.drawString(50, 690, f"Calculated Income: {result.calculated_income}")
    c.drawString(50, 670, f"Calculated Tax: {result.calculated_tax}")
    c.drawString(50, 650, f"Compliance Status: {result.status}")

    c.save()

    return FileResponse(filename)

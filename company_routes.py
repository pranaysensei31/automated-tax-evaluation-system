from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.company import Company

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post("/add")
def add_company(
    name: str = Form(...),
    registration_no: str = Form(...),
    db: Session = Depends(get_db)
):
    company = Company(
        name=name,
        registration_no=registration_no
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return {
        "message": "Company added successfully",
        "company_id": company.id
    }

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import csv
from io import StringIO

from app.database.db import get_db
from app.models.bank_transaction import BankTransaction

router = APIRouter(
    prefix="/bank",
    tags=["Bank Transactions"]
)


@router.post("/upload/{company_id}")
def upload_bank_csv(
    company_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    try:
        content = file.file.read().decode("utf-8")
        reader = csv.DictReader(StringIO(content))

        for row in reader:
            transaction = BankTransaction(
                company_id=company_id,
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                amount=float(row["amount"]),
                type=row["type"].lower()
            )

            db.add(transaction)

        db.commit()

        return {
            "message": "Bank transactions uploaded successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"CSV processing failed: {str(e)}"
        )

from fastapi import FastAPI
from app.database.db import Base, engine

from app.routes.company_routes import router as company_router
from app.routes.filing_routes import router as filing_router
from app.routes.tax_routes import router as tax_router
from app.routes.bank_routes import router as bank_router

app = FastAPI(title="Automated Tax Evaluation System")

Base.metadata.create_all(bind=engine)

app.include_router(company_router)
app.include_router(filing_router)
app.include_router(tax_router)
app.include_router(bank_router)

@app.get("/")
def home():
    return {"message": "Automated Tax Evaluation System Running"}

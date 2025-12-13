
from fastapi import APIRouter, UploadFile, File
from app.services.pdf.extract import extract_text_from_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/extract")
async def extract(pdf: UploadFile = File(...)):
    text = await extract_text_from_pdf(pdf)      
    return {"text": text}
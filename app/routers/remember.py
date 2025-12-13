from fastapi import APIRouter, UploadFile, File, Form
from google import genai
from app.generate.model.remember import submit_vertex_ai_request
from app.services.prompt.remember2 import create_quiz_prompt

router = APIRouter(prefix="/core", tags=["remember"])

@router.post("/R001")
async def generate_quiz_from_pdf(
    pdf: UploadFile = File(...),
    num_questions: int = Form(default=3),
    language: str = Form(default="TH")
):
    prompt = await create_quiz_prompt(num_questions, language)
    try:        
        quiz_data = submit_vertex_ai_request(pdf, prompt)
        return quiz_data
    except Exception as e:
        return {"error": str(e)}

from fastapi import APIRouter, UploadFile, File, Form
from app.generate.model.understand_coding import submit_vertex_ai_request
from app.services.prompt.understand import create_quiz_prompt

router = APIRouter(prefix="/core", tags=["understand"])

@router.post("/U001")
async def generate_quiz_from_pdf(
    pdf: UploadFile = File(...),
    num_questions: int = Form(default=5),
    language: str = Form(default="TH")
):
    try:
        prompt = await create_quiz_prompt(num_questions, language)
        quiz_data = await submit_vertex_ai_request(pdf, prompt)
        return quiz_data
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

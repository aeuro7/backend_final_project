
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import json
from app.services.quiz_service.remember import generate_quiz_R001

router = APIRouter(prefix="/quiz", tags=["Quiz"])


class GenerateQuizRequest(BaseModel):
    text: str = Field(..., description="ข้อความจาก PDF หรือเนื้อหาที่ต้องการสร้างข้อสอบ")
    bloom_level: str = Field(default="Remember", description="Bloom's Taxonomy level")
    question_type: str = Field(default="multiple_choice", description="ประเภทข้อสอบ (multiple_choice, short_answer, code_completion)")
    num_questions: int = Field(default=6, description="จำนวนข้อสอบ")
    language: str = Field(default="TH", description="ภาษาของข้อสอบ (TH/EN)")
    include_explanation: bool = Field(default=True, description="รวมคำอธิบายคำตอบหรือไม่")


@router.post("/generate")
async def generate_quiz_endpoint(request: GenerateQuizRequest):
    """
    สร้างข้อสอบจากข้อความที่ให้มา
    
    Parameters:
    - text: ข้อความจาก PDF หรือเนื้อหา
    - bloom_level: ระดับของ Bloom's Taxonomy (Remember)
    - question_type: ประเภทข้อสอบ (multiple_choice, short_answer, code_completion)
    - num_questions: จำนวนข้อสอบ
    - language: ภาษา (TH/EN)
    - include_explanation: รวมคำอธิบายหรือไม่
    
    Returns:
    - JSON object ที่มีข้อสอบที่สร้างขึ้น
    """
    try:
        # แปลง text เป็น JSON safe string
        text_safe = json.dumps(request.text, ensure_ascii=False)

        quiz = await generate_quiz_R001(
            text=text_safe,
            bloom_level=request.bloom_level,
            question_type=request.question_type,
            num_questions=request.num_questions,
            language=request.language,
            include_explanation=request.include_explanation
        )
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการสร้างข้อสอบ: {str(e)}")


@router.get("/")
async def index():
    return {
        "message": "Quiz API Endpoint",
        "description": "ใช้เพื่อสร้างข้อสอบจากข้อความ",
        "endpoints": {
            "POST /quiz/generate": "สร้างข้อสอบจากข้อความ",
            "GET /quiz/": "ข้อมูล endpoint นี้"
        }
    }

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.services.pdf_service import extract_text_from_pdf
from app.services.quiz_service.remember import generate_quiz_R001
from app.services.quiz_service.understand import generate_quiz_U001
from app.services.quiz_service.understand import check_quiz_answer_U003

router = APIRouter(prefix="/core", tags=["Core"])

@router.post("/R001")
async def R001(
    pdf: UploadFile = File(...),
    bloom_level: str = Form(default="Remember"),
    question_type: str = Form(default="multiple_choice"),
    num_questions: int = Form(default=6),
    language: str = Form(default="TH"),
    include_explanation: bool = Form(default=True)
):
    try:
        # Extract text from PDF file
        text = await extract_text_from_pdf(pdf)

        if not text.strip():
            raise HTTPException(status_code=400, detail="ไม่พบข้อความใน PDF")

        # Generate Quiz
        quiz = await generate_quiz_R001(
            text=text,
            bloom_level=bloom_level,
            question_type=question_type,
            num_questions=num_questions,
            language=language,
            include_explanation=include_explanation
        )

        return {
            "pdf_filename": pdf.filename,
            "num_questions": num_questions,
            "quiz": quiz
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการสร้างข้อสอบ: {str(e)}")


@router.post("/U001")
async def U001(
    pdf: UploadFile = File(...),
    bloom_level: str = Form(default="Understand"),
    question_type: str = Form(default="multiple_choice"),
    num_questions: int = Form(default=6),
    language: str = Form(default="TH"),
    include_explanation: bool = Form(default=True)
):
    try:
        # Extract text from PDF file
        text = await extract_text_from_pdf(pdf)

        if not text.strip():
            raise HTTPException(status_code=400, detail="ไม่พบข้อความใน PDF")

        # Generate Quiz
        quiz = await generate_quiz_U001(
            text=text,
            bloom_level=bloom_level,
            question_type=question_type,
            num_questions=num_questions,
            language=language,
            include_explanation=include_explanation
        )

        return {
            "pdf_filename": pdf.filename,
            "num_questions": num_questions,
            "quiz": quiz
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการสร้างข้อสอบ: {str(e)}")

@router.post("/U002")
async def U002(
    pdf: UploadFile = File(...),
    bloom_level: str = Form(default="Understand"),
    question_type: str = Form(default="short_answer"),
    num_questions: int = Form(default=6),
    language: str = Form(default="TH"),
    include_explanation: bool = Form(default=True)
):
    try:
        # Extract text from PDF file
        text = await extract_text_from_pdf(pdf)

        if not text.strip():
            raise HTTPException(status_code=400, detail="ไม่พบข้อความใน PDF")

        # Generate Quiz
        quiz = await generate_quiz_U001(
            text=text,
            bloom_level=bloom_level,
            question_type=question_type,
            num_questions=num_questions,
            language=language,
            include_explanation=include_explanation
        )

        return {
            "pdf_filename": pdf.filename,
            "num_questions": num_questions,
            "quiz": quiz
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการสร้างข้อสอบ: {str(e)}")

@router.post("/U003")
async def U003(
    question: str = Form(...),
    user_answer: str = Form(...),
    correct_answer: str = Form(...),
    detail: bool = Form(default=True)
):
    try:
        # Check Quiz Answer
        result = await check_quiz_answer_U003(
            question=question,
            user_answer=user_answer,
            correct_answer=correct_answer,
            detail=detail
        )

        return {
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "detail": detail,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการตรวจสอบคำตอบ: {str(e)}")



    #     {
    #     "id": 6,
    #     "question": "ใน Python เมื่อคุณกำหนดเมธอดภายในคลาส (เช่น `def my_method(self, parameter): ...`) `self` พารามิเตอร์ตัวแรกมีบทบาทและความสำคัญอย่างไร? จงอธิบายการทำงานและวัตถุประสงค์หลักของมัน",
    #     "answer": "`self` เป็นพารามิเตอร์ตัวแรกที่ต้องระบุในเมธอดของคลาส Python ทุกเมธอด (ยกเว้น static methods) มันทำหน้าที่เป็นตัวอ้างอิงถึง **อินสแตนซ์ของอ็อบเจกต์ปัจจุบัน** ที่เรียกใช้เมธอดนั้นๆ",
    #     "explanation": "วัตถุประสงค์หลักของ `self` คืออนุญาตให้เมธอดเข้าถึงและจัดการกับ **คุณสมบัติ (attributes/fields)** และ **เมธอดอื่นๆ** ของอ็อบเจกต์นั้นๆ ได้ ตัวอย่างเช่น ถ้าคุณมีอ็อบเจกต์ `p` จากคลาส `Point` และเรียกใช้ `p.move(dx, dy)` ภายในเมธอด `move` `self` จะหมายถึงอ็อบเจกต์ `p` นั้นเอง ทำให้สามารถเข้าถึง `self.x` และ `self.y` เพื่อเปลี่ยนแปลงค่าของมันได้ หากไม่มี `self` เมธอดจะไม่สามารถทราบได้ว่าจะดำเนินการกับคุณสมบัติของอ็อบเจกต์ใด ทำให้ไม่สามารถทำงานกับข้อมูลเฉพาะของแต่ละอินสแตนซ์ได้"
    #   }

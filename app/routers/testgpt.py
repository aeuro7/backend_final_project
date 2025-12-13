from fastapi import APIRouter, UploadFile, File, Form
import openai
import tempfile
import shutil

OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

router = APIRouter(prefix="/test", tags=["test"])

@router.post("/upload_pdf")
async def upload_pdf(
    pdf: UploadFile = File(...),
    num_questions: int = Form(default=6),
    language: str = Form(default="TH"),
):
    # บันทึกไฟล์ชั่วคราว
    tmp_dir = tempfile.mkdtemp()
    tmp_path = f"{tmp_dir}/{pdf.filename}"
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(pdf.file, f)

    # อัปโหลดไฟล์ไปยัง OpenAI
    with open(tmp_path, "rb") as file:
        file_response = openai.File.create(
            file=file,
            purpose='fine-tune'  # หรือ purpose อื่น ๆ ตามที่ต้องการ
        )

    # สร้าง prompt
    prompt = f"สร้าง {num_questions} คำถามแบบ multiple choice จากไฟล์นี้เป็นภาษา {language}: {file_response['id']}"

    # เรียก GPT-4o-mini
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    # ลบไฟล์ชั่วคราว
    shutil.rmtree(tmp_dir)

    return {"quiz": response.choices[0].message.content}

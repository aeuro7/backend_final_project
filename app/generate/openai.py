from openai import OpenAI
from fastapi import UploadFile
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def submit_openai_request(pdf: UploadFile) -> str:
    # อ่านไฟล์ PDF ที่อัปโหลด
    file_bytes = await pdf.read()

    # อัปโหลดไฟล์ไปยัง OpenAI
    uploaded_file = client.files.create(
        file=(pdf.filename, file_bytes, pdf.content_type),
        purpose="responses"
    )

    # prompt
    prompt = "สร้างคำถามมาจากเนื้อหาในไฟล์นี้ 1 ข้อ"

    # เรียกใช้ Responses API พร้อมแนบไฟล์
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        attachments=[{"file_id": uploaded_file.id}]
    )

    # ดึงข้อความตอบกลับ
    return response.output_text
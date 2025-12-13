from openai import OpenAI
from fastapi import UploadFile
import os

client = OpenAI(api_key=("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"))

async def submit_openai_request(pdf: UploadFile) -> str:
    # 🧾 อ่านไฟล์ PDF ที่อัปโหลด
    file_bytes = await pdf.read()

    # 📎 อัปโหลดไฟล์ไปยัง OpenAI
    uploaded_file = client.files.create(
        file=(pdf.filename, file_bytes, pdf.content_type),
        purpose="responses"
    )

    # 🧠 prompt สั้น ๆ
    prompt = "สร้างคำถามมาจากเนื้อหาในไฟล์นี้ 1 ข้อ"

    # 🚀 เรียกใช้ Responses API พร้อมแนบไฟล์
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        attachments=[{"file_id": uploaded_file.id}]
    )

    # ✅ ดึงข้อความตอบกลับ
    return response.output_text
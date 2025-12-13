import vertexai
from fastapi import UploadFile
from vertexai.generative_models import GenerativeModel, Part
from pathlib import Path
import shutil
import tempfile
import json
import re
import os

# --- ข้อมูล Endpoint ของคุณ ---
# --- ข้อมูล Endpoint ของคุณ ---
PROJECT_ID = "gen-lang-client-0058632069" 
REGION = "us-south1"
ENDPOINT_ID = "1863878917266341888" 

# --- สร้าง Endpoint Resource Name ที่สมบูรณ์ ---
FULL_ENDPOINT_NAME = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

def submit_vertex_ai_request(pdf: UploadFile, prompt: str):
    """
    ส่งคำขอไปยังโมเดล Gemini บน Vertex AI
    โดยระบุ Endpoint ID (สำหรับ Provisioned Throughput หรือ Deployment เฉพาะ)
    """
    
    # 1. บันทึกไฟล์ PDF ชั่วคราว
    tmp_dir = tempfile.mkdtemp()
    tmp_path = Path(tmp_dir) / pdf.filename
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(pdf.file, f)
    
    try:
        # --- 2. Initialize Vertex AI ---
        vertexai.init(project=PROJECT_ID, location=REGION)
        
        # --- 3. Load Model from Endpoint ---
        # ใช้ Endpoint Resource Name ที่ระบุ เพื่อยิงไปที่ Endpoint ของเราโดยตรง
        model = GenerativeModel(FULL_ENDPOINT_NAME)

        # --- 4. Prepare Data ---
        with open(tmp_path, "rb") as f:
            file_bytes = f.read()
            
        # สร้าง Part object สำหรับไฟล์ PDF (Vertex AI SDK จัดการ Base64 ให้)
        pdf_part = Part.from_data(
            mime_type="application/pdf",
            data=file_bytes
        )

        # --- 5. Generate Content ---
        # ส่ง Prompt และไฟล์ PDF ไปยังโมเดล
        response = model.generate_content(
            [pdf_part, prompt]
        )
        
        # --- 6. Process Response ---
        # ดึงข้อความตอบกลับ
        response_text = response.text
        
        # 7. คัดแยกและ Parse JSON
        json_data = extract_and_parse_json(response_text)
        return json_data

    except Exception as e:
        raise Exception(f"Failed to call Vertex AI: {e}")
        
    finally:
        # ลบไฟล์ชั่วคราวทิ้งเสมอ
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)


def extract_and_parse_json(response_text: str):
    """ฟังก์ชันเดิมสำหรับคัดแยก JSON จากข้อความ"""
    response_text = response_text.strip()
    
    # Try to extract JSON from markdown code blocks if present
    json_match = re.search(r'```json\s*(\{.*\})\s*```', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(1)
    else:
        # Try to find JSON object
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
    
    # Parse JSON
    try:
        quiz_data = json.loads(response_text)
        return quiz_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nResponse text: {response_text}")
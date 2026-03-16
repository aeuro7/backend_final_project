import vertexai
from fastapi import UploadFile
from vertexai.generative_models import GenerativeModel, Part
from pathlib import Path
import shutil
import tempfile
import json
import re
import os
from google.oauth2 import service_account

# --- ข้อมูล Endpoint ของคุณ ---
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/euro/Work/Backend_2/gen-lang-client-0058632069-7b124e65a759.json"
PROJECT_ID = "gen-lang-client-0058632069" 
REGION = "us-south1"
ENDPOINT_ID = "2842532226917203968" 

# --- สร้าง Endpoint Resource Name ที่สมบูรณ์ ---
FULL_ENDPOINT_NAME = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

async def submit_vertex_ai_request(pdf: UploadFile, prompt: str):
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
        creds = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if creds:
            with open("gcp-key.json", "w") as f:
                f.write(creds)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"
        elif os.path.exists("gen-lang-client-0058632069-7b124e65a759.json"): 
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0058632069-7b124e65a759.json"
            
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
        response = await model.generate_content_async(
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
    """คัดแยกและ Parse JSON จากข้อความ รองรับทั้ง Array และ Object"""
    response_text = response_text.strip()
    
    # 1. ลองหา JSON ใน markdown code blocks ก่อน
    # รองรับทั้ง [...] และ {...}
    json_match = re.search(r'```(?:json)?\s*(\[.*\]|\{.*\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
    if json_match:
        response_text = json_match.group(1)
    else:
        # 2. ลองหา JSON Array [...] 
        # ใช้ stack ในการหา bracket ที่จับคู่กันถูกต้อง เพื่อรองรับ nested list/dict
        try:
            start_index = response_text.find('[')
            if start_index != -1:
                stack = []
                for i, char in enumerate(response_text[start_index:], start=start_index):
                    if char == '[':
                        stack.append('[')
                    elif char == ']':
                        stack.pop()
                        if not stack:
                            response_text = response_text[start_index:i+1]
                            break
            else:
                 # 3. ถ้าไม่เจอ array ลองหา object {...}
                 start_index = response_text.find('{')
                 if start_index != -1:
                    stack = []
                    for i, char in enumerate(response_text[start_index:], start=start_index):
                        if char == '{':
                            stack.append('{')
                        elif char == '}':
                            stack.pop()
                            if not stack:
                                response_text = response_text[start_index:i+1]
                                break
        except Exception:
            # Fallback to simple regex if stacking fails
            pass
            
    # 4. Parse JSON
    try:
        # ทำความสะอาด string ก่อน parse
        response_text = response_text.strip()
        # บางที model อาจจะส่ง empty string หรือ whitespace นำหน้า/ตามหลัง
        if not response_text:
             raise ValueError("Empty JSON string found")
             
        quiz_data = json.loads(response_text)
        return quiz_data
    except json.JSONDecodeError as e:
        # 5. ถ้า parse ไม่ได้ อาจเป็นเพราะได้หลาย objects แยกกัน
        # ลองหาทุก {...} แล้วรวมเป็น array
        try:
            # ใช้ regex ที่ซับซ้อนขึ้นเพื่อจับคู่ json object
            objects = []
            decoder = json.JSONDecoder()
            pos = 0
            while True:
                response_text = response_text[pos:].lstrip()
                if not response_text:
                    break
                try:
                    obj, idx = decoder.raw_decode(response_text)
                    objects.append(obj)
                    pos = idx
                except json.JSONDecodeError:
                    # ถ้า decode ต่อไม่ได้ ให้ข้ามไปหา { ตัวถัดไป
                    next_brace = response_text.find('{', 1)
                    if next_brace == -1:
                        break
                    pos = next_brace
            
            if objects:
                return objects
        except:
            pass
        
        # 6. ถ้ายังไม่ได้ ให้ raise error
        raise ValueError(f"Failed to parse JSON response: {e}\nResponse text: {response_text[:500]}...")

from fastapi import APIRouter, UploadFile, File, Form
from google import genai
from pathlib import Path
import shutil
import tempfile
import json, re
import os


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)


def submit_gemini_request(pdf: UploadFile, prompt: str):
    tmp_dir = tempfile.mkdtemp()
    tmp_path = Path(tmp_dir) / pdf.filename
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(pdf.file, f)

    uploaded_file = client.files.upload(file=tmp_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, uploaded_file]
    )
    shutil.rmtree(tmp_dir)

    # Extract JSON from response
    response_text = response.text.strip()
    
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



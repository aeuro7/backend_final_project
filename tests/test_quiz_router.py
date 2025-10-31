import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_quiz_index():
    """ทดสอบ endpoint GET /quiz/"""
    response = client.get("/quiz/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert "POST /quiz/generate" in data["endpoints"]


def test_generate_quiz_basic():
    """ทดสอบการสร้างข้อสอบแบบพื้นฐาน"""
    payload = {
        "text": "Python เป็นภาษาโปรแกรมที่ยืดหยุ่นและใช้งานง่าย",
        "num_questions": 2
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert isinstance(data["questions"], list)
    assert len(data["questions"]) == 2


def test_generate_quiz_with_all_params():
    """ทดสอบการสร้างข้อสอบพร้อมพารามิเตอร์ทั้งหมด"""
    payload = {
        "text": "FastAPI เป็น web framework สำหรับ Python ที่มีประสิทธิภาพสูง",
        "bloom_level": "Remember",
        "question_type": "multiple_choice",
        "num_questions": 3,
        "language": "TH",
        "include_explanation": True
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) == 3


def test_generate_quiz_english():
    """ทดสอบการสร้างข้อสอบภาษาอังกฤษ"""
    payload = {
        "text": "JavaScript is a high-level programming language",
        "language": "EN",
        "num_questions": 2
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data


def test_generate_quiz_short_answer():
    """ทดสอบการสร้างข้อสอบแบบ short answer"""
    payload = {
        "text": "Git เป็นระบบควบคุมเวอร์ชัน (version control)",
        "question_type": "short_answer",
        "num_questions": 2
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data


def test_generate_quiz_without_explanation():
    """ทดสอบการสร้างข้อสอบโดยไม่มีคำอธิบาย"""
    payload = {
        "text": "REST API เป็นรูปแบบการออกแบบ API",
        "include_explanation": False,
        "num_questions": 2
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data


def test_generate_quiz_missing_text():
    """ทดสอบการส่ง request โดยไม่มี text (ควร error)"""
    payload = {
        "num_questions": 2
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 422  # Validation error


def test_quiz_question_structure_multiple_choice():
    """ตรวจสอบโครงสร้างข้อสอบแบบ multiple choice"""
    payload = {
        "text": "Python มีหลาย data types เช่น int, str, list",
        "question_type": "multiple_choice",
        "num_questions": 1
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    question = data["questions"][0]
    
    assert "id" in question
    assert "question" in question
    assert "options" in question
    assert "correct_answer" in question
    assert isinstance(question["options"], dict)
    assert len(question["options"]) == 4


def test_quiz_question_structure_short_answer():
    """ตรวจสอบโครงสร้างข้อสอบแบบ short answer"""
    payload = {
        "text": "SQL คือภาษา query สำหรับ database",
        "question_type": "short_answer",
        "num_questions": 1
    }
    response = client.post("/quiz/generate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    question = data["questions"][0]
    
    assert "id" in question
    assert "question" in question
    assert "answer" in question


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



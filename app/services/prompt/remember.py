import json
from app.models.example_json_remember import example_json as example_json_remember

async def create_quiz_prompt(num_questions: int, language: str) -> str:
    
    # แปลง example JSON เป็น string เพื่อใส่ใน prompt
    example_json_str = json.dumps(example_json_remember, ensure_ascii=False, indent=2)
    
    # สร้าง prompt ที่ครอบคลุม
    prompt_parts = [
        f"Bloom's Level: Remember",
        "",
        "Focus the question on recalling the basic syntax, terminology, or fundamental commands related to the topic. "
        "The question should test whether the student can remember or recognize: "
        "syntax structure (e.g., correct format, use of brackets, keywords, indentation), "
        "the meaning of basic technical terms or programming principles (e.g., variable, loop, function), "
        "the purpose or function of common commands or built-in functions (e.g., print(), len(), input()). "
        "Make the question simple but precise, avoiding conceptual or applied reasoning.",
        "",
        f"Create {num_questions} multiple choice questions with 4 options from the following content:",
        "",
        "Please provide the content here.",
        "",
        "**IMPORTANT: Please respond in JSON format only. Follow this exact structure:**",
        "",
        "Example JSON structure:",
        example_json_str,
        "",
        #  "Include detailed explanations for each answer in the 'explanation' field."
        # if language == "EN" else "รวมคำอธิบายโดยละเอียดสำหรับแต่ละคำตอบในฟิลด์ 'explanation'",
        # "",
        f"Respond with valid JSON only in {language} language. Do not include any additional text or formatting outside the JSON structure."
        if language == "EN" else f"ตอบกลับด้วย JSON ที่ถูกต้องในภาษา {language} เท่านั้น อย่าใส่ข้อความหรือการจัดรูปแบบเพิ่มเติมนอกเหนือจากโครงสร้าง JSON",
        "",        
    ]

    # รวม prompt เป็นข้อความเดียว
    prompt = "\n".join(prompt_parts)

    return prompt

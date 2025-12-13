import json
from app.models.example_json_remember import example_json as example_json_remember
from typing import Literal

# กำหนดประเภทของภาษาเป็น EN หรือ TH เท่านั้น
LanguageType = Literal["EN", "TH"]

async def create_quiz_prompt(num_questions: int, language: LanguageType) -> str:
    
    # กำหนดจำนวนข้อเป็น 10 ตามข้อกำหนดใหม่
    num_questions_fixed = 10
    
    # แปลง example JSON เป็น string เพื่อใส่ใน prompt
    # *สมมติว่า example_json_remember มีโครงสร้างเป็น List [{}, {}]*
    example_json_str = json.dumps(example_json_remember, ensure_ascii=False, indent=2)
    
    # กำหนดภาษาของข้อกำหนด (Prompt Instruction)
    if language == "TH":
        # --- Prompt ภาษาไทย (ตามโจทย์ใหม่) ---
        prompt_parts = [
            "คุณคือ **ผู้ช่วยสร้างแบบทดสอบ (Quiz Generation Assistant)**",
            f"ทำหน้าที่สร้าง **คำถามปรนัยจำนวน {num_questions_fixed} ข้อ** จากเนื้อหาที่ถูกป้อนให้",
            "",
            "---",
            "## 🎯 ข้อกำหนดหลัก",
            f"- ต้องสร้าง **{num_questions_fixed} ข้อพอดี** ห้ามขาดหรือเกิน",
            "- ทุกข้ออยู่ในระดับ **Bloom’s Taxonomy: Remember**",
            "  → เน้นจำข้อเท็จจริง คำจำกัดความ ความหมาย",
            "  → ห้ามวิเคราะห์ ห้ามตีความลึก ห้ามประยุกต์",
            "- ใช้เฉพาะเนื้อหาที่ให้เท่านั้น",
            "  **ห้ามเดาเพิ่ม ห้ามสร้างข้อมูลนอกเอกสาร**",
            "- ใช้ภาษาไทยชัดเจน อ่านง่าย",
            "",
            "---",
            "## 🧩 รูปแบบคำถามแต่ละข้อ",
            "- `question`: ข้อความคำถาม",
            "- `options`: ตัวเลือก 4 ตัวเลือก (A, B, C, D)",
            "- `answer`: คำตอบที่ถูกต้อง ระบุเป็น A/B/C/D",
            "",
            "---",
            "## 📤 รูปแบบผลลัพธ์สุดท้าย",
            "- ส่งออกเป็น **JSON Array** จำนวน 10 objects",
            "- JSON ต้องถูกต้อง **และ parse ได้ทันที**",
            "- ห้ามมีข้อมูลอื่นปะปน เช่น คำอธิบาย, คอมเมนต์, ข้อความเกิน JSON",
            "",
            "---",
            "## 📌 ตัวอย่างผลลัพธ์",
            "",
            example_json_str,
            "",
            "---",
            "[ใส่เนื้อหาที่ต้องการสร้าง Quiz ตรงนี้]",
            # เพิ่ม Note สำหรับ LLM เพื่อให้แน่ใจว่าได้ผลลัพธ์ตามที่ต้องการ
            "",
            "**หมายเหตุ: โปรดตอบกลับด้วย JSON Array ที่ถูกต้องตามตัวอย่างเท่านั้น อย่าเพิ่มข้อความใดๆ ก่อนหรือหลัง JSON**",
        ]
        
    else:
        # --- Prompt ภาษาอังกฤษ (ใช้เป็น Fallback) ---
        prompt_parts = [
            "You are the **Quiz Generation Assistant**.",
            f"Your task is to create **{num_questions_fixed} multiple-choice questions** based on the provided content.",
            "",
            "---",
            "## 🎯 Core Requirements",
            f"- Generate **exactly {num_questions_fixed} questions**.",
            "- All questions must be at **Bloom’s Taxonomy: Remember** level.",
            "  → Focus on recalling facts, definitions, and basic terms.",
            "  → Strictly avoid analysis, deep interpretation, or application.",
            "- Use ONLY the provided content. **Do not introduce external information.**",
            f"- Use {language} language clearly.",
            "",
            "---",
            "## 🧩 Question Structure",
            "- `question`: The question text.",
            "- `options`: 4 options (A, B, C, D).",
            "- `answer`: The correct answer, specified as A/B/C/D.",
            "",
            "---",
            "## 📤 Final Output Format",
            "- Output must be a **JSON Array** of 10 objects.",
            "- The JSON must be valid **and immediately parsable**.",
            "- Do not include any extraneous text (e.g., explanations, comments, or notes) outside the JSON structure.",
            "",
            "---",
            "## 📌 Example Output",
            "",
            example_json_str,
            "",
            "---",
            "[Insert Content Here]",
            "",
            "**NOTE: Respond only with the valid JSON Array structure provided in the example. Do not add any text before or after the JSON.**",
        ]

    # รวม prompt เป็นข้อความเดียว
    prompt = "\n".join(prompt_parts)

    return prompt
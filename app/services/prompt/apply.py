import json
from app.models.example_json_apply import example_json as example_json_apply
from typing import Literal

LanguageType = Literal["EN", "TH"]

async def create_quiz_prompt(num_questions: int, language: LanguageType) -> str:

    example_json_str = json.dumps(
        example_json_apply,
        ensure_ascii=False,
        indent=2
    )

    if language == "TH":
        prompt_parts = [
            "คุณเป็น **ผู้ช่วยสร้างแบบทดสอบโค้ด (Coding Quiz Generation Assistant)**",
            "",
            "---",
            "## 🎯 งานของคุณ",
            f"สร้าง **คำถามเกี่ยวกับการประยุกต์ใช้โค้ดจำนวน {num_questions} ข้อ** (ไม่มากกว่าและไม่น้อยกว่า)",
            "",
            "คำถามต้องเป็นระดับ **Bloom’s Taxonomy: Apply_Coding**",
            "ทดสอบ “การประยุกต์ความรู้เพื่อแก้ปัญหาจริง” เช่น:",
            "- ใช้ฟังก์ชันนี้แก้ปัญหา X อย่างไร",
            "- วิธีการเขียนโค้ดเพื่อให้ได้ผลลัพธ์ Y",
            "- เลือก structure หรือ algorithm ที่เหมาะสมสำหรับสถานการณ์ Z",
            "- การนำ concept ไปใช้ในบริบทใหม่",
            "",
            "(ห้ามเป็นระดับจำ หรือเข้าใจเพียงอย่างเดียว ต้องมีการ **Apply**)",
            "",
            "---",
            "## 🔒 กฎสำคัญ (ต้องทำตามทุกข้อ)",
            f"- ต้องสร้าง **{num_questions} ข้อพอดี**",
            "- คำตอบ **ต้องอยู่ในรูปแบบ JSON เท่านั้น**",
            "- แต่ละข้อเป็น 1 JSON object และต้องมีฟิลด์ดังนี้:",
            "  - **question:** ข้อความคำถามสถานการณ์",
            "  - **options:** ตัวเลือก 4 ตัวเลือก (A–D)",
            "  - **answer:** คำตอบที่ถูกต้อง (A/B/C/D)",
            f"- ทั้งหมดต้องรวมเป็น **JSON Array จำนวน {num_questions} objects**",
            "- ใช้ภาษาไทยทั้งหมด",
            "- ห้ามใช้เนื้อหานอกเหนือจากที่ให้มา",
            "- เน้นการประยุกต์ใช้ความรู้",
            "",
            "---",
            "📌 หมายเหตุด้านภาษา (เพื่อความเข้าใจตรง ไม่มีผลต่อโครงสร้างหลัก):",
            "",
            "### 1) การใช้คำทับศัพท์",
            "- หากมีการอ้างถึง “ศัพท์เทคนิค” เช่น function, loop, queue, array, pointer, class, object",
            "  → ให้ใช้ **คำทับศัพท์** เท่านั้น",
            "- หลีกเลี่ยงการแปลศัพท์เทคนิคเป็นไทย เพื่อคงความหมายในบริบท programming",
            "- ใช้เฉพาะเมื่อบริบทคำถามมีศัพท์เทคนิคจริงเท่านั้น",
            "",
            "---",
            "## 📌 ฟอร์แมตผลลัพธ์ที่ “ต้องทำตาม”",
            "",
            example_json_str,
            "",
            f"(ต้องมีทั้งหมด {num_questions} objects)",
            "",
            "---",
            "## 📥 เนื้อหาหรือโค้ดที่ต้องนำไปออกข้อสอบ",
            "[วางเนื้อหาหรือโค้ดจาก PDF/TEXT/RAG ตรงนี้]"
        ]

    else:
        # EN fallback
        prompt_parts = [
            "You are a **Coding Quiz Generation Assistant**.",
            f"Generate exactly {num_questions} code-application questions.",
            "Bloom’s Taxonomy level: Apply_Coding.",
            "Focus on applying knowledge to solve problems, not just understanding.",
            "Output JSON only.",
            example_json_str,
            "[Insert content here]"
        ]

    return "\n".join(prompt_parts)

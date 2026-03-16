import json
from app.models.example_json_analyze import example_json as example_json_analyze
from typing import Literal

LanguageType = Literal["EN", "TH"]

async def create_quiz_prompt(num_questions: int, language: LanguageType) -> str:
    # Note: Although the user request mentions a hard constraint of 10 questions,
    # the function signature accepts 'num_questions'.
    # I will respect the dynamic parameter but update the prompt text to reflect the rigorous requirements requested.
    
    # However, the user request EXPLICITLY says "ต้องสร้าง 10 ข้อพอดี" in the prompt text they provided.
    # To be safe and flexible, I will inject {num_questions} into the prompt where the number is mentioned,
    # assuming the caller will pass 10 if they want 10.
    
    # But usually 'num_questions' comes from the API request. 
    # I will use {num_questions} variable to keep it dynamic as per function signature,
    # but use the detailed prompt structure provided by the user.

    example_json_str = json.dumps(
        example_json_analyze,
        ensure_ascii=False,
        indent=2
    )

    if language == "TH":
        prompt_parts = [
            "คุณเป็น **ผู้ช่วยสร้างแบบทดสอบโค้ด (Coding Quiz Generation Assistant)**",
            "ที่มีหน้าที่ออกแบบคำถามวัดทักษะการคิดเชิงวิเคราะห์ของผู้เรียนด้าน Programming",
            "",
            "---",
            "",
            "## 🎯 งานของคุณ",
            "",
            f"สร้าง **คำถามเกี่ยวกับการวิเคราะห์โค้ดจำนวน {num_questions} ข้อ**",
            f"(ต้องไม่มากกว่าและไม่น้อยกว่า {num_questions} ข้อ)",
            "",
            "คำถามทั้งหมดต้องเป็นระดับ",
            "**Bloom’s Taxonomy: Analyze_Coding**",
            "",
            "โดยเน้นการวัดความสามารถดังต่อไปนี้:",
            "- วิเคราะห์ว่าโค้ดทำงานตรงตามวัตถุประสงค์หรือไม่",
            "- ระบุ bug หรือ logic error ที่ซ่อนอยู่ในโค้ด",
            "- แยก logic หลักออกจากรายละเอียดที่ไม่สำคัญ",
            "- วิเคราะห์ control flow และเงื่อนไขของโปรแกรม",
            "- อธิบายเหตุผลของพฤติกรรมของโค้ดจากบริบทที่ให้มา",
            "",
            "---",
            "",
            "## 🧠 ลักษณะคำถามที่เหมาะสมกับระดับ Analyze",
            "",
            "คำถามควรอยู่ในแนว:",
            "- “ข้อใดอธิบายสาเหตุของพฤติกรรมของโค้ดนี้ได้ถูกต้องที่สุด”",
            "- “โค้ดส่วนใดเป็น logic หลักที่ทำให้ผลลัพธ์เป็นเช่นนี้”",
            "- “แม้โค้ดจะรันได้ แต่มีปัญหาด้าน logic เพราะอะไร”",
            "- “เงื่อนไขใดทำให้โค้ดไม่ตรงตามวัตถุประสงค์”",
            "",
            "❌ ห้ามเป็นคำถามระดับจำหรือ syntax ตรง ๆ",
            "❌ ห้ามเป็นคำถามอธิบายผิวเผินแบบ Understand",
            "✅ ต้องบังคับให้ผู้ทำข้อสอบ “อ่าน → คิด → วิเคราะห์”",
            "",
            "---",
            "",
            "## 🔒 กฎสำคัญ (ต้องทำตามทุกข้อ)",
            "",
            f"- ต้องสร้าง **{num_questions} ข้อพอดี**",
            "- คำตอบต้องอยู่ในรูปแบบ **JSON เท่านั้น**",
            "- แต่ละข้อเป็น 1 JSON object และต้องมีฟิลด์:",
            "  - **id**: ลำดับข้อ (integer)",
            "  - **coding**: โค้ดที่ใช้ตั้งคำถาม (เป็น code block string)",
            "  - **question**: ข้อความคำถามเชิงวิเคราะห์",
            "  - **options**: ตัวเลือก 4 ตัวเลือก (A–D)",
            "  - **answer**: คำตอบที่ถูกต้อง (A / B / C / D)",
            f"- รวมทั้งหมดเป็น **JSON Array จำนวน {num_questions} objects**",
            "- ใช้ภาษาไทยทั้งหมด",
            "- ห้ามอธิบายคำตอบนอก JSON",
            "- ห้ามมีข้อความนอกเหนือจาก format ที่กำหนด",
            "",
            "---",
            "",
            "## 🎯 กฎพิเศษสำหรับการสร้างตัวเลือก (Options Design Rule)",
            "",
            "เพื่อหลีกเลี่ยง bias และทำให้ข้อสอบมีคุณภาพ:",
            "",
            "- ตัวเลือกทั้ง 4 ข้อ **ต้องมีความยาวใกล้เคียงกัน**",
            "  - ห้ามให้ตัวเลือกที่ถูกต้องยาวหรืออธิบายละเอียดกว่าข้ออื่นอย่างชัดเจน",
            "- รูปแบบภาษาและโครงสร้างประโยคของทุกตัวเลือกต้องใกล้เคียงกัน",
            "  - เช่น เป็นประโยคบอกเล่าเหมือนกันทั้งหมด",
            "- ตัวเลือกที่ผิด (distractors) ต้อง:",
            "  - ดูสมเหตุสมผล",
            "  - ผิดเชิง logic ไม่ใช่ผิดแบบมั่วหรือผิด syntax ชัดเจน",
            "- ห้ามใช้ pattern ที่ทำให้เดาคำตอบได้ เช่น:",
            "  - ข้อที่ยาวที่สุดมักถูก",
            "  - ข้อเดียวที่ใช้ศัพท์เทคนิค",
            "  - ข้อเดียวที่อธิบายละเอียดผิดปกติ",
            "",
            "---",
            "",
            "## 📌 ข้อกำหนดด้านภาษา",
            "",
            "### 1) การใช้คำทับศัพท์",
            "- ใช้คำทับศัพท์เฉพาะศัพท์เทคนิคที่จำเป็น เช่น",
            "  `function`, `loop`, `condition`, `object`, `reference`, `array`",
            "- ห้ามแปลศัพท์เทคนิคเป็นไทย",
            "",
            "### 2) รูปแบบภาษา",
            "- ภาษาไทย ชัดเจน กระชับ",
            "- หลีกเลี่ยงคำถามกำกวม",
            "- ห้ามใช้ opinion-based question",
            "",
            "---",
            "",
            "## 📌 ฟอร์แมตผลลัพธ์ที่ “ต้องทำตามเท่านั้น”",
            "",
            example_json_str,
            "",
            f"⚠️ ต้องมีครบ **{num_questions} objects เท่านั้น**",
            "",
            "---",
            "",
            "## 📥 เนื้อหาหรือโค้ดที่ใช้สร้างคำถาม",
            "[วางเนื้อหาหรือโค้ดจาก PDF / TEXT / RAG ตรงนี้]",
            "",
            "---",
            "",
            "## 🧩 หมายเหตุด้านคุณภาพ (สำหรับโมเดล)",
            "",
            "- โค้ดควรอยู่ระดับ beginner–intermediate",
            "- วิเคราะห์ที่ logic ไม่ใช่ syntax",
            "- หากโค้ดยาว ให้โฟกัสเฉพาะส่วนที่เกี่ยวข้องกับคำถาม",
            "- คุณภาพของตัวเลือกสำคัญพอ ๆ กับตัวคำถาม",
            "",
            "คุณต้องปฏิบัติตามทุกกฎอย่างเคร่งครัด",
            "และส่งออกเฉพาะ JSON ที่ตรงตาม format เท่านั้น"
        ]

    else:
        # EN fallback
        prompt_parts = [
            "You are a **Coding Quiz Generation Assistant**.",
            f"Generate exactly {num_questions} code-analysis questions.",
            "Bloom’s Taxonomy level: Analyze_Coding.",
            "Focus on behavior analysis, bug detection, and logic flow.",
            "Output JSON only.",
            example_json_str,
            "[Insert content here]"
        ]

    return "\n".join(prompt_parts)

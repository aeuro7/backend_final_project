import google.generativeai as genai
import json
import re

GOOGLE_API_KEY='AIzaSyC1czHW9KniQNoQ3ojhYvGbTs3aWkCNCiU'
genai.configure(api_key=GOOGLE_API_KEY)

def build_quiz_prompt(
    text: str,
    bloom_level: str = "Understand",
    question_type: str = "multiple_choice",
    num_questions: int = 6,
    language: str = "TH",
    include_explanation: bool = True
) -> str:

    # Define prompts for each Bloom's Taxonomy level
    BLOOM_PROMPTS = {
        "Understand": (
    "Create questions that require students to demonstrate comprehension of the presented content. "
    "Focus on ensuring learners understand how a concept or code actually works rather than just memorizing rules. "
    "Questions should be designed in one of the following forms:\n\n"
    
    "1️⃣ Code Output Interpretation:\n"
    "- Provide short, clear code snippets.\n"
    "- Ask students what will be printed or what the program result will be.\n"
    "- May include tricky basic behaviors such as variable updates, loops, conditional branching, type casting, or string manipulation.\n\n"
    
    "2️⃣ Concept Meaning Understanding:\n"
    "- Ask the meaning or purpose of common programming concepts (e.g., recursion, class/object in OOP, list vs tuple, stack/queue).\n"
    "- Questions must verify the student can explain behavior or core idea rather than recall definitions.\n\n"
    
    "Avoid focusing on memorization alone. Ensure each question checks if the learner truly understands functionality or conceptual reasoning."
)
,
    }

    # Define prompts for each question type
    QUESTION_TYPE_PROMPTS = {
        "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options from the following content:",
        "short_answer": f"Create {num_questions} short answer questions:",
        "code_completion": f"Create {num_questions} code completion exercises:"
    }

    # Define JSON format templates for each question type
    JSON_FORMAT_TEMPLATES = {
        "multiple_choice": '''
{
  "questions": [
    {
      "id": 1,
      "question": "Question text here",
      "options": {
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
      },
      "correct_answer": "A",
      "explanation": "Explanation for the correct answer"
    }
  ]
}''',
        "short_answer": '''
{
  "questions": [
    {
      "id": 1,
      "question": "Question text here",
      "answer": "Expected answer",
      "explanation": "Explanation for the answer"
    }
  ]
}''',
        "code_completion": '''
{
  "questions": [
    {
      "id": 1,
      "question": "Complete the following code:",
      "incomplete_code": "Code with blanks or missing parts",
      "complete_code": "Complete correct code",
      "explanation": "Explanation of the solution"
    }
  ]
}'''
    }

    # Validate input parameters
    if bloom_level not in BLOOM_PROMPTS:
        raise ValueError(f"Unsupported bloom_level: {bloom_level}")

    if question_type not in QUESTION_TYPE_PROMPTS:
        raise ValueError(f"Unsupported question_type: {question_type}")

    if language not in ["TH", "EN"]:
        raise ValueError(f"Unsupported language: {language}")

    # Build main prompt
    prompt_parts = [
        f"Bloom's Level: {bloom_level}",
        "",
        BLOOM_PROMPTS[bloom_level],
        "",
        QUESTION_TYPE_PROMPTS[question_type],
        "",
        f"{{\n{text}\n}}",
        "",
        "**IMPORTANT: Please respond in JSON format only. Follow this exact structure:**",
        JSON_FORMAT_TEMPLATES[question_type]
    ]

    # Add explanation instruction
    if include_explanation:
        explanation_instruction = (
            "Include detailed explanations for each answer in the 'explanation' field."
            if language == "EN"
            else "รวมคำอธิบายโดยละเอียดสำหรับแต่ละคำตอบในฟิลด์ 'explanation'"
        )
        prompt_parts.append(f"\n{explanation_instruction}")
    else:
        no_explanation_instruction = (
            "Set 'explanation' field to empty string for all questions."
            if language == "EN"
            else "ตั้งค่าฟิลด์ 'explanation' เป็นสตริงว่างสำหรับทุกข้อ"
        )
        prompt_parts.append(f"\n{no_explanation_instruction}")

    # Add final JSON instruction
    json_instruction = (
        "\nRespond with valid JSON only. Do not include any additional text or formatting outside the JSON structure."
        if language == "EN"
        else "\nตอบกลับด้วย JSON ที่ถูกต้องเท่านั้น อย่าใส่ข้อความหรือการจัดรูปแบบเพิ่มเติมนอกเหนือจากโครงสร้าง JSON"
    )
    prompt_parts.append(json_instruction)

    # Combine prompt parts
    prompt = "\n".join(prompt_parts)

    # Add language instruction
    language_instruction = (
        "Generate the quiz in English.\n\n" if language == "EN"
        else "สร้างข้อสอบเป็นภาษาไทย\n\n"
    )

    return language_instruction + prompt


async def generate_quiz_U001(
    text: str,
    bloom_level: str = "Understand",
    question_type: str = "multiple_choice",
    num_questions: int = 6,
    language: str = "TH",
    include_explanation: bool = True
) -> dict:
    
    # Build the prompt
    prompt = build_quiz_prompt(
        text=text,
        bloom_level=bloom_level,
        question_type=question_type,
        num_questions=num_questions,
        language=language,
        include_explanation=include_explanation
    )
    
    # Generate using Gemini
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
    response = model.generate_content(prompt)
    
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

async def generate_quiz_U002(
    text: str,
    bloom_level: str = "Understand",
    question_type: str = "short_answer",
    num_questions: int = 3,
    language: str = "TH",
    include_explanation: bool = True
) -> dict:
    
    # Build the prompt
    prompt = build_quiz_prompt(
        text=text,
        bloom_level=bloom_level,
        question_type=question_type,
        num_questions=num_questions,
        language=language,
        include_explanation=include_explanation
    )
    
    # Generate using Gemini
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
    response = model.generate_content(prompt)
    
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


async def check_quiz_answer_U003(
    question: str,
    user_answer: str,
    correct_answer: str,
    detail: bool = True
) -> dict:
    """
    Compare user's answer with correct answer using Gemini AI.
    Returns a dict with evaluation result and optional explanation.
    """
    
    # สร้าง prompt ให้ AI เข้าใจบริบท
    prompt = f"""
    You are a helpful quiz evaluator.
    Compare the user's answer to the correct answer and judge if it's correct, partially correct, or incorrect.
    Return JSON only in this format:

    {{
        "result": "correct" | "partially_correct" | "incorrect",
        "score": 0-5,
        "explanation": "..."
    }}

    Question: {question}
    Correct Answer: {correct_answer}
    User Answer: {user_answer}
    {"Please include explanation in the output." if detail else "No explanation needed."}
    """

    # เรียกใช้โมเดล Gemini
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
    response = model.generate_content(prompt)
    
    response_text = response.text.strip()

    # พยายามดึง JSON ออกมา
    json_match = re.search(r'```json\s*(\{.*\})\s*```', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(1)
    else:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)

    # แปลง JSON เป็น dict
    try:
        result = json.loads(response_text)
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nResponse text: {response_text}")

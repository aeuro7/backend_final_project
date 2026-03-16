from typing import List, Dict, Any, Union

class InvalidQuizFormatException(Exception):
    """Exception raised for errors in the quiz data format."""
    pass

def validate_quiz_response(quiz_data: Any, expected_count: int) -> List[Dict[str, Any]]:
    """
    ตรวจสอบว่า quiz_data ที่ได้จาก Model ถูกต้องตามเงื่อนไขหรือไม่
    
    Args:
        quiz_data: ข้อมูล JSON ที่ได้จาก model (ควรเป็น list ของ dict)
        expected_count: จำนวนข้อสอบที่คาดหวัง
        
    Returns:
        List[Dict[str, Any]]: ข้อมูล quiz ที่ผ่านการตรวจสอบแล้ว
        
    Raises:
        InvalidQuizFormatException: ถ้าข้อมูลไม่ถูกต้องตามเงื่อนไข
    """
    
    # 1. เช็คว่าเป็น List หรือไม่
    if not isinstance(quiz_data, list):
        raise InvalidQuizFormatException(f"Format error: Expected a list of questions, but got {type(quiz_data).__name__}.")
    
    # 2. เช็คจำนวนข้อ
    if len(quiz_data) != expected_count:
        raise InvalidQuizFormatException(f"Count error: Expected {expected_count} questions, but got {len(quiz_data)}.")
    
    # 3. เช็คโครงสร้างแต่ละข้อ และ ID
    # สร้าง set ของ id เพื่อเช็คความซ้ำและเช็คว่าครบ 1 ถึง expected_count ไหม
    found_ids = set()
    
    for index, item in enumerate(quiz_data):
        if not isinstance(item, dict):
            raise InvalidQuizFormatException(f"Item error: Item at index {index} is not a JSON object.")
        
        # เช็ค field พื้นฐาน
        required_fields = ["question", "options", "answer"]
        # 'coding' field อาจจะมีหรือไม่มีก็ได้ ขึ้นอยู่กับประเภท quiz แต่ถ้า Analyze/Understand ควรมี
        # แต่เพื่อความ general เราอาจจะเช็คแค่ fields หลักที่ต้องมีแน่ๆ
        
        for field in required_fields:
            if field not in item:
                raise InvalidQuizFormatException(f"Field error: Item at index {index} missing required field '{field}'.")
        
        # เช็ค options ว่ามีครบ 4 ข้อไหม
        options = item.get("options", {})
        if not isinstance(options, dict) or len(options) < 4:
             raise InvalidQuizFormatException(f"Options error: Item at index {index} must have at least 4 options.")

        # เช็ค ID (ถ้ามี)
        # ถ้า Model ไม่ส่ง ID มา เราอาจจะยอมหยวนๆ หรือ force ให้มีก็ได้
        # แต่จาก requirement คุณบอกว่า "วนลูปเช็คว่ามี id ข้อครบตามที่สั่งไหม"
        # แปลว่า ID ต้องมี และต้องเรียงถูกต้อง
        
        item_id = item.get("id")
        if item_id is None:
             raise InvalidQuizFormatException(f"ID error: Item at index {index} missing 'id' field.")
             
        try:
            item_id = int(item_id)
        except (ValueError, TypeError):
             raise InvalidQuizFormatException(f"ID error: Item ID at index {index} is not an integer.")
        
        if item_id in found_ids:
             raise InvalidQuizFormatException(f"ID error: Duplicate ID {item_id} found.")
        
        found_ids.add(item_id)

    # 4. เช็คว่า ID ครบถ้วนตั้งแต่ 1 ถึง expected_count หรือไม่
    expected_ids = set(range(1, expected_count + 1))
    missing_ids = expected_ids - found_ids
    if missing_ids:
        raise InvalidQuizFormatException(f"ID mismatch: Missing IDs {missing_ids}. Expected IDs 1 to {expected_count}.")

    return quiz_data

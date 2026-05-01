import re
from datetime import datetime, date
from typing import Any, List, Dict, Tuple
from app.models.models import FormField, FieldType

class FormValidator:
    @staticmethod
    def validate_field(field: FormField, value: Any) -> Tuple[bool, str]:
        # 1. Check Required
        if field.required and (value is None or str(value).strip() == ""):
            return False, f"Trường '{field.label}' là bắt buộc."

        if value is None or str(value).strip() == "":
            return True, ""

        # 2. Type-specific validation
        try:
            if field.type == FieldType.TEXT:
                if len(str(value)) > 200:
                    return False, f"'{field.label}' không được vượt quá 200 ký tự."
            
            elif field.type == FieldType.NUMBER:
                try:
                    num_val = float(value)
                    if not (0 <= num_val <= 100):
                        return False, f"'{field.label}' phải nằm trong khoảng từ 0 đến 100."
                except ValueError:
                    return False, f"'{field.label}' phải là một con số hợp lệ."
            
            elif field.type == FieldType.DATE:
                try:
                    # Expecting YYYY-MM-DD
                    input_date = datetime.strptime(str(value), "%Y-%m-%d").date()
                    if input_date < date.today():
                        return False, f"'{field.label}' không được là ngày trong quá khứ."
                except ValueError:
                    return False, f"'{field.label}' định dạng ngày không hợp lệ (Y-m-d)."
            
            elif field.type == FieldType.COLOR:
                if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", str(value)):
                    return False, f"'{field.label}' phải là mã HEX hợp lệ (ví dụ: #RRGGBB)."
            
            elif field.type == FieldType.SELECT:
                if field.options and value not in field.options:
                    return False, f"Giá trị của '{field.label}' không hợp lệ."
            
        except Exception as e:
            return False, f"Lỗi xử lý trường '{field.label}': {str(e)}"

        return True, ""

    @classmethod
    def validate_submission(cls, fields: List[FormField], submission_data: Dict[int, Any]) -> List[str]:
        errors = []
        for field in fields:
            value = submission_data.get(field.id)
            is_valid, error_msg = cls.validate_field(field, value)
            if not is_valid:
                errors.append(error_msg)
        return errors

from app.services.validator import FormValidator
from app.models.models import FormField, FieldType

def test_text_validation():
    field = FormField(label="Tên", type=FieldType.TEXT, required=True)
    
    # Valid
    valid, msg = FormValidator.validate_field(field, "Nguyễn Văn A")
    assert valid is True
    
    # Required check
    valid, msg = FormValidator.validate_field(field, "")
    assert valid is False
    assert "bắt buộc" in msg
    
    # Length check
    valid, msg = FormValidator.validate_field(field, "a" * 201)
    assert valid is False
    assert "200 ký tự" in msg

def test_number_validation():
    field = FormField(label="Điểm", type=FieldType.NUMBER)
    
    assert FormValidator.validate_field(field, 50)[0] is True
    assert FormValidator.validate_field(field, 101)[0] is False
    assert FormValidator.validate_field(field, -1)[0] is False
    assert FormValidator.validate_field(field, "abc")[0] is False

def test_color_validation():
    field = FormField(label="Màu", type=FieldType.COLOR)
    
    assert FormValidator.validate_field(field, "#FFF")[0] is True
    assert FormValidator.validate_field(field, "#aabbcc")[0] is True
    assert FormValidator.validate_field(field, "red")[0] is False
    assert FormValidator.validate_field(field, "123456")[0] is False

def test_date_validation():
    field = FormField(label="Ngày", type=FieldType.DATE)
    from datetime import date, timedelta
    
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    assert FormValidator.validate_field(field, tomorrow)[0] is True
    assert FormValidator.validate_field(field, yesterday)[0] is False

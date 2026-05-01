from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import get_session
from app.models.models import Form, FormField
from app.schemas.schemas import FieldCreate, FieldUpdate, FieldRead

router = APIRouter()

@router.post("/{id}/fields", response_model=FieldRead)
def add_field(id: int, field_input: FieldCreate, session: Session = Depends(get_session)):
    """Thêm field vào form"""
    form = session.get(Form, id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    db_field = FormField.model_validate(field_input, update={"form_id": id})
    session.add(db_field)
    session.commit()
    session.refresh(db_field)
    return db_field

@router.put("/{id}/fields/{fid}", response_model=FieldRead)
def update_field(id: int, fid: int, field_input: FieldUpdate, session: Session = Depends(get_session)):
    """Cập nhật field"""
    db_field = session.get(FormField, fid)
    if not db_field or db_field.form_id != id:
        raise HTTPException(status_code=404, detail="Field not found in this form")
    
    field_data = field_input.model_dump(exclude_unset=True)
    for key, value in field_data.items():
        setattr(db_field, key, value)
    
    session.add(db_field)
    session.commit()
    session.refresh(db_field)
    return db_field

@router.delete("/{id}/fields/{fid}")
def delete_field(id: int, fid: int, session: Session = Depends(get_session)):
    """Xóa field"""
    db_field = session.get(FormField, fid)
    if not db_field or db_field.form_id != id:
        raise HTTPException(status_code=404, detail="Field not found in this form")
    
    session.delete(db_field)
    session.commit()
    return {"success": True, "message": "Field deleted successfully"}

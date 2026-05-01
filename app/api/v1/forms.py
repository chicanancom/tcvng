from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.models import Form, FormField
from app.schemas.schemas import FormCreate, FormUpdate, FormRead

router = APIRouter()

@router.get("/", response_model=List[FormRead])
def get_forms(
    offset: int = 0, 
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    """Lấy danh sách tất cả form (Admin)"""
    forms = session.exec(select(Form).offset(offset).limit(limit).order_by(Form.order)).all()
    return forms

@router.post("/", response_model=FormRead)
def create_form(form_input: FormCreate, session: Session = Depends(get_session)):
    """Tạo form mới (Admin)"""
    db_form = Form.model_validate(form_input)
    session.add(db_form)
    session.commit()
    session.refresh(db_form)
    return db_form

@router.get("/{id}", response_model=dict)
def get_form_detail(id: int, session: Session = Depends(get_session)):
    """Lấy chi tiết 1 form kèm danh sách field"""
    form = session.get(Form, id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    # Sort fields by order
    sorted_fields = sorted(form.fields, key=lambda x: x.order)
    
    return {
        **form.model_dump(),
        "fields": sorted_fields
    }

@router.put("/{id}", response_model=FormRead)
def update_form(id: int, form_input: FormUpdate, session: Session = Depends(get_session)):
    """Cập nhật thông tin form (Admin)"""
    db_form = session.get(Form, id)
    if not db_form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    form_data = form_input.model_dump(exclude_unset=True)
    for key, value in form_data.items():
        setattr(db_form, key, value)
    
    session.add(db_form)
    session.commit()
    session.refresh(db_form)
    return db_form

@router.delete("/{id}")
def delete_form(id: int, session: Session = Depends(get_session)):
    """Xóa form (Admin)"""
    db_form = session.get(Form, id)
    if not db_form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    session.delete(db_form)
    session.commit()
    return {"success": True, "message": "Form deleted successfully"}

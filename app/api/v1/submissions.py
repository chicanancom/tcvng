from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.models import Form, FormField, Submission, SubmissionValue, FormStatus
from app.schemas.schemas import SubmissionCreate, SubmissionRead
from app.services.validator import FormValidator

router = APIRouter()

@router.get("/forms/active", response_model=List[dict])
def get_active_forms(session: Session = Depends(get_session)):
    """Danh sách form active, sắp theo thứ tự (Nhân viên)"""
    statement = select(Form).where(Form.status == FormStatus.ACTIVE).order_by(Form.order)
    forms = session.exec(statement).all()
    return [{"id": f.id, "title": f.title, "description": f.description, "order": f.order} for f in forms]

@router.post("/forms/{id}/submit")
def submit_form(id: int, submission: SubmissionCreate, session: Session = Depends(get_session)):
    """Nhân viên submit form"""
    db_form = session.get(Form, id)
    if not db_form or db_form.status != FormStatus.ACTIVE:
        raise HTTPException(status_code=404, detail="Form not found or not active")
    
    # 1. Map input values to field_id
    input_data = {v.field_id: v.value for v in submission.values}
    
    # 2. Run Validation
    errors = FormValidator.validate_submission(db_form.fields, input_data)
    if errors:
        return {
            "success": False,
            "error": "Dữ liệu không hợp lệ",
            "details": errors
        }
    
    # 3. Save Submission
    db_submission = Submission(form_id=id)
    session.add(db_submission)
    session.commit()
    session.refresh(db_submission)
    
    # 4. Save Submission Values
    for field_id, value in input_data.items():
        sub_value = SubmissionValue(
            submission_id=db_submission.id,
            field_id=field_id,
            value=str(value)
        )
        session.add(sub_value)
    
    session.commit()
    return {"success": True, "submission_id": db_submission.id, "message": "Submit thành công!"}

@router.get("/submissions")
def get_submissions(session: Session = Depends(get_session)):
    """Xem lại danh sách bài đã submit"""
    submissions = session.exec(select(Submission).order_by(Submission.submitted_at.desc())).all()
    result = []
    for sub in submissions:
        result.append({
            "id": sub.id,
            "form_title": sub.form.title,
            "submitted_at": sub.submitted_at,
            "values": [{"field": v.field.label, "value": v.value} for v in sub.values]
        })
    return result

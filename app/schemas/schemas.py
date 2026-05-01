from typing import List, Optional, Any
from pydantic import BaseModel
from app.models.models import FormStatus, FieldType

# --- Form Schemas ---
class FormCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0
    status: FormStatus = FormStatus.DRAFT

class FormUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    status: Optional[FormStatus] = None

class FormRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    order: int
    status: FormStatus
    
    class Config:
        from_attributes = True

# --- Field Schemas ---
class FieldCreate(BaseModel):
    label: str
    type: FieldType
    order: int = 0
    required: bool = False
    options: Optional[List[str]] = None

class FieldUpdate(BaseModel):
    label: Optional[str] = None
    type: Optional[FieldType] = None
    order: Optional[int] = None
    required: Optional[bool] = None
    options: Optional[List[str]] = None

class FieldRead(BaseModel):
    id: int
    form_id: int
    label: str
    type: FieldType
    order: int
    required: bool
    options: Optional[List[str]]
    
    class Config:
        from_attributes = True

# --- Submission Schemas ---
class SubmissionValueInput(BaseModel):
    field_id: int
    value: Any  # Raw input value from user

class SubmissionCreate(BaseModel):
    values: List[SubmissionValueInput]

class SubmissionRead(BaseModel):
    id: int
    form_id: int
    submitted_at: Any
    values: List[Any]
    
    class Config:
        from_attributes = True

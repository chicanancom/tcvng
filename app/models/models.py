from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel

class FormStatus(str, Enum):
    ACTIVE = "active"
    DRAFT = "draft"

class FieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    COLOR = "color"
    SELECT = "select"

class FormBase(SQLModel):
    title: str
    description: Optional[str] = None
    order: int = 0
    status: FormStatus = FormStatus.DRAFT

class Form(FormBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    fields: List["FormField"] = Relationship(back_populates="form", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    submissions: List["Submission"] = Relationship(back_populates="form")

class FormFieldBase(SQLModel):
    label: str
    type: FieldType
    order: int = 0
    required: bool = False
    options: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

class FormField(FormFieldBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    form_id: int = Field(foreign_key="form.id")
    
    form: Form = Relationship(back_populates="fields")
    values: List["SubmissionValue"] = Relationship(back_populates="field")

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    form_id: int = Field(foreign_key="form.id")
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    form: Form = Relationship(back_populates="submissions")
    values: List["SubmissionValue"] = Relationship(back_populates="submission")

class SubmissionValue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submission.id")
    field_id: int = Field(foreign_key="formfield.id")
    value: str  # We store everything as string, validation happens at logic level
    
    submission: Submission = Relationship(back_populates="values")
    field: FormField = Relationship(back_populates="values")

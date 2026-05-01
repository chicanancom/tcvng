from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.db.database import init_db
from app.api.v1 import forms, fields, submissions

app = FastAPI(
    title="Form Management System API",
    description="Hệ thống quản lý form đơn giản cho Admin và Nhân viên",
    version="1.0.0"
)

# Initialize Database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Unified Error Response Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Dữ liệu không hợp lệ",
            "details": exc.errors()
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Lỗi hệ thống",
            "message": str(exc)
        },
    )

# Include Routers
app.include_router(forms.router, prefix="/api/forms", tags=["Forms"])
app.include_router(fields.router, prefix="/api/forms", tags=["Fields"])
app.include_router(submissions.router, prefix="/api", tags=["Submissions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Form Management API", "docs": "/docs"}

from sqlmodel import Session, create_engine, select
from app.models.models import Form, FormField, FormStatus, FieldType
from app.db.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

def seed_data():
    with Session(engine) as session:
        # Check if already seeded
        existing = session.exec(select(Form)).first()
        if existing:
            print("Database đã có dữ liệu, không cần seed thêm.")
            return

        # 1. Create Form
        form = Form(
            title="Đăng ký Thông tin SW",
            description="Vui lòng điền đầy đủ các thông tin bên dưới để hoàn tất thủ tục.",
            status=FormStatus.ACTIVE,
            order=1
        )
        session.add(form)
        session.commit()
        session.refresh(form)

        # 2. Create Fields
        fields = [
            FormField(form_id=form.id, label="Họ và Tên", type=FieldType.TEXT, order=1, required=True),
            FormField(form_id=form.id, label="Tuổi (0-100)", type=FieldType.NUMBER, order=2, required=True),
            FormField(form_id=form.id, label="Ngày bắt đầu", type=FieldType.DATE, order=3, required=True),
            FormField(form_id=form.id, label="Màu sắc yêu thích", type=FieldType.COLOR, order=4, required=False),
            FormField(form_id=form.id, label="Vị trí công tác", type=FieldType.SELECT, order=5, required=True, 
                      options=["Frontend Developer", "Backend Developer", "DevOps", "Tester"])
        ]
        
        for field in fields:
            session.add(field)
        
        session.commit()
        print("Đã Seed dữ liệu mẫu thành công!")

if __name__ == "__main__":
    seed_data()

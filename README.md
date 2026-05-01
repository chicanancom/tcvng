# Form Management System (Python/FastAPI)

Hệ thống quản lý form đơn giản cho phép Admin tạo form và Nhân viên nộp bài với bộ máy validation mạnh mẽ.

## 🚀 Công nghệ sử dụng
- **Python 3.11**
- **FastAPI**: Web framework hiện đại, hiệu năng cao.
- **SQLModel**: ORM kết hợp SQLAlchemy và Pydantic.
- **PostgreSQL**: Cơ sở dữ liệu quan hệ.
- **Docker & Docker Compose**: Đóng gói và triển khai dễ dàng.

## 🛠 Cách cài đặt và chạy project

### Cách 1: Sử dụng Docker (Khuyến khích)
Bạn chỉ cần cài đặt Docker và chạy lệnh sau:
```bash
docker-compose up --build
```
Hệ thống sẽ tự động cài đặt DB, Migrate bảng và chạy App tại: `http://localhost:8000`

### Cách 2: Chạy local (Yêu cầu Python 3.10+)
1. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
2. Cấu hình file `.env` (nếu cần thay đổi DB):
   ```text
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/form_db
   ```
3. Chạy ứng dụng:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📖 Tài liệu API (Swagger UI)
Sau khi chạy project, bạn có thể truy cập vào đường dẫn sau để xem tài liệu chi tiết và test API trực tiếp:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## 🏗 Quyết định thiết kế (Design Decisions)
1. **Layered Architecture**: Tách biệt logic giữa Controller (API), Service (Validation) và Repository (CRUD) để dễ bảo trì.
2. **Validation Engine**: Logic validation được tách riêng thành một module `validator.py`. Điều này giúp chúng ta có thể mở rộng thêm các loại field mới (ví dụ: `email`, `url`) một cách dễ dàng mà không làm ảnh hưởng đến code chính.
3. **Unified Error Handling**: Mọi lỗi (từ nhập liệu đến lỗi server) đều được trả về dưới định dạng JSON chuẩn:
   ```json
   {
     "success": false,
     "error": "Mô tả lỗi",
     "details": ["Lỗi chi tiết 1", "Lỗi chi tiết 2"]
   }
   ```
4. **Database Schema**: Sử dụng bảng `SubmissionValue` để lưu giá trị theo từng field, giúp việc thống kê và truy vấn dữ liệu sau này linh hoạt hơn so với việc lưu JSON cục bộ.

## 🧪 Testing
Chạy unit test cho bộ máy validation:
```bash
pytest
```

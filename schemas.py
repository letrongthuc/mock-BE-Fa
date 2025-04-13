# schemas.py
from pydantic import BaseModel

# Schema cho dữ liệu gửi lên khi đăng ký
class UserCreate(BaseModel):
    email: str
    password: str
    fullname: str

    class Config:
        orm_mode = True  # Cho phép trả về đối tượng từ ORM như SQLAlchemy

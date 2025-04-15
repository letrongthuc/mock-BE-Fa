from pydantic import BaseModel

# Schema cho dữ liệu gửi lên khi đăng ký
class UserCreate(BaseModel):
    email: str
    password: str
    fullname: str

    class Config:
        # Cập nhật Config theo cách mới
        from_attributes = True

# Schema trả về khi lấy thông tin người dùng
class UserResponse(BaseModel):
    email: str
    is_verified: bool

    class Config:
        # Cập nhật Config theo cách mới
        from_attributes = True
    
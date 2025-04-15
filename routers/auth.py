#auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import UserCreate
from utils.email_utils import send_verification_email  # Đảm bảo đã import
import uuid
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm mã hóa mật khẩu
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Hàm tạo token xác thực (dùng UUID)
def generate_verification_token() -> str:
    return str(uuid.uuid4())

# Route đăng ký
@router.post("/register")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra email tồn tại
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Mã hóa mật khẩu
    hashed_password = hash_password(user.password)

    # Tạo token xác thực
    token = generate_verification_token()

    # Tạo user mới
    new_user = User(
        email=user.email,
        password=hashed_password,
        fullname=user.fullname,
        is_verified=False,
        verification_token=token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Gửi email xác thực
    try:
        await send_verification_email(new_user.email, new_user.fullname, token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {str(e)}")

    return {
        "msg": "User created successfully. Please check your email to verify your account.",
        "user_id": new_user.id
    }

# Route xác thực email
@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    # Tìm người dùng có token khớp
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    # Cập nhật trạng thái xác thực
    user.is_verified = True
    user.verification_token = None  # Xoá token sau khi xác thực
    db.commit()
    
    return {"msg": "Email successfully verified. You can now log in."}

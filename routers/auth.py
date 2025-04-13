# routers/auth.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from database import get_db
from passlib.context import CryptContext
from fastapi import Depends

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm mã hóa mật khẩu
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Route đăng ký
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra xem email đã tồn tại chưa
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Mã hóa mật khẩu
    hashed_password = hash_password(user.password)
    
    # Tạo người dùng mới và lưu vào DB
    new_user = User(email=user.email, password=hashed_password, fullname=user.fullname)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "User created successfully", "user_id": new_user.id}

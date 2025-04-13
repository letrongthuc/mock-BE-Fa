from fastapi.testclient import TestClient
from passlib.context import CryptContext
from database import SessionLocal
from main import app
from models import User

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_signup():
    # Xóa user cũ nếu có để test lại
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == "testuser@example.com").first()
        if user:
            db.delete(user)
            db.commit()

    response = client.post("/signup", json={
        "email": "testuser@example.com",
        "password": "securePassword123",
        "fullname": "Test User"
    })
    print(response.json())
    assert response.status_code == 200
    assert response.json()["msg"] == "User created successfully"
    assert isinstance(response.json()["user_id"], int)


def test_signup_email_exists():
    test_email = "existinguser@example.com"

    # Thêm user giả lập vào database nếu chưa tồn tại
    with SessionLocal() as db:
        existing = db.query(User).filter(User.email == test_email).first()
        if not existing:
            user = User(
                email=test_email,
                password=pwd_context.hash("somepassword"),
                fullname="Existing User"
            )
            db.add(user)
            db.commit()

    # Gửi lại request đăng ký với email trùng
    response = client.post("/signup", json={
        "email": test_email,
        "password": "securePassword123",
        "fullname": "Existing User"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

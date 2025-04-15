from fastapi.testclient import TestClient
from database import SessionLocal
from main import app
from models import User

client = TestClient(app)

def test_email_verification():
    token = "test-verification-token"

    # Tạo user giả với token xác minh
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == "verifyme@example.com").first()
        if user:
            db.delete(user)
            db.commit()

        user = User(
            email="verifyme@example.com",
            password="hashedpassword",
            fullname="Verify Me",
            is_verified=False,
            verification_token=token,
        )
        db.add(user)
        db.commit()

    # Gửi yêu cầu xác minh email
    response = client.get(f"/verify-email?token={token}")
    assert response.status_code == 200
    assert response.json()["msg"] == "Email successfully verified. You can now log in."

    # Kiểm tra xem user đã được cập nhật trong database chưa
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == "verifyme@example.com").first()
        assert user.is_verified is True
        assert user.verification_token is None


def test_email_verification_invalid_token():
    response = client.get("/verify-email?token=invalid-token")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired verification token"
